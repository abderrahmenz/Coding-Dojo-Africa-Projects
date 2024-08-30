# controllers/friends_controller.py
from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.friend import Friend

@app.route("/manage_friends")  # Renamed route
def manage_friends():  # Renamed function
    if "user_id" not in session:
        return redirect("/")
    
    data = {"id": session["user_id"]}
    non_friends = Friend.get_non_friends(data)
    friends = Friend.get_friends(data)
    
    return render_template("friends.html", non_friends=non_friends, friends=friends)

@app.route("/add_friend/<int:friend_id>", methods=["POST"])
def add_friend(friend_id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "user_id": session["user_id"],
        "friend_user_id": friend_id
    }
    Friend.add_friend(data)
    return redirect("/manage_friends")  # Make sure this redirects to the correct new route
    
@app.route("/delete_friend/<int:friend_id>", methods=["POST"])
def delete_friend(friend_id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "user_id": session["user_id"],
        "friend_user_id": friend_id
    }
    Friend.delete_friend(data)
    return redirect("/manage_friends")
@app.route('/conversation')
def new_conversation():
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']
    friends = Friend.get_friends_by_user_id(user_id)
    return render_template('conversation.html', friends=friends)