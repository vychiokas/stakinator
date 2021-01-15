
from controller.api_parser import StackExchange_API
from controller.db_manager import DatabaseManager
from model.data_model import Question


class PopulateQuestionTable():
  def __init__(self, parsed_json):
    self.parsed_json = parsed_json
    self.dbm = DatabaseManager()

  def run(self):
    for item in self.parsed_json["items"]:
      id = item["question_id"]
      body = item["title"]
      print({id: body})
      question = Question(id=id, body=body)
      self.dbm.session.add(question)
      self.dbm.session.commit()

class PopulateCommentTable():
  def __init__(self):
    pass

if __name__ == "__main__":
  api = StackExchange_API(version=StackExchange_API._VERSION, field="questions", order="desc", min="20", sort="votes", tag="python", filter="!*SU8CGYZitCB.D*(BDVIfh2KKqQ)7jqYCBJzAPqv1FF5P6ymFq8a9Bc8edtQc*PqJ)28g05P" )
  questions = api.get_data()
  popq = PopulateQuestionTable(questions)
  popq.run()