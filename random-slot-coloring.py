import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# --- 1. Načtení kurzů ---
try:
    df_kurzy = pd.read_csv("data/kurzy.csv")
    seznam_kurzu = df_kurzy["Nazev"].tolist()
except:
    print("Výchozí kurzy.")
    seznam_kurzu = ["PRO", "TINF", "NUMA"]

# --- 2. Vytvoření grafu (vrcholy a hrany) ---
G = nx.Graph()
G.add_nodes_from(seznam_kurzu)

# V základní variantě chodí všech 20 studentů na všechny 3 kurzy.
for i in range(len(seznam_kurzu)):
    for j in range(i + 1, len(seznam_kurzu)):
        G.add_edge(seznam_kurzu[i], seznam_kurzu[j])

# --- 3. Obarvení grafu (přiřazení abstraktních barev) ---
obarveni = nx.coloring.greedy_color(G, strategy="largest_first")

pouzite_barvy = list(set(obarveni.values()))
pocet_barev = len(pouzite_barvy)

# Máme 5 dostupných slotů
dostupne_sloty = [1, 2, 3, 4, 5]

# NÁHODNÝ VÝBĚR: 3 unikátní sloty z 5 dostupných
vybrane_sloty = random.sample(dostupne_sloty, pocet_barev)

mapa_slotu = {pouzite_barvy[i]: vybrane_sloty[i] for i in range(pocet_barev)}

print(f"Algoritmus použil {pocet_barev} barvy. Mapuji je na sloty: {vybrane_sloty}")

# ==========================================
# --- 4. EXPORT DO CSV (Sestavení rozvrhu) ---
# ==========================================
rozvrh_grafy = []
studenti = [f"Student_{i + 1}" for i in range(20)]

for kurz, abstraktni_barva in obarveni.items():
    skutecny_slot = mapa_slotu[abstraktni_barva]

    for s in studenti:
        rozvrh_grafy.append({
            "Student": s,
            "Kurz": kurz,
            "Slot": f"Slot_{skutecny_slot}"
        })

df_vysledek = pd.DataFrame(rozvrh_grafy)
df_vysledek.to_csv("results/graph-theory/random-rozvrh_grafy.csv", index=False)
print("\nRozvrh byl úspěšně uložen do 'rozvrh_grafy.csv'.")

# ==========================================
# --- 5. VIZUALIZACE GRAFU ---
# ==========================================
plt.figure(figsize=(8, 6))

# Nastavení vizuálního rozložení uzlů (např. do kruhu)
pos = nx.circular_layout(G)

paleta_barev = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

# Každému uzlu v grafu přiřadíme barvu podle toho, jaký slot (číslo 0-4) dostal
barvy_uzlu = [paleta_barev[obarveni[uzel]] for uzel in G.nodes()]

# Vykreslení samotného grafu
nx.draw(G, pos, with_labels=True, node_color=barvy_uzlu,
        node_size=4000, font_size=12, font_weight='bold', edge_color='gray', width=2)

legenda = []
# Zjistíme, jaké unikátní barvy (sloty) se reálně použily
pouzite_sloty = set(obarveni.values())
for slot_id in sorted(pouzite_sloty):
    legenda.append(mpatches.Patch(color=paleta_barev[slot_id], label=f"Slot {slot_id + 1}"))

plt.legend(handles=legenda, title="Přiřazené časové sloty", loc="upper left", bbox_to_anchor=(1, 1))
plt.title("Vizualizace rozvrhu: Barvení grafu kolizí", fontsize=16)

plt.tight_layout()

# ==========================================
# --- 6. VIZUALIZACE 2: REÁLNÝ ROZVRH ---
# ==========================================
data_rozvrhu = []
for i in range(1, 6):
    obsazeno_kurzem = "--- Volno ---"
    for kurz, abstraktni_barva in obarveni.items():
        if mapa_slotu[abstraktni_barva] == i:
            obsazeno_kurzem = kurz
    data_rozvrhu.append([f"Slot {i}", obsazeno_kurzem])

df_viz = pd.DataFrame(data_rozvrhu, columns=["Časový slot", "Přiřazený kurz"])

fig2, ax = plt.subplots(figsize=(6, 4))
ax.axis('tight')
ax.axis('off')

# Vykreslení tabulky
table = ax.table(cellText=df_viz.values, colLabels=df_viz.columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1.2, 2)

# Estetické obarvení tabulky
for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_facecolor('#4CAF50') # Zelená hlavička
        cell.set_text_props(color='white', weight='bold')
    elif cell.get_text().get_text() != "--- Volno ---" and key[1] == 1:
        cell.set_facecolor('#D5E8D4') # Světle zelené podbarvení obsazených slotů
    elif cell.get_text().get_text() == "--- Volno ---" and key[1] == 1:
        cell.set_text_props(color='gray', style='italic')

plt.title("Uživatelský pohled: Výsledný školní rozvrh", fontsize=14, pad=20)
plt.tight_layout()

plt.show()