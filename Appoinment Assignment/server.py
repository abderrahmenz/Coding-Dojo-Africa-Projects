from flask_app import app
from flask_app.controllers import users_controller
from flask_app.controllers import posts
from flask_app.controllers import comments
from flask_app.controllers import goals_controller
from flask_app.controllers import friends_controller
from flask_app.controllers import messages_controller
from flask_app.controllers import progress_controller
if __name__ == "__main__":
    app.run(debug=True, port=1337)