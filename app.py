from controller.db_manager import DatabaseManager

from importlib import import_module
from model.data_model import Question


class StakinatorApp():
  def __init__(self):
    self.dm = DatabaseManager()
  

  def create_database(self):
    self.dm.drop_structure()
    self.dm.create_structure()

if __name__ == "__main__":
  
  app = StakinatorApp()
  app.create_database()
  app.dm.session.commit()

  