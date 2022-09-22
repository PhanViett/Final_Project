#!/bin/bash
echo "Deploy  Frontend Docker image to Local registry"

ls -la
#remove container
docker ps
docker stop $(docker ps -a | grep '10.86.144.152:5000/cong-suc-khoe' |awk '{print $1}')
docker rm -f $(docker ps -a | grep '10.86.144.152:5000/cong-suc-khoe' |awk '{print $1}')
sleep 5
docker ps

#remove images
docker rmi $(docker images '10.86.144.152:5000/cong-suc-khoe' -a -q)

echo "Docker Images before deploy"
docker image ls

echo "Begin build docker images  "
docker build --no-cache=true -t 10.86.144.152:5000/cong-suc-khoe .
echo "Finish build docker images  "

echo "Begin Push Images to Local Docker Repository"

docker push "10.86.144.152:5000/cong-suc-khoe:latest"

echo "Finish Push Images to Local Docker Repository"
docker image ls

echo "Finish Push Images to Local Docker Repository"


exit 0