#!/bin/bash
cp .flaskenv.prod .flaskenv

CURRENT_UID=$(id -u):$(id -g) /usr/bin/docker-compose up -d

exit 0