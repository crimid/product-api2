FROM python:3.12-slim

WORKDIR /app

# Copy all source code
COPY . .

# Install dependencies (uses setup.py)
RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
