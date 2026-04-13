import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# --- 1. Načtení kurzů ---
try:
    df_kurzy = pd.read_csv("data/kurzy.csv", sep=";")
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

# --- 3. Obarvení grafu (přiřazení slotů) ---
obarveni = nx.coloring.greedy_color(G, strategy="largest_first")

# ==========================================
# --- 4. EXPORT DO CSV (Sestavení rozvrhu) ---
# ==========================================
rozvrh_grafy = []
# Předpokládáme 20 studentů
studenti = [f"Student_{i + 1}" for i in range(20)]

for kurz, barva in obarveni.items():
    slot = barva + 1  # Barva 0 -> Slot 1, Barva 1 -> Slot 2, atd.

    for s in studenti:
        rozvrh_grafy.append({
            "Student": s,
            "Kurz": kurz,
            "Slot": f"Slot_{slot}"
        })

df_vysledek = pd.DataFrame(rozvrh_grafy)
df_vysledek.to_csv("results/graph-theory/rozvrh_grafy.csv", index=False)
print("Rozvrh byl úspěšně uložen do 'rozvrh_grafy.csv'.")

# ==========================================