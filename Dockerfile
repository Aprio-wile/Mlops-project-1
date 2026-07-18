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

# Copy full project first (required because requirements.txt uses -e . which needs setup.py)
COPY . .

# Upgrade pip and install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt



# Expose streamlit port
EXPOSE 8501
EXPOSE 8500

# Run streamlit
CMD ["streamlit","run","app/streamlit_app.py","--server.address=0.0.0.0","--server.port=8501"]