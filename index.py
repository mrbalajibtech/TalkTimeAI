from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the API key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Configure Google AI
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Handle the message sent from the frontend
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_input = data.get('message', '')

    # Create chat session and send message
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)

    return jsonify({"response": response.text})
