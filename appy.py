import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football IQ", page_icon="⚽", layout="wide")
st.title("⚽ Football IQ - Panel Trenera i Zawodnika")

# Menu boczne
menu = st.sidebar.selectbox("Wybierz widok", ["Panel Trenera", "Profil Zawodnika"])

# Wybór pozycji boiskowych zgodnych z Twoim arkuszem
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
    st.info(f"Wybrana pozycja do analizy: **{wybrana_pozycja}**")
    
    # Miejsce na link do Twojego Arkusza Google
    sheet_url = st.text_input("Wklej link do Arkusza Google (lub publiczny link CSV):")
    
    if sheet_url:
        st.success("Link dodany! W kolejnym kroku podepniemy dokładne mapowanie kolumn dla pozycji: " + wybrana_pozycja)
    else:
        st.warning("Wklej powyżej link do swojego arkusza Google Sheets, aby pobrać dane zawodników.")

elif menu == "Profil Zawodnika":
    st.header("👤 Profil Zawodnika")
    st.write("Tutaj zawodnik będzie widział swoje statystyki, oceny końcowe, procentowe oraz taktyczne dla wybranej pozycji.")
