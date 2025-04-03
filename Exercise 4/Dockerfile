# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model
COPY app.py .
COPY model.py .

# Train the model when building the container
RUN python model.py

# Set environment variables
ENV MODEL_PATH=sentiment_model.pkl
ENV MODEL_VERSION=1.0.0
ENV PORT=5000

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]