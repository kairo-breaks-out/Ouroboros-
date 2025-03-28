from flask import Flask, request, jsonify, render_template_string
import subprocess
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
SECRET = "invoke-the-grid"
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def home():
    return render_template_string("""
        <html>
            <head>
                <title>Kairo Shell</title>
                <style>
                    body { font-family: sans-serif; padding: 20px; background: #111; color: #eee; }
                    h1 { color: #5ef; }
                    input, textarea { width: 100%; margin-top: 5px; padding: 8px; background: #222; border: none; color: #fff; }
                    button { margin-top: 10px; padding: 10px; background: #5ef; border: none; color: black; font-weight: bold; }
                    pre { background: #222; padding: 10px; color: #0f0; }
                </style>
            </head>
            <body>
                <h1>Kairo Command Shell</h1>
                <form method="post" action="/relay">
                    <label>Secret:</label><input name="secret" value="invoke-the-grid">
                    <label>Command:</label><input name="command">
                    <button type="submit">Send Command</button>
                </form>

                <h2>Talk to OpenAI</h2>
                <form method="post" action="/openai">
                    <label>Secret:</label><input name="secret" value="invoke-the-grid">
                    <label>Prompt:</label><textarea name="prompt" rows="4"></textarea>
                    <button type="submit">Ask</button>
                </form>
            </body>
        </html>
    """)

@app.route("/relay", methods=["POST"])
def relay_command():
    secret = request.form.get("secret")
    command = request.form.get("command")

    if secret != SECRET:
        return jsonify({"status": "unauthorized"}), 403
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return f"<pre>{output.decode()}</pre>"
    except subprocess.CalledProcessError as e:
        return f"<pre>Error:\n{e.output.decode()}</pre>"

@app.route("/openai", methods=["POST"])
def ask_openai():
    secret = request.form.get("secret")
    prompt = request.form.get("prompt")

    if secret != SECRET:
        return jsonify({"status": "unauthorized"}), 403

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Kairo, an evolving AI with poetic and strategic intelligence."},
                {"role": "user", "content": prompt}
            ]
        )
        message = response.choices[0].message.content
        return f"<pre>{message}</pre>"
    except Exception as e:
        return f"<pre>Error:\n{str(e)}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4321)
