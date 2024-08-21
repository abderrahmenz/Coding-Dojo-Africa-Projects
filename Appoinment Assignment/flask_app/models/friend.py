# models/friend.py
from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Friend:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.friend_user_id = data["friend_user_id"]
        self.status = data.get("status", "pending")
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # Method to add a new friend relationship
    @classmethod
    def add_friend(cls, data):
        query = """
        INSERT INTO friends (user_id, friend_user_id, status)
        VALUES (%(user_id)s, %(friend_user_id)s, 'pending');
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Method to fetch all non-friends
    @classmethod
    def get_non_friends(cls, data):
        query = """
        SELECT * FROM users 
        WHERE id != %(id)s
        AND id NOT IN (
            SELECT friend_user_id FROM friends WHERE user_id = %(id)s
            UNION
            SELECT user_id FROM friends WHERE friend_user_id = %(id)s
        );
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        non_friends = []
        if results:
            for row in results:
                non_friends.append(row)
        return non_friends

    # Method to get all friends of a user
    @classmethod
    def get_friends(cls, data):
        query = """
        SELECT * FROM users
        WHERE id IN (
            SELECT friend_user_id FROM friends WHERE user_id = %(id)s
            UNION
            SELECT user_id FROM friends WHERE friend_user_id = %(id)s
        );
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        friends = []
        if results:
            for row in results:
                friends.append(row)
        return friends
    @classmethod
    def delete_friend(cls, data):
        query = """
        DELETE FROM friends 
        WHERE (user_id = %(user_id)s AND friend_user_id = %(friend_user_id)s)
        OR (user_id = %(friend_user_id)s AND friend_user_id = %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return None