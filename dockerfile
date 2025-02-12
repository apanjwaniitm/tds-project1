# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install Git (Fix for GitPython error)
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (to cache dependencies)
COPY requirements.txt .

# Install dependencies before copying the rest of the files
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY . .

# Expose API port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
