from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models.message import Message
from flask_app.models.friend import Friend

@app.route("/conversation/<int:friend_id>")
def conversation(friend_id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "sender_id": session["user_id"],
        "receiver_id": friend_id
    }
    
    # Fetch the conversation between the current user and the selected friend
    messages = Message.get_conversation(data)
    
    # Attempt to fetch the friend's details
    friend = Friend.get_by_id(friend_id)
    
    return render_template("messages.html", messages=messages, friend=friend, friend_id=friend_id)

@app.route("/send_message/<int:friend_id>", methods=["POST"])
def send_message(friend_id):
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "sender_id": session["user_id"],
        "receiver_id": friend_id,
        "content": request.form["content"]
    }
    
    Message.send(data)
    return redirect(f"/conversation/{friend_id}")
