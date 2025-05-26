# Use official Python image as a base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose the port the app runs on
EXPOSE 5001

# Run the app
CMD ["python", "run.py"]
