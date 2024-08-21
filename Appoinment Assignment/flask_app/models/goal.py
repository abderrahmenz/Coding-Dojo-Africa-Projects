from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Goal:
    def __init__(self, data):
        self.id = data.get("id")
        self.goal_type = data.get("goal_type")
        self.target = data.get("target")
        self.duration_days = data.get("duration_days")
        self.start_date = data.get("start_date")
        self.end_date = data.get("end_date")
        self.user_id = data.get("user_id")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO goals (goal_type, target, duration_days, start_date, end_date, user_id)
                VALUES (%(goal_type)s, %(target)s, %(duration_days)s, %(start_date)s, %(end_date)s, %(user_id)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_by_user(cls, data):
        query = """
                SELECT * FROM goals
                WHERE user_id = %(user_id)s;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print("DEBUG: Query results:", results)
        goals = []
        if results:
            for row in results:
                print("DEBUG: Row data:", row)
                goals.append(cls(row))
        return goals

    @classmethod
    def get_by_id(cls, data):
        query = """
                SELECT * FROM goals
                WHERE id = %(id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def update(cls, data):
        query = """
                UPDATE goals
                SET activity = %(activity)s, status = %(status)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM goals
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)
