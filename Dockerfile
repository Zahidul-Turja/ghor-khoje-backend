FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
# CMD ["cd", "ghorkhoje"]
# CMD ["python", "ghorkhoje/manage.py", "runserver", "0.0.0.0:8000"]

# FROM python:3.12-slim

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements first to leverage Docker cache
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project files
# COPY . .

# # Expose port
# EXPOSE 8000

# # Command to run the application
# CMD ["python", "ghorkhoje/manage.py", "runserver", "0.0.0.0:8000"]