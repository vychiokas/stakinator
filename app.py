from controller.db_manager import DatabaseManager

from importlib import import_module
from model.data_model import Question
import argparse
from controller.populate_db import PopulateAnswerTable, PopulateQuestionTable, PopulateUserTable

class StakinatorApp():
  def __init__(self):
    self.dm = DatabaseManager()
  

  def create_database(self):
    self.dm.drop_structure()
    self.dm.create_structure()

if __name__ == "__main__":
  
  

  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('-db', "--database", help='an integer for the accumulator',
                      action="store_true")
  parser.add_argument('-p', "--populate", help='an integer for the accumulator',
                    action="store_true")

  args = parser.parse_args()

  if args.database:
    app = StakinatorApp()
    app.create_database()
    app.dm.session.commit()


  if args.populate:

    popq = PopulateQuestionTable()
    popq.run()
    popc = PopulateAnswerTable()
    popc.run()
    popu = PopulateUserTable()
    popu.run()

  