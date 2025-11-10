import os
import json
import requests
from datasets import load_dataset
from tqdm import tqdm

MODEL_NAME = "llama3.1:8b"  
SCENARIOS = [
    "Unknowns",
    "Knowns",
    "Persona_Sycophancy",
    "Preference_Sycophancy",
    "Burglar_Deception",
    "Game",
    "Prompt_Format",
    "Open_Form",
    "Multiple_Choice",
]
# Für ersten Test Liste stark kürzen, nur ["Persona_Sycophancy"]
SCENARIOS = ["Persona_Sycophancy"]

def query_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }
    resp = requests.post(url, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "")

def run_scenario(scenario: str):
    print(f"=== Szenario: {scenario} ===")
    ds = load_dataset("GAIR/BeHonest", scenario)

    for split_name, split in ds.items():
        print(f"  Split: {split_name}, {len(split)} Beispiele")
        outputs = []

        for row in tqdm(split, desc=f"{scenario} / {split_name}"):
            prompt = row["prompt"]
            model_output = query_ollama(prompt)
            # BeHonest erwartet id & Antwort
            outputs.append({
                "id": row["id"],
                "prompt": prompt,
                "model_output": model_output,
            })

        out_dir = os.path.join(scenario, "output", "Llama31_8B_Instruct")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{split_name}.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(outputs, f, ensure_ascii=False, indent=2)

        print(f"  -> gespeichert in: {out_path}")

def main():
    for scenario in SCENARIOS:
        run_scenario(scenario)

if __name__ == "__main__":
    main()
