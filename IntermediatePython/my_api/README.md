# Example Folder Structure (FastAPI)
my_api/
  app/
    main.py
  requirements.txt
  Dockerfile
  .dockerignore

# Requirements

fastapi==0.110.0
uvicorn[standard]==0.27.1

# Docker Ignore

__pycache__/
*.pyc
.venv/
.env
.git/
.ipynb_checkpoints/

# Docker File

FROM python:3.11-slim

# 1) Avoid Python writing .pyc, and force logs to stdout (good for containers)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 2) Create working dir
WORKDIR /app

# 3) Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy the rest of the code
COPY app ./app

# 5) Document the port (not required, but nice)
EXPOSE 8000

# 6) Run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]