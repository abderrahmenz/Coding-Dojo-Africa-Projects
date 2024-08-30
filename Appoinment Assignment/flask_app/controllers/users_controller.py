from flask_app import app
from flask_app.models.goal import Goal 
from flask_app.models.plan import Plan

from flask import redirect, render_template, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.users import User
from flask_app.models.post import Post
from flask_app.models.qna import QnA

bcrypt = Bcrypt(app)

# * View Routes
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("registration.html")

@app.route("/goalsetting")
def goalsetting():
    if "user_id" not in session:
        return redirect("/")
    return render_template("goalsetting.html")

@app.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect("/")
    
    goals = Goal.get_goals_by_user_id(session["user_id"])
    
    return render_template("progress.html", goals=goals)
@app.route("/plans")
def page_plans():
    if "user_id" not in session:
        return redirect("/")
    
    # Fetch all plans (not just those specific to the logged-in user)
    plans = Plan.get_all_plans()
    
    # Print to debug
    print("Fetched Plans:", plans)
    
    return render_template("plans.html", plans=plans)

@app.route('/plans/join/<int:plan_id>', methods=['POST'])
def join_plan(plan_id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "plan_id": plan_id,
        "user_id": session['user_id']
    }

    # Check if the user has already joined the plan
    if Plan.has_joined(data):
        flash("You have already joined this plan.", "warning")
        return redirect('/plans')

    Plan.join_plan(data)
    return redirect('/plans')
@app.route('/plans/leave/<int:plan_id>', methods=['POST'])
def leave_plan(plan_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to leave a plan.', 'danger')
        return redirect('/login')
    
    # Assuming you have a Plan class and a method to leave a plan
    Plan.leave_plan(plan_id, user_id)
    
    flash('You have successfully left the plan.', 'success')
    return redirect('/plans')


@app.route("/conversation")
def start_conversation():
    if "user_id" not in session:
        return redirect("/")
    return render_template("conversation.html")

@app.route("/friends")
def friends():
    if "user_id" not in session:
        return redirect("/")
    
    data = {"id": session["user_id"]}
    non_friends = User.get_non_friends(data)
    
    return render_template("friends.html", non_friends=non_friends)

# * Action Routes
@app.route("/register", methods=["POST"])
def process_register():
    if not User.validate_user(request.form):
        return redirect("/")
    
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {**request.form, "password": pw_hash}
    
    user_id = User.create(data)
    session["user_id"] = user_id
    
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def process_login():
    if not User.validate_login_user(request.form):
        return redirect("/")
    
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    
    if not user_in_db or not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password", "login")
        return redirect("/")
    
    # Store the user ID in the session
    session["user_id"] = user_in_db.id
    return redirect("/dashboard")

@app.route("/dashboard")
def dash():
    if "user_id" not in session:
        return redirect("/")
    
    data = {"id": session["user_id"]}
    current_user = User.get_by_id(data)
    
    # Get all posts
    posts = Post.get_all_with_users()

    # Get all Q&As
    qnas = QnA.get_all()  # Fetch all Q&A entries

    return render_template("dashboard.html", username=current_user.first_name, posts=posts, qnas=qnas)
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route('/myprogress')
def my_progress():
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']
    progress_list = Progress.get_by_user_id({'user_id': user_id})
    return render_template('myprogress.html', progress_list=progress_list)