from flask import Flask, render_template, request, jsonify
# from google.cloud import secretmanager
# import openai
import os

app = Flask(__name__)

# Setup secret manager client (commented out for now)
# client = secretmanager.SecretManagerServiceClient()

# def access_secret(secret_id):
#     name = f"projects/health-ai-app-2024-439109/secrets/{secret_id}/versions/latest"
#     response = client.access_secret_version(request={"name": name})
#     return response.payload.data.decode("UTF-8")

# Cache secrets at startup (commented out for now)
# openai_api_key = access_secret('openai-api-key')
# assistant_id = access_secret('openai-assistant-id')

# openai.api_key = openai_api_key

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

        # Format prompt for OpenAI (commented out for now)
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
            # Commented out the OpenAI call for now
            # response = openai.ChatCompletion.create(
            #     model="gpt-4",
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         {"role": "user", "content": prompt}
            #     ]
            # )
            # assistant_response = response.choices[0].message['content']

            # For now, mock the assistant response
            assistant_response = "This is a mock 
