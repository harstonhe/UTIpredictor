#!/bin/bash

# --- Configuration ---
DOCKER_USERNAME="heharston"
DOCKER_PASSWORD="aa7112766"
IMAGE_NAME="heharston/uti-risk-calculator"
TAG="latest"

# --- Script Logic ---

# Function to print messages
print_message() {
    echo "===================================================="
    echo "$1"
    echo "===================================================="
}

# 1. Build the Docker image
print_message "Building Docker image: $IMAGE_NAME:$TAG"
docker build -t "$IMAGE_NAME:$TAG" .
if [ $? -ne 0 ]; then
    echo "Docker build failed. Aborting."
    exit 1
fi

# 2. Log in to Docker Hub
print_message "Logging in to Docker Hub as $DOCKER_USERNAME"
docker login -u heharston -p aa7112766
if [ $? -ne 0 ]; then
    echo "Docker login failed. Aborting."
    exit 1
fi

# 3. Push the image to Docker Hub
print_message "Pushing image to Docker Hub: $IMAGE_NAME:$TAG"
docker push "$IMAGE_NAME:$TAG"
if [ $? -ne 0 ]; then
    echo "Docker push failed. Aborting."
    exit 1
fi

print_message "Deployment script finished successfully!"
echo "Image '$IMAGE_NAME:$TAG' has been pushed to Docker Hub." 