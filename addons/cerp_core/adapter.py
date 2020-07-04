# -*- coding: utf-8 -*-


class Adapter(object):

    def __init__(self, model):
        self.model = model

    @classmethod
    def validate_credentials(cls, data):
        raise NotImplementedError

    def update(self, credentials):
        raise NotImplementedError
