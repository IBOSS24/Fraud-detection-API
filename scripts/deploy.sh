#!/usr/bin/env bash

set -Eeuo pipefail

# -----------------------------
# Configuration
# -----------------------------

IMAGE_REPO="iboss17/fraud-api"

PROD_CONTAINER="fraud-api-prod"
GREEN_CONTAINER="fraud-api-green"
ROLLBACK_CONTAINER="fraud-api-rollback"

PROD_PORT="8000"
GREEN_PORT="8001"

# -----------------------------
# Helper functions
# -----------------------------

container_exists() {
    docker ps -a --format '{{.Names}}' | grep -qx "$1"
}

container_running() {
    docker ps --format '{{.Names}}' | grep -qx "$1"
}

get_api_version() {
    local port="$1"

    curl --fail --silent "http://127.0.0.1:${port}/version" |
        python3 -c 'import sys, json; print(json.load(sys.stdin)["api_version"])'
}

wait_for_health() {
    local port="$1"

    for i in {1..30}; do
        if curl --fail --silent \
            "http://127.0.0.1:${port}/health" > /dev/null; then
            return 0
        fi

        echo "API not ready yet. Retrying..."
        sleep 2
    done

    return 1
}

# -----------------------------
# Target release
# -----------------------------

if [ -z "${1:-}" ]; then
    echo "Usage: ./deploy.sh <version>"
    exit 1
fi

TARGET_VERSION="$1"
TARGET_IMAGE="${IMAGE_REPO}:${TARGET_VERSION}"

echo "Target version: ${TARGET_VERSION}"
echo "Target image:   ${TARGET_IMAGE}"

# -----------------------------
# Read current production state
# -----------------------------

CURRENT_VERSION="none"

if container_running "${PROD_CONTAINER}"; then

    if ! CURRENT_VERSION=$(get_api_version "${PROD_PORT}"); then
        echo "Unable to determine current production version."
        exit 1
    fi

fi

echo "Current production version: ${CURRENT_VERSION}"

# -----------------------------
# Idempotency check
# -----------------------------

if [ "${CURRENT_VERSION}" = "${TARGET_VERSION}" ]; then
    echo "Version ${TARGET_VERSION} is already deployed."
    echo "Nothing to do."
    exit 0
fi

# -----------------------------
# Pull exact release artifact
# -----------------------------

echo "Pulling ${TARGET_IMAGE}..."
docker pull "${TARGET_IMAGE}"

# -----------------------------
# Remove stale Green container
# -----------------------------

if container_exists "${GREEN_CONTAINER}"; then
    echo "Removing stale Green container..."
    docker rm -f "${GREEN_CONTAINER}"
fi

# -----------------------------
# Start Green candidate
# -----------------------------

echo "Starting Green candidate..."

docker run -d \
    --name "${GREEN_CONTAINER}" \
    -p 127.0.0.1:${GREEN_PORT}:8000 \
    "${TARGET_IMAGE}"

# -----------------------------
# Validate Green health
# -----------------------------

echo "Checking Green health..."

if ! wait_for_health "${GREEN_PORT}"; then

    echo "Green candidate failed health check."

    docker logs "${GREEN_CONTAINER}" || true
    docker rm -f "${GREEN_CONTAINER}"

    echo "Production remains untouched."
    exit 1
fi

# -----------------------------
# Validate Green identity
# -----------------------------

GREEN_VERSION=$(get_api_version "${GREEN_PORT}")

echo "Expected candidate version: ${TARGET_VERSION}"
echo "Actual candidate version:   ${GREEN_VERSION}"

if [ "${GREEN_VERSION}" != "${TARGET_VERSION}" ]; then

    echo "Green candidate failed version check."

    docker rm -f "${GREEN_CONTAINER}"

    echo "Production remains untouched."
    exit 1
fi

echo "Green candidate validated successfully."

# -----------------------------
# Prepare rollback state
# -----------------------------

HAD_PREVIOUS_PRODUCTION=false

if container_exists "${ROLLBACK_CONTAINER}"; then
    echo "Removing previous rollback container..."
    docker rm -f "${ROLLBACK_CONTAINER}"
fi

if container_exists "${PROD_CONTAINER}"; then

    HAD_PREVIOUS_PRODUCTION=true

    echo "Preserving current production for rollback..."

    docker stop "${PROD_CONTAINER}"
    docker rename "${PROD_CONTAINER}" "${ROLLBACK_CONTAINER}"
fi

# -----------------------------
# Candidate container no longer needed
# -----------------------------

docker rm -f "${GREEN_CONTAINER}"

# -----------------------------
# Rollback function
# -----------------------------

rollback() {

    echo "Production validation failed."
    echo "Starting rollback..."

    if container_exists "${PROD_CONTAINER}"; then
        docker rm -f "${PROD_CONTAINER}" || true
    fi

    if [ "${HAD_PREVIOUS_PRODUCTION}" = true ] &&
       container_exists "${ROLLBACK_CONTAINER}"; then

        docker rename "${ROLLBACK_CONTAINER}" "${PROD_CONTAINER}"
        docker start "${PROD_CONTAINER}"

        if wait_for_health "${PROD_PORT}"; then
            echo "Rollback successful."
            echo "Production restored to ${CURRENT_VERSION}."
        else
            echo "CRITICAL: rollback container failed health check."
        fi

    else
        echo "No previous production container is available."
    fi

    exit 1
}

# -----------------------------
# Promote target to production
# -----------------------------

echo "Promoting ${TARGET_VERSION} to production..."

if ! docker run -d \
    --name "${PROD_CONTAINER}" \
    --restart unless-stopped \
    -p ${PROD_PORT}:8000 \
    "${TARGET_IMAGE}"; then

    rollback
fi

# -----------------------------
# Post-promotion health gate
# -----------------------------

if ! wait_for_health "${PROD_PORT}"; then

    docker logs "${PROD_CONTAINER}" || true
    rollback
fi

# -----------------------------
# Post-promotion version gate
# -----------------------------

ACTUAL_VERSION=$(get_api_version "${PROD_PORT}") || rollback

echo "Expected production version: ${TARGET_VERSION}"
echo "Actual production version:   ${ACTUAL_VERSION}"

if [ "${ACTUAL_VERSION}" != "${TARGET_VERSION}" ]; then
    rollback
fi

echo "Deployment successful."
echo "Production is now running version ${TARGET_VERSION}."