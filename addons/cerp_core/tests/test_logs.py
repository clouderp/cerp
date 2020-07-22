# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from odoo.addons.cerp_core import logs

from .test_base import TestCloudERPBase


class TestCloudERPLogs(TestCloudERPBase):

    def test_cerp_log(self):
        env = MagicMock()

        logs.cerp_log(env, 'MODULE_NAME', 'MESSAGE')

        assert (
            list(env.__getitem__.call_args)
            == [('cerp_core.log',), {}])
        assert (
            list(env.__getitem__.return_value.create.call_args)
            == [({'message': 'MESSAGE',
                  'module_name': 'MODULE_NAME',
                  'log_type': 'info'},), {}])
        assert not env.cr.commit.called

    def test_cerp_log_not_info(self):
        env = MagicMock()

        logs.cerp_log(env, 'MODULE_NAME', 'MESSAGE', log_type='NOTINFO')

        assert (
            list(env.__getitem__.call_args)
            == [('cerp_core.log',), {}])
        assert (
            list(env.__getitem__.return_value.create.call_args)
            == [({'message': 'MESSAGE',
                  'module_name': 'MODULE_NAME',
                  'log_type': 'NOTINFO'},), {}])
        assert not env.cr.commit.called

    def test_cerp_log_commit(self):
        env = MagicMock()

        logs.cerp_log(env, 'MODULE_NAME', 'MESSAGE', commit=True)

        assert (
            list(env.__getitem__.call_args)
            == [('cerp_core.log',), {}])
        assert (
            list(env.__getitem__.return_value.create.call_args)
            == [({'message': 'MESSAGE',
                  'module_name': 'MODULE_NAME',
                  'log_type': 'info'},), {}])
        assert (
            list(env.cr.commit.call_args)
            == [(), {}])
