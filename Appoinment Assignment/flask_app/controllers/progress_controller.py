from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.goal import Goal
from flask_app.models.progress import Progress

@app.route("/progress_overview")
def progress_overview():
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
@app.route("/progress/update/<int:goal_id>")
def update_progress_form(goal_id):
    if "user_id" not in session:
        return redirect("/")
    
    progress = Progress.get_progress_by_goal_id({"goal_id": goal_id})
    return render_template("progressupdate.html", progress=progress)

@app.route("/progress/update", methods=["POST"])
def update_progress():
    if "user_id" not in session:
        return redirect("/")

    try:
        data = {
            "goal_id": request.form["goal_id"],
            "user_id": session["user_id"],  # Ensure the user_id is being passed
            "steps_taken": request.form["steps_taken"],
            "progress_percentage": request.form["progress_percentage"],
            "completed": request.form["completed"]
        }

        # Debugging statement to check the incoming data
        print("Data to be saved:", data)

        # Save or update the progress in the database
        if request.form.get("id"):
            data['id'] = request.form["id"]
            Progress.update(data)
        else:
            Progress.save(data)
        
        flash("Progress updated successfully!")
    except Exception as e:
        print("Error occurred while saving progress:", e)
        flash("An error occurred while updating progress.")
    
    return redirect("/trackprogress")


@app.route("/progress")
def display_progress():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session["user_id"]
    progress_list = Progress.get_progress_by_user_id({"user_id": user_id})
    
    return render_template("progress.html", progress_list=progress_list)

@app.route('/progressupdate/<int:id>', methods=['GET', 'POST'])
def new_progress_update(id):
    if 'user_id' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        data = {
            'id': id,
            'steps_taken': request.form['steps_taken'],
            'progress_percentage': request.form['progress_percentage'],
            'progress_date': request.form['progress_date'],
            'completed': request.form['completed']
        }
        Progress.update(data)
        return redirect('/trackprogress')

    progress = Progress.get_by_id({'id': id})
    return render_template('progressupdate.html', progress=progress)

@app.route('/trackprogress')
def track_progress():
    if 'user_id' not in session:
        return redirect('/')
    
    # Fetch progress for the logged-in user
    goals = Goal.get_goals_by_user_id(session['user_id'])
    progress_list = []
    for goal in goals:
        progress_entries = Progress.get_by_goal_id({'goal_id': goal.id})
        for progress in progress_entries:
            progress_list.append({
                'goal_type': goal.goal_type,  # Add goal type here
                'steps_taken': progress.steps_taken,
                'progress_percentage': progress.progress_percentage,
                'completed': progress.completed
            })
    
    return render_template('trackprogress.html', progress_list=progress_list)
@app.route('/edit_progress/<int:progress_id>', methods=['GET', 'POST'])
def edit_progress(progress_id):
    # Fetch the progress entry from the database using progress_id
    progress = Progress.query.get_or_404(progress_id)
    
    if request.method == 'POST':
        # Update the progress entry with new data
        progress.steps_taken = request.form['steps_taken']
        progress.progress_percentage = request.form['progress_percentage']
        progress.completed = request.form['completed']
        
        db.session.commit()
        return redirect(url_for('track_progress'))

    return render_template('edit_progress.html', progress=progress)
@app.route('/delete_progress/<int:progress_id>', methods=['POST'])
def delete_progress(progress_id):
    progress = Progress.query.get_or_404(progress_id)
    db.session.delete(progress)
    db.session.commit()
    return redirect(url_for('track_progress'))