import pandas as pd
import os
import re

# --- 1. NAČTENÍ PREFERENCÍ (Plně dynamické z CSV) ---
# Předpokládáme, že první sloupec (index_col=0) jsou jména a zbylých 5 sloupců jsou sloty
df_preference = pd.read_csv("data/rozvrh-ukazka.csv", sep=",", index_col=0)
kurzy = ["PRO", "TINF", "NUMA"]

# Maximální možný počet bodů (každý student dostane své 3 nejoblíbenější sloty)
max_body_celkem = df_preference.apply(lambda row: sum(sorted(row, reverse=True)[:len(kurzy)]), axis=1).sum()


# --- POMOCNÁ FUNKCE: Načtení mapy rozvrhu z CSV ---
def nacti_mapu_z_csv(cesta_k_souboru):
    try:
        df_rozvrh = pd.read_csv(cesta_k_souboru)
        unikatni_kurzy = df_rozvrh[['Kurz', 'Slot']].drop_duplicates()

        mapa = {}
        for _, row in unikatni_kurzy.iterrows():
            kurz = row['Kurz']

            hledane_cislo = re.search(r'\d+', str(row['Slot']))
            if hledane_cislo:
                mapa[kurz] = int(hledane_cislo.group())
        return mapa
    except Exception as e:
        print(f"Pozor: Problém se souborem {cesta_k_souboru}. Chyba: {e}")
        return None


grafy_mapa = nacti_mapu_z_csv("results/graph-theory/rozvrh_grafy.csv")
hry_mapa = nacti_mapu_z_csv("results/game-theory/rozvrh_hry.csv")
ai_mapa = nacti_mapu_z_csv("results/ai/rozvrh_ai.csv")


# --- 3. VÝPOČET METRIK ---
def spocitej_skore_preference(mapa_rozvrhu):
    if not mapa_rozvrhu: return 0
    ziskane_body = 0

    for _, preference in df_preference.iterrows():
        for kurz, slot_cislo in mapa_rozvrhu.items():
            index_sloupce = int(slot_cislo) - 1
            if index_sloupce < len(df_preference.columns):
                odpovidajici_sloupec = df_preference.columns[index_sloupce]
                ziskane_body += preference[odpovidajici_sloupec]

    return ziskane_body / max_body_celkem


def spocitej_cekani(mapa_rozvrhu):
    if not mapa_rozvrhu: return 0
    sloty = sorted(mapa_rozvrhu.values())
    # Čekání je rozdíl mezi prvním a posledním slotem mínus počet kurzů (které trvají 1 slot)
    # Příklad: sloty 1, 3, 5 -> (5 - 1) = 4 sloty rozpětí, ale jsou tam 3 kurzy, takže 2 sloty čekání
    rozpeti = sloty[-1] - sloty[0]
    pocet_kurzu = len(sloty)
    cekani = max(0, rozpeti - (pocet_kurzu - 1))
    return cekani


# --- 4. SESTAVENÍ FINÁLNÍ TABULKY ---
def vytvor_radek(nazev, mapa):
    if not mapa: return None
    score = spocitej_skore_preference(mapa)
    cekani = spocitej_cekani(mapa)

    radek = {
        'Rozvrhy': nazev,
        'Spokojenost': f"{round(score * 100, 1)}%",
        'Cekani_Sloty': cekani
    }
    for i in range(1, 6):
        kurz_ve_slotu = ""
        for k, s in mapa.items():
            if s == i: kurz_ve_slotu = k
        radek[f'Slot{i}'] = kurz_ve_slotu
    return radek


data_vysledek = [
    vytvor_radek("Teorie_Grafu", grafy_mapa),
    vytvor_radek("Teorie_Her", hry_mapa),
    vytvor_radek("Generativni_AI", ai_mapa)
]
# Vyfiltrujeme případné prázdné řádky
data_vysledek = [r for r in data_vysledek if r is not None]

df_final = pd.DataFrame(data_vysledek)

# --- 5. ULOŽENÍ A VÝPIS ---
os.makedirs("results/final", exist_ok=True)
cesta = "results/final/Rozvrh_Srovnani.csv"
df_final.to_csv(cesta, index=False)

print(f"\n--- Finální srovnávací tabulka uložena do: {cesta} ---\n")
print(df_final.to_string(index=False))