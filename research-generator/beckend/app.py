from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder="static")
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"

# ------------------ FAVICON FIX ------------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        app.static_folder,
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# ------------------ GENERATE TITLES ------------------
@app.route("/generate-titles", methods=["POST"])
def generate_titles():
    theme = request.json.get("theme", "Artificial Intelligence")

    titles = [
        f"An AI-Driven Framework for {theme}",
        f"Automating Academic Research Writing in {theme} Using LLaMA",
        f"A Generative AI-Based Approach for Research Assistance in {theme}",
        f"Comparative Study of Human and LLaMA-Based Research Writing in {theme}",
        f"Intelligent Research Abstract Generation Using LLaMA for {theme}"
    ]

    return jsonify({"titles": titles})

# ------------------ GENERATE ABSTRACT ------------------
@app.route("/generate-abstract", methods=["POST"])
def generate_abstract():
    title = request.json.get("title", "")

    prompt = f"""
Write a detailed academic research abstract (300–500 words) for the title:

"{title}"

Follow IEEE style with structured sections.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=240
        )

        data = response.json()
        abstract_text = data.get("response", "")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "abstract": abstract_text,
        "comparison": {
            "human": "Human-written abstracts require time and expertise.",
            "llm": "LLaMA generates abstracts instantly with consistency."
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
