import json
from accessify import protected
import random

class InitJsonError(Exception):
    pass

class Config:
    def __init__(self, config_path: str):
        if '.json' in config_path:
            self.config_path = config_path
        else:
            self.config_path = str(config_path) + '.json'

        self.indent = 2

    @protected
    def InitJsonFile(self) -> dict:
        try:
            with open(self.config_path, "r") as read_file:
                data = json.load(read_file)

                return data
        except Exception as E:
            data = {}

            return data

    def add(self, name: str, value: any) -> bool:
       json_data = self.InitJsonFile()
       json_data[name] = value

       with open(self.config_path, 'w') as json_file:
           json.dump(json_data, json_file, indent = self.indent)


    def get(self, name: any = None) -> dict or any:
        json_data = self.InitJsonFile()

        if name == None:
            return dict(json_data)

        else:
            return json_data[name]

    def change(self, name: str, value: any) -> bool:
        json_data = self.InitJsonFile()

        if json_data[name]:
            json_data[name] = value

            with open(self.config_path, 'w') as json_file:
                json.dump(json_data, json_file, indent = self.indent)

            return True
        else:
            return False

    def create_copy(self, name: str = None) -> bool:

        if name == None:
            name = str(self.config_path).split('.json')[0] + '-copy.json'

        json_data = self.InitJsonFile()

        if json_data:

            with open(name, 'w') as new_json_file:
                json.dump(json_data, new_json_file, indent = self.indent)

                return True

        else:
            return False


