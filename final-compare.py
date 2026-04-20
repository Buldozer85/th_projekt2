import pandas as pd
import numpy as np
import os
import re

# --- 1. NAČTENÍ PREFERENCÍ ---
df_preference = pd.read_csv("data/rozvrh-ukazka.csv", sep=",", index_col=0)
kurzy = ["PRO", "TINF", "NUMA"]

# Maximální možný počet bodů
max_body_celkem = df_preference.apply(
    lambda row: sum(sorted(row, reverse=True)[: len(kurzy)]), axis=1
).sum()


# --- POMOCNÁ FUNKCE ---
def nacti_mapu_z_csv(cesta_k_souboru):
    try:
        df_rozvrh = pd.read_csv(cesta_k_souboru)
        unikatni_kurzy = df_rozvrh[["Kurz", "Slot"]].drop_duplicates()
        mapa = {}
        for _, row in unikatni_kurzy.iterrows():
            match = re.search(r"\d+", str(row["Slot"]))
            if match:
                mapa[row["Kurz"]] = int(match.group())
        return mapa
    except Exception as e:
        print(f"Chyba při načítání {cesta_k_souboru}: {e}")
        return None


# Načtení map pro srovnání
grafy_mapa = nacti_mapu_z_csv("results/graph-theory/rozvrh_grafy.csv")
hry_mapa = nacti_mapu_z_csv("results/game-theory/rozvrh_hry.csv")
ai_mapa = nacti_mapu_z_csv("results/ai/rozvrh_ai.csv")
ai_adv_mapa = nacti_mapu_z_csv("results/ai/rozvrh_ai_advanced.csv")
aukce_mapa = nacti_mapu_z_csv("results/game-theory/rozvrh_aukce.csv")


# --- 3. VÝPOČET METRIK ---
def spocitej_skore_preference(mapa_rozvrhu):
    if not mapa_rozvrhu:
        return 0
    ziskane_body = 0
    for _, preference in df_preference.iterrows():
        for kurz, slot_cislo in mapa_rozvrhu.items():
            idx_sloupce = int(slot_cislo) - 1
            if idx_sloupce < len(df_preference.columns):
                col_name = df_preference.columns[idx_sloupce]
                ziskane_body += preference[col_name]
    return ziskane_body / max_body_celkem


def spocitej_cekani(mapa_rozvrhu):
    if not mapa_rozvrhu:
        return 0
    sloty = sorted(mapa_rozvrhu.values())
    rozpeti = sloty[-1] - sloty[0]
    return max(0, rozpeti - (len(sloty) - 1))


# --- 4. SESTAVENÍ FINÁLNÍ TABULKY ---
def vytvor_radek(nazev, mapa):
    if not mapa:
        return None
    score = spocitej_skore_preference(mapa)
    cekani = spocitej_cekani(mapa)
    radek = {
        "Rozvrhy": nazev,
        "Spokojenost": f"{round(score * 100, 1)}%",
        "Cekani_Sloty": cekani,
    }
    for i in range(1, 6):
        kurz_ve_slotu = ""
        for k, s in mapa.items():
            if s == i:
                kurz_ve_slotu = k
        radek[f"Slot{i}"] = kurz_ve_slotu
    return radek


data_vysledek = [
    vytvor_radek("Teorie_Grafu", grafy_mapa),
    vytvor_radek("Teorie_Her", hry_mapa),
    vytvor_radek("Aukce", aukce_mapa),
    vytvor_radek("AI_Zakladni", ai_mapa),
    vytvor_radek("AI_Pokrocila", ai_adv_mapa),
]
df_final = pd.DataFrame([r for r in data_vysledek if r is not None])

# --- 5. ULOŽENÍ A VÝPIS ---
os.makedirs("results/final", exist_ok=True)
df_final.to_csv("results/final/Rozvrh_Srovnani.csv", index=False)
print("\n--- Finální srovnávací tabulka ---")
print(df_final.to_string(index=False))
