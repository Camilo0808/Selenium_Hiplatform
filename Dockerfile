# Use an official Python runtime as a base image
FROM python:3.11.4-slim
RUN mkdir -p /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Install needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r app/requirements/prod.txt

ENV PROJECT_HOME="/app"

# Expose the port that the app runs on
EXPOSE 8000

# Run the command to start your app
CMD ["python", "app/services/export_hsm_report.py"]