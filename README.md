# Boekenwinkel

## 1. Projectbeschrijving

De Boekenwinkel is een webapplicatie voor een fictieve boekenwinkel. Gebruikers kunnen boeken bekijken, een account aanmaken, inloggen, boeken reserveren en hun aankopen bekijken. Gebruikers kunnen ook reviews schrijven over boeken die ze gekocht hebben.

Het project bestaat uit een frontend en een backend die via een API met elkaar communiceren.

## 2. Technologieën

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT voor authenticatie

### Frontend
- HTML
- CSS
- JavaScript

### Testing
- Pytest

## 3. Projectstructuur

```text
boekenwinkel/
├── backend/
│   ├── routers/
│   ├── tests/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── README.md
└── .gitignore
```

## 4. Installatie en uitvoering

### Vereisten
- Python geïnstalleerd op de computer.
- Een moderne webbrowser.
- Visual Studio Code is aanbevolen.

### Backend starten

Open een terminal in de map `backend`.

Activeer de bestaande virtuele omgeving in Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Installeer de vereiste pakketten:

```powershell
pip install -r requirements.txt
```

Start de API:

```powershell
uvicorn main:app --reload
```

De interactieve API-documentatie is beschikbaar via:

`http://127.0.0.1:8000/docs`

### Frontend starten

Open de map `frontend` in Visual Studio Code en start `index.html` met Live Server.

De backend moet actief zijn om de frontend met de API te laten communiceren.

## 5. Functionaliteiten

- Boeken bekijken in de catalogus.
- Boekdetails bekijken.
- Een gebruikersaccount aanmaken.
- Inloggen.
- Boeken reserveren.
- Reserveringen bekijken.
- Aankopen voltooien en aankopen bekijken.
- Reviews met een score en tekst indienen.
- Reviews op de detailpagina van een boek bekijken.

## 6. API-endpoints

De backend biedt de volgende endpoints aan:

| Methode | Endpoint | Beschrijving |
|---|---|---|
| GET | `/books/` | De beschikbare boeken ophalen |
| POST | `/books/` | Een boek toevoegen |
| GET | `/books/{book_id}` | De details van een boek ophalen |
| POST | `/users/register` | Een gebruiker registreren |
| POST | `/users/login` | Inloggen |
| GET | `/reservations/` | Eigen reserveringen ophalen |
| POST | `/reservations/` | Een reservering aanmaken |
| POST | `/purchases/{reservation_id}/complete` | Een aankoop voltooien |
| GET | `/purchases/me` | Eigen aankopen ophalen |
| POST | `/reviews/` | Een review aanmaken |
| GET | `/reviews/book/{book_id}` | Reviews van een boek ophalen |

De volledige API-specificatie en de vereiste parameters zijn beschikbaar via de interactieve documentatie op `/docs`.

## 7. Architectuur

De applicatie is opgesplitst in drie belangrijke onderdelen:

- **Frontend:** toont de gebruikersinterface en stuurt HTTP-verzoeken naar de backend.
- **Backend:** verwerkt verzoeken, controleert gegevens en voert de bedrijfslogica uit.
- **Datalaag:** slaat gebruikers, boeken, reserveringen, aankopen en reviews op in de database.

De backend gebruikt afzonderlijke routers voor verschillende functionaliteiten. SQLAlchemy wordt gebruikt voor de interactie met de database.

## 8. Tests uitvoeren

Open een terminal in de map `backend` en voer uit:

```powershell
python -m pytest -v
```

De tests controleren belangrijke functionaliteiten en bedrijfsregels. De testresultaten moeten worden gecontroleerd voordat het project wordt ingediend.

## 9. Bronnen en AI-tools

- FastAPI-documentatie: https://fastapi.tiangolo.com/
- SQLAlchemy-documentatie: https://docs.sqlalchemy.org/
- Pytest-documentatie: https://docs.pytest.org/

AI-tools: ChatGPT (OpenAI) werd gebruikt als ondersteuning bij het begrijpen van code, het oplossen van fouten en het opstellen van documentatie.
