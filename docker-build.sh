#!/bin/bash

# Stopping all containers
#docker container stop SICAR-Appeals-Analysis-API

VERSION=$(git describe --tags --abbrev=0)
export VERSION
# build all images
docker build --no-cache -t terrabrasilis/SICAR-Appeals-Analysis-API:$VERSION --build-arg VERSION=$VERSION -f environment/Dockerfile .

# send to dockerhub
docker login
docker push terrabrasilis/SICAR-Appeals-Analysis-API:$VERSION

# If you want run containers, uncomment this lines
#docker run -d --rm -p 84:80 --name SICAR-Appeals-Analysis-API terrabrasilis/SICAR-Appeals-Analysis-API