from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.goal import Goal

# Route to display the goal setting form
@app.route("/goalsettingnew")
def goalsetting_new():
    if "user_id" not in session:
        return redirect("/")
    
    goal_type = request.args.get("goal_type")
    return render_template("goalsettingnew.html", goal_type=goal_type)

# Route to handle form submission and save the goal
@app.route("/save_goal", methods=["POST"])
def save_goal():
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "user_id": session["user_id"],
        "goal_type": request.form["goal_type"],
        "target": request.form["target"],
        "duration_days": request.form["duration_days"],
        "start_date": request.form["start_date"],
        "end_date": request.form["end_date"]
    }

    Goal.save(data)
    flash("Goal saved successfully!")
    return redirect("/goalsetting")
