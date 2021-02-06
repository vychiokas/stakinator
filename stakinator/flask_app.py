from flask import Flask
from flask import jsonify
app = Flask(__name__)
from controller.db_manager import DatabaseManager
from model.data_model import User


@app.route('/')
def hello_world():
    return 'Welcome to the Stakinator API!'

@app.route('/users')
def show_user_profile():
    dbm = DatabaseManager()
    users = dbm.session.query(User)
    response = {"Users":
    [user.as_dict() for user in users]}
    response = jsonify(response)
    return response

if __name__ == "__main__":
    app.run()