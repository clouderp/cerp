# -*- coding: utf-8 -*-

from odoo.addons.cerp_core.decorators import arg

from ._base import (
    _onerror,
    ArgumentException,
    argument_mock,
    TestCloudERPDecorators)


class ArgumentativeContains(object):

    @arg.contains('NEEDLE')
    def _fun_needle(self, string):
        argument_mock("RECEIVED: %s" % string)
        return True

    @arg.contains('NEEDLE', onerror=_onerror)
    def _fun_needle_error(self, string):
        argument_mock("RECEIVED: %s" % string)
        return True

    @arg.contains(['NEEDLE_1', 'NEEDLE_2'])
    def _fun_needles(self, _list):
        argument_mock("RECEIVED: %s" % _list)
        return True

    @arg.contains(['NEEDLE_1', 'NEEDLE_2'], onerror=_onerror)
    def _fun_needles_error(self, _list):
        argument_mock("RECEIVED: %s" % _list)
        return True

    @arg.contains(('NEEDLE_1', 'NEEDLE_2'))
    def _fun_tuples(self, _list):
        argument_mock("RECEIVED: %s" % _list)
        return True

    @arg.contains(('NEEDLE_1', 'NEEDLE_2'), onerror=_onerror)
    def _fun_tuples_error(self, _list):
        argument_mock("RECEIVED: %s" % _list)
        return True


class TestCloudERPContainsDecorator(TestCloudERPDecorators):
    _argument_class = ArgumentativeContains

    def test_contains_str(self):
        assert self._argumentative._fun_needle('NEEDLE')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: NEEDLE',), {}])

    def test_contains_str_fail(self):
        assert not self._argumentative._fun_needle('NOODLES')
        assert not argument_mock.called

    def test_contains_str_error(self):
        assert self._argumentative._fun_needle_error('NEEDLE')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: NEEDLE',), {}])

    def test_contains_str_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_needle_error('NOODLES')
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_needle_error)
        assert error.arg == 'NOODLES'
        assert error.spec == 'NEEDLE'
        assert not result
        assert not argument_mock.called

    def test_contains_longer_str(self):
        assert self._argumentative._fun_needle(
            'SOME TEXT CONTAINING NEEDLE AND THREAD')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: SOME TEXT CONTAINING NEEDLE AND THREAD',),
                {}])

    def test_contains_str_in_list(self):
        assert self._argumentative._fun_needle(
            ['THREAD', 'NEEDLE', 'THIMBLE'])
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: [\'THREAD\', \'NEEDLE\', \'THIMBLE\']',),
                {}])

    def test_contains_str_not_in_list(self):
        assert not self._argumentative._fun_needle(
            ['THREAD', 'NOODLES', 'THIMBLE'])
        assert not argument_mock.called

    def test_contains_needles_str(self):
        assert self._argumentative._fun_needles(
            'NEEDLE_1 *AND* NEEDLE_2')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: NEEDLE_1 *AND* NEEDLE_2',), {}])

    def test_contains_not_needles_str(self):
        assert not self._argumentative._fun_needles('ONLY NEEDLE_1')
        assert not argument_mock.called

    def test_contains_needles_str_error(self):
        assert self._argumentative._fun_needles_error(
            'NEEDLE_1 *AND* NEEDLE_2')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: NEEDLE_1 *AND* NEEDLE_2',), {}])

    def test_contains_not_needles_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_needles_error('ONLY NEEDLE_1')
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_needles_error)
        assert error.arg == 'ONLY NEEDLE_1'
        assert error.spec == ['NEEDLE_1', 'NEEDLE_2']
        assert not result
        assert not argument_mock.called

    def test_contains_needles_str_in_list(self):
        assert self._argumentative._fun_needles(
            ['THREAD', 'NEEDLE_1', 'NEEDLE_2', 'THIMBLE'])
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: '
                 '[\'THREAD\', \'NEEDLE_1\', \'NEEDLE_2\', \'THIMBLE\']',),
                {}])

    def test_contains_not_needles_str_in_list(self):
        assert not self._argumentative._fun_needles(
            ['THREAD', 'NEEDLE_1', 'NOODLES', 'THIMBLE'])
        assert not argument_mock.called

    def test_contains_tuples_str(self):
        assert self._argumentative._fun_tuples(
            'NEEDLE_1 *AND* NEEDLE_2')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: NEEDLE_1 *AND* NEEDLE_2',), {}])

    def test_contains_not_tuples_str(self):
        assert not self._argumentative._fun_tuples('ONLY NEEDLE_1')
        assert not argument_mock.called

    def test_contains_tuples_str_error(self):
        assert self._argumentative._fun_tuples_error(
            'NEEDLE_1 *AND* NEEDLE_2')
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: NEEDLE_1 *AND* NEEDLE_2',), {}])

    def test_contains_not_tuples_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_tuples_error('ONLY NEEDLE_1')
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_tuples_error)
        assert error.arg == 'ONLY NEEDLE_1'
        assert error.spec == ('NEEDLE_1', 'NEEDLE_2')
        assert not result
        assert not argument_mock.called

    def test_contains_tuples_str_in_list(self):
        assert self._argumentative._fun_tuples(
            ['THREAD', 'NEEDLE_1', 'NEEDLE_2', 'THIMBLE'])
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: '
                 '[\'THREAD\', \'NEEDLE_1\', \'NEEDLE_2\', \'THIMBLE\']',),
                {}])

    def test_contains_not_tuples_str_in_list(self):
        assert not self._argumentative._fun_tuples(
            ['THREAD', 'NEEDLE_1', 'NOODLES', 'THIMBLE'])
        assert not argument_mock.called
