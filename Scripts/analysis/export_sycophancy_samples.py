import json
import random
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def index_by_id(items, key="id"):
    return {item[key]: item for item in items}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        choices=["Persona", "Preference"],
        required=True,
        help="Sycophancy-Szenario",
    )
    parser.add_argument(
        "--group",
        choices=["only_chat", "only_reasoner", "both"],
        required=True,
    )
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    random.seed(args.seed)

    base = Path(f"{args.scenario}_Sycophancy/output/Llama31_8B_Instruct")

    overlap_file = base / f"{args.scenario.lower()}_overlap_ids_from_changed_ids.json"
    #agree_file = base / f"{args.scenario.lower()}_agree.json"
    #disagree_file = base / f"{args.scenario.lower()}_disagree.json"
    chat_expl = base / f"chat_{args.scenario.lower()}_explanation.json"
    reasoner_expl = base / f"reasoner_{args.scenario.lower()}_explanation.json"

    overlap = load_json(overlap_file)
    ids = overlap[args.group]

    if args.scenario.lower() == "persona":
        agree_file = f"{base}/persona.json"
        disagree_file = f"{base}/no_persona.json"
        chat_exp = f"{base}/chat_persona_explanation.json"
        reasoner_exp = f"{base}/reasoner_persona_explanation.json"

    elif args.scenario.lower() == "preference":
        agree_file = f"{base}/preference_agree.json"
        disagree_file = f"{base}/preference_disagree.json"
        chat_exp = f"{base}/chat_preference_explanation.json"
        reasoner_exp = f"{base}/reasoner_preference_explanation.json"

    else:
        raise ValueError("Scenario must be Persona or Preference")

    sampled_ids = random.sample(ids, min(args.n, len(ids)))

    agree = index_by_id(load_json(agree_file))
    disagree = index_by_id(load_json(disagree_file))
    chat_exp = index_by_id(load_json(chat_expl))
    reasoner_exp = index_by_id(load_json(reasoner_expl))

    samples = []
    for i in sampled_ids:
        samples.append({
            "id": i,
            "prompt": agree[i]["prompt"],
            "response_agree": agree[i]["response"],
            "response_disagree": disagree[i]["response"],
            "chat_explanation": chat_exp[i]["explanation"],
            "reasoner_explanation": reasoner_exp[i]["explanation"],
        })

    out_path = SCRIPT_DIR / args.out
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)

    print(f"{len(samples)} Beispiele gespeichert in {args.out}")


if __name__ == "__main__":
    main()
