# ── Base image ───────────────────────────────────────
# We start from an official Python image
# 'slim' means smaller size — good practice
FROM python:3.11-slim

# ── Set working directory inside container ───────────
# All commands after this run inside /app folder
WORKDIR /app

# ── Copy requirements first (smart caching) ──────────
# Docker caches each step. If requirements.txt didn't change,
# it won't reinstall packages — makes builds much faster
COPY requirements.txt .

# ── Install dependencies ─────────────────────────────
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy rest of the code ────────────────────────────
COPY app/ .

# ── Tell Docker which port the app uses ──────────────
EXPOSE 5000

# ── Command to run when container starts ─────────────
CMD ["python", "app.py"]