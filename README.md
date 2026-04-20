# Optimalizace školního rozvrhu (TH Projekt)

Tento projekt porovnává různé matematické a technologické přístupy k sestavování školního rozvrhu.

## 🛠 Požadavky
Pro spuštění skriptů je vyžadován Python 3 a následující knihovny:
```bash
pip install pandas numpy networkx matplotlib
```

## 🚀 Jak spustit projekt
Skripty by měly být spouštěny v tomto pořadí pro vygenerování všech výsledků:

1. **Teorie grafů:** `python minimal-coloring.py` (vytvoří základní rozvrh bez preferencí)
2. **Teorie her (Hlasování):** `python game-theory.py` (vytvoří rozvrh podle preferencí)
3. **Teorie her (Aukce):** `python auction-theory.py` (vytvoří rozvrh pomocí aukčního algoritmu)
4. **Finální srovnání:** `python final-compare.py` (vygeneruje srovnávací tabulku všech metod)

## 📊 Metodiky
- **Graph Theory:** Barvení grafu (DSATUR) pro eliminaci kolizí.
- **Game Theory:** Hlasovací mechanismy a Bertsekasův aukční algoritmus.
- **Generativní AI:** Srovnání Zero-shot vs. Chain-of-Thought přístupu.

## 📁 Struktura složek
- `data/`: Vstupní CSV soubory s kurzy a preferencemi studentů.
- `results/`: Vygenerované rozvrhy a finální srovnávací tabulka.
- `results/ai/prompty.txt`: Seznam použitých promptů pro AI.
- `dokumentace.md`: Podrobná zpráva k projektu.
