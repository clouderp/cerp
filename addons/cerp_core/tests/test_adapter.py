# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from odoo.addons.cerp_core import adapter, records

from .test_base import TestCloudERPBase


class TestCloudERPAdapter(TestCloudERPBase):

    def test_constructor(self):
        keychain = MagicMock()
        _adapter = adapter.Adapter(keychain)
        assert _adapter.keychain == keychain
        assert _adapter.collector == records.RecordCollector
        assert (
            list(keychain.env.__getitem__.call_args)
            == [('cerp_core.account',), {}])
        assert (
            list(keychain.env.__getitem__.return_value.search.call_args)
            == [([('keychain2', '=', keychain.id)],), {}])
        assert (
            _adapter.account
            == keychain.env.__getitem__.return_value.search.return_value)
        assert (
            _adapter.metricsets
            == _adapter.account.metricsets)

    def test_validate_credentials(self):
        error = None
        validation = None
        try:
            validation = adapter.Adapter.validate_credentials('CREDENTIALS')
        except NotImplementedError as e:
            error = e
        assert error
        assert validation is None

    def test_fetch(self):
        keychain = MagicMock()
        error = None
        validation = None
        try:
            validation = adapter.Adapter(keychain).fetch('CREDENTIALS')
        except NotImplementedError as e:
            error = e
        assert error
        assert validation is None

    def test_collect(self):
        keychain = MagicMock()
        records = MagicMock()
        with self._patch('adapter.Adapter.collector') as collect_mock:
            collected = adapter.Adapter(keychain).collect(records)
        assert collected == collect_mock.return_value
        assert (
            list(collect_mock.call_args)
            == [(keychain.env.__getitem__.return_value.search.return_value,
                 records), {}])
