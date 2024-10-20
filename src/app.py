from flask import Flask, render_template, request, jsonify
from google.cloud import secretmanager
import openai
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Setup Secret Manager client
client = secretmanager.SecretManagerServiceClient()

# Function to access the secret from Secret Manager
def access_secret(secret_id):
    try:
        name = f"projects/health-ai-app-2024-439109/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        secret = response.payload.data.decode("UTF-8")
        app.logger.info(f"Successfully retrieved secret: {secret[:5]}...")  # Log first few characters
        return secret
    except Exception as e:
        app.logger.error(f"Error accessing secret {secret_id}: {str(e)}")
        raise

try:
    # Cache secrets at startup
    openai_api_key = access_secret('openai-api-key-2')
    assistant_id = access_secret('openai-assistant-id')

    # Check if the API key is properly retrieved
    if not openai_api_key:
        raise ValueError("OpenAI API key is empty or None!")
    app.logger.info(f"OpenAI API Key retrieved: {openai_api_key[:5]}...")

    # Set the OpenAI API key (globally for the client)
    openai.api_key = openai_api_key
    app.logger.info("OpenAI API Key set successfully.")
except Exception as e:
    app.logger.error(f"Failed to load secrets: {str(e)}")
    raise

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect form data
        patient_data = {
            'identifier': request.form['identifier'],
            'gender': request.form['gender'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'medications': request.form['medications'],
            'allergies': request.form['allergies'],
            'conditions': request.form['conditions'],
            'procedure': request.form['procedure']
        }

        # Format prompt for OpenAI
        prompt = f"""
        Patient Information:
        Identifier: {patient_data['identifier']}
        Gender: {patient_data['gender']}
        Height: {patient_data['height']} inches
        Weight: {patient_data['weight']} pounds
        Current Medications: {patient_data['medications']}
        Drug Allergies: {patient_data['allergies']}
        Current Medical Conditions: {patient_data['conditions']}
        Planned Procedure: {patient_data['procedure']}

        Please provide a comprehensive analysis of this patient's medical profile, including potential risks, considerations for the planned procedure, and any recommendations for their care.
        """

        try:
            app.logger.info("Sending request to OpenAI")

            # Correct API call for chat-based models (GPT-4, GPT-3.5-turbo)
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                timeout=10  # Timeout after 10 seconds if OpenAI is unresponsive
            )
            assistant_response = response['choices'][0]['message']['content']
            app.logger.info("Received response from OpenAI")
            return render_template('index.html', response=assistant_response)

        except openai.error.OpenAIError as e:
            app.logger.error(f"Error in OpenAI API call: {str(e)}")
            return render_template('index.html', error=f"An error occurred with OpenAI API: {str(e)}")
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            return render_template('index.html', error=f"An unexpected error occurred: {str(e)}")

    return render_template('index.html')

# Health check route to ensure the service is running
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "health-ai-app"}), 200

# Test route to confirm OpenAI API key is set
@app.route('/test-openai')
def test_openai_key():
    if openai.api_key:
        return f"OpenAI API key is set: {openai.api_key[:5]}...", 200
    else:
        return "OpenAI API key is not set!", 500

# Test route to check environment variable
@app.route('/test-env')
def test_env():
  
