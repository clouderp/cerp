# -*- coding: utf-8 -*-

import importlib
import os
from unittest.mock import patch

from odoo.tests.common import SavepointCase

from odoo.addons.cerp_core import records


class TestCloudERPAdapter(SavepointCase):

    @classmethod
    def setUpClass(cls):
        assert cls.addon
        super(TestCloudERPAdapter, cls).setUpClass()

    def _get_manifest(self):
        return importlib.import_module(
            'odoo.addons.%s.__manifest__' % self.addon)

    @property
    def path(self):
        return os.path.dirname(self._get_manifest().__file__)

    def _import(self, dottedname):
        return getattr(
            importlib.import_module(
                '.'.join(
                    ["odoo.addons", self.addon]
                    + dottedname.split(".")[:-1])),
            dottedname.split(".")[-1])

    def _patch(self, path):
        return patch(
            'odoo.addons.%s.%s'
            % (self.addon, path))

    def _test_validator(self):
        Adapter = self._import('adapter.CloudERPAdapter')
        valid_credentials = self._import(
            'tests._credentials.VALID_CREDENTIALS')

        for credential in valid_credentials:
            Adapter.validate_credentials(credential)

    def _test_manifest(self):
        pass

    def _test_icon(self):
        assert os.path.exists(
            os.path.join(
                self.path,
                'static', 'description', 'icon.png'))

    def _test_model(self):
        Account = self._import('models.models.CloudERPAccount')
        constants = self._import('constants')
        keychain_account = self.env['keychain2.account']

        assert Account._inherit == 'keychain2.account'
        assert not Account._name

        with self._patch('adapter.CloudERPAdapter.fetch') as fetch_mock:
            _records = records.RecordCollector(Account)
            fetch_mock.return_value = _records
            fetch = getattr(
                keychain_account,
                '%s_fetch'
                % constants.KEY_NAMESPACE)
            assert fetch("CREDENTIALS") is _records
        assert (
            list(fetch_mock.call_args)
            == [('CREDENTIALS',), {}])

        validate_fun = 'adapter.CloudERPAdapter.validate_credentials'
        assert validate_fun.__doc__
        with self._patch(validate_fun) as validate_mock:
            validate = getattr(
                keychain_account,
                '%s_validate_credentials'
                % constants.KEY_NAMESPACE)
            validate(['abc', 'xyz'])
        assert (
            list(validate_mock.call_args)
            == [(['abc', 'xyz'],), {}])

        # key_namespace, short_name have been added to to account.namespaces
        # might need to make this more robust, so test passes even if other
        # addons are installed
        assert (
            keychain_account.fields_get()['namespace']['selection']
            == [(constants.KEY_NAMESPACE,
                 constants.SHORT_NAME)])
