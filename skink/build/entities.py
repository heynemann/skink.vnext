# -*- coding: utf-8 -*-
import yaml


class Config(object):

    @classmethod
    def create_from_file(cls, file_path):
        stream = file(file_path, 'r')
        config_data = yaml.load(stream)
        return cls(config_data)

    def __init__(self, config_data):
        self.__dict__ = config_data
