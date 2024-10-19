from flask import Flask, render_template, request, jsonify
from google.cloud import secretmanager
import os
import openai

app = Flask(__name__)

# Setup secret manager client
client = secretmanager.SecretManagerServiceClient()

def access_secret(secret_id):
    name = f"projects/health-ai-app-2024-439109/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Set OpenAI API key and Assistant ID
openai.api_key = access_secret('openai-api-key')
ASSISTANT_ID = access_secret('openai-assistant-id')

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

        # Send prompt to OpenAI Assistant
        try:
            client = openai.OpenAI()
            thread = client.beta.threads.create()
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSISTANT_ID
            )

            # Wait for the run to complete
            while run.status != 'completed':
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            # Retrieve the assistant's response
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            assistant_response = next(msg.content[0].text.value for msg in messages if msg.role == "assistant")

            return render_template('index.html', response=assistant_response)
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "health-ai-app"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))