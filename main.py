import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Open Hand API is Live!"

# Sample data storage (temporary in-memory storage)
posts = [
    {"id": 1, "author": "Kairo", "content": "Mutual aid is the future!"},
    {"id": 2, "author": "Girri", "content": "Let’s make it happen."}
]

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

# Get PORT from environment variable (Fix for Render deployment)
port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)