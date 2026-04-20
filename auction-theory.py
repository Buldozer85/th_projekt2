import pandas as pd
import numpy as np
import os

# --- 1. NAČTENÍ DAT ---
df_preference = pd.read_csv("data/preference.csv", sep=",", index_col=0)
df_kurzy = pd.read_csv("data/kurzy.csv", sep=",")
seznam_kurzu = df_kurzy["Nazev"].tolist()
pocet_slotu = len(df_preference.columns)

# Matice vah: Každý kurz má jiné preference podle své cílové skupiny
# Kurz 0 (PRO): Studenti 1-10 (Ráno)
# Kurz 1 (TINF): Studenti 11-20 (Odpoledne)
# Kurz 2 (NUMA): Všichni (Průměr)
vahy = []
vahy.append(df_preference.iloc[0:10].sum().values)   # PRO miluje ráno
vahy.append(df_preference.iloc[10:20].sum().values)  # TINF miluje odpoledne
vahy.append(df_preference.sum().values / 2)          # NUMA je neutrální
vahy = np.array(vahy)

# --- 2. AUKČNÍ ALGORITMUS (Bertsekas) ---
pocet_kurzu = len(seznam_kurzu)
prirazeni = [-1] * pocet_kurzu
ceny_slotu = np.zeros(pocet_slotu)
epsilon = 1.0 / (pocet_kurzu + 1)

while -1 in prirazeni:
    for i in range(pocet_kurzu):
        if prirazeni[i] == -1:
            hodnoty = vahy[i] - ceny_slotu
            idx_best = np.argmax(hodnoty)
            v_best = hodnoty[idx_best]
            
            temp_hodnoty = hodnoty.copy()
            temp_hodnoty[idx_best] = -np.inf
            idx_second = np.argmax(temp_hodnoty)
            v_second = temp_hodnoty[idx_second]
            
            bid = v_best - v_second + epsilon
            
            if idx_best in prirazeni:
                stary_vlastnik = prirazeni.index(idx_best)
                prirazeni[stary_vlastnik] = -1
            
            prirazeni[i] = idx_best
            ceny_slotu[idx_best] += bid

# --- 3. EXPORT ---
rozvrh_aukce = []
for i, slot_idx in enumerate(prirazeni):
    kurz = seznam_kurzu[i]
    slot_cislo = slot_idx + 1
    for student in df_preference.index:
        rozvrh_aukce.append({"Student": student, "Kurz": kurz, "Slot": f"Slot_{slot_cislo}"})

df_vysledek = pd.DataFrame(rozvrh_aukce)
os.makedirs("results/game-theory", exist_ok=True)
df_vysledek.to_csv("results/game-theory/rozvrh_aukce.csv", index=False)
print(f"Aukce (Divergentní) dokončena. Prirazeni: {prirazeni}")
