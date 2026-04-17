FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/models /app/output

EXPOSE 8503

HEALTHCHECK CMD curl --fail http://localhost:8503/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8503", "--server.address=0.0.0.0"]
