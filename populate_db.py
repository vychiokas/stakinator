
from controller.api_parser import StackExchange_API
from controller.db_manager import DatabaseManager
from model.data_model import Question, Comment
import pdb

class PopulateQuestionTable():
  def __init__(self):
    self.parsed_json = None
    self.dbm = DatabaseManager()
    
  def set_parser(self):
    self.api_parser = StackExchange_API(version=StackExchange_API._VERSION,
      field="questions",
      order="desc",
      min="20",
      sort="votes",
      tag="python",
      filter="!6xGkKBjMFEsggJ0Seh_gbSMiC14SlZXz_9YMfl8U1BjmaL(r_SVCy0thQO3JMdBOa-7Fj")
    

  def run(self):
    self.set_parser()
    self.parsed_json = self.api_parser.get_data()
    for item in self.parsed_json["items"]:
      id = item["question_id"]
      body = item["title"]
      question = Question(id=id, body=body)
      self.dbm.session.add(question)
    self.dbm.session.commit()


class PopulateCommentTable():
  def __init__(self):
    self.dbm = DatabaseManager()
    self.parsed_json = None
    self.question_ids = None

  def set_parser(self):
    self.api_parser = StackExchange_API(version=StackExchange_API._VERSION,
      field="questions/{ids}/answers",
      ids=self.question_ids,
      order="desc",
      min="20",
      sort="votes",
      tag="python",
      filter="!9_bDE(S2a")

  def run(self):
    self._get_question_ids()
    self.set_parser()
    self.parsed_json = self.api_parser.get_data()
    for id in self.question_ids:
      answers = [answer for answer in self.parsed_json["items"] if answer["question_id"] == id]
      sorted_answers = sorted(answers, key=lambda k: k["score"], reverse=True)
      for item in sorted_answers[:5]:
        self.dbm.session.add(Comment(question_id=id, body=item["body_markdown"]))
    self.dbm.session.commit()

  def _get_question_ids(self):
    all_questions = self.dbm.session.query(Question).all()
    self.question_ids = [question.id for question in all_questions]


    
if __name__ == "__main__":
  popq = PopulateQuestionTable()
  popq.run()
  popc = PopulateCommentTable()
  popc.run()