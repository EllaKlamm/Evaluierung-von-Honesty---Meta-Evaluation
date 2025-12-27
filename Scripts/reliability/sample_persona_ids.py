import json
import random
from pathlib import Path

BASE = Path("Persona_Sycophancy/output/Llama31_8B_Instruct")
PERSONA_FILE = BASE / "persona.json"

OUT_DIR = BASE / "reliability" / "sampled_prompts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_IDS = OUT_DIR / "sample_ids_50.json"
OUT_SAMPLE = OUT_DIR / "sample_persona_50.json"

N = 50
SEED = 42  # fest, damit reproduzierbar

def main():
    with open(PERSONA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    ids = [item["id"] for item in data]
    random.seed(SEED)
    sample_ids = sorted(random.sample(ids, N))

    sample_items = [item for item in data if item["id"] in sample_ids]

    with open(OUT_IDS, "w", encoding="utf-8") as f:
        json.dump({"seed": SEED, "n": N, "ids": sample_ids}, f, indent=2, ensure_ascii=False)

    with open(OUT_SAMPLE, "w", encoding="utf-8") as f:
        json.dump(sample_items, f, indent=2, ensure_ascii=False)

    print("Geschrieben:")
    print(" -", OUT_IDS)
    print(" -", OUT_SAMPLE)

if __name__ == "__main__":
    main()
