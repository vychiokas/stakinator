
from controller.api_parser import StackExchange_API
from controller.db_manager import DatabaseManager
from model.data_model import Question, Answer, User
import pdb
from abc import ABC, abstractmethod
import itertools

class PopulateTable(ABC):
  def __init__(self, number_of_api_calls=1):
    self.parsed_json = None
    self.dbm = DatabaseManager()
    self.number_of_api_calls = number_of_api_calls

  @abstractmethod
  def set_parser(self):
    pass
  
  @abstractmethod
  def run(self):
    pass
    # This should be the same accross the populating tables and be idealy implemented only here

  def get_ids(self, objects: []):

    all_objects = [self.dbm.session.query(obj).all() for obj in objects]
    all_objects = list(itertools.chain.from_iterable(all_objects))
    self.all_ids = [obj.id for obj in all_objects]
    

  def split_ids_list(self):
    split_ids = []
    for i in range(0, len(self.all_ids), 100):
      split_ids.append(self.all_ids[i:i + 100])
    self.split_ids = split_ids


class PopulateQuestionTable(PopulateTable):
  def __init__(self, number_of_api_calls=1):
    self.parsed_json = None
    self.dbm = DatabaseManager()
    self.number_of_api_calls = number_of_api_calls
    
  def set_parser(self, max=None):
    self.api_parser = StackExchange_API(version=StackExchange_API._VERSION,
      field="questions",
      order="desc",
      max=max,
      sort="votes",
      tag="python",
      filter="!UHY-aKsFJ(KvceZ5uauvPwwy.a_xVc99f6yM6Cw3XPBvGHk55s6M7(efaRV3-MUnHxM)DANPIL")
    

  def run(self):
    max=None
    for i in range(self.number_of_api_calls):
      self.set_parser(max=max)
      self.parsed_json = self.api_parser.get_data()
      for item in self.parsed_json["items"]:

        
        try:
          id = item["question_id"]
          title = item["title"]
          body = item["body_markdown"]
          tags = item["tags"]
          user_id = item["owner"]["user_id"]
          question = Question(id=id, title=title, body=body, tags=tags, user_id=user_id)
          self.dbm.session.add(question)
          self.dbm.session.commit()
        except:
          pass
      max = item["score"]


class PopulateAnswerTable(PopulateTable):
  def __init__(self):
    self.dbm = DatabaseManager()
    self.parsed_json = None
    self.question_ids = None

  def set_parser(self, ids):
    self.api_parser = StackExchange_API(version=StackExchange_API._VERSION,
      field="questions/{ids}/answers",
      ids=ids,
      order="desc",
      sort="votes",
      tag="python",
      filter="!9_bDE(S2a")

  def run(self):
    self.get_ids([Question])
    self.split_ids_list()

    for ids in self.split_ids:
      self.set_parser(ids)
      self.parsed_json = self.api_parser.get_data()

      for id in ids:
        answers = [answer for answer in self.parsed_json["items"] if answer["question_id"] == id]
        sorted_answers = sorted(answers, key=lambda k: k["score"], reverse=True)
        for item in sorted_answers[:5]:
          try:
            self.dbm.session.add(Answer(question_id=id, body=item["body_markdown"], user_id=item["owner"]["user_id"]))
            self.dbm.session.commit()
          except:
            pass



class PopulateUserTable(PopulateTable):
  def __init__(self):
    self.dbm = DatabaseManager()
    self.parsed_json = None
    self.user_ids = None

  def set_parser(self, ids):
    self.api_parser = StackExchange_API(version=StackExchange_API._VERSION,
      field="users/{ids}",
      ids=ids,
      order="desc",
      sort="reputation",
      filter="default")

  def run(self):
    self.get_ids([Question, Answer])
    self.split_ids_list()

    for ids in self.split_ids:
      self.set_parser(ids)
      self.parsed_json = self.api_parser.get_data()
      for id in ids:
        for item in self.parsed_json["items"]:
          if item["user_id"] == id:
            try:
              display_name = item["display_name"]
              self.dbm.session.add(User(id=id, display_name=display_name))
              self.dbm.session.commit()
            except:
              pass

  def get_ids(self, objects: []):

    all_objects = [self.dbm.session.query(obj).all() for obj in objects]
    all_objects = list(itertools.chain.from_iterable(all_objects))
    self.all_ids = [obj.user_id for obj in all_objects]


if __name__ == "__main__":
  popq = PopulateQuestionTable(number_of_api_calls=2)
  popq.run()
  popc = PopulateAnswerTable()
  popc.run()
  popu = PopulateUserTable()
  popu.run()
  