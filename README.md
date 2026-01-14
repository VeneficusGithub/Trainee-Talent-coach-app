# 🚀 Persoonlijke Ontwikkelplan Coach

Een interactieve AI-coach gebouwd met Streamlit en Google Gemini die trainees helpt bij het maken van een persoonlijk ontwikkelplan.

## ✨ Functies

- **Interactieve chat** met AI-coach
- **Stapsgewijze begeleiding** bij het maken van een ontwikkelplan
- **SMART doelen** formuleren
- **Download** je plan als tekstbestand
- **Google Drive integratie** om je plan op te slaan

## 🛠️ Installatie

### 1. Clone de repository
```bash
git clone <jouw-repo-url>
cd mijn-coach-app
```

### 2. Installeer dependencies
```bash
pip install -r requirements.txt
```

### 3. Configureer API keys

Maak een `secrets.toml` bestand aan:

```toml
GEMINI_API_KEY = "jouw_gemini_api_key"
GOOGLE_CLIENT_ID = "jouw_google_client_id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "jouw_google_client_secret"
REDIRECT_URI = "http://localhost:8501"
```

#### Gemini API Key krijgen:
1. Ga naar [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Maak een nieuwe API key aan
3. Kopieer de key naar je secrets.toml

#### Google Drive OAuth setup:
1. Ga naar [Google Cloud Console](https://console.cloud.google.com)
2. Maak een nieuw project aan
3. Schakel de **Google Drive API** in
4. Ga naar "Credentials" → "Create Credentials" → "OAuth client ID"
5. Kies "Web application"
6. Voeg redirect URI toe: `http://localhost:8501`
7. Kopieer Client ID en Client Secret naar secrets.toml

### 4. Start de app
```bash
streamlit run app.py
```

De app opent automatisch in je browser op `http://localhost:8501`

## 🚀 Deployen naar Streamlit Cloud

1. Push je code naar GitHub (zonder secrets.toml!)
2. Ga naar [Streamlit Cloud](https://streamlit.io/cloud)
3. Klik op "New app"
4. Selecteer je repository
5. Voeg secrets toe via de app settings:
   - Ga naar "Settings" → "Secrets"
   - Plak de inhoud van je secrets.toml
   - **Pas REDIRECT_URI aan** naar je Streamlit Cloud URL

## 📝 Gebruik

1. **Start een gesprek** met de coach
2. **Beantwoord de vragen** over je ambities en doelen
3. **Ontwikkel samen** een concreet actieplan
4. **Download of sla op** je ontwikkelplan
5. **Start opnieuw** wanneer je wilt

## ⚙️ Configuratie

Je kunt het gedrag van de coach aanpassen in `app.py`:

```python
generation_config={
    "temperature": 0.7,      # Creativiteit (0.0-1.0)
    "top_p": 0.95,           # Diversiteit
    "max_output_tokens": 2048 # Max lengte antwoord
}
```

## 🔒 Beveiliging

- **Sla secrets.toml NOOIT op in Git**
- Voeg `.streamlit/secrets.toml` toe aan je `.gitignore`
- Gebruik environment variables voor productie
- OAuth tokens worden alleen in sessie opgeslagen

## 📦 Bestandsstructuur

```
mijn-coach-app/
├── app.py                 # Hoofdapplicatie
├── requirements.txt       # Python dependencies
├── README.md             # Deze file
├── .gitignore            # Git ignore regels
└── .streamlit/
    └── secrets.toml      # API keys (niet committen!)
```

## 🐛 Troubleshooting

**"Geen API Key gevonden"**
- Check of secrets.toml correct is aangemaakt
- Controleer of de key namen exact kloppen

**"Google authenticatie mislukt"**
- Controleer of redirect URI klopt
- Check of Drive API is ingeschakeld
- Verifieer Client ID en Secret

**"Module niet gevonden"**
- Run: `pip install -r requirements.txt`
- Check of je in de juiste virtual environment zit

## 🤝 Bijdragen

Pull requests zijn welkom! Voor grote wijzigingen, open eerst een issue.

## 📄 Licentie

[MIT](https://choosealicense.com/licenses/mit/)

## 👤 Contact

Voor vragen of feedback, open een issue op GitHub.
