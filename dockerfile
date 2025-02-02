# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the API to be accessible
EXPOSE 8000

# Set environment variables for OpenAI API Key
ENV AIPROXY_TOKEN=your-ai-proxy-token-here

# Run the FastAPI app using Uvicorn (ASGI server)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
