#!/usr/bin/env bash

# It's possible we don't have docker-compose, so if necessary bring our own.
docker_compose_exe=$(command -v docker-compose)
if ! [[ -x "$docker_compose_exe" ]]; then
    if ! [[ -x "./docker-compose" ]]; then
        echo "Getting docker-compose..."
        curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" \
        -o ./docker-compose

        if [[ $? -ne 0 ]]; then
            echo "Failed to fetch docker-compose!"
            exit 1
        fi

        chmod +x docker-compose
    fi
    docker_compose_exe="./docker-compose"
fi

# Get the containers running, build them, and exit on any of them exiting
echo "Starting containers... running test"
${docker_compose_exe} -f docker-compose.yml up  --build --abort-on-container-exit
test_result=$?
# Clean up
echo "Cleaning up containers..."
${docker_compose_exe} down

exit ${test_result}