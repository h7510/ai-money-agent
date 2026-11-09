from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

def ask_ai(prompt):
    if not API_KEY:
        return "API key not configured"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

    response = requests.post(
        url,
        headers={"x-goog-api-key": API_KEY},
        json={
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        },
        timeout=45
    )

    response.raise_for_status()
    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"]


@app.route("/")
def home():
    return "AI Money Agent is running!"


@app.route("/outreach", methods=["POST"])
def outreach():
    data = request.json or {}

    prompt = f"""
    Write a professional personalized business
    introduction message.

    Business: {data.get('business')}
    Prospect: {data.get('prospect')}
    Service: {data.get('service')}

    Keep it short, honest and professional.
    """

    return jsonify({"message": ask_ai(prompt)})


@app.route("/reply", methods=["POST"])
def reply():
    data = request.json or {}

    prompt = f"""
    Write a helpful professional customer reply.

    Customer message:
    {data.get('message')}

    Business context:
    {data.get('business')}

    Do not invent facts.
    """

    return jsonify({"reply": ask_ai(prompt)})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )