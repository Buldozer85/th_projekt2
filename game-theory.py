import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# --- 1. NAČTENÍ DAT ---
try:
    df_kurzy = pd.read_csv("data/kurzy.csv", sep=",")
    seznam_kurzu = df_kurzy["Nazev"].tolist()
except Exception:
    seznam_kurzu = ["PRO", "TINF", "NUMA"]

try:
    df_preference = pd.read_csv("data/preference.csv", sep=",", index_col=0)
except FileNotFoundError:
    print("Soubor preference.csv nenalezen.")
    exit()

# --- 2. HLASOVACÍ MECHANISMUS ---
hlasy_pro_sloty = df_preference.sum()
vitezne_sloty_nazvy = hlasy_pro_sloty.sort_values(ascending=False).index.tolist()[
    : len(seznam_kurzu)
]

# Robustní extrakce čísel slotů
vitezne_sloty_cisla = []
for s in vitezne_sloty_nazvy:
    match = re.search(r"\d+", str(s))
    if match:
        vitezne_sloty_cisla.append(int(match.group()))

mapa_rozvrhu = {kurz: vitezne_sloty_cisla[i] for i, kurz in enumerate(seznam_kurzu)}

# --- 3. EXPORT DO CSV ---
rozvrh_hry = []
studenti = df_preference.index.tolist()

for kurz, slot_cislo in mapa_rozvrhu.items():
    for s in studenti:
        rozvrh_hry.append(
            {"Student": s, "Kurz": kurz, "Slot": f"Slot_{slot_cislo}"}
        )

df_vysledek = pd.DataFrame(rozvrh_hry)
os.makedirs("results/game-theory", exist_ok=True)
df_vysledek.to_csv("results/game-theory/rozvrh_hry.csv", index=False)
print("Rozvrh (Teorie her - Hlasování) uložen.")

# --- 4. VIZUALIZACE ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Graf 1: Výsledky hlasování
barvy = [
    "#4CAF50" if slot in vitezne_sloty_nazvy else "#cccccc"
    for slot in hlasy_pro_sloty.index
]
hlasy_pro_sloty.plot(kind="bar", color=barvy, ax=ax1, edgecolor="black")
ax1.set_title("Výsledky hlasování studentů", fontsize=14)
ax1.set_ylabel("Celkový počet bodů")
ax1.tick_params(axis="x", rotation=0)

# Graf 2: Tabulka
data_rozvrhu = []
for i in range(1, 6):
    obsazeno = "--- Volno ---"
    for kurz, slot_cislo in mapa_rozvrhu.items():
        if slot_cislo == i:
            obsazeno = kurz
    data_rozvrhu.append([f"Slot {i}", obsazeno])

df_viz = pd.DataFrame(data_rozvrhu, columns=["Časový slot", "Přiřazený kurz"])
ax2.axis("off")
table = ax2.table(
    cellText=df_viz.values, colLabels=df_viz.columns, cellLoc="center", loc="center"
)
table.set_fontsize(14)
table.scale(1.2, 2)

plt.tight_layout()
plt.show()
