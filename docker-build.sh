#!/bin/bash

# Stopping all containers
#docker container stop SICAR-Appeals-Analysis-API

VERSION=$(git describe --tags --abbrev=0)

# build all images
docker build -t terrabrasilis/sicar-appeals-analysis-api:v$VERSION -f ./Dockerfile .

# send to dockerhub
docker login
docker push terrabrasilis/sicar-appeals-analysis-api:v$VERSION

# If you want run containers, uncomment this lines
#docker run -d --rm -p 84:80 --name SICAR-Appeals-Analysis-API terrabrasilis/sicar-appeals-Analysis-API