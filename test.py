import pdb
from stakinator.controller.db_manager import DatabaseManager
from stakinator.model.data_model import User

dbm = DatabaseManager()
# users_list = []
# users = dbm.session.query(User)
# for user in users:
#   users_list.append(user.as_dict())
# response = {"Users":
# [user.as_dict() for user in users]}
# pdb.set_trace()
user_id = 124946123
user = dbm.session.query(User).filter(User.id == user_id).first()
if user:
  response = {"User":
  user.serialize()}
  response = jsonify(response)
else:
  reponse = "NOT FOUND"
pdb.set_trace()