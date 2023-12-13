# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

## The following code was meant to authenticate using service account -- however, it seems this is no longer possible.

# Update package lists and install curl
# RUN apt-get update && \
#    apt-get install -y curl && \
#    rm -rf /var/lib/apt/lists/*

# Downloading gcloud package
# RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
# RUN mkdir -p /usr/local/gcloud \
#  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
#  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
# ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
# ENV GOOGLE_APPLICATION_CREDENTIALS toothcheck-app-92b838d1c483.json

# Copy and run the Bash script
# COPY script.sh /app
# RUN chmod +x script.sh


# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python", "mqtt_handler.py"]