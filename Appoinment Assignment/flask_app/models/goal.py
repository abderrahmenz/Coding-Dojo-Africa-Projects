from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Goal:
    db = "appointments_db"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.goal_type = data['goal_type']
        self.target = data['target']
        self.duration_days = data['duration_days']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO goals (user_id, goal_type, target, duration_days, start_date, end_date)
            VALUES (%(user_id)s, %(goal_type)s, %(target)s, %(duration_days)s, %(start_date)s, %(end_date)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
