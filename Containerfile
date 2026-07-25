FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only copy source — tests are not needed at runtime
COPY src/ src/

CMD ["python", "src/migrate.py"]
