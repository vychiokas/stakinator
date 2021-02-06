from abc import ABC, abstractmethod
import requests
import json
import pdb
from stakinator.utils.logger import LOG
# from utils.singleton import SingletonMeta

class Source(ABC):

  @abstractmethod
  def get_data(self):
    pass


class StackExchange_API(Source):

  _VERSION = 2.2
  _STACK_EXCHANGE_URL = "https://api.stackexchange.com/"
  _FIELD = "questions"
  _ORDER = "desc&min=10000"
  _SORT = "votes"
  _TAGGED = "python"
  _SITE = "stackoverflow"
  _FILTER = "!*SU8CGYZitCB.D*(BDVIfh2KKqQ)7jqYCBJzAPqv1FF5P6ymFq8a9Bc8edtQc*PqJ)28g05P"
  _NUM_CALLED = 0
  _REMAINING_CALLS = None

  def __init__(self, call_count=1, version=None, field=None, ids=None, page=1, pagesize=100, order=None, sort=None, min=None, max=None, tag=None, site=_SITE, filter=None):
    self.version = version
    self.field = field
    self.ids = ids
    self.page = page
    self.pagesize = pagesize
    self.order = order
    self.sort = sort
    self.min = min
    self.max = max
    self.tag = tag
    self.site = site
    self.filter = filter
    self.data = None
    self.call_count = call_count


  def generate_api_call_string(self):
    api_call_string = f"{StackExchange_API._STACK_EXCHANGE_URL}{self.version}/"

    if self.field:
      api_call_string = api_call_string + f"{self.field}?"
    
    if self.ids:
      api_call_string = api_call_string.replace('{ids}', ";".join(map(str, self.ids))) 

    if self.page:
      api_call_string = api_call_string + f"page={self.page}"

    if self.pagesize:
      api_call_string = api_call_string + f"&pagesize={self.pagesize}"

    if self.order:
      api_call_string = api_call_string + f"&order={self.order}"

    if self.min:
      api_call_string = api_call_string + f"&min={self.min}"

    if self.max:
      api_call_string = api_call_string + f"&max={self.max}"

    if self.sort:
      api_call_string = api_call_string + f"&sort={self.sort}"

    if self.tag:
      api_call_string = api_call_string + f"&tagged={self.tag}"

    api_call_string = api_call_string + f"&site={StackExchange_API._SITE}"

    if self.filter:
      api_call_string = api_call_string + f"&filter={self.filter}"

    return api_call_string

  def get_data(self):
    LOG.info(f"Calling API: {self.call_count} times.")
    if self.call_count > 1:
      data = {"items": []}
      self.max=None
      for i in range(self.call_count):
        LOG.info(f"Calling an API with: \n {self.generate_api_call_string()}")
        parsed_data = requests.get(self.generate_api_call_string()).json()
        StackExchange_API._NUM_CALLED+= 1
        LOG.info(f"API now called {StackExchange_API._NUM_CALLED} times")
        StackExchange_API._REMAINING_CALLS = parsed_data["quota_remaining"]
        LOG.info(f"API calls left: {StackExchange_API._REMAINING_CALLS}")
        data["items"] = data["items"] + parsed_data["items"]
        self.max = data["items"][-1]["score"]

      pass
    else:
      LOG.info(f"Calling an API with: \n {self.generate_api_call_string()}")
      data = requests.get(self.generate_api_call_string()).json()
      StackExchange_API._NUM_CALLED+= 1
      LOG.info(f"API now called {StackExchange_API._NUM_CALLED} times")
      StackExchange_API._REMAINING_CALLS = data["quota_remaining"]
      LOG.info(f"API calls left: {StackExchange_API._REMAINING_CALLS}")
    return data


if __name__ == "__main__":
  api = StackExchange_API(version=StackExchange_API._VERSION, field="questions", order="desc", min="20", sort="votes", tag="python", filter="!*SU8CGYZitCB.D*(BDVIfh2KKqQ)7jqYCBJzAPqv1FF5P6ymFq8a9Bc8edtQc*PqJ)28g05P" )
  questions = api.get_data()
  for item in questions["items"]:

      answers = item["answers"]
      newlist = sorted(answers, key=lambda k: k["score"], reverse=True)
      print(json.dumps(newlist[0], indent=4, sort_keys=True))
      print(f"question id:{item['question_id']}")

      print("good answers")
      print(json.dumps(newlist[0], indent=4, sort_keys=True))
