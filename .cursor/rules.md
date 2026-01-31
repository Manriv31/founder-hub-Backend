# Founders Hub – Reglas de Cursor

## Definición del Producto
Founders Hub es una plataforma SaaS que conecta founders de startups con potenciales inversionistas.
Los founders publican proyectos que buscan inversión y los inversionistas pueden descubrir, evaluar y contactar dichos proyectos.

## Objetivos del Producto
- Facilitar el descubrimiento de startups
- Dar visibilidad a proyectos en etapa temprana
- Ayudar a inversionistas a encontrar oportunidades relevantes
- Habilitar conexiones tempranas entre founders e inversionistas

## Principios de Diseño
- Interfaz simple e intuitiva
- Flujos de usuario claros
- Mínima fricción para el usuario
- Priorizar claridad sobre complejidad

## Principios Técnicos
- Soluciones simples y mantenibles
- Evitar sobre–ingeniería
- Lógica explícita y nombres claros
- Componentes pequeños y enfocados

## Control de Alcance
- Enfocarse solo en los flujos principales:
  - Creación de proyectos
  - Descubrimiento de proyectos
  - Contacto básico entre inversionistas y founders
- Posponer funcionalidades avanzadas si no son críticas

## Reglas estrictas
- Usar FastAPI con estructura modular por capas.
- SQLAlchemy models SOLO en app/models.
- Pydantic schemas SOLO en app/schemas.
- Lógica de negocio SOLO en app/services.
- Endpoints solo llaman services, sin lógica.
- No usar SQLAlchemy models como response.
- Usar dependency injection para DB sessions.
- Usar tipado estricto y Pydantic v2.
- No escribir rutas en main.py.
- API versionada bajo app/api/v1.


## Stack Tecnologico

### Backend
- **Python** - Lenguaje de programacion principal de backend
- **FastAPI** - Framework para la creacion de API
- **SQLite** - Base de desarrollo y para implementacion rapida (facil de escalar a otro motor de bd relacional)
- **SQLAlchemy** - ORM 

### Frontend

## Estructura de carpetas
app/
├── main.py                     # punto de entrada FastAPI
├── core/                        # configuración transversal
│   ├── config.py               # settings, env vars
│   ├── security.py             # auth, hashing, JWT
│   └── database.py             # engine, session, Base
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── router.py           # include_router
│       └── endpoints/          # solo rutas HTTP
│           ├── users.py
│           ├── products.py
│           └── companies.py
├── models/                     # SOLO SQLAlchemy models
│   ├── user.py
│   ├── product.py
│   └── company.py
├── schemas/                    # SOLO Pydantic schemas
│   ├── user.py
│   ├── product.py
│   └── company.py
├── services/                   # lógica de negocio
│   ├── user_service.py
│   ├── product_service.py
│   └── company_service.py
├── migrations/
└── __init__.py

## Modelos de Dominio

product_model
______________
name
active_users
selling (True/ false)
seaking_inversion (True / false)
publish (true / false)
price 
founder (fk)
is_company (boolean)
country
publish_date

User_model
________
name
last_name
email
phone
country
direction
inversor (true / false)

company_model
_________
name
description
founders
