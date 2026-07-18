# Base image
FROM python:3.12-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Print logs immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (better Docker cache)
COPY requirements.txt .

# Upgrade pip and install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of project
COPY . .



# Expose streamlit port
EXPOSE 8501
EXPOSE 8500

# Run streamlit
CMD ["streamlit","run","app/streamlit_app.py","--server.address=0.0.0.0","--server.port=8501"]