import json

with open('ans.json', 'r', encoding='utf-8') as file:
    data = json.load(file)  # Load JSON data into a Python dictionary



def gunc(req):
    return data[req]