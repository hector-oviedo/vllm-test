# MIAA Middleware (Abstraction Layer)
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src

# Expose port
EXPOSE 8080

# Run the API Gateway
# MIAA Compliance: Runs on port 8080, forwarding to Inference on 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]