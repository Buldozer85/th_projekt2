import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

# --- 1. NAČTENÍ DAT ---
try:
    df_kurzy = pd.read_csv("data/kurzy.csv", sep=";")
    seznam_kurzu = df_kurzy["Nazev"].tolist()
except:
    print("Výchozí kurzy.")
    seznam_kurzu = ["PRO", "TINF", "NUMA"]

try:
    # sep="," protože tvá data mají čárky
    df_preference = pd.read_csv("data/preference.csv", sep=",", index_col=0)
except FileNotFoundError:
    print("Soubor preference.csv nenalezen. Ukončuji.")
    exit()

# --- 2. TEORIE HER (Hlasovací mechanismus) ---
hlasy_pro_sloty = df_preference.sum()
vitezne_sloty_nazvy = hlasy_pro_sloty.sort_values(ascending=False).index.tolist()[:len(seznam_kurzu)]

# ROBUSTNÍ ŘEŠENÍ: Získá číslo slotu pomocí regulárních výrazů
vitezne_sloty_cisla = []
for s in vitezne_sloty_nazvy:
    hledane_cislo = re.search(r'\d+', str(s))
    if hledane_cislo:
        vitezne_sloty_cisla.append(int(hledane_cislo.group()))

mapa_rozvrhu = {}
for i, kurz in enumerate(seznam_kurzu):
    mapa_rozvrhu[kurz] = vitezne_sloty_cisla[i]

# ==========================================
# --- 3. EXPORT DO CSV (Sestavení rozvrhu) ---
# ==========================================
rozvrh_hry = []
studenti = df_preference.index.tolist() # Přesná jména z dat (např. Student1)

for kurz, slot_cislo in mapa_rozvrhu.items():
    for s in studenti:
        rozvrh_hry.append({
            "Student": s,
            "Kurz": kurz,
            "Slot": f"Slot_{slot_cislo}"
        })

df_vysledek = pd.DataFrame(rozvrh_hry)
os.makedirs("results/game-theory", exist_ok=True)
df_vysledek.to_csv("results/game-theory/rozvrh_hry.csv", index=False)
print(f"Rozvrh uložen do 'results/game-theory/rozvrh_hry.csv'. Vítězné sloty: {vitezne_sloty_cisla}")

# ==========================================
# --- 4. VIZUALIZACE ---
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# GRAF 1: Výsledky hlasování
barvy = ['#4CAF50' if slot in vitezne_sloty_nazvy else '#cccccc' for slot in hlasy_pro_sloty.index]
hlasy_pro_sloty.plot(kind='bar', color=barvy, ax=ax1, edgecolor='black')
ax1.set_title("Výsledky hlasování studentů o časové sloty", fontsize=14)
ax1.set_ylabel("Celkový počet bodů (Společenský blahobyt)")
ax1.set_xlabel("Časové sloty")
ax1.tick_params(axis='x', rotation=0)

for p in ax1.patches:
    ax1.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.015))

# GRAF 2: Reálný rozvrh
data_rozvrhu = []
for i in range(1, 6):
    obsazeno = "--- Volno ---"
    for kurz, slot_cislo in mapa_rozvrhu.items():
        if slot_cislo == i:
            obsazeno = kurz
    data_rozvrhu.append([f"Slot {i}", obsazeno])

df_viz = pd.DataFrame(data_rozvrhu, columns=["Časový slot", "Přiřazený kurz"])
ax2.axis('tight')
ax2.axis('off')

table = ax2.table(cellText=df_viz.values, colLabels=df_viz.columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1.2, 2)

for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_facecolor('#FF9800')
        cell.set_text_props(color='white', weight='bold')
    elif cell.get_text().get_text() != "--- Volno ---" and key[1] == 1:
        cell.set_facecolor('#FFE0B2')
    elif cell.get_text().get_text() == "--- Volno ---" and key[1] == 1:
        cell.set_text_props(color='gray', style='italic')

ax2.set_title("Uživatelský pohled: Rozvrh z Teorie her", fontsize=14, pad=20)
plt.tight_layout()
plt.show()