from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Goal:
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
            INSERT INTO goals (user_id, goal_type, target, duration_days, start_date, end_date, created_at, updated_at)
            VALUES (%(user_id)s, %(goal_type)s, %(target)s, %(duration_days)s, %(start_date)s, %(end_date)s, NOW(), NOW());
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_goals_by_user_id(cls, user_id):
        query = """
            SELECT goals.*, users.first_name AS username
            FROM goals
            JOIN users ON goals.user_id = users.id
            WHERE goals.user_id = %(user_id)s;
        """
        data = {"user_id": user_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        goals = []
        for row in results:
            goal = cls(row)
            goal.username = row['username']  # Add the username to the goal object
            goals.append(goal)
        
        return goals
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM goals;"
        results = connectToMySQL(DATABASE).query_db(query)

        if not results:
            print("No goals found in the database.")  # Debugging statement
            return []

        goals = []
        for row in results:
            goals.append(cls(row))
        return goals

    @classmethod
    def get_goal_by_id(cls, data):
        query = "SELECT * FROM goals WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def get_goal_by_user_id(cls, data):
        query = "SELECT * FROM goals WHERE user_id = %(user_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return None
        return cls(result[0])

    @classmethod
    def update_goal(cls, data):
        query = """
            UPDATE goals
            SET goal_type = %(goal_type)s, target = %(target)s, duration_days = %(duration_days)s,
                start_date = %(start_date)s, end_date = %(end_date)s, updated_at = NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def delete_goal(cls, data):
        query = "DELETE FROM goals WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)