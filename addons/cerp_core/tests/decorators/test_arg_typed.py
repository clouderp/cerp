# -*- coding: utf-8 -*-

from odoo.addons.cerp_core.decorators import arg

from ._base import (
    _onerror,
    ArgumentException,
    argument_mock,
    TestCloudERPDecorators)


class ArgumentativeType(object):

    @arg.typed(str)
    def _fun_str(self, string):
        argument_mock("RECEIVED: %s" % string)
        return True

    @arg.typed(str, onerror=_onerror)
    def _fun_str_error(self, string):
        argument_mock("RECEIVED: %s" % string)
        return True

    @arg.typed(list)
    def _fun_list(self, _list):
        argument_mock("RECEIVED: %s" % _list)
        return True

    @arg.typed(list, onerror=_onerror)
    def _fun_list_error(self, _list):
        argument_mock("RECEIVED: %s" % _list)
        return True


class TestCloudERPTypedDecorator(TestCloudERPDecorators):
    _argument_class = ArgumentativeType

    def test_typed_str(self):
        assert self._argumentative._fun_str('STRING')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: STRING',), {}])

    def test_typed_str_fail(self):
        assert not self._argumentative._fun_str(['SOMELIST'])
        assert not argument_mock.called

    def test_typed_str_error(self):
        assert self._argumentative._fun_str_error('STRING')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: STRING',), {}])

    def test_typed_str_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_str_error(['SOMELIST'])
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_str_error)
        assert error.arg == ['SOMELIST']
        assert error.spec == str
        assert not result
        assert not argument_mock.called

    def test_typed_list(self):
        assert self._argumentative._fun_list(['SOMELIST'])
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: [\'SOMELIST\']',), {}])

    def test_typed_list_fail(self):
        assert not self._argumentative._fun_list('STRING')
        assert not argument_mock.called

    def test_typed_list_error(self):
        assert self._argumentative._fun_list_error(
            ['SOMELIST'])
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: [\'SOMELIST\']',), {}])

    def test_typed_list_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_list_error('STRING')
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_list_error)
        assert error.arg == 'STRING'
        assert error.spec == list
        assert not result
        assert not argument_mock.called
