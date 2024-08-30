from flask import render_template, session, redirect, request
from flask_app.models.plan import Plan
from flask_app.models.users import User
from flask_app import app
from datetime import datetime

@app.route('/plans/new')
def new_plan():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('createplans.html')

@app.route('/plans/create', methods=['POST'])
def create_plan():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "user_id": session['user_id'],
        "goal_type": request.form['goal_type'],
        "location": request.form['location'],
        "daily_target": request.form['daily_target'],
        "start_date": request.form['start_date'],
        "end_date": request.form['end_date']
    }
    Plan.create(data)
    return redirect('/plans')

@app.route("/plans")
def display_plans():
    if "user_id" not in session:
        return redirect("/")
    
    user_id = session.get("user_id")
    print("User ID from session:", user_id)  # Debug: Verify user_id
    
    # Fetch plans specific to the logged-in user
    plans = Plan.get_plans_by_user_id(user_id)
    
    # Print to debug
    print("Fetched Plans:", plans)
    
    return render_template("plans.html", plans=plans)

@app.route('/plans')
def plans():
    query = "SELECT * FROM plans"
    plans = mysql.query_db(query)
    
    for plan in plans:
        query = """
            SELECT users.id, users.first_name 
            FROM plan_participants 
            JOIN users ON plan_participants.user_id = users.id 
            WHERE plan_participants.plan_id = %s
        """
        participants = mysql.query_db(query, (plan['id'],))
        plan['participants'] = participants

    return render_template('plans.html', plans=plans)

@app.route('/plans/join/<int:plan_id>', methods=['POST'])
def other_join_plan(plan_id):
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
def other_leave_plan(plan_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to leave a plan.', 'danger')
        return redirect('/login')
    
    # Assuming you have a Plan class and a method to leave a plan
    Plan.leave_plan(plan_id, user_id)
    
    flash('You have successfully left the plan.', 'success')
    return redirect('/plans')
