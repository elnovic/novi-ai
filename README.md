# NOVI AI Engine

The AI engine behind NOVI learning workflows. This repository contains Python components for generating structured learning courses, managing course content, and recommending learning paths.

## Main capabilities

- Generate course plans and chapter content with an AI provider.
- Build structured learning materials, quizzes, exercises, and final assessments.
- Validate and manage generated course content.
- Recommend learning paths from learner profile information.
- Expose a FastAPI service for course and platform data operations.
- Integrate course records with Supabase.

## Technology

- Python
- FastAPI
- Pydantic
- Supabase
- AI provider integration
- JSON-based course content

## Project structure

- `api.py` — FastAPI application and API endpoints.
- `main.py` — end-to-end course generation and recommendation pipeline.
- `novi_ai/` — AI client, course manager, recommender, and related modules.
- `requirements.txt` — Python dependencies.
- `.env.example` — environment variable template.

## Local setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the environment variables listed in `.env.example` in a local `.env` file. Do not commit API keys or database credentials.

## Run the API

```bash
uvicorn api:app --reload
```

The API documentation is available at `/docs` while the local server is running.

## Important notes

- The service depends on valid AI-provider and Supabase configuration.
- Review database permissions and endpoint access controls before deploying publicly.
- Generated course content should be reviewed before being presented as certified learning material.

## Project status

This is an evolving engine supporting NOVI's educational technology work. The README describes the repository's current code structure and should be updated as modules and deployment workflows evolve.
