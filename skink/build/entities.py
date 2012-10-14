# -*- coding: utf-8 -*-


class Config(object):

    @classmethod
    def create_from_file(cls, file_path):
        open(file_path)
        return cls()
