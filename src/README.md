# Health AI App

## Service Health Check

To check the health of the deployed service, you can use the following methods:

1. Use the health check endpoint:
   ```
   curl https://[YOUR-SERVICE-URL]/health
   ```
   Replace `[YOUR-SERVICE-URL]` with your actual Cloud Run service URL.

2. Run the health check script:
   ```
   ./check_health.sh
   ```
   This script will automatically fetch the service URL and perform a health check.

## Deployment

This project uses Google Cloud Build for continuous deployment. Any push to the main branch will trigger a new deployment.

## Local Development

To run the application locally:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```
   python src/app.py
   ```

## Project Structure

- `src/app.py`: Main Flask application
- `Dockerfile`: Used for containerizing the application
- `cloudbuild.yaml`: Cloud Build configuration for CI/CD
- `check_health.sh`: Script to check the health of the deployed service
- `requirements.txt`: Python dependencies

## Environment Variables

The following environment variables are used:

- `FLASK_APP`: Set to `src/app.py`
- `FLASK_RUN_HOST`: Set to `0.0.0.0`

## Deployed Service

The application is deployed on Google Cloud Run. The service URL can be found by running:

```
gcloud run services describe health-ai-app-service --region=us-central1 --format='value(status.url)'
```

## Health Check

Our application includes a health check endpoint to verify its operational status. Here's how you can use it:

### Using cURL

To check the health of the deployed service using cURL:

```bash
SERVICE_URL=$(gcloud run services describe health-ai-app-service --region=us-central1 --format='value(status.url)')
curl ${SERVICE_URL}/health
```

Expected response:
```json
{"status": "healthy", "service": "health-ai-app"}
```

### Using the Health Check Script

We've provided a convenient script to check the health of the service:

1. Ensure the script is executable:
   ```bash
   chmod +x check_health.sh
   ```

2. Run the script:
   ```bash
   ./check_health.sh
   ```

The script will output the health check response and provide a simple interpretation of the HTTP status code.

### Manually Checking

You can also manually check the health by visiting the `/health` endpoint in your web browser. The URL will be:



https://health-ai-app-service-251454609175.us-central1.run.app/
```

Replace `[unique-id]` with the actual unique identifier of your Cloud Run service.

If you need to find your service URL, you can use this command:
```bash
gcloud run services describe health-ai-app-service --region=us-central1 --format='value(status.url)'
```