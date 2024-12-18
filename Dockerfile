# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY main.py .
COPY server.py .
COPY streamlit_app.py .

# Expose ports for both Streamlit and Flask
EXPOSE 8501
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV FLASK_PORT=8000

# Run the main script that starts both servers
CMD ["python", "main.py"]
