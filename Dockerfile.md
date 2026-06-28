# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8001

# Run FastAPI with uvicorn
CMD ["uvicorn", "risk_api:app", "--host", "0.0.0.0", "--port", "8001"]
