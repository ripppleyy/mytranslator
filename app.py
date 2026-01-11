from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("q", "")
    target = data.get("target", "en")

    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target,
        "dt": "t",
        "q": text
    }

    r = requests.get(url, params=params)
    result = r.json()

    translated = result[0][0][0]

    return jsonify({"translatedText": translated})
