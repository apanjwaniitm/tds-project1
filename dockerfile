FROM python:3.11

# Install git
RUN apt-get update && apt-get install -y git

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py phaseB_tasks.py tasks.py requirements.txt /app/

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
