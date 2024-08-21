from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Progress:
    db = "appointments_db"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.goal_id = data['goal_id']
        self.steps_taken = data['steps_taken']
        self.progress_date = data['progress_date']
        self.daily_goal = data['daily_goal']
        self.progress_percentage = data['progress_percentage']
        self.completed = data['completed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO progress (user_id, goal_id, steps_taken, progress_date, daily_goal, progress_percentage, completed)
            VALUES (%(user_id)s, %(goal_id)s, %(steps_taken)s, %(progress_date)s, %(daily_goal)s, %(progress_percentage)s, %(completed)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_progress_by_user_id(cls, data):
        query = "SELECT * FROM progress WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        progress_list = []
        for row in results:
            progress_list.append(cls(row))
        return progress_list
    @classmethod
    def update(cls, data):
        query = """
            UPDATE progress 
            SET steps_taken = %(steps_taken)s, progress_percentage = %(progress_percentage)s, 
            progress_date = %(progress_date)s, daily_goal = %(daily_goal)s, completed = %(completed)s
            WHERE goal_id = %(goal_id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
