from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Progress:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.goal_id = data['goal_id']
        self.steps_taken = data['steps_taken']
        self.progress_percentage = data['progress_percentage']
        self.completed = data['completed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO progress (goal_id, user_id, steps_taken, progress_percentage, completed, created_at, updated_at)
            VALUES (%(goal_id)s, %(user_id)s, %(steps_taken)s, %(progress_percentage)s, %(completed)s, NOW(), NOW());
        """
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_by_goal_id(cls, data):
        query = "SELECT * FROM progress WHERE goal_id = %(goal_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return [cls(row) for row in results] if results else []

    @classmethod
    def update(cls, data):
        query = """
            UPDATE progress 
            SET steps_taken = %(steps_taken)s, progress_percentage = %(progress_percentage)s, 
            completed = %(completed)s, updated_at = NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM progress WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return None
