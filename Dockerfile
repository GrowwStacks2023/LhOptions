# Use the official Python image from Docker Hub as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the app's code into the container
COPY . /app

# Expose the port the app will run on (5000 is the default for Flask)
EXPOSE 5000

# Set the command to run the Flask application
CMD ["python", "app.py"]
