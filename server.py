from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "AIzaSyABQHobyJo2wEqHaYJp-5WoD0cwjHlw04Q"  # Gemini API key (safe on server side)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": user_message}]}
        ]
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": reply})
        else:
            return jsonify({"error": data}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
