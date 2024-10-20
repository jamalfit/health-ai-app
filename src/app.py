from flask import Flask, render_template, request, jsonify
from google.cloud import secretmanager
import openai
import os

app = Flask(__name__)

# Setup secret manager client
client = secretmanager.SecretManagerServiceClient()

def access_secret(secret_id):
    name = f"projects/health-ai-app-2024-439109/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Cache secrets at startup
#openai_api_key = access_secret('openai-api-key')
#assistant_id = access_secret('openai-assistant-id')

openai_api_key = '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'
assistant_id = 'asst_P3tTEDFn8OLQEOeS55T66Zuz'


openai.api_key = openai_api_key

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
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            assistant_response = response.choices[0].message['content']

            return render_template('index.html', response=assistant_response)

        except Exception as e:
            app.logger.error(f"Error: {e}")
            return render_template('index.html', error="An error occurred, please try again later.")

    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "health-ai-app"}), 200
