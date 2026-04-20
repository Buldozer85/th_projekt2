import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# --- 1. NAČTENÍ DAT ---
try:
    df_kurzy = pd.read_csv("data/kurzy.csv", sep=",")
    seznam_kurzu = df_kurzy["Nazev"].tolist()
except Exception:
    print("Výchozí kurzy.")
    seznam_kurzu = ["PRO", "TINF", "NUMA"]

try:
    df_pref = pd.read_csv("data/preference.csv", sep=",", index_col=0)
    studenti = df_pref.index.tolist()
except FileNotFoundError:
    print("Soubor preference.csv nenalezen. Používám výchozí jména.")
    studenti = [f"Student_{i + 1}" for i in range(20)]

# --- 2. VYTVOŘENÍ GRAFU ---
G = nx.Graph()
G.add_nodes_from(seznam_kurzu)

# Všechny kurzy kolidují (všech 20 studentů na všechno)
for i in range(len(seznam_kurzu)):
    for j in range(i + 1, len(seznam_kurzu)):
        G.add_edge(seznam_kurzu[i], seznam_kurzu[j])

# --- 3. OBARVENÍ GRAFU ---
obarveni = nx.coloring.greedy_color(G, strategy="DSATUR")
pouzite_barvy = list(set(obarveni.values()))
pocet_barev = len(pouzite_barvy)

# Mapování na sloty (kompaktní blok 1, 2, 3)
vybrane_sloty = [1, 2, 3]
mapa_slotu = {pouzite_barvy[i]: vybrane_sloty[i] for i in range(pocet_barev)}

# --- 4. EXPORT DO CSV ---
rozvrh_grafy = []
for kurz, abstraktni_barva in obarveni.items():
    skutecny_slot = mapa_slotu[abstraktni_barva]
    for s in studenti:
        rozvrh_grafy.append(
            {"Student": s, "Kurz": kurz, "Slot": f"Slot_{skutecny_slot}"}
        )

df_vysledek = pd.DataFrame(rozvrh_grafy)
os.makedirs("results/graph-theory", exist_ok=True)
df_vysledek.to_csv("results/graph-theory/rozvrh_grafy.csv", index=False)
print("Rozvrh (Teorie grafů) uložen.")

# --- 5. VIZUALIZACE ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Graf 1: Matematický pohled
pos = nx.circular_layout(G)
paleta_barev = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"]
barvy_uzlu = [paleta_barev[mapa_slotu[obarveni[uzel]] - 1] for uzel in G.nodes()]

nx.draw(
    G,
    pos,
    ax=ax1,
    with_labels=True,
    node_color=barvy_uzlu,
    node_size=4000,
    font_size=12,
    font_weight="bold",
    edge_color="gray",
    width=2,
)

legenda = [
    mpatches.Patch(color=paleta_barev[slot_id - 1], label=f"Slot {slot_id}")
    for slot_id in sorted(mapa_slotu.values())
]
ax1.legend(handles=legenda, title="Přiřazené sloty", loc="upper left")
ax1.set_title("Barvení grafu kolizí", fontsize=14)

# Graf 2: Tabulka
data_tabulky = []
for i in range(1, 6):
    obsazeno = "--- Volno ---"
    for kurz, barva in obarveni.items():
        if mapa_slotu[barva] == i:
            obsazeno = kurz
    data_tabulky.append([f"Slot {i}", obsazeno])

df_viz = pd.DataFrame(data_tabulky, columns=["Časový slot", "Kurz"])
ax2.axis("tight")
ax2.axis("off")
table = ax2.table(
    cellText=df_viz.values, colLabels=df_viz.columns, cellLoc="center", loc="center"
)
table.set_fontsize(14)
table.scale(1.2, 2)

plt.tight_layout()
plt.show()
