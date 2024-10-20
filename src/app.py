from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

# Option 1: Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Option 2: Retrieve OpenAI API key from Google Cloud Secret Manager
# Uncomment the following lines if you prefer this option
# from google.cloud import secretmanager

# def access_secret(secret_id):
#     client = secretmanager.SecretManagerServiceClient()
#     name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
#     response = client.access_secret_version(request={"name": name})
#     secret = response.payload.data.decode("UTF-8")
#     return secret

# openai_api_key = access_secret('openai-api-key')
# openai.api_key = openai_api_key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Collect form data
            patient_data = request.form

            # Format the prompt
            prompt = f"""
            Patient Information:
            Identifier: {patient_data.get('identifier')}
            Gender: {patient_data.get('gender')}
            Height: {patient_data.get('height')} inches
            Weight: {patient_data.get('weight')} pounds
            Current Medications: {patient_data.get('medications')}
            Drug Allergies: {patient_data.get('allergies')}
            Current Medical Conditions: {patient_data.get('conditions')}
            Planned Procedure: {patient_data.get('procedure')}

            Please provide a comprehensive analysis of this patient's medical profile, including potential risks, considerations for the planned procedure, and any recommendations for their care.
            """

            # Make the OpenAI API call using the ChatGPT model
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            assistant_response = response['choices'][0]['message']['content']

            return render_template('index.html', response=assistant_response)

        except Exception as e:
            return render_template('index.html', error=str(e))

    # For GET request, render the form
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True)
