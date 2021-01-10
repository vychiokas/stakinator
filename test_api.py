from stackapi import StackAPI
import json
import requests


SITE = StackAPI('stackoverflow')
SITE.page_size = 2
SITE.max_pages = 2

questions = requests.get('https://api.stackexchange.com/2.2/questions?order=desc&min=10000&sort=votes&tagged=python&site=stackoverflow&filter=!*SU8CGYZitCB.D*(BDVIfh2KKqQ)7jqYCBJzAPqv1FF5P6ymFq8a9Bc8edtQc*PqJ)28g05P')
questions = questions.json()

good_answers = []
print(json.dumps(questions, indent=4, sort_keys=True))

for item in questions["items"]:
    answers = item["answers"]
    newlist = sorted(answers, key=lambda k: k["score"], reverse=True) 

print("good answers")
print(json.dumps(newlist[0], indent=4, sort_keys=True))

