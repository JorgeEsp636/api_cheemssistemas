# API Cheems Sistemas (backend)

API REST **Django** para **CHEEMS Transport** (transporte público en bus: rutas, tarifas, conductores, buses, PQRS, JWT y asistente **Google Gemini** vía proxy en servidor).

## Documentación

La guía completa (stack técnico, variables de entorno, **configuración de `GEMINI_API_KEY`**, endpoint `POST /api/chat/`, instalación y estructura) está en:

**[api_cheems/README.md](api_cheems/README.md)**

## Inicio rápido

```bash
cd api_cheems
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
# Configurar api_cheems/api_cheems/.env (ver README en api_cheems)
python manage.py migrate
python manage.py runserver
```

Repositorio: [github.com/JorgeEsp636/api_cheemssistemas](https://github.com/JorgeEsp636/api_cheemssistemas)
