#!/bin/bash
# Log everything to start_docker.log
exec > /home/ubuntu/start_docker.log 2>&1

echo "Logging in to ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 208408932111.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling Docker image..."
docker pull 208408932111.dkr.ecr.ap-south-1.amazonaws.com/yt-chrome-plugin-ecr:latest

echo "Checking for existing container..."
if [ "$(docker ps -q -f name=youtube-insights-app)" ]; then
    echo "Stopping existing container..."
    docker stop youtube-insights-app
fi

if [ "$(docker ps -aq -f name=youtube-insights-app)" ]; then
    echo "Removing existing container..."
    docker rm youtube-insights-app
fi

echo "Starting new container..."
docker run -d -p 80:5000 --name youtube-insights-app 208408932111.dkr.ecr.ap-south-1.amazonaws.com/yt-chrome-plugin-ecr:latest

echo "Container started successfully."