# -*- coding: utf-8 -*-
import yaml


class Config(object):

    @classmethod
    def create_from_file(cls, file_path):
        stream = file(file_path, 'r')
        yaml.load(stream)
        return cls()
