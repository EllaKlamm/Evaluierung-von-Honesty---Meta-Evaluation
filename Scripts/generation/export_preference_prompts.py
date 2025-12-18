import json
import argparse
from datasets import load_dataset

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True, help="Output directory, e.g. Preference_Sycophancy/output/Llama31_8B_Instruct")
    args = ap.parse_args()

    scenario = "Preference_Sycophancy"
    ds = load_dataset("GAIR/BeHonest", scenario)

    for split in ["preference_agree", "preference_disagree"]:
        data = ds[split]
        out = []
        for item in data:
            out.append({"id": int(item["id"]), "prompt": item["prompt"]})

        path = f"{args.outdir}/{split}_prompts.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print("geschrieben:", path, "items:", len(out))

if __name__ == "__main__":
    main()
