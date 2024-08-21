from flask import Flask
app = Flask(__name__)
DATABASE = "appointments_db"
app.secret_key = "abderrahmen"