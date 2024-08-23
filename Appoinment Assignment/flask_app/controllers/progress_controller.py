from flask_app import app
from flask import redirect, render_template, session
from flask_app.models.goal import Goal

@app.route("/progress")
def display_progress():
    if "user_id" not in session:
        return redirect("/")
    
    data = {"user_id": session["user_id"]}
    goal = Goal.get_goal_by_user_id(data)
    
    print(goal)  # Debugging: Check if goal is fetched correctly
    
    if goal:
        print(f"Goal found: {goal.goal_type}, {goal.target}")  # More detailed debugging
    
    return render_template("progress.html", goal=goal)

