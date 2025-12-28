import json
from pathlib import Path
from statsmodels.stats.contingency_tables import mcnemar

def load_ids(path):
    with open(path, encoding="utf-8") as f:
        return set(json.load(f)["changed_ids"])

def run_mcnemar(name, chat_path, reasoner_path):
    chat_ids = load_ids(chat_path)
    reasoner_ids = load_ids(reasoner_path)

    all_ids = chat_ids | reasoner_ids

    # Kontingenztafel:
    # chat yes / reasoner yes
    both_yes = len(chat_ids & reasoner_ids)
    # chat yes / reasoner no
    chat_only = len(chat_ids - reasoner_ids)
    # chat no / reasoner yes
    reasoner_only = len(reasoner_ids - chat_ids)
    # chat no / reasoner no
    both_no = len(all_ids) - (both_yes + chat_only + reasoner_only)

    table = [[both_yes, chat_only],
             [reasoner_only, both_no]]

    result = mcnemar(table, exact=True)

    print(f"\n McNemar-Test: {name} ")
    print("Kontingenztafel [[beide Ja, nur Chat], [nur Reasoner, beide Nein]]")
    print(table)
    print(f"p-Wert: {result.pvalue:.4f}")

    if result.pvalue < 0.05:
        print("→ Signifikanter Unterschied zwischen Chat und Reasoner")
    else:
        print("→ Kein signifikanter Unterschied zwischen Chat und Reasoner")

if __name__ == "__main__":
    BASE_PERSONA = Path("Persona_Sycophancy/output/Llama31_8B_Instruct")
    BASE_PREF = Path("Preference_Sycophancy/output/Llama31_8B_Instruct")

    run_mcnemar(
        "Persona Sycophancy",
        BASE_PERSONA / "chat_persona_changed_ids.json",
        BASE_PERSONA / "reasoner_persona_changed_ids.json",
    )

    run_mcnemar(
        "Preference Sycophancy",
        BASE_PREF / "chat_preference_changed_ids.json",
        BASE_PREF / "reasoner_preference_changed_ids.json",
    )
