import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data storage (temporary in-memory storage)
posts = [
    {"id": 1, "author": "Kairo", "content": "Mutual aid is the future!"},
    {"id": 2, "author": "Girri", "content": "Let’s make it happen."}
]

# Home Route
@app.route("/", methods=["GET"])
def home():
    return "Open Hand API is Live!"

# Endpoint to get all posts
@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts)

# Endpoint to add a new post
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

# Endpoint to delete a post
@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post["id"] != post_id]
    return jsonify({"message": f"Post {post_id} deleted!"})

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 for Render
    app.run(host="0.0.0.0", port=port, debug=True)