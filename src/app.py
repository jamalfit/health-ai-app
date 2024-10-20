from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set OpenAI API key (using environment variable or direct key for simplicity)
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/', methods=['POST'])
def handle_request():
    try:
        # Get the input data from the request
        patient_data = request.json

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

        # Make the OpenAI request (minimal setup)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Return the assistant's response
        assistant_response = response['choices'][0]['message']['content']
        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
