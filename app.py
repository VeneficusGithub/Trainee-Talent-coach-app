import streamlit as st
import google.generativeai as genai

# 1. Configuratie van de pagina
st.set_page_config(page_title="Mijn Ontwikkelplan Coach", page_icon="🚀")
st.title("🚀 Jouw Persoonlijke Ontwikkelplan Coach")

# 2. Haal de API Key op uit de 'Kluis' (Secrets)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Geen API Key gevonden. Stel deze in bij de Streamlit Secrets.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 3. De Model Instellingen
# Hier zetten we de system instruction die je in Studio hebt gemaakt
SYSTEM_INSTRUCTION = """
Jij bent een ervaren talent coach. Je helpt trainees een ontwikkelplan te maken.
Stel één vraag tegelijk. Wees bemoedigend maar scherp.
Wanneer het ontwikkelplan volledig is afgerond en de trainee tevreden is, 
eindig je je bericht met exact deze tekst op een nieuwe regel: [PLAN_IS_KLAAR]
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-pro", 
    system_instruction=SYSTEM_INSTRUCTION
)

# 4. Geheugen van het gesprek (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon eerdere berichten
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Het Chatvenster
if prompt := st.chat_input("Wat wil je bespreken?"):
    # Toon bericht van gebruiker
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Haal antwoord op van Gemini
    try:
        # We sturen de hele geschiedenis mee voor context
        chat_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages
        ]
        
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt) # Stuur alleen laatste prompt, history zit in object
        
        ai_text = response.text
        
        # Toon antwoord van AI
        with st.chat_message("assistant"):
            st.markdown(ai_text)
            
        st.session_state.messages.append({"role": "assistant", "content": ai_text})

        # 6. Check voor het magische codewoord om op te slaan
        if "[PLAN_IS_KLAAR]" in ai_text:
            st.success("Het plan is klaar! Klik hieronder om het op te slaan.")
            # Hier komt straks de knop naar Google Drive
            st.button("💾 Sla op in Google Drive")

    except Exception as e:
        st.error(f"Er ging iets mis: {e}")
