# Dokumentace projektu: Optimalizace školního rozvrhu

## 1. Úvod
Tento projekt porovnává tři přístupy k sestavování rozvrhu pro 20 studentů a 3 kurzy. Pro účely testování byl vytvořen **scénář střetu zájmů**, kde je polovina studentů zaměřena na ranní výuku (Sloty 1, 2) a druhá polovina na večerní výuku (Sloty 4, 5). Cílem je zjistit, jak si algoritmy poradí s takto polarizovanou poptávkou.

## 2. Popis zvolených algoritmů

### A. Teorie grafů (Barvení grafu)
- **Strategie:** Minimalizace časového rozpětí (kompaktnost).
- **Chování:** Algoritmus ignoruje preference a snaží se "napěchovat" kurzy do prvních volných slotů (1, 2, 3).

### B. Teorie her (Mechanismy)
1.  **Hlasovací mechanismus:** Sčítá body všech studentů. V polarizovaném scénáři se snaží najít kompromis nebo uspokojit obě skupiny rozdělením kurzů mezi ráno a večer.
2.  **Aukční algoritmus (Bertsekas):** Kurzy soutěží o sloty. V této verzi má každý kurz svou "cílovou skupinu" studentů, což nutí trh najít optimální rovnováhu.

### C. Generativní AI
1.  **Základní AI:** Volí mechanické rozestupy (1, 3, 5).
2.  **Pokročilá AI (CoT):** Zaměřuje se na efektivitu a kompaktnost, čímž paradoxně v tomto specifickém scénáři dosahuje podobných výsledků jako Teorie grafů.

## 3. Načítání a ukládání dat
Využívá se Python (pandas) pro práci s CSV soubory v `data/` a `results/`. Skript `final-compare.py` provádí objektivní srovnání.

## 4. Výsledky a objektivní srovnání

| Metoda | Spokojenost | Čekání (okna) | Vítězná strategie |
| :--- | :--- | :--- | :--- |
| **Teorie grafů** | 57,5 % | **0 (vynikající)** | Kompaktní blok (1, 2, 3) |
| **Teorie her (Hlasování)** | **72,5 %** | 2 (horší) | Rozdělení Ráno/Večer (1, 2, 5) |
| **Teorie her (Aukce)** | **72,5 %** | 2 (horší) | Rozdělení Ráno/Večer (1, 2, 5) |
| **AI (Základní)** | 60,0 % | 2 (horší) | Mechanické (1, 3, 5) |
| **AI (Pokročilá)** | 57,5 % | **0 (vynikající)** | Kompaktní blok (1, 2, 3) |

**Zjištěné limity a poznatky:**
- **Teorie grafů** je skvělá pro školu (žádná okna), ale v tomto scénáři "ubližuje" polovině studentů (sovy musí ráno do školy).
- **Teorie her** (Hlasování/Aukce) vykazuje nejvyšší spokojenost, protože dokáže reflektovat potřeby obou skupin studentů, i za cenu volných oken v rozvrhu.
- **Pokročilá AI** se ukázala jako "příliš zaměřená na výkon" – optimalizovala na nulová okna (jako grafy), čímž ale obětovala spokojenost soví skupiny.

## 5. Závěr
Projekt prokázal, že **matematické modely Teorie her jsou nejvhodnější pro diverzifikované skupiny studentů**. Teorie grafů by měla být použita pouze jako doplňkový nástroj pro hlídání kapacitních limitů a kolizí.
