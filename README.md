# Profile Matcher Service

Microservice built with FastAPI + SQLAlchemy that matches player profiles with campaigns based on predefined conditions (level, inventory, country, etc.).
## 📋 Requirements
- Python 3.9
- `pip` installed
- SQLite (incluido con Python)

## ⚙️ Installation
```bash
python -m venv .venv
. .venv/Scripts/activate   #  Windows
source .venv/bin/activate  #  macOS / Linux

pip install -r requirements.txt
```

## ▶️ Running in development

````
uvicorn app.main:app --reload

Esto levantará el servicio en:
http://127.0.0.1:8000

Swagger/OpenAPI Docs disponibles en:
http://127.0.0.1:8000/docs

````

## 🌐 Endpoints

`GET /get_client_config/{player_id}
`

Retrieves the player's profile.
Applies active campaigns if conditions are met.
Returns the updated profile.


`{
  "player_id": "p1",
  "credential": "apple_credential",
  "active_campaigns": ["mycampaign"],
  "_customfield": "mycustom",
  "devices": [
    {
      "id": 1,
      "model": "apple iphone 11",
      "carrier": "vodafone",
      "firmware": "123"
    }
  ]
}`


``GET /health``

Health check endpoint for monitoring.
Returns "ok" or "degraded".

`{
  "status": "ok"
}
`
## Testing 

````
all 
pytest -v
or specific one
pytest tests/test_main.py::test_get_client_config_updates_and_returns -v
```` 

## Project Structure
````
app/
 ├── api/             # Rutas (endpoints)
 ├── core/            # Configuración DB y funciones core
 ├── domain/          # Modelos y lógica de dominio
 ├── services/        # Lógica de negocio
 ├── main.py          # Punto de entrada FastAPI
tests/
 └── test_main.py     # Tests unitarios e integrados
````

