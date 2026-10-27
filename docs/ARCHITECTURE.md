# Architectuur van de Boekenwinkel

## 1. Overzicht

De Boekenwinkel is een webapplicatie die bestaat uit een frontend, een backend en een datalaag.

De onderdelen hebben elk hun eigen verantwoordelijkheid. De frontend verzorgt de gebruikersinterface, de backend verwerkt de aanvragen en de datalaag bewaart de gegevens.

## 2. Architectuurschema

```text
┌──────────────────────────────┐
│           Frontend           │
│       HTML, CSS, JavaScript  │
└──────────────┬───────────────┘
               │ HTTP-verzoeken
               │ JSON
               ▼
┌──────────────────────────────┐
│            Backend           │
│           FastAPI             │
│                              │
│  ┌──────────┐ ┌────────────┐ │
│  │ Books    │ │ Users      │ │
│  ├──────────┤ ├────────────┤ │
│  │ Reserve- │ │ Purchases  │ │
│  │ tions    │ │            │ │
│  ├──────────┤ ├────────────┤ │
│  │ Reviews  │ │ Security   │ │
│  └──────────┘ └────────────┘ │
└──────────────┬───────────────┘
               │ SQLAlchemy
               ▼
┌──────────────────────────────┐
│          Database            │
│            SQLite            │
└──────────────────────────────┘
```

## 3. Verantwoordelijkheden

### Frontend

De frontend bestaat uit HTML, CSS en JavaScript.

De frontend:
- Toont de boekencatalogus.
- Laat gebruikers registreren en inloggen.
- Toont reserveringen en aankopen.
- Toont boekdetails en reviews.
- Stuurt HTTP-verzoeken naar de backend.
- Verwerkt antwoorden en foutmeldingen van de API.

### Backend

De backend gebruikt FastAPI.

De backend:
- Ontvangt HTTP-verzoeken.
- Valideert inkomende gegevens.
- Verwerkt de bedrijfslogica.
- Controleert de rechten van gebruikers.
- Beheert boeken, reserveringen, aankopen en reviews.
- Communiceert met de database.

De verschillende routers verdelen de API-functionaliteit volgens verantwoordelijkheid.

### Datalaag

De datalaag gebruikt SQLite en SQLAlchemy.

De database bewaart de gegevens die nodig zijn voor de werking van de applicatie, waaronder boeken, gebruikers, reserveringen, aankopen en reviews.

SQLAlchemy wordt gebruikt om databasebewerkingen vanuit Python uit te voeren.

## 4. Gegevensstroom

Wanneer een gebruiker een actie uitvoert, zoals het reserveren van een boek, verloopt de verwerking als volgt:

1. De gebruiker voert een actie uit in de frontend.
2. JavaScript stuurt een HTTP-verzoek naar de backend.
3. FastAPI ontvangt het verzoek bij het juiste endpoint.
4. De backend valideert de gegevens en voert de nodige controles uit.
5. SQLAlchemy voert de vereiste databasebewerkingen uit.
6. De backend stuurt een antwoord terug.
7. De frontend toont het resultaat aan de gebruiker.

## 5. Scheiding van verantwoordelijkheden

De applicatie is opgesplitst in afzonderlijke onderdelen.

- De frontend is verantwoordelijk voor de gebruikersinterface.
- De routers verwerken specifieke API-functionaliteiten.
- De modellen beschrijven de databasegegevens.
- De schema's beschrijven de gegevensstructuren voor invoer en uitvoer.
- De databaseconfiguratie beheert de verbinding met de database.
- De beveiligingsmodule ondersteunt authenticatie en toegangscontrole.

Deze scheiding maakt het eenvoudiger om onderdelen afzonderlijk te onderhouden en te testen.

## 6. Belangrijke bedrijfsregels

De backend moet de volgende regels bewaken:

- Een ISBN-code moet uniek zijn.
- Een gebruiker moet ingelogd zijn voor beveiligde acties.
- Een reservering mag de beschikbare voorraad niet onder nul brengen.
- Een aankoop moet gekoppeld zijn aan een geldige reservering.
- Een gebruiker mag alleen reviews schrijven voor boeken die hij gekocht heeft.
