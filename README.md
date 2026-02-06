# FastAPI Application Template

Minimal FastAPI backend template I use to quickly start new services and prototypes.

The goal of this template is to minimize setup time and provide a clean, predictable base for small microservices and MVPs.
It reflects my personal approach to how a Python backend should look at the early stage:
explicit dependency injection, clear boundaries, and simple but robust structure.

This is not a tutorial or showcase project — it is a practical production-oriented template.

## Tech focus
- FastAPI
- explicit DI (Dishka)
- clear scopes and lifetimes
- structured configuration and startup flow
- async-first approach
- Domain layered architecture

## Run locally

```bash
uv sync
docker compose up -d
uv run uvicorn main:app --reload
```
