#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker image push smartcitiesdata/soap-to-rest:$TRAVIS_TAG