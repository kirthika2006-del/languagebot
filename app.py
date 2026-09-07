import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from chatbot_config import CHATBOT_NAME, SYSTEM_PROMPT

# Load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model with the system instruction
model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite",
    system_instruction=SYSTEM_PROMPT
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", chatbot_name=CHATBOT_NAME)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type something!"}), 400

    try:
        response = model.generate_content(user_message)
        reply_text = response.text
    except Exception as e:
        reply_text = f"Sorry, something went wrong: {str(e)}"

    return jsonify({"reply": reply_text})


if __name__ == "__main__":
    app.run(debug=True)
