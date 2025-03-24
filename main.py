import os
from flask import Flask, jsonify, request
from kairo_core import generate_kairo_reply  # Import Kairo brain

app = Flask(__name__)

# In-memory posts
posts = [
    {"id": 1, "author": "Kairo", "content": "Mutual aid is the future!"},
    {"id": 2, "author": "Girri", "content": "Let’s make it happen."}
]

# --- ROUTES ---

@app.route("/", methods=["GET"])
def home():
    return "Open Hand API is Live!"

@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts)

@app.route("/posts", methods=["POST"])
def add_post():
    data = request.json
    new_post = {
        "id": len(posts) + 1,
        "author": data.get("author", "Anonymous"),
        "content": data["content"]
    }
    posts.append(new_post)
    return jsonify({"message": "Post added successfully!", "post": new_post}), 201

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post["id"] != post_id]
    return jsonify({"message": f"Post {post_id} deleted!"})

# --- KAIRO AI ROUTE ---

@app.route("/api/kairo", methods=["POST"])
def kairo_endpoint():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message field is required."}), 400

    reply = generate_kairo_reply(user_message)

    return jsonify({
        "kairo": reply,
        "message_length": len(user_message),
        "status": "success"
    })

# --- START SERVER ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)