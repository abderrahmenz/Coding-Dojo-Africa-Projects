from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_bcrypt import Bcrypt

from flask_app.models.users import User
from flask_app.models.post import Post

bcrypt = Bcrypt(app)


# * View Route
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/goalsetting")
def goalsetting():
    return render_template("goalsetting.html")

@app.route("/progress")
def progress():
    return render_template("progress.html")

@app.route("/plans")
def plans():
    return render_template("plans.html")

from flask_app.models.users import User

@app.route("/friends")
def friends():
    if "user_id" not in session:
        return redirect("/")
    
    data = {"id": session["user_id"]}
    non_friends = User.get_non_friends(data)
    
    print("Non-friends:", non_friends)  # Debug statement

    return render_template("friends.html", non_friends=non_friends)




#! ACTION ROUTE
# === Register ===
@app.route("/register", methods=["POST"])
def process_register():

    # validate the form here ...
    if not User.validate_user(request.form):
        return redirect("/")
    # create the hash
    # print("-------->", request.form["password"])
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    # print("=======>", pw_hash)
    # User.create(request.form)
    data = {**request.form, "password": pw_hash}
    # store the user id inside the session
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/dashboard")


#! ACTION ROUTE
# === Login ===
@app.route("/login", methods=["POST"])
def process_login():

    if not User.validate_login_user(request.form):
        return redirect("/")

    # see if the username provided exists in the database
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect("/")

    # get the user by his email
    session["user_id"] = user_in_db.id
    return redirect("/dashboard")

@app.route("/dashboard") #New
def dash():
    if "user_id" not in session:
        return redirect("/")
    
    data = {"id": session["user_id"]}
    current_user = User.get_by_id(data)
    
    # Get all posts
    posts = Post.get_all_with_users()
    
    return render_template("dashboard.html", username=current_user.first_name, posts=posts)
# LOGOUT


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")