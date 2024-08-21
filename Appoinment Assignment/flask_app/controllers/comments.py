# controllers/comments.py

from flask_app import app
from flask import redirect, request, session
from flask_app.models.comment import Comment

# Create a new comment
@app.route("/comments/new", methods=["POST"])
def create_comment():
    if "user_id" not in session:
        return redirect("/")
    
    comment_data = {
        "user_id": session["user_id"],
        "post_id": request.form["post_id"],
        "content": request.form["content"]
    }
    Comment.create(comment_data)
    return redirect("/dashboard")
