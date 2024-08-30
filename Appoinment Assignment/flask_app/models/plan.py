from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Plan:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.goal_type = data['goal_type']
        self.location = data['location']
        self.daily_target = data['daily_target']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.participants = []

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO plans (user_id, goal_type, location, daily_target, start_date, end_date)
        VALUES (%(user_id)s, %(goal_type)s, %(location)s, %(daily_target)s, %(start_date)s, %(end_date)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_by_user(cls, data):
        query = "SELECT * FROM plans WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return [cls(row) for row in results] if results else []

    @classmethod
    def get_plans_by_user_id(cls, user_id):
        query = "SELECT * FROM plans WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, {"user_id": user_id})
        plans = []
        for result in results:
            plan = cls(result)
            plan.participants = cls.get_participants_by_plan_id(plan.id)
            plans.append(plan)
        return plans

    @classmethod
    def get_participants_by_plan_id(cls, plan_id):
        query = """
        SELECT users.first_name
        FROM plan_participants
        JOIN users ON plan_participants.user_id = users.id
        WHERE plan_participants.plan_id = %(plan_id)s;
        """
        data = {"plan_id": plan_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        return [row['first_name'] for row in results] if results else []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM plans;"
        results = connectToMySQL(DATABASE).query_db(query)
        return [cls(row) for row in results] if results else []
    
    @classmethod
    def join_plan(cls, data):
        query = """
        INSERT INTO plan_participants (plan_id, user_id)
        VALUES (%(plan_id)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def get_all_plans(cls):
        query = "SELECT * FROM plans;"
        results = connectToMySQL(DATABASE).query_db(query)
        plans = []
        for result in results:
            plan = cls(result)
            plan.participants = cls.get_participants_by_plan_id(plan.id)
            plans.append(plan)
        return plans

    @classmethod
    def has_joined(cls, data):
        query = """
        SELECT * FROM plan_participants 
        WHERE plan_id = %(plan_id)s AND user_id = %(user_id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query, data)
        return len(result) > 0

    @classmethod
    def leave_plan(cls, plan_id, user_id):
        query = "DELETE FROM plan_participants WHERE plan_id = %(plan_id)s AND user_id = %(user_id)s;"
        data = {
            'plan_id': plan_id,
            'user_id': user_id
        }
        connectToMySQL('appointments_db').query_db(query, data)