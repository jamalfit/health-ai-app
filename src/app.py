from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

# Set OpenAI API key
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
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )

            assistant_response = response['choices'][0]['message']['content']

            return render_template('index.html', response=assistant_response)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True)
