
from controller.api_parser import StackExchange_API
from controller.db_manager import DatabaseManager
from model.data_model import Question, Answer, User
import pdb
from abc import ABC, abstractmethod
import itertools
from utils.logger import LOG

class PopulateTable(ABC):
  def __init__(self):
    self.parsed_json = None
    self.dbm = DatabaseManager()

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
  def __init__(self):
    super().__init__()
    
  def set_parser(self):
    self.api_parser = StackExchange_API(version=StackExchange_API._VERSION,
      call_count = 2,
      field="questions",
      order="desc",
      max=max,
      sort="votes",
      tag="python",
      filter="!UHY-aKsFJ(KvceZ5uauvPwwy.a_xVc99f6yM6Cw3XPBvGHk55s6M7(efaRV3-MUnHxM)DANPIL")
    

  def run(self):
    LOG.info(f"Fetching answers from API")
    self.set_parser()
    self.parsed_json = self.api_parser.get_data()
    count_success = 0
    count_fail = 0
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
        LOG.info(f"Question Added: id: {id}")
        count_success+= 1
      except Exception as e:
        LOG.warning(f"An error occured inserting question id: {id} With Error: \n {e}")
        self.dbm.session.rollback()
        count_fail+= 1
    LOG.info(f"Successfully added {count_success} questions to database")
    LOG.info(f"Issues Occured with {count_fail} questions")

class PopulateAnswerTable(PopulateTable):
  def __init__(self):
    super().__init__()
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
    LOG.info(f"Fetching answers from API")
    self.get_ids([Question])
    self.split_ids_list()
    count_success = 0
    count_fail = 0
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
            count_success+=1
            LOG.info(f"Answer Added: id: {id}")
          except Exception as e:
            LOG.warning(f"An error occured inserting answer id: {id} With Error: \n {e}")
            self.dbm.session.rollback()
            count_fail+= 1
    LOG.info(f"Successfully added {count_success} answers to database")
    LOG.info(f"Issues Occured with {count_fail} answers")


class PopulateUserTable(PopulateTable):
  def __init__(self):
    super().__init__()
    self.user_ids = None

  def set_parser(self, ids):
    self.api_parser = StackExchange_API(version=StackExchange_API._VERSION,
      field="users/{ids}",
      ids=ids,
      order="desc",
      sort="reputation",
      filter="default")

  def run(self):
    LOG.info(f"Fetching Users from API")
    self.get_ids([Question, Answer])
    self.split_ids_list()
    count_success = 0
    count_fail = 0
    for ids in self.split_ids:
      self.set_parser(ids)
      self.parsed_json = self.api_parser.get_data()
      for id in ids:
        for item in self.parsed_json["items"]:
          # pdb.set_trace()
          if item["user_id"] == id:
            try:
              self.dbm.session.add(User(id=item["user_id"], display_name=item["display_name"]))
              self.dbm.session.commit()
              count_success+= 1
              LOG.info(f"User Added: id: {id}")
            except Exception as e:
              self.dbm.session.rollback()
              LOG.warning(f"An error occured inserting user id: {id} With Error: \n {e}")
              count_fail+=1
            break
            
    LOG.info(f"Successfully added {count_success} users to database")
    LOG.info(f"Issues Occured with {count_fail} users")

  def get_ids(self, objects: []):

    all_objects = [self.dbm.session.query(obj).all() for obj in objects]
    all_objects = list(itertools.chain.from_iterable(all_objects))
    self.all_ids = [obj.user_id for obj in all_objects]
    self.all_ids = list(set(self.all_ids))

if __name__ == "__main__":

  popq = PopulateQuestionTable()
  popq.run()
  popc = PopulateAnswerTable()
  popc.run()
  popu = PopulateUserTable()
  popu.run()
  