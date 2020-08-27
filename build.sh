#!/bin/bash
docker build -t smartcitiesdata/soap-to-rest:${TRAVIS_TAG:-build} .