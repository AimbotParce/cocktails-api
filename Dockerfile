FROM python:latest

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]