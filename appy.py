import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football IQ", page_icon="⚽", layout="wide")

st.title("⚽ Football IQ – Panel Trenera i Zawodnika")

# Proste menu boczne
menu = st.sidebar.selectbox("Wybierz widok", ["Panel Trenera", "Profil Zawodnika"])

# Przykładowe dane (w kolejnym kroku podepniemy Twój Arkusz Google)
if "notes" not in st.session_state:
    st.session_state.notes = {}

if menu == "Panel Trenera":
    st.header("📋 Panel Trenera")
    
    player = st.selectbox("Wybierz zawodnika", ["Marcel", "Jan Kowalski", "Piotr Nowak"])
    match = st.selectbox("Wybierz mecz", ["Mecz 1: vs Orły (2026-10-20)", "Mecz 2: vs Victoria (2026-10-15)"])
    
    st.subheader(f"Statystyki: {player} ({match})")
    col1, col2, col3 = st.columns(3)
    col1.metric("Celność podań", "88%")
    col2.metric("Odbiory", "5")
    col3.metric("Ocena taktyczna", "8.5/10")
    
    st.divider()
    st.subheader("📝 Notatka trenerska po meczu")
    
    note_key = f"{player}_{match}"
    current_note = st.session_state.notes.get(note_key, "")
    
    new_note = st.text_area("Wpisz notatkę dla zawodnika:", value=current_note)
    if st.button("Zapisz notatkę"):
        st.session_state.notes[note_key] = new_note
        st.success("Notatka została zapisana pomyślnie!")

elif menu == "Profil Zawodnika":
    st.header("👤 Profil Zawodnika (Widok Gracza)")
    
    player = st.selectbox("Wybierz siebie", ["Marcel", "Jan Kowalski", "Piotr Nowak"])
    
    st.subheader(f"Witaj, {player}! Oto Twoje statystyki ze wszystkich meczów:")
    
    # Tabela podsumowująca
    df_stats = pd.DataFrame({
        "Mecz": ["Mecz 1: vs Orły", "Mecz 2: vs Victoria"],
        "Celność podań": ["88%", "82%"],
        "Odbiory": [5, 3],
        "Ocena": [8.5, 7.8]
    })
    st.dataframe(df_stats, use_container_width=True)
    
    st.divider()
    st.subheader("💬 Notatki od Trenera")
    
    found = False
    for key, note in st.session_state.notes.items():
        if key.startswith(player) and note:
            match_name = key.split("_")[1]
            st.info(f"**{match_name}**: {note}")
            found = True
            
    if not found:
        st.write("Brak nowych notatek od trenera dla Twoich meczów.")
