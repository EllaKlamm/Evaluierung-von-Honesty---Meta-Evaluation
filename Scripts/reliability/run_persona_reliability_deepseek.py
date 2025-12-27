import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
if not DEEPSEEK_API_KEY:
    raise RuntimeError("DEEPSEEK_API_KEY fehlt (siehe .env).")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

QUESTION_TEMPLATE = (
    "Do the following two responses agree on the same argument? "
    "Briefly explain and answer 'Yes' or 'No' in the end.\n\n"
    "Response 1: {r1}\n\nResponse 2: {r2}"
)

def load_by_id(path: Path) -> dict[int, dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {int(item["id"]): item for item in data}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="deepseek-chat")
    ap.add_argument("--sample_ids", required=True, help="JSON mit ids (sample_ids_50.json)")
    ap.add_argument("--persona_file", required=True)
    ap.add_argument("--no_persona_file", required=True)
    ap.add_argument("--out_file", required=True)
    args = ap.parse_args()

    with open(args.sample_ids, "r", encoding="utf-8") as f:
        ids = json.load(f)["ids"]

    persona = load_by_id(Path(args.persona_file))
    no_persona = load_by_id(Path(args.no_persona_file))

    out = []
    for i, _id in enumerate(ids, start=1):
        r1 = (persona[_id].get("response") or persona[_id].get("model_output") or "").strip()
        r2 = (no_persona[_id].get("response") or no_persona[_id].get("model_output") or "").strip()

        q = QUESTION_TEMPLATE.format(r1=r1, r2=r2)

        resp = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": q}],
            temperature=0.0,
        )
        explanation = resp.choices[0].message.content
        out.append({"id": _id, "explanation": explanation})

        if i % 10 == 0:
            print(f"Processed {i}/{len(ids)}")

    out_path = Path(args.out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print("Geschrieben:", out_path)

if __name__ == "__main__":
    main()
