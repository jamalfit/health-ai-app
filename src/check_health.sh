#!/bin/bash

SERVICE_URL=$(gcloud run services describe health-ai-app-service --region=us-central1 --format='value(status.url)')
HEALTH_CHECK_URL="${SERVICE_URL}/health"

echo "Checking health of service at: ${HEALTH_CHECK_URL}"
curl -s "${HEALTH_CHECK_URL}"
echo  # Print a newline

# Check the HTTP status code
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HEALTH_CHECK_URL}")

if [ $HTTP_STATUS -eq 200 ]; then
    echo "Service is healthy (HTTP Status: ${HTTP_STATUS})"
else
    echo "Service may not be healthy (HTTP Status: ${HTTP_STATUS})"
fi