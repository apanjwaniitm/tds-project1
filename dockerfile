# Use a lightweight base image
FROM python:3.9-slim

# Ensure the container runs as root
USER root

# Install system dependencies (including Git)
RUN apt-get update && apt-get install -y git bash && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only necessary files to speed up build
COPY requirements.txt .

# Install dependencies in a virtual environment for size optimization
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY main.py phaseB_tasks.py tasks.py /app/

# Set environment variables to use venv
ENV PATH="/opt/venv/bin:$PATH"

# Verify Git is installed
RUN git --version

# Expose API port
EXPOSE 8000

# Start the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
