import json
import os


class VersionPostfixLoader(object):
    def __init__(self):
        self.postfix_config_location = 'data/postfix_config.json'
        self.loaded_postfixes_data = []
        self.__load_postfix_configuration__()

    def get_all_postfix_configuration(self):
        return self.configured_postfixes

    def __load_postfix_configuration__(self):
        root = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(root, self.postfix_config_location)
        with open(filename) as json_file:
            data = json.load(json_file)
            self.configured_postfixes = self.__parse_postfix_config_list__(data)

    def __parse_postfix_config_list__(self, value) -> list['PostfixConfig']:
        postfix_list = []
        for p in value:
            config_parsed = self.__parse_postfix_config_item__(p)
            postfix_list.append(config_parsed)
        return postfix_list

    def __parse_postfix_config_item__(self, value) -> 'PostfixConfig':
        postfix_config = PostfixConfig()
        postfix_config.name = value['name']
        postfix_config.weight = int(value['weight'])
        postfix_config.with_seq = bool(value['with_seq'])
        postfix_config.promotable = bool(value['promotable'])
        return postfix_config


class PostfixConfig(object):
    def __init__(self):
        self.name = ''
        self.weight = 1
        self.with_seq = False
        self.promotable = False

    def __str__(self):
        return f'<name: {self.name}, ' \
               f'weight: {self.weight}, ' \
               f'with_seq: {self.with_seq}, ' \
               f'promotable: {self.promotable}>'
