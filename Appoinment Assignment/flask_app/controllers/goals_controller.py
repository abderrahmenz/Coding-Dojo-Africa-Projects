from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.goal import Goal
from flask_app.models.progress import Progress

# Route to display the goal setting form
@app.route("/goalsettingnew")
def goalsetting_new():
    if "user_id" not in session:
        return redirect("/")
    
    goal_type = request.args.get("goal_type")
    img_url = request.args.get('img_url')
    return render_template("goalsettingnew.html", goal_type=goal_type, img_url=img_url)

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


@app.route("/progress")
def all_goals():
    if "user_id" not in session:
        return redirect("/")
    
    # Fetch goals and progress specific to the logged-in user
    goals = Goal.get_goals_by_user_id(session["user_id"])
    
    progress_data = []
    for goal in goals:
        progress_entries = Progress.get_by_goal_id({"goal_id": goal.id})
        latest_progress = progress_entries[-1].progress if progress_entries else 0  # Get the latest progress or 0
        progress_percentage = (latest_progress / goal.target) * 100 if goal.target else 0
        progress_data.append({
            "goal": goal,
            "latest_progress": latest_progress,
            "progress_percentage": progress_percentage
        })
    
    return render_template("progress.html", progress_data=progress_data)

@app.route("/progress/<int:goal_id>/update")
def progress_update(goal_id):
    if "user_id" not in session:
        return redirect("/")
    
    goal = Goal.get_goal_by_id({"id": goal_id})
    return render_template("progressupdate.html", goal=goal)


@app.route("/progress/<int:goal_id>/save", methods=["POST"])
def save_progress(goal_id):
    if "user_id" not in session:
        return redirect("/")

    # Save the progress update
    progress_data = {
        "goal_id": goal_id,
        "steps_taken": request.form["progress"]  # Adjusted to match the 'steps_taken' column
    }
    Progress.save(progress_data)

    flash("Progress updated successfully!")
    return redirect("/progress")
@app.route("/goals/<int:goal_id>/delete", methods=["POST"])
def delete_goal(goal_id):
    if "user_id" not in session:
        return redirect("/")

    Goal.delete_goal({"id": goal_id})
    flash("Goal deleted successfully!")
    return redirect("/progress")