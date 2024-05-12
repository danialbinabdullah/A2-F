# Use the official Python image as a base
FROM python:3.8-slim

# Set environment variables
ENV AIRFLOW_HOME=/usr/local/airflow
ENV PYTHONPATH=${PYTHONPATH}:${AIRFLOW_HOME}

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        default-libmysqlclient-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install additional Python dependencies
COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

# Install Airflow
RUN pip install --no-cache-dir apache-airflow

# Initialize Airflow database
RUN airflow db init

# Expose the web server port
EXPOSE 8080

# Start Airflow web server
CMD ["airflow", "webserver", "--port", "8080"]
