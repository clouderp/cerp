# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from ..test_base import TestCloudERPBase


argument_mock = MagicMock()


class ArgumentException(Exception):

    def __init__(self, obj, fun, arg, spec):
        self.obj = obj
        self.fun = fun
        self.arg = arg
        self.spec = spec


def _onerror(obj, fun, arg, spec):
    raise ArgumentException(obj, fun, arg, spec)


class TestCloudERPDecorators(TestCloudERPBase):

    def setUp(self):
        super(TestCloudERPDecorators, self).setUp()
        argument_mock.reset_mock()

    @property
    def _argumentative(self):
        return self._argument_class()
