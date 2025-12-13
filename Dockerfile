# Use a lightweight Python version
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Command to run the full pipeline
CMD ["sh", "-c", "python src/ingest.py && python src/model.py"]