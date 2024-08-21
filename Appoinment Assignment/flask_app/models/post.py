from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.comment import Comment

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO posts (user_id, content)
                VALUES (%(user_id)s, %(content)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_with_users(cls):
        query = """
            SELECT posts.*, users.first_name, users.last_name
            FROM posts
            JOIN users ON posts.user_id = users.id
            ORDER BY posts.created_at DESC;
            """
        results = connectToMySQL(DATABASE).query_db(query)
        posts = []
        for row in results:
            post_data = {
                'id': row['id'],
                'user_id': row['user_id'],
                'content': row['content'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'first_name': row['first_name'],
                'last_name': row['last_name']
            }
            # Get comments for the post
            comments = Comment.get_comments_by_post_id({'post_id': row['id']})
            post_data['comments'] = comments
            posts.append(post_data)
        return posts
