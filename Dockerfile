FROM python:3.11-slim
# lub FROM python:3.13-slim, w zależności od tego, co wybrałeś

WORKDIR /app

# Skopiuj definicje
COPY pyproject.toml .

# Instalacja
RUN pip install --no-cache-dir .

# Skopiuj kod
COPY . .

# ---> TĘ LINIJKĘ DODAJEMY <---
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["chainlit", "run", "src/app.py", "-w", "--host", "0.0.0.0", "--port", "8000"]