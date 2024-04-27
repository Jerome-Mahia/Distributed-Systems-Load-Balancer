# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Server.py file into the container at /app
COPY server.py .

# Install Flask and any other dependencies required by your server
RUN pip install flask

# Expose port 5000 to allow external access
EXPOSE 5000

# Command to run the Flask server when the container starts
CMD ["python", "server.py"]
