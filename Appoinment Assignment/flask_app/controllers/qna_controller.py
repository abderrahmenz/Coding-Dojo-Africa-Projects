from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.qna import QnA

# Route to display the dashboard with Q&A
@app.route('/dashboard_qna')
def dashboard_qna():
    if 'user_id' not in session:
        return redirect('/')
    
    qnas = QnA.get_all()
    return render_template('dashboard.html', qnas=qnas)

# Route to handle question submission
@app.route('/qna/submit_question', methods=['POST'])
def submit_question():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'question': request.form['question'],
        'user_id': session['user_id']
    }
    QnA.create_question(data)
    return redirect('/dashboard')

# Route to handle answer submission
@app.route('/qna/answer/<int:id>', methods=['POST'])
def submit_answer(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': id,
        'answer': request.form['answer']
    }
    QnA.create_answer(data)
    return redirect('/dashboard')

# Route to display a specific question and its answer
@app.route('/qna/view/<int:id>')
def display_single_qna(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {'id': id}
    qna = QnA.get_by_id(data)
    if not qna:
        flash("Question not found", "qna")
        return redirect('/dashboard_qna')

    return render_template('single_qna.html', qna=qna)
