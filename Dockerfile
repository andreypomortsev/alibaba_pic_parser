# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Create a non-root user
RUN adduser --disabled-password --gecos '' aliparser

# Set the ownership of the working directory to the non-root user
RUN chown -R aliparser:aliparser /usr/src/app

# Switch to the non-root user
USER aliparser

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the TOKEN build argument as an environment variable
ARG TOKEN
ENV TOKEN=$TOKEN

# Run app.py when the container launches
CMD ["python", "app.py"]