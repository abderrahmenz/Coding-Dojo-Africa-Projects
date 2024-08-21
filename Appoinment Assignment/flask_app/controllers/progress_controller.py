from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.progress import Progress

# Route to display the progress tracking page
@app.route("/progress")
def display_progress():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    progress_list = Progress.get_progress_by_user_id({"user_id": user_id})
    
    # Debugging: Check if progress_list has data
    print(progress_list)  # This will output the progress_list to the console
    
    return render_template("progress.html", progress_list=progress_list)

# Route to handle updating progress
@app.route("/update_progress", methods=["POST"])
def update_progress():
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "user_id": session["user_id"],
        "goal_id": request.form["goal_id"],
        "steps_taken": request.form["steps_taken"],
        "progress_date": request.form["progress_date"],
        "daily_goal": request.form["daily_goal"],
        "progress_percentage": request.form["progress_percentage"],
        "completed": request.form["completed"]
    }

    # Use either `save` or `update` method based on your requirement
    if request.form.get("is_new"):  # Assuming a hidden input field `is_new` to determine save or update
        Progress.save(data)
    else:
        Progress.update(data)
    
    flash("Progress updated successfully!")
    return redirect("/progress")
