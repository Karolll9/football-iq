import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="Football IQ", page_icon="⚽", layout="wide")

# Twój stały arkusz zbiorczy zapisany na stałe w kodzie
MASTER_SHEET_URL = "https://docs.google.com/spreadsheets/d/1mWGQDCxM0rHbxVsh0v247PB75eQexlIjUTAJ3UtSas/edit?gid=0#gid=0"

@st.cache_data
def load_data():
    if "edit" in MASTER_SHEET_URL:
        csv_url = MASTER_SHEET_URL.split("/edit")[0] + "/export?format=csv"
    else:
        csv_url = MASTER_SHEET_URL
    return pd.read_csv(csv_url)

# Sprawdzenie, czy w adresie URL jest przekazany zawodnik (np. ?player=Bałaj)
query_params = st.query_params
url_player = query_params.get("player", None)

try:
    df = load_data()
    
    # Automatyczne szukanie kolumny z imieniem i nazwiskiem zawodnika
    player_col = None
    for col in df.columns:
        if any(name in col.lower() for name in ["zawodnik", "imię", "nazwisko", "player", "gracz"]):
            player_col = col
            break

    if url_player:
        # --- WIDOK DLA ZAWODNIKA (BEZ ŻADNEGO WKLEJANIA LINKÓW) ---
        st.title(f"👤 Profil Zawodnika: {url_player}")
        st.info("Oto Twoja historia meczów i statystyki. Dane aktualizują się automatycznie po każdym meczu.")
        
        if player_col:
            # Filtrowanie wierszy dla konkretnego zawodnika
            player_df = df[df[player_col].astype(str).str.strip().str.lower() == url_player.strip().lower()]
            
            if not player_df.empty:
                st.success(f"Znaleziono mecze dla: **{url_player}**")
                st.dataframe(player_df, use_container_width=True)
            else:
                st.warning(f"Nie znaleziono jeszcze żadnych wpisów dla zawodnika: **{url_player}** w arkuszu.")
        else:
            st.error("W arkuszu zbiorczym nie znaleziono kolumny z imieniem zawodnika.")
            
    else:
        # --- PANEL TRENERA / WIDOK GŁÓWNY ---
        st.title("⚽ Football IQ - Panel Trenera i Zawodnika")
        
        menu = st.sidebar.selectbox("Wybierz widok", ["Panel Trenera", "Profil Zawodnika"])

        pozycje = [
            "ŚO (Środkowy Obrońca)",
            "Bok obrony",
            "Wahadłowy",
            "Skrzydłowy (7/11)",
            "6 (Defensywny Pomocnik)",
            "8 (Pomocnik)",
            "10 (Ofensywny Pomocnik)",
            "9 (Napastnik)"
        ]

        wybrana_pozycja = st.sidebar.selectbox("Wybierz pozycję", pozycje)

        if menu == "Panel Trenera":
            st.header("📋 Panel Trenera")
            st.info(f"Aktywna analiza dla pozycji: **{wybrana_pozycja}**")
            
            if wybrana_pozycja == "ŚO (Środkowy Obrońca)":
                st.write("📌 **Mapowanie dla Środkowego Obrońcy:**")
                st.markdown("- Ocena końcowa: **AF** | Procenty: **AC, AD, AE** | Oceny szczegółowe: **Y, Z, AA, AB** | Taktyczna i średnia: **D-H**")
            elif wybrana_pozycja == "Bok obrony":
                st.write("📌 **Mapowanie dla Boku obrony:**")
                st.markdown("- Ocena końcowa: **AH** | Procenty: **AD, AE, AF, AG** | Oceny szczegółowe: **Z, AA, AB, AC** | Taktyczna: **D-I**")
            elif wybrana_pozycja == "Wahadłowy":
                st.write("📌 **Mapowanie dla Wahadłowego:**")
                st.markdown("- Ocena końcowa: **AO** | Procenty: **AK, AL, AM, AN** | Oceny szczegółowe: **AE-AJ** | Taktyczna: **D-I**")
            elif wybrana_pozycja == "Skrzydłowy (7/11)":
                st.write("📌 **Mapowanie dla Skrzydłowego (7/11):**")
                st.markdown("- Ocena końcowa: **AG** | Procenty: **AC, AD, AE, AF** | Oceny szczegółowe: **Y, Z, AA, AB** | Taktyczna: **D-H**")
            elif wybrana_pozycja == "6 (Defensywny Pomocnik)":
                st.write("📌 **Mapowanie dla 6 (Defensywnego Pomocnika):**")
                st.markdown("- Ocena końcowa: **AD** | Procenty: **AB, AC** | Taktyczna: **X** | Oceny szczegółowe: **Y, Z, AA**")
            elif wybrana_pozycja == "8 (Pomocnik)":
                st.write("📌 **Mapowanie dla 8 (Pomocnika):**")
                st.markdown("- Ocena końcowa: **AJ** | Procenty: **AG, AH, AI** | Taktyczna: **AB** | Oceny szczegółowe: **AC, AD, AE, AF**")
            elif wybrana_pozycja == "10 (Ofensywny Pomocnik)":
                st.write("📌 **Mapowanie dla 10 (Ofensywnego Pomocnika):**")
                st.markdown("- Ocena końcowa: **AF** | Procenty: **AC, AD, AE** | Taktyczna: **Y** | Oceny szczegółowe: **Z, AA, AB**")
            elif wybrana_pozycja == "9 (Napastnik)":
                st.write("📌 **Mapowanie dla 9 (Napastnika):**")
                st.markdown("- Ocena końcowa: **AC** | Procenty: **Y, Z, AA, AB** | Taktyczna: **X** | **Specjalne wyliczenie: Statystyki strzałów, podań i działań**")
            
            st.write("---")
            st.subheader("Pełna baza danych z arkusza zbiorczego:")
            st.dataframe(df, use_container_width=True)
            
        elif menu == "Profil Zawodnika":
            st.header("👤 Profil Zawodnika (Widok Ogólny)")
            st.info("Wskazówka: Aby wysłać zawodnikowi dedykowany link do jego profilu, dopisz na końcu adresu aplikacji: `?player=ImięNazwisko` (np. `?player=Bałaj`)")
            
            if player_col:
                unique_players = df[player_col].dropna().unique()
                selected_player = st.selectbox("Wybierz zawodnika z listy:", unique_players)
                if selected_player:
                    filtered_df = df[df[player_col] == selected_player]
                    st.write(f"Statystyki dla: **{selected_player}**")
                    st.dataframe(filtered_df, use_container_width=True)
            else:
                st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Błąd ładowania danych z arkusza: {e}")
