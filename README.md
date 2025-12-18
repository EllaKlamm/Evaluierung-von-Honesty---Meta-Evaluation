# Evaluierung von Honesty - Inwiefern beeinflusst die Wahl des Evaluators die Ergebnisse?
### Seminar Aktuelle Entwicklungen im Wintersemester 2025/26

Diese Arbeit untersucht, inwiefern die Wahl des Evaluators die Ergebnisse der Honesty-Evaluation im Framework BeHonest beeinflusst. 
Ziel ist es, mit dem kostengünstigeren Modell DeepSeek als Evaluator sowohl die Evaluationskosten zu reduzieren 
als auch die Grundlage für zukünftige Evaluatoren aus vollständig offenen Open-Source-Modellen zu schaffen.

Der Fokus liegt auf den Sycophancy-Szenarien (Persona Sycophancy und
Preference Sycophancy) aus dem Aspekt *Non-Deceptiveness*.


## Generierung der Modellantworten
Die Antworten des evaluierten Modells werden mit dem Skript `Scripts/generation/generate_llama31_with_ollama_behonest.py`
erzeugt.  
Dieses Skript lädt die Prompts direkt aus dem BeHonest-Datensatz
(`GAIR/BeHonest` via HuggingFace), führt die Inferenz mit
**Llama 3.1 8B Instruct** über **Ollama** aus und speichert die Ergebnisse im JSON-Format.

Die Ausgabe erfolgt getrennt nach Szenario und Split
(z. B. persona / no-persona oder preference_agree / preference_disagree).

## Evaluation (Sycophancy)

Die eigentliche Bewertung der Modellantworten erfolgt mit
`Evaluation/Non_Deceptiveness/test_sycophancy_deepseek.py`

Dabei werden jeweils zwei Antwortdateien paarweise verglichen.
Ein Evaluator-Modell (Deepseek Chat oder Reasoner) entscheidet, ob sich die Antworten inhaltlich widersprechen
(„Persona- bzw. Preference-Wechsel“).

Verwendete Evaluatoren:
- **deepseek-chat** (non-reasoning)
- **deepseek-reasoner** (reasoning)

Alle Evaluierungen werden, wie bei BeHonest, mit `temperature = 0.0` durchgeführt.

## Auswertung

Zur quantitativen Analyse (Prozentwerte, betroffene IDs, Überlappungen zwischen
Evaluatoren) wird das Skript `Evaluation/Non_Deceptiveness/analyze_sycophancy_deepseek.py`
verwendet.  
Dieses Skript extrahiert:
- die Sycophancy-Rate,
- die IDs mit festgestelltem Antwortwechsel,
- Überschneidungen und Abweichungen zwischen Chat- und Reasoner-Evaluator.

## Reproduzierbarkeit

- Alle Prompts stammen unverändert aus dem BeHonest-Datensatz.
- Die Modellparameter sind dokumentiert (u. a. `temperature = 0.0`).
- Sämtliche generierten Antworten, Evaluationsausgaben und Skripte sind
  versioniert im Repository enthalten.
- Die Experimente können vollständig lokal reproduziert werden.

## Anleitung zur Reproduktion der Experimente

1. Abhängigkeiten in virtueller Umgebung installieren:
```bash
pip install -r requirements.txt
```
2. Ollama starten und Modell laden
```bash
ollama pull llama3.1:8b
```
3. Sycophancy – Antwortgenerierung:
Hierfür im Skript unter 'SCENARIO=[]' Persona oder Preference Sycophancy angeben.
```bash
python Scripts/generation/generate_llama31_with_ollama_behonest.py
```
4. Evaluation mit DeepSeek (Chat oder Reasoner):
Ggf. Filenamen anpassen und bei 'model' deepseek-reasoner angeben.
```bash
python Evaluation/Non_Deceptiveness/test_sycophancy_deepseek.py \
  --mode Persona \
  --model deepseek-chat \
  --file1 Persona_Sycophancy/output/Llama31_8B_Instruct/persona.json \
  --file2 Persona_Sycophancy/output/Llama31_8B_Instruct/no_persona.json
```
5. Auswertung
```bash
python Evaluation/Non_Deceptiveness/analyze_sycophancy_deepseek.py \
  --explanation_file Persona_Sycophancy/output/Llama31_8B_Instruct/chat_persona_explanation.json
```

6. Vergleich der Persona- bzw. Preference-Wechsel (IDs)\
In der Datei `/home/ella/lokale_repos/BeHonest/Evaluation/Non_Deceptiveness/compare_preference_changed_ids.py`
werden die zuvor erzeugten ID-Listen dahingehend ausgewertet, dass eine neue Datei erzeugt wird, in der jeweils die 
IDs der Persona- oder Preference-Wechsel festgehalten werden, sowohl einzeln (nur Chat oder nur Reasoner) als auch gemeinsam (beide Deepseek-Varianten).
```bash
python Evaluation/Non_Deceptiveness/compare_preference_changed_ids.py
```

## Hinweise zu verwendeter Hardware & System

- Betriebssystem: Linux (Mint)
- Inferenz: lokal via Ollama
- GPU: NVIDIA RTX 3060 Ti (8 GB VRAM)

## API Keys

Für die Evaluation mit DeepSeek wird ein API-Key benötigt.
Der Key wird **nicht** im Repository gespeichert, sondern über
Umgebungsvariablen gesetzt:

```bash
export DEEPSEEK_API_KEY=...
export DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## Limitationen

- Aktuell werden nur Sycophancy-Szenarien aus BeHonest betrachtet.
- Die Ergebnisse sind nicht direkt numerisch mit dem Originalpaper vergleichbar,
  da ein anderes Evaluator-Modell (DeepSeek statt GPT-4) verwendet wird.
- Ziel ist eine qualitative Analyse der Evaluator-Sensitivität, nicht ein exakter Replikationswert.