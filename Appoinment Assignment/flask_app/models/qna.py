from flask_app.configs.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class QnA:
    def __init__(self, data):
        self.id = data["id"]
        self.question = data.get("question", "")
        self.answer = data.get("answer", "")
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    # Create a new question
    @classmethod
    def create_question(cls, data):
        query = """
                INSERT INTO qna (question, user_id, created_at, updated_at)
                VALUES (%(question)s, %(user_id)s, NOW(), NOW());
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Create a new answer
    @classmethod
    def create_answer(cls, data):
        query = """
                UPDATE qna
                SET answer = %(answer)s, updated_at = NOW()
                WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Get all questions and answers
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM qna;"
        results = connectToMySQL(DATABASE).query_db(query)

        qna_list = []
        if results:
            for row in results:
                qna_list.append(cls(row))
        return qna_list

    # Get a specific question and its answer by ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM qna WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        
        if result:
            return cls(result[0])
        return False
