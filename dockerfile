# Stage 1: Build dependencies
FROM python:3.9-alpine AS builder
WORKDIR /app
COPY requirements.txt .

# Install dependencies
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.9-alpine
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
