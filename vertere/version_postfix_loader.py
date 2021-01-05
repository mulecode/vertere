import json
import os


class VersionPostfixLoader(object):
    def __init__(self):
        self.postfix_config_location = 'data/postfix_config.json'
        self.loaded_postfixes_data = []
        self.__load_postfix_configuration__()

    def __load_postfix_configuration__(self):
        root = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(root, self.postfix_config_location)
        with open(filename) as json_file:
            self.loaded_postfixes_data = json.load(json_file)

    def get_all_postfix_configuration(self):
        return self.loaded_postfixes_data
