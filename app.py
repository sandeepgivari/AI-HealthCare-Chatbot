import os
import json
import base64
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["healthcare_bot"]
users_collection = db["users"]

# Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env file.")


@app.route('/register', methods=['POST'])
def register_user():
    """Register or update user details"""
    data = request.json
    name = data.get('name')
    age = data.get('age')
    place = data.get('place')
    mobile = data.get('mobile')

    if not all([name, age, place, mobile]):
        return jsonify({"error": "All fields are required"}), 400

    # Check if user already exists by mobile number
    existing_user = users_collection.find_one({"mobile": mobile})

    if existing_user:
        # Update existing user details
        users_collection.update_one(
            {"mobile": mobile},
            {"$set": {"name": name, "age": age, "place": place}}
        )
        message = "User details updated."
    else:
        # Insert new user record
        users_collection.insert_one({
            "name": name,
            "age": age,
            "place": place,
            "mobile": mobile,
            "chats": []
        })
        message = "User registered successfully."

    return jsonify({"message": message}), 200


@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for AI healthcare bot"""
    try:
        mobile = request.form.get('mobile')
        message = request.form.get('message', '')
        file_obj = request.files.get('file')

        user = users_collection.find_one({"mobile": mobile})
        if not user:
            return jsonify({"error": "User not registered."}), 400

        parts = []
        if message:
            parts.append({"text": message})

        if file_obj:
            file_bytes = file_obj.read()
            file_base64 = base64.b64encode(file_bytes).decode('utf-8')
            mime_type = file_obj.mimetype
            parts.append({
                "inlineData": {
                    "mimeType": mime_type,
                    "data": file_base64
                }
            })

        payload = {
            "contents": [{
                "parts": parts,
                "role": "user"
            }],
            "systemInstruction": {
                "parts": [{"text": "You are an AI healthcare assistant. Keep answers short (2-3 lines). You give general health information and suggest professional consultation for diagnosis."}]
            }
        }

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GOOGLE_API_KEY}"

        response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        response.raise_for_status()

        response_data = response.json()
        response_text = response_data.get('candidates')[0]['content']['parts'][0]['text']

        # Save chat to user's record
        users_collection.update_one(
            {"mobile": mobile},
            {"$push": {"chats": {"user": message, "bot": response_text}}}
        )

        return jsonify({"text": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
