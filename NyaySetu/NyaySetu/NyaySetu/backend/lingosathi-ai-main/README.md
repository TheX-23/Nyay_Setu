# LingoSathi

**LingoSathi** is a multilingual chatbot backend built with Flask. It supports Indian languages like Hindi, Marathi, Tamil, Bhojpuri, and more.

## Features

- Accepts user messages via POST request
- Sends bot reply (currently dummy) translated to the target language
- Uses Google Translator API via `deep-translator`

## API Endpoint

**POST** `/chat`

**Request Body (JSON):**

{
  "message": "Hello",
  "lang": "hi"
}

**Response:**

{
  "original": "Hello! How can I help you?",
  "translated": "नमस्ते! मैं आपकी किस प्रकार सहायता कर सकता हूँ?",
  "lang": "hi"
}

## Running Locally

Install dependencies:

pip install flask deep-translator

Run the app:

python app.py

## Coming Soon

- Real AI chatbot integration
- Android frontend (LingoSathi app)
- More Indian language support
