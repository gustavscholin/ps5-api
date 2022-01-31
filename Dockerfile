FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Set PYTHONPATH
ENV PYTHONPATH "${APP_HOME}/src"

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the API with gunicorn
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --access-logfile access.log src.app:app
