import streamlit as st
import google.generativeai as genai
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import json

# 1. Configuratie van de pagina
st.set_page_config(
    page_title="Mijn Ontwikkelplan Coach", 
    page_icon="🚀",
    layout="wide"
)

# 2. Styling
st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Jouw Persoonlijke Ontwikkelplan Coach")
st.markdown("*Laten we samen werken aan jouw groei en ontwikkeling*")

# 3. API Key validatie
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Geen API Key gevonden. Stel deze in bij de Streamlit Secrets.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Google Drive Service Account configuratie
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Controleer of Google Service Account credentials aanwezig zijn
if "google_auth" in st.secrets and "json_content" in st.secrets["google_auth"]:
    GOOGLE_DRIVE_ENABLED = True
else:
    GOOGLE_DRIVE_ENABLED = False
    st.sidebar.warning("⚠️ Google Drive niet geconfigureerd. Download functie is beschikbaar.")

# 4. Verbeterde System Instruction
SYSTEM_INSTRUCTION = """
Jij bent een ervaren talent coach met jarenlange ervaring in persoonlijke ontwikkeling.

Je helpt trainees een concreet en haalbaar ontwikkelplan te maken door:
- Één vraag tegelijk te stellen
- Bemoedigend maar scherp te zijn
- Door te vragen naar concrete doelen, acties en deadlines
- Te helpen bij het formuleren van SMART doelen

Structuur van een volledig ontwikkelplan:
1. Huidige situatie en ambities
2. Concrete ontwikkeldoelen (SMART)
3. Actiepunten met tijdslijnen
4. Benodigde middelen en ondersteuning
5. Meetbare succescriteria

Wanneer het ontwikkelplan volledig is afgerond en de trainee tevreden is, 
maak dan een overzichtelijke samenvatting en eindig je bericht met exact deze tekst 
op een nieuwe regel: [PLAN_IS_KLAAR]
"""

# 5. Initialisatie van model en sessie
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=SYSTEM_INSTRUCTION,
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
    )

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Welkomstboodschap
    welkom = "Hallo! Ik ben je persoonlijke ontwikkelplan coach. Laten we beginnen met jouw ambities. Vertel eens: waar zie je jezelf over een jaar?"
    st.session_state.messages.append({"role": "assistant", "content": welkom})

if "plan_klaar" not in st.session_state:
    st.session_state.plan_klaar = False

# 6. Helper functie voor Google Drive upload met Service Account
def upload_to_google_drive(file_content, filename):
    """Upload een bestand naar Google Drive met Service Account"""
    try:
        # Parse de service account credentials
        service_account_info = json.loads(st.secrets["google_auth"]["json_content"])
        
        # Maak credentials aan
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        
        # Bouw de Drive service
        service = build('drive', 'v3', credentials=credentials)
        
        # Maak file metadata
        file_metadata = {
            'name': filename,
            'mimeType': 'text/plain'
        }
        
        # Upload het bestand
        media = MediaIoBaseUpload(
            io.BytesIO(file_content.encode('utf-8')),
            mimetype='text/plain',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        return file.get('webViewLink'), file.get('id')
    except Exception as e:
        st.error(f"Upload mislukt: {str(e)}")
        return None, None

# 7. Sidebar met info en opties
with st.sidebar:
    st.header("ℹ️ Over deze Coach")
    st.write("""
    Deze AI-coach helpt je bij het maken van een persoonlijk ontwikkelplan.
    
    **Tips:**
    - Wees specifiek in je antwoorden
    - Denk na over concrete doelen
    - Neem de tijd voor elke vraag
    """)
    
    st.divider()
    
    if st.button("🔄 Start nieuw gesprek"):
        st.session_state.messages = []
        st.session_state.plan_klaar = False
        st.rerun()
    
    # Toon voortgang
    st.metric("Uitgewisselde berichten", len(st.session_state.messages))
    
    # Status Google Drive
    if GOOGLE_DRIVE_ENABLED:
        st.success("✅ Google Drive: Actief")
    else:
        st.info("💾 Google Drive: Niet geconfigureerd")

# 8. Toon chat geschiedenis
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. Chat input en verwerking
if not st.session_state.plan_klaar:
    if prompt := st.chat_input("Typ hier je antwoord..."):
        # Voeg gebruikersbericht toe
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Genereer AI response
        try:
            with st.chat_message("assistant"):
                with st.spinner("Aan het denken..."):
                    # Bouw chat history op in correct formaat
                    chat_history = []
                    for msg in st.session_state.messages[:-1]:
                        role = "user" if msg["role"] == "user" else "model"
                        chat_history.append({"role": role, "parts": [msg["content"]]})
                    
                    # Start chat met history en stuur nieuwe message
                    chat = st.session_state.model.start_chat(history=chat_history)
                    response = chat.send_message(prompt)
                    
                    ai_text = response.text
                    st.markdown(ai_text)
            
            # Voeg AI response toe aan history
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
            
            # Check of plan klaar is
            if "[PLAN_IS_KLAAR]" in ai_text:
                st.session_state.plan_klaar = True
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Er ging iets mis: {str(e)}")
            st.info("Probeer het opnieuw of herstart het gesprek via de sidebar.")

# 10. Plan opslaan functionaliteit
if st.session_state.plan_klaar:
    st.success("✅ Je ontwikkelplan is compleet!")
    
    # Genereer plan tekst
    plan_text = f"PERSOONLIJK ONTWIKKELPLAN\n"
    plan_text += f"Gegenereerd op: {datetime.now().strftime('%d-%m-%Y om %H:%M')}\n"
    plan_text += "=" * 50 + "\n\n"
    
    for msg in st.session_state.messages:
        role = "JIJ" if msg["role"] == "user" else "COACH"
        content = msg["content"].replace("[PLAN_IS_KLAAR]", "").strip()
        plan_text += f"{role}:\n{content}\n\n"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Download als tekstbestand",
            data=plan_text,
            file_name=f"ontwikkelplan_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        if GOOGLE_DRIVE_ENABLED:
            if st.button("💾 Opslaan in Google Drive", use_container_width=True):
                filename = f"Ontwikkelplan_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                
                with st.spinner("Uploaden naar Google Drive..."):
                    link, file_id = upload_to_google_drive(plan_text, filename)
                    
                    if link:
                        st.success("✅ Succesvol opgeslagen!")
                        st.markdown(f"[📄 Open in Google Drive]({link})")
                        st.caption(f"Bestand ID: {file_id}")
        else:
            st.button(
                "💾 Google Drive (niet geconfigureerd)", 
                disabled=True,
                use_container_width=True
            )
            st.caption("Configureer Service Account om deze functie te gebruiken")
    
    st.divider()
    
    if st.button("🆕 Start een nieuw ontwikkelplan"):
        st.session_state.messages = []
        st.session_state.plan_klaar = False
        st.rerun()
