# -*- coding: utf-8 -*-

from odoo.addons.cerp_core.decorators import arg

from ._base import (
    _onerror,
    argument_mock,
    ArgumentException,
    TestCloudERPDecorators)


class ArgumentativeLength(object):

    # int
    @arg.length(23)
    def _fun_int(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    @arg.length(23, onerror=_onerror)
    def _fun_int_error(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    # str
    @arg.length('23')
    def _fun_str(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    @arg.length('23', onerror=_onerror)
    def _fun_str_error(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    # gt
    @arg.length('> 23')
    def _fun_gt(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    @arg.length('> 23', onerror=_onerror)
    def _fun_gt_error(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    # lt
    @arg.length('< 23')
    def _fun_lt(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    @arg.length('< 23', onerror=_onerror)
    def _fun_lt_error(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    # lte
    @arg.length('<= 23')
    def _fun_lte(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    @arg.length('<= 23', onerror=_onerror)
    def _fun_lte_error(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    # gte
    @arg.length('>= 23')
    def _fun_gte(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True

    @arg.length('>= 23', onerror=_onerror)
    def _fun_gte_error(self, arg):
        argument_mock("RECEIVED: %s" % arg)
        return True


class TestCloudERPLengthDecorator(TestCloudERPDecorators):
    _argument_class = ArgumentativeLength

    # int
    def test_length_int(self):
        assert self._argumentative._fun_int('x' * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 23),), {}])

    def test_length_int_list(self):
        assert self._argumentative._fun_int(['x'] * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 23),), {}])

    def test_length_int_error(self):
        assert self._argumentative._fun_int_error('x' * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 23),), {}])

    def test_length_int_list_error(self):
        assert self._argumentative._fun_int_error(['x'] * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 23),), {}])

    def test_length_int_fail(self):
        assert not self._argumentative._fun_int('x' * 22)
        assert not argument_mock.called

    def test_length_int_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_int_error('x' * 22)
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_int_error)
        assert error.arg == 'x' * 22
        assert error.spec == 23
        assert not result
        assert not argument_mock.called

    # str
    def test_length_str(self):
        assert self._argumentative._fun_str('x' * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 23),), {}])

    def test_length_str_list(self):
        assert self._argumentative._fun_str(['x'] * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 23),), {}])

    def test_length_str_error(self):
        assert self._argumentative._fun_str_error('x' * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 23),), {}])

    def test_length_str_list_error(self):
        assert self._argumentative._fun_str(['x'] * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 23),), {}])

    def test_length_str_fail(self):
        assert not self._argumentative._fun_str('x' * 22)
        assert not argument_mock.called

    def test_length_str_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_str_error('x' * 22)
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_str_error)
        assert error.arg == 'x' * 22
        assert error.spec == 23
        assert not result
        assert not argument_mock.called

    # gt
    def test_length_gt(self):
        assert self._argumentative._fun_gt('x' * 24)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 24),), {}])

    def test_length_gt_list(self):
        assert self._argumentative._fun_gt(['x'] * 24)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 24),), {}])

    def test_length_gt_error(self):
        assert self._argumentative._fun_gt_error('x' * 24)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 24),), {}])

    def test_length_gt_list_error(self):
        assert self._argumentative._fun_gt(['x'] * 24)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 24),), {}])

    def test_length_gt_fail(self):
        assert not self._argumentative._fun_gt('x' * 23)
        assert not argument_mock.called

    def test_length_gt_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_gt_error('x' * 23)
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_gt_error)
        assert error.arg == 'x' * 23
        assert error.spec == '> 23'
        assert not result
        assert not argument_mock.called

    # gte
    def test_length_gte(self):
        assert self._argumentative._fun_gte('x' * 24)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 24),), {}])

    def test_length_gte_equal(self):
        assert self._argumentative._fun_gte('x' * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 23),), {}])

    def test_length_gte_list(self):
        assert self._argumentative._fun_gte(['x'] * 24)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 24),), {}])

    def test_length_gte_list_equal(self):
        assert self._argumentative._fun_gte(['x'] * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 23),), {}])

    def test_length_gte_error(self):
        assert self._argumentative._fun_gte_error('x' * 24)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 24),), {}])

    def test_length_gte_list_error(self):
        assert self._argumentative._fun_gte(['x'] * 24)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 24),), {}])

    def test_length_gte_fail(self):
        assert not self._argumentative._fun_gte('x' * 22)
        assert not argument_mock.called

    def test_length_gte_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_gte_error('x' * 22)
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_gte_error)
        assert error.arg == 'x' * 22
        assert error.spec == '>= 23'
        assert not result
        assert not argument_mock.called

    # lt
    def test_length_lt(self):
        assert self._argumentative._fun_lt('x' * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 22),), {}])

    def test_length_lt_list(self):
        assert self._argumentative._fun_lt(['x'] * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 22),), {}])

    def test_length_lt_error(self):
        assert self._argumentative._fun_lt_error('x' * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 22),), {}])

    def test_length_lt_list_error(self):
        assert self._argumentative._fun_lt(['x'] * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 22),), {}])

    def test_length_lt_fail(self):
        assert not self._argumentative._fun_lt('x' * 23)
        assert not argument_mock.called

    def test_length_lt_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_lt_error('x' * 23)
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_lt_error)
        assert error.arg == 'x' * 23
        assert error.spec == '< 23'
        assert not result
        assert not argument_mock.called

    # lte
    def test_length_lte(self):
        assert self._argumentative._fun_lte('x' * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 22),), {}])

    def test_length_lte_equal(self):
        assert self._argumentative._fun_lte('x' * 23)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 23),), {}])

    def test_length_lte_list(self):
        assert self._argumentative._fun_lte(['x'] * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 22),), {}])

    def test_length_lte_list_equal(self):
        assert self._argumentative._fun_lte(['x'] * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 22),), {}])

    def test_length_lte_error(self):
        assert self._argumentative._fun_lte_error('x' * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % ('x' * 22),), {}])

    def test_length_lte_list_error(self):
        assert self._argumentative._fun_lte(['x'] * 22)
        assert (
            list(argument_mock.call_args)
            == [('RECEIVED: %s' % (['x'] * 22),), {}])

    def test_length_lte_fail(self):
        assert not self._argumentative._fun_lte('x' * 24)
        assert not argument_mock.called

    def test_length_lte_fail_error(self):
        error = None
        result = None
        argumentative = self._argumentative
        try:
            result = argumentative._fun_lte_error('x' * 24)
        except ArgumentException as e:
            error = e
        assert error.obj is argumentative
        assert (
            getattr(error.obj, error.fun.__name__)
            == argumentative._fun_lte_error)
        assert error.arg == 'x' * 24
        assert error.spec == '<= 23'
        assert not result
        assert not argument_mock.called
