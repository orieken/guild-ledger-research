FROM python:3.12.10-slim-bookworm@sha256:fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db
WORKDIR /app
COPY services/guild/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/guild/app.py .
COPY fixtures /fixtures
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
