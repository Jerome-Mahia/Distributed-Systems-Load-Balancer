#Use the official python image as base image
FROM python:3.9-slim

#Set environment variables
ENV SERVER_ID=""

#Set the working directory in the container
WORKDIR /app
 
#Copy the server Python Script into the container
COPY server.py .

#Install FLask
RUN pip install flask

#Expose port 5000
EXPOSE 5000

#Command to run the server when the container starts
CMD ["python3", "server.py"]


