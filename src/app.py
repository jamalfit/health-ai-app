from flask import Flask, render_template, request, jsonify
from google.cloud import secretmanager
import openai
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Setup secret manager client
client = secretmanager.SecretManagerServiceClient()

def access_secret(secret_id):
    try:
        name = f"projects/health-ai-app-2024-439109/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        app.logger.error(f"Error accessing secret {secret_id}: {str(e)}")
        raise

try:
    # Cache secrets at startup
    openai_api_key = access_secret('openai-api-key-2')
    assistant_id = access_secret('openai-assistant-id')

    # Log first few characters of the API key
    app.logger.info(f"OpenAI API Key loaded: {openai_api_key[:5]}...")

    # Set OpenAI API key
    openai.api_key = openai_api_key
    app.logger.info("Secrets loaded successfully")
except Exception as e:
    app.logger.error(f"Failed to load secrets: {str(e)}")

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
            # Use the correct API call for OpenAI completions in version >= 1.0.0
            response = openai.completions.create(
                model="gpt-4",
                prompt=prompt,
                max_tokens=500  # Adjust based on your needs
            )
            assistant_response = response['choices'][0]['text']
            app.logger.info("Received response from OpenAI")
            return render_template('index.html', response=assistant_response)

        except Exception as e:
            app.logger.error(f"Error in OpenAI API call: {str(e)}")
            return render_template('index.html', error=f"An error occurred: {str(e)}")

    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "health-ai-app"}), 200

@app.route('/test-secrets')
def test_secrets():
    try:
        return f"OpenAI API Key: {openai_api_key[:5]}..., Assistant ID: {assistant_id}"
    except Exception as e:
        return f"Error accessing secrets: {str(e)}"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
