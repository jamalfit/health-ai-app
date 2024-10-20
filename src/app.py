from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

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

            Please provide a comprehensive analysis of this patient's medical profile.
            """

            # Make the OpenAI API call using the new interface
            response = openai.Completion.create(
                engine="gpt-4",  # Note: 'engine' instead of 'model'
                prompt=prompt,
                max_tokens=500
            )

            assistant_response = response.choices[0].text.strip()

            return render_template('index.html', response=assistant_response)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
