from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.post import Post



@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    
    # Fetch all posts with user information
    posts = Post.get_all_with_users()
    
    # Pass the posts to the template
    return render_template("dashboard.html", posts=posts)



@app.route("/posts/new", methods=["POST"])
def create_post():
    if "user_id" not in session:
        return redirect("/")
    
    content = request.form.get("content")
    print("Received content:", content)  # Debugging line

    if content:
        post_data = {
            "user_id": session["user_id"],
            "content": content
        }
        Post.create(post_data)
    else:
        print("No content received")  # Debugging line
    
    return redirect("/dashboard")
