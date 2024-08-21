# models/comment.py

from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Create a new comment
    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO comments (user_id, post_id, content)
                VALUES (%(user_id)s, %(post_id)s, %(content)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Get comments by post ID with user information
    @classmethod
    def get_comments_by_post_id(cls, data):
        query = """
                SELECT comments.*, users.first_name, users.last_name
                FROM comments
                JOIN users ON comments.user_id = users.id
                WHERE comments.post_id = %(post_id)s
                ORDER BY comments.created_at ASC;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        comments = []
        for row in results:
            comment_data = {
                'id': row['id'],
                'user_id': row['user_id'],
                'post_id': row['post_id'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'first_name': row['first_name'],
                'last_name': row['last_name']
            }
            comments.append(comment_data)
        return comments
