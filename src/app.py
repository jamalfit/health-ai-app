from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('status.html')

@app.route('/health')
def health_check():
    return "Service running", 200

if __name__ == '__main__':
    app.run(debug=True)
