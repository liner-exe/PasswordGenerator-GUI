import json, os

class Response:
    def __init__(self, directory, locale):
       self.directory = directory
       self.locale = locale

    def load(self):
        data = {}
        for file in os.listdir(self.directory):
           if file.endswith(".json") and file.startswith(self.locale):
              with open(f"{self.directory}/{file}", encoding="utf-8") as f:
                   data = json.load(f)
        
        return data
    
    def get(self, key):
       data = self.load()
       return data[key]