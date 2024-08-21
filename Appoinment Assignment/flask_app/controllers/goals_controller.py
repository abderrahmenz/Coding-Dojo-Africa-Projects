from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.goal import Goal

@app.route("/goals")
def goals():
    if "user_id" not in session:
        return redirect("/")
    
    data = {"user_id": session["user_id"]}
    goals = Goal.get_all_by_user(data)
    
    return render_template("goals.html", goals=goals)

@app.route("/goals/new", methods=["POST"])
def create_goal():
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "user_id": session["user_id"],
        "goal_type": request.form["goal_type"],
        "target": request.form.get("target"),
        "duration_days": request.form.get("duration_days")
    }

    Goal.create(data)

    return redirect("/goalsetting")  # Ensure redirection back to goalsetting page

@app.route("/goals/<int:id>")
def show_goal(id):
    if "user_id" not in session:
        return redirect("/")
    
    goal = Goal.get_by_id({"id": id})
    
    return render_template("goal_detail.html", goal=goal)

@app.route("/goals/<int:id>/edit")
def edit_goal(id):
    if "user_id" not in session:
        return redirect("/")
    
    goal = Goal.get_by_id({"id": id})
    
    return render_template("edit_goal.html", goal=goal)

@app.route("/goals/<int:id>/update", methods=["POST"])
def update_goal(id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "id": id,
        "activity": request.form["activity"],
        "steps": request.form.get("steps"),
        "duration": request.form["duration"],
        "daily_steps": request.form.get("daily_steps"),
        "total_walks": request.form.get("total_walks")
    }
    
    print("Updating goal with data:", data)
    
    Goal.update(data)
    return redirect(f"/goals/{id}")

@app.route("/goals/<int:id>/delete")
def delete_goal(id):
    if "user_id" not in session:
        return redirect("/")
    
    Goal.delete({"id": id})
    return redirect("/goals")
