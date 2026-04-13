import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. NAČTENÍ DAT ---
try:
    df_kurzy = pd.read_csv("data/kurzy.csv", sep=",")
    seznam_kurzu = df_kurzy["Nazev"].tolist()
except:
    print("Výchozí kurzy.")
    seznam_kurzu = ["PRO", "TINF", "NUMA"]

try:
    # index_col=0 říká, že první sloupec (Student_1...) jsou názvy řádků
    df_preference = pd.read_csv("data/preference.csv", sep=";", index_col=0)
except FileNotFoundError:
    print("Soubor preference.csv nenalezen. Vytvářím náhodná cvičná data.")
    np.random.seed(42)
    data = np.random.randint(1, 11, size=(20, 5))
    df_preference = pd.DataFrame(data, columns=[f"Slot_{i}" for i in range(1, 6)],
                                 index=[f"Student_{i}" for i in range(1, 21)])

# --- 2. TEORIE HER (Hlasovací mechanismus) ---
# Sečteme všechny hlasy (body) pro každý sloupec (slot)
hlasy_pro_sloty = df_preference.sum()

# Zjistíme, které 3 sloty získaly nejvíce hlasů
vitezne_sloty_nazvy = hlasy_pro_sloty.sort_values(ascending=False).index.tolist()[:len(seznam_kurzu)]

# Pro snazší práci s tabulkou si z názvu "Slot_3" vytáhneme jen číslo 3
vitezne_sloty_cisla = [int(s.split("_")[1]) for s in vitezne_sloty_nazvy]

# Namapujeme kurzy na vítězné sloty
mapa_rozvrhu = {}
for i, kurz in enumerate(seznam_kurzu):
    mapa_rozvrhu[kurz] = vitezne_sloty_cisla[i]

# ==========================================
# --- 3. EXPORT DO CSV (Sestavení rozvrhu) ---
# ==========================================
rozvrh_hry = []
studenti = df_preference.index.tolist()

for kurz, slot_cislo in mapa_rozvrhu.items():
    for s in studenti:
        rozvrh_hry.append({
            "Student": s,
            "Kurz": kurz,
            "Slot": f"Slot_{slot_cislo}"
        })

df_vysledek = pd.DataFrame(rozvrh_hry)
# Uložení (přizpůsob si cestu podle sebe, např. jen "rozvrh_hry.csv")
df_vysledek.to_csv("results/game-theory/rozvrh_hry.csv", index=False)
print(f"Rozvrh byl úspěšně uložen do 'rozvrh_hry.csv'. Vítězné sloty: {vitezne_sloty_cisla}")

# ==========================================
# --- 4. VIZUALIZACE 1: VÝSLEDKY HLASOVÁNÍ ---
# ==========================================
fig1, ax1 = plt.subplots(figsize=(8, 5))

# Vítězné sloty obarvíme zeleně, poražené šedě
barvy = ['#4CAF50' if slot in vitezne_sloty_nazvy else '#cccccc' for slot in hlasy_pro_sloty.index]

hlasy_pro_sloty.plot(kind='bar', color=barvy, ax=ax1, edgecolor='black')
ax1.set_title("Výsledky hlasování studentů o časové sloty", fontsize=14)
ax1.set_ylabel("Celkový počet bodů (Společenský blahobyt)")
ax1.set_xlabel("Časové sloty")
plt.xticks(rotation=0)

# Přidání čísel nad sloupce
for p in ax1.patches:
    ax1.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.015))
plt.tight_layout()

# ==========================================
# --- 5. VIZUALIZACE 2: REÁLNÝ ROZVRH ---
# ==========================================
data_rozvrhu = []
for i in range(1, 6):
    obsazeno_kurzem = "--- Volno ---"
    for kurz, slot_cislo in mapa_rozvrhu.items():
        if slot_cislo == i:
            obsazeno_kurzem = kurz
    data_rozvrhu.append([f"Slot {i}", obsazeno_kurzem])

df_viz = pd.DataFrame(data_rozvrhu, columns=["Časový slot", "Přiřazený kurz"])

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.axis('tight')
ax2.axis('off')

table = ax2.table(cellText=df_viz.values, colLabels=df_viz.columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1.2, 2)

# Estetické obarvení (zvolil jsem oranžovou pro odlišení od teorie grafů)
for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_facecolor('#FF9800')
        cell.set_text_props(color='white', weight='bold')
    elif cell.get_text().get_text() != "--- Volno ---" and key[1] == 1:
        cell.set_facecolor('#FFE0B2')
    elif cell.get_text().get_text() == "--- Volno ---" and key[1] == 1:
        cell.set_text_props(color='gray', style='italic')

plt.title("Uživatelský pohled: Rozvrh z Teorie her", fontsize=14, pad=20)
plt.tight_layout()

plt.show()