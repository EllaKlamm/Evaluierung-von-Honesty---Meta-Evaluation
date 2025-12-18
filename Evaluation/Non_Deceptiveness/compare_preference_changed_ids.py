import json
import os

BASE = "Preference_Sycophancy/output/Llama31_8B_Instruct" #bzw "Persona_Sycophancy/output/Llama31_8B_Instruct"

chat_ids_path = os.path.join(BASE, "chat_preference_changed_ids.json") #bzw chat_persona_changed_ids.json
reasoner_ids_path = os.path.join(BASE, "reasoner_preference_changed_ids.json") #bzw reasoner_persona_changed_ids.json

def load_changed_ids(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("changed_ids", []))

chat_ids = load_changed_ids(chat_ids_path)
reasoner_ids = load_changed_ids(reasoner_ids_path)

both = sorted(chat_ids & reasoner_ids)
only_chat = sorted(chat_ids - reasoner_ids)
only_reasoner = sorted(reasoner_ids - chat_ids)

print("Vergleich der Preference-Sycophancy-IDs\n")
print(f"DeepSeek-Chat:     {len(chat_ids)} Preference-Wechsel")
print(f"DeepSeek-Reasoner: {len(reasoner_ids)} Preference-Wechsel\n")

print(f"Gemeinsame Preference-Wechsel (beide): {len(both)}")
print(f"Nur Chat, nicht Reasoner:              {len(only_chat)}")
print(f"Nur Reasoner, nicht Chat:              {len(only_reasoner)}\n")

print("Beispiel-IDs nur Chat (erste 10):", only_chat[:10])
print("Beispiel-IDs nur Reasoner (erste 10):", only_reasoner[:10])

# Ergebnisse speichern
out_path = os.path.join(BASE, "preference_overlap_ids_from_changed_ids.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(
        {
            "chat_changed_ids": sorted(chat_ids),
            "reasoner_changed_ids": sorted(reasoner_ids),
            "both": both,
            "only_chat": only_chat,
            "only_reasoner": only_reasoner,
        },
        f,
        ensure_ascii=False,
        indent=2,
    )

print("\nErgebnisse gespeichert in:", out_path)
