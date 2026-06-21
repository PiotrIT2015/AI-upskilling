import streamlit as st
import ollama

st.set_page_config(page_title="AI Note Summarizer", page_icon="📝")

st.title("📝 AI Note Summarizer")
st.subheader("Zamień długie notatki w konkretne podsumowania")

# Boczne menu - konfiguracja
with st.sidebar:
    st.header("Ustawienia")
    model_name = st.selectbox("Wybierz model", ["llama3", "mistral", "phi3"], index=0)
    summary_style = st.radio(
        "Styl podsumowania:",
        ["Krótkie streszczenie", "Punkty (Bullet points)", "Lista zadań (Action Items)"]
    )
    st.divider()
    st.info("Aplikacja korzysta z lokalnego silnika Ollama.")

# Pole tekstowe na notatkę
user_input = st.text_area("Wklej swoją notatkę tutaj:", height=300, placeholder="Twoja długa treść...")

if st.button("Generuj podsumowanie ✨"):
    if not user_input.strip():
        st.warning("Najpierw wprowadź tekst!")
    else:
        # Przygotowanie Promptu w zależności od wybranego stylu
        prompts = {
            "Krótkie streszczenie": "Streść poniższy tekst w kilku zdaniach:",
            "Punkty (Bullet points)": "Wypisz najważniejsze punkty z poniższego tekstu (użyj pauz):",
            "Lista zadań (Action Items)": "Na podstawie tekstu stwórz listę zadań do wykonania (To-Do List):"
        }
        
        system_prompt = f"{prompts[summary_style]} Odpowiadaj wyłącznie w języku polskim."

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ]

        st.divider()
        st.subheader("Wynik:")
        
        # Kontener na tekst generowany w czasie rzeczywistym
        response_placeholder = st.empty()
        full_response = ""

        try:
            # Wywołanie Ollamy ze streamingiem
            response = ollama.chat(model=model_name, messages=messages, stream=True)
            
            for chunk in response:
                content = chunk['message']['content']
                full_response += content
                # Aktualizacja tekstu w interfejsie
                response_placeholder.markdown(full_response + "▌")
            
            # Finalne wyświetlenie bez kursora
            response_placeholder.markdown(full_response)
            
            # Opcja pobrania wyniku
            st.download_button("Pobierz podsumowanie (.txt)", full_response, file_name="summary.txt")

        except Exception as e:
            st.error(f"Wystąpił błąd: {e}")
            st.info("Upewnij się, że Ollama jest uruchomiona (komenda: ollama serve)")