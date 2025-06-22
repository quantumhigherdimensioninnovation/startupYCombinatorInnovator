# Use the official lightweight Python image.
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Install system dependencies (if you need others, add here)
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Set Streamlit config to allow Cloud Run ingress
ENV PORT 8080

# Expose the port Streamlit listens on
EXPOSE 8080

# Command to run the app
CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0
