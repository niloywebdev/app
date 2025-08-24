# First, install the necessary libraries for the web app.
# You can run this command in your terminal:
# pip install Flask cohere python-dotenv

import os
from flask import Flask, render_template_string, request
import cohere
from dotenv import load_dotenv

# --- Security Note: Use environment variables for API keys ---
# This line loads environment variables from a .env file.
# You MUST create a .env file in the same directory with your API key:
# COHERE_API_KEY="your_api_key_here"
load_dotenv()

COHERE_API_KEY = os.getenv("sztIbfwPJ9abhjxMm7lVGLHmBTzd7p3vL7Ks0sOG")

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY environment variable not set.")

co = cohere.Client(api_key=COHERE_API_KEY)
app = Flask(__name__)

# --- HTML for the web page ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Awesome Quote Generator</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; color: #333; text-align: center; padding: 40px; }
        .container { max-width: 600px; margin: 0 auto; background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h1 { color: #0056b3; margin-bottom: 20px; }
        .mood-selector { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 25px; }
        .mood-selector button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
        }
        .mood-selector button:hover {
            background-color: #0056b3;
            transform: translateY(-2px);
        }
        #quote-display {
            background-color: #e9ecef;
            border-left: 5px solid #007bff;
            padding: 20px;
            margin-top: 20px;
            border-radius: 8px;
            font-style: italic;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Awesome Quote Generator</h1>
        <p>Select a mood to generate an awesome quote!</p>
        <form method="post" action="/">
            <div class="mood-selector">
                <button type="submit" name="mood" value="happy">Happy</button>
                <button type="submit" name="mood" value="sad">Sad</button>
                <button type="submit" name="mood" value="motivational">Motivational</button>
                <button type="submit" name="mood" value="inspirational">Inspirational</button>
                <button type="submit" name="mood" value="funny">Funny</button>
            </div>
        </form>
        <div id="quote-display">
            {% if quote %}
                {{ quote }}
            {% else %}
                Your quote will appear here.
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# --- Quote Generation Logic (Reused from your script) ---
def generate_quote(mood):
    prompt_map = {
        'happy': "Generate a single, uplifting and memorable quote about finding happiness in everyday life, with a relevant emoji at the end.",
        'sad': "Generate a single, thoughtful quote about navigating through a sad moment, with a relevant emoji at the end.",
        'motivational': "Generate a single, powerful quote that motivates someone to take action and overcome challenges, with a relevant emoji at the end.",
        'inspirational': "Generate a single, inspirational quote about believing in oneself and personal growth, with a relevant emoji at the end.",
        'funny': "Generate a single, very short and clever quote that is humorous and light-hearted, with a relevant emoji at the end. Make it a funny saying or observation."
    }
    
    prompt = prompt_map.get(mood.lower())
    if not prompt:
        return "Invalid mood selected."

    try:
        response = co.generate(
            prompt=prompt,
            model="command",
            max_tokens=40,
            temperature=0.9,
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"An API error occurred: {e}"

# --- Web App Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    quote = None
    if request.method == "POST":
        selected_mood = request.form.get("mood")
        if selected_mood:
            quote = generate_quote(selected_mood)
    
    return render_template_string(HTML_TEMPLATE, quote=quote)

if __name__ == "__main__":
    app.run(debug=True)
