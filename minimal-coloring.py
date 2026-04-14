import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import os

# --- 1. NAČTENÍ DAT ---
try:
    df_kurzy = pd.read_csv("data/kurzy.csv", sep=";")
    seznam_kurzu = df_kurzy["Nazev"].tolist()
except:
    print("Výchozí kurzy.")
    seznam_kurzu = ["PRO", "TINF", "NUMA"]

# Dynamické načtení jmen studentů (podle tvého souboru s preferencemi)
try:
    # sep="," protože tvá data mají čárky
    df_pref = pd.read_csv("data/preference.csv", sep=",", index_col=0)
    studenti = df_pref.index.tolist()
except FileNotFoundError:
    print("Soubor preference.csv nenalezen. Používám výchozí jména Student_1 až Student_20.")
    studenti = [f"Student_{i + 1}" for i in range(20)]

# --- 2. VYTPOŘENÍ GRAFU ---
G = nx.Graph()
G.add_nodes_from(seznam_kurzu)

# Úplný graf pro základní variantu (všechny kurzy kolidují)
for i in range(len(seznam_kurzu)):
    for j in range(i + 1, len(seznam_kurzu)):
        G.add_edge(seznam_kurzu[i], seznam_kurzu[j])

# --- 3. OBARVENÍ GRAFU A MAPOVÁNÍ SLOTŮ ---
obarveni = nx.coloring.greedy_color(G, strategy="DSATUR")

pouzite_barvy = list(set(obarveni.values()))
pocet_barev = len(pouzite_barvy)
dostupne_sloty = [1, 2, 3, 4, 5]

# Můžeš změnit na random.sample(dostupne_sloty, pocet_barev), pokud chceš sloty rozházet náhodně.
# Zde nechávám pevné první 3 sloty pro nejlepší kontrast u obhajoby (jak jsme se bavili).
vybrane_sloty = [1, 2, 5]
mapa_slotu = {pouzite_barvy[i]: vybrane_sloty[i] for i in range(pocet_barev)}

# ==========================================
# --- 4. EXPORT DO CSV ---
# ==========================================
rozvrh_grafy = []

for kurz, abstraktni_barva in obarveni.items():
    skutecny_slot = mapa_slotu[abstraktni_barva]
    for s in studenti:
        rozvrh_grafy.append({
            "Student": s,
            "Kurz": kurz,
            "Slot": f"Slot_{skutecny_slot}"
        })

df_vysledek = pd.DataFrame(rozvrh_grafy)
os.makedirs("results/graph-theory", exist_ok=True)
df_vysledek.to_csv("results/graph-theory/rozvrh_grafy.csv", index=False)
print("Rozvrh byl úspěšně uložen do 'results/graph-theory/rozvrh_grafy.csv'.")

# ==========================================
# --- 5. VIZUALIZACE ---
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# GRAF 1: Trojúhelník
pos = nx.circular_layout(G)
paleta_barev = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
barvy_uzlu = [paleta_barev[mapa_slotu[obarveni[uzel]] - 1] for uzel in G.nodes()]

nx.draw(G, pos, ax=ax1, with_labels=True, node_color=barvy_uzlu,
        node_size=4000, font_size=12, font_weight='bold', edge_color='gray', width=2)

legenda = [mpatches.Patch(color=paleta_barev[slot_id - 1], label=f"Slot {slot_id}") for slot_id in sorted(mapa_slotu.values())]
ax1.legend(handles=legenda, title="Přiřazené časové sloty", loc="upper left", bbox_to_anchor=(1, 1))
ax1.set_title("Matematický pohled: Barvení grafu kolizí", fontsize=14)

# GRAF 2: Tabulka
data_rozvrhu = []
for i in range(1, 6):
    obsazeno = "--- Volno ---"
    for kurz, barva in obarveni.items():
        if mapa_slotu[barva] == i:
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
        cell.set_facecolor('#4CAF50')
        cell.set_text_props(color='white', weight='bold')
    elif cell.get_text().get_text() != "--- Volno ---" and key[1] == 1:
        cell.set_facecolor('#D5E8D4')
    elif cell.get_text().get_text() == "--- Volno ---" and key[1] == 1:
        cell.set_text_props(color='gray', style='italic')

ax2.set_title("Uživatelský pohled: Výsledný školní rozvrh", fontsize=14, pad=20)
plt.tight_layout()
plt.show()