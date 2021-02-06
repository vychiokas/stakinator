from flask import Flask
from flask import jsonify
app = Flask(__name__)
from stakinator.controller.db_manager import DatabaseManager
from stakinator.model.data_model import User


@app.route('/')
def hello_world():
    return 'Welcome to the Stakinator API!'

@app.route('/users')
def show_all_users():
    dbm = DatabaseManager()
    users = dbm.session.query(User)
    response = {"Users":
    [user.serialize() for user in users]}
    response = jsonify(response)
    return response, 200


@app.route('/user/<user_id>')
def show_single_user(user_id):
    dbm = DatabaseManager()
    user = dbm.session.query(User).filter(User.id == user_id).first()
    if user:
        response = {"User": user.serialize()}
        return response
    else:
        reponse = {"message": f"user with id: {user_id} not found"}
        return reponse, 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)