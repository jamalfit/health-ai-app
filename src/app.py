from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set OpenAI API key (using environment variable or direct key for simplicity)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Route to handle form submission or API request
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Collect form data from the request
            patient_data = request.form

            # Format the prompt for OpenAI
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

            Please provide a comprehensive analysis of this patient's medical profile.
            """

            # Make the OpenAI request
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )

            # Get the response from OpenAI
            assistant_response = response['choices'][0]['message']['content']

            return render_template('index.html', response=assistant_response)

        except Exception as e:
            return render_template('index.html', error=str(e))

    # If it's a GET request, render a simple form
    return render_template('index.html')

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
