# AutoDoc AI — Automatic Documentation Generator

## What it does
- Upload a Python file, parse structure (functions, classes, imports),
- Use a Groq LLM to generate professional Markdown documentation,
- Preview documentation in the browser,
- Download a professional PDF (cover page, TOC, architecture diagram).

## Run locally
1. Create `.env` with `GROQ_API_KEY=...` in `backend/`.
2. Install dependencies:
cd backend
pip install -r requirements.txt

3. Start backend:


python -m uvicorn main:app --reload

4. Open `frontend/index.html` via Live Server or direct file and test.

## Notes
- If Graphviz PNG generation fails, install Graphviz binary and add to PATH on Windows.
- If your Groq model name differs, change the `model` argument in `ai_generator.py`