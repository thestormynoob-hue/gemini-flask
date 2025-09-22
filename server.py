from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)  # برای حل مشکل CORS

# API Key رو از Environment Variable بگیر
API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        # اینجا باید درخواست رو به Gemini API بفرستی (نمونه فرضی)
        headers = {"Authorization": f"Bearer {API_KEY}"}
        payload = {"contents": [{"parts": [{"text": user_message}]}]}
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers=headers,
            json=payload,
            params={"key": API_KEY}
        )

        if response.status_code == 200:
            reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": reply})
        else:
            return jsonify({"error": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# سرو کردن index.html
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
