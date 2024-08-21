from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Message:
    def __init__(self, data):
        self.id = data["id"]
        self.sender_id = data["sender_id"]
        self.receiver_id = data["receiver_id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def send(cls, data):
        query = """
        INSERT INTO messages (sender_id, receiver_id, content)
        VALUES (%(sender_id)s, %(receiver_id)s, %(content)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_conversation(cls, data):
        query = """
        SELECT * FROM messages
        WHERE (sender_id = %(sender_id)s AND receiver_id = %(receiver_id)s)
        OR (sender_id = %(receiver_id)s AND receiver_id = %(sender_id)s)
        ORDER BY created_at ASC;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        messages = []
        if results:
            for row in results:
                messages.append(cls(row))
        return messages
