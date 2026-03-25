# Finance AI

Simple backend to track expenses using natural language input.

## Features
- Add expenses via API
- Parse natural language ("15k supermercado")
- Confirmation flow (pending → confirmed)

## Tech
- FastAPI
- PostgreSQL
- SQLAlchemy

## Run

```bash
uvicorn app.main:app --reload