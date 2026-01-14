# 🚀 Persoonlijke Ontwikkelplan Coach

Een interactieve AI-coach gebouwd met Streamlit en Google Gemini die trainees helpt bij het maken van een persoonlijk ontwikkelplan.

## ✨ Functies

-   **Interactieve chat** met de AI-coach
-   **Stapsgewijze begeleiding** bij het opstellen van een ontwikkelplan
-   Formuleren van **SMART doelen**
-   **Download** je plan als een tekstbestand
-   **Google Drive integratie** om je plan direct op te slaan

## 🛠️ Installatie

### 1. Repository Clonen

```bash
git clone <jouw-repo-url>
cd mijn-coach-app
2. Dependencies Installeren
code
Bash
pip install -r requirements.txt
3. API Keys Configureren
Voor deze stap heb je API-sleutels nodig van Google.
A. Maak het secrets bestand aan
Maak in de hoofddirectory van je project een nieuwe map aan met de naam .streamlit.
Maak in deze .streamlit map een bestand aan genaamd secrets.toml.
Plak de volgende inhoud in secrets.toml:
code
Toml
# .streamlit/secrets.toml

GEMINI_API_KEY = "jouw_gemini_api_key"
GOOGLE_CLIENT_ID = "jouw_google_client_id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "jouw_google_client_secret"
REDIRECT_URI = "http://localhost:8501"
B. Verkrijg je API Keys
Gemini API Key:
Ga naar Google AI Studio.
Klik op "Create API key".
Kopieer de sleutel en plak deze in je secrets.toml bestand.
Google Drive OAuth Credentials:
Ga naar de Google Cloud Console.
Maak een nieuw project aan (of selecteer een bestaand project).
Zorg ervoor dat de Google Drive API is ingeschakeld voor je project.
Navigeer naar "APIs & Services" → "Credentials".
Klik op "+ CREATE CREDENTIALS" en kies "OAuth client ID".
Selecteer "Web application" als applicatietype.
Voeg onder "Authorized redirect URIs" de volgende URI toe: http://localhost:8501
Klik op "Create" en kopieer de Client ID en Client Secret naar je secrets.toml bestand.
4. Start de Applicatie Lokaal
code
Bash
streamlit run app.py
De app wordt nu geopend in je browser op http://localhost:8501.

⭐ Speciale Instructies: Gebruik met GitHub Codespaces
Als je deze repository in GitHub Codespaces gebruikt, werkt de Google authenticatie niet met http://localhost:8501. Volg deze extra stappen:
Start de applicatie in je Codespace (streamlit run app.py).
Codespaces stuurt poort 8501 automatisch door en opent de app op een unieke URL. Deze URL ziet er ongeveer zo uit: https://<jouw-codespace-naam>.app.github.dev.
Ga terug naar de Google Cloud Console.
Bewerk je OAuth Client ID en voeg onder "Authorized redirect URIs" deze nieuwe URL van je Codespace toe.
Pas de REDIRECT_URI in je .streamlit/secrets.toml bestand aan zodat deze exact overeenkomt met de URL van je Codespace.
Herstart de Streamlit app. De authenticatie zal nu werken.

🚀 Deployen naar Streamlit Community Cloud
Push je code naar een publieke GitHub repository (zorg ervoor dat .streamlit/secrets.toml in je .gitignore staat!).
Ga naar Streamlit Community Cloud.
Klik op "New app" en selecteer je repository.
Navigeer in de app-instellingen naar "Settings" → "Secrets".
Plak de volledige inhoud van je lokale secrets.toml bestand hierin.
Belangrijk: Pas de REDIRECT_URI in de secrets aan naar de URL van je Streamlit Cloud app (bijv. https://jouw-app-naam.streamlit.app).

📝 Gebruik
Start een gesprek met de coach.
Beantwoord de vragen over je ambities en doelen.
Ontwikkel samen een concreet actieplan.
Download of sla op je voltooide ontwikkelplan.
Start opnieuw wanneer je maar wilt.

⚙️ Configuratie
Je kunt het gedrag van de AI-coach aanpassen in app.py:
code
Python
generation_config={
    "temperature": 0.7,      # Creativiteit (0.0 - 1.0)
    "top_p": 0.95,           # Woordkeuze-diversiteit
    "max_output_tokens": 2048 # Maximale lengte van antwoord
}

🔒 Beveiliging
Commit secrets.toml NOOIT naar Git.
Zorg ervoor dat het pad .streamlit/secrets.toml is opgenomen in je .gitignore bestand.
Gebruik voor productieomgevingen altijd de ingebouwde secret management tools van het platform.
OAuth-tokens worden uitsluitend in de gebruikerssessie opgeslagen en niet permanent bewaard.

📦 Bestandsstructuur
code
Code
mijn-coach-app/
├── .streamlit/
│   └── secrets.toml      # API keys (NIET committen!)
├── app.py                # Hoofdapplicatie
├── requirements.txt      # Python dependencies
├── README.md             # Deze documentatie
└── .gitignore            # Git ignore regels

🐛 Troubleshooting
"StreamlitAPIException: No API key found for Gemini"
Controleer of het bestand .streamlit/secrets.toml correct is aangemaakt.
Verifieer dat de variabelenaam GEMINI_API_KEY exact klopt.
"Google authentication failed / redirect_uri_mismatch"
Controleer of de REDIRECT_URI in je secrets.toml exact overeenkomt met de URI die is geconfigureerd in de Google Cloud Console.
Zorg ervoor dat de Google Drive API is ingeschakeld.
Verifieer dat je Client ID en Client Secret correct zijn gekopieerd.
"ModuleNotFoundError"
Voer pip install -r requirements.txt opnieuw uit.
Controleer of je de juiste Python virtual environment hebt geactiveerd.

🤝 Bijdragen
Pull requests zijn welkom! Voor grotere wijzigingen vragen we je eerst een issue te openen om de voorgestelde verandering te bespreken.
📄 Licentie
Dit project is gelicentieerd onder de MIT Licentie.
👤 Contact
Voor vragen, feedback of problemen kun je een issue openen op GitHub.
