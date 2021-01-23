from abc import ABC, abstractmethod
import requests
import json
import pdb

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

  def __init__(self, call_count=None, version=None, field=None, ids=None, page=1, pagesize=100, order=None, sort=None, min=None, max=None, tag=None, site=_SITE, filter=None):
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
    
    if self.call_count:
      data = {"items": []}
      self.max=None
      for i in range(self.call_count):
        print(self.generate_api_call_string())
        parsed_data = requests.get(self.generate_api_call_string()).json()
        data["items"] = data["items"] + parsed_data["items"]
        self.max = data["items"][-1]["score"]

      pass
    else:
      print(self.generate_api_call_string())
      data = requests.get(self.generate_api_call_string()).json()
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
