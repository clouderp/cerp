# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from psycopg2 import IntegrityError

from odoo import exceptions, fields, models, tools

from odoo.addons.cerp_core import (
    adapter, exceptions as cerp_exceptions, records)
from odoo.addons.cerp_core.models.account import (
    cerp_account_factory)
from ._base import TestCloudERPModels


adapter_mock = MagicMock()
account_mock = MagicMock()
records_mock = MagicMock()


class DummyException(Exception):
    pass


class DummyCloudERPAccount(models.Model):
    _inherit = 'keychain2.account'


class DummyCloudERPAdapter(adapter.Adapter):

    def __init__(self, model):
        adapter_mock(model)

    @classmethod
    def validate_credentials(self, credentials):
        return account_mock(credentials)

    def fetch(self, credentials):
        return records_mock(credentials)


class DummyCloudERPAdapterWithDocs(DummyCloudERPAdapter):

    @classmethod
    def validate_credentials(self, credentials):
        """ Validation docs
        """
        return account_mock(credentials)


class TestCloudERPAccountProviderModel(TestCloudERPModels):

    def test_account_create(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        with self._patch('models.account.logs.cerp_log') as log_mock:
            account = self.env['cerp_core.account'].create(
                {'provider': provider.id,
                 'namespace': provider.key_namespace})
        assert (
            list(log_mock.call_args)
            == [(self.env,
                 provider.module.name,
                 'Account \'default\' created'),
                {}])
        assert account.name == 'default'
        assert account.provider == provider
        assert account.provider_name == account.provider.name
        assert account.provider_icon == account.provider.module_icon
        assert account.provider_type == account.provider.module_type

    def test_account_create_multi_provider(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        for x in range(5):
            self.env['cerp_core.account'].create(
                {'provider': provider.id,
                 'name': 'provider-%s' % x,
                 'namespace': provider.key_namespace})

    def test_account_create_many(self):
        modules = self.env['ir.module.module'].search([])
        for x in range(5):
            provider = self.env['cerp_core.account_provider'].create(
                {'name': 'PROVIDER%s' % x,
                 'key_namespace': 'provider-%s' % x,
                 'module': modules[x].id})
            self.env['keychain2.account']._fields[
                'namespace'].selection.append(
                    ('provider-%s' % x, 'Test provider namespace'))
            self.env['cerp_core.account'].create(
                {'provider': provider.id,
                 'namespace': provider.key_namespace})

    def test_account_update(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        account = self.env['cerp_core.account'].create(
            {'provider': provider.id,
             'namespace': provider.key_namespace})
        with self._patch('models.account.logs.cerp_log') as log_mock:
            account.write({'name': 'other'})
        assert account.name == 'other'
        assert (
            list(log_mock.call_args)
            == [(self.env,
                 provider.module.name,
                 'Account \'other\' updated'),
                {}])

    def test_account_update_provider(self):
        module = self.env['ir.module.module'].search([])[0]
        module2 = self.env['ir.module.module'].search([])[2]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        provider2 = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER2',
             'key_namespace': 'provider2',
             'module': module2.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider2', 'Test provider namespace'))
        account = self.env['cerp_core.account'].create(
            {'provider': provider.id,
             'namespace': provider.key_namespace})
        account.write({'provider': provider2.id})
        assert account.provider == provider2
        assert provider2.account == account

    def test_account_delete(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        account = self.env['cerp_core.account'].create(
            {'provider': provider.id,
             'namespace': provider.key_namespace})
        # should probs log account removal
        account.unlink()
        assert not account.exists()
        assert provider.exists()

    def test_account_create_unique_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        self.env['cerp_core.account'].create(
            {'provider': provider.id,
             'namespace': provider.key_namespace})
        error = None
        result = None
        try:
            with tools.mute_logger('odoo.sql_db'), self.env.cr.savepoint():
                result = self.env['cerp_core.account'].create(
                    {'provider': provider.id,
                     'namespace': provider.key_namespace})
        except IntegrityError as e:
            error = e
        assert not result
        assert error

    def test_account_cerp_fetch(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        account = self.env['cerp_core.account'].create(
            {'provider': provider.id,
             'namespace': provider.key_namespace})
        rec = MagicMock()
        rec.keychain2.namespace = 'NAMESPACE'
        rec.keychain2.get_credentials.return_value = '*CREDENTIALS*'
        rec.keychain2._parse_credentials.return_value = 'CREDENTIALS'
        with self._patch('models.account.getattr') as getattr_mock:
            getattr_mock.return_value.return_value = 'FETCHED'
            result = account._cerp_fetch(rec)
        assert (
            list(getattr_mock.call_args)
            == [(rec.keychain2,
                 "NAMESPACE_fetch"),
                {}])
        assert rec.keychain2.get_credentials.called
        assert (
            list(rec.keychain2._parse_credentials.call_args)
            == [('*CREDENTIALS*',), {}])
        assert (
            list(getattr_mock.return_value.call_args)
            == [('CREDENTIALS',), {}])
        assert result == 'FETCHED'

    def test_account_cerp_update(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        account = self.env['cerp_core.account'].create(
            {'provider': provider.id,
             'namespace': provider.key_namespace})
        rec = MagicMock()

        _clog_mock = self._patch('models.account.logs')
        _logger_mock = self._patch('models.account._logger')
        _fetch_mock = self._patch('models.account.CloudERPAccount._cerp_fetch')

        with _clog_mock as clog_mock:
            with _logger_mock as logger_mock:
                with _fetch_mock as fetch_mock:
                    account._cerp_update(rec)

        assert (
            list(fetch_mock.call_args)
            == [(rec,), {}])
        assert (
            list(fetch_mock.return_value.save.call_args)
            == [(), {}])
        assert not logger_mock.called
        assert (
            list(clog_mock.cerp_log.call_args)
            == [(self.env,
                 rec.provider.module.name,
                 'Fetch successful'),
                {}])

    def test_account_cerp_update_fetch_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        account = self.env['cerp_core.account'].create(
            {'provider': provider.id,
             'namespace': provider.key_namespace})
        rec = MagicMock()

        _clog_mock = self._patch('models.account.logs')
        _logger_mock = self._patch('models.account._logger')
        _fetch_mock = self._patch('models.account.CloudERPAccount._cerp_fetch')

        def _fetch_error(rec):
            raise exceptions.Warning('SOMETHING WENT WRONG')

        error = None

        with _clog_mock as clog_mock:
            with _logger_mock as logger_mock:
                with _fetch_mock as fetch_mock:
                    fetch_mock.side_effect = _fetch_error
                    try:
                        account._cerp_update(rec)
                    except exceptions.Warning as e:
                        error = e
        assert str(error) == "('SOMETHING WENT WRONG', '')"
        assert (
            list(logger_mock.warn.call_args)
            == [("Fetch failed for %s: ('SOMETHING WENT WRONG', '')" % rec,),
                {}])
        assert (
            list(clog_mock.cerp_log.call_args)
            == [(self.env,
                 rec.provider.module.name,
                 "Fetch failed: ('SOMETHING WENT WRONG', '')"),
                {'log_type': 'warn', 'commit': True}])
        assert not fetch_mock.return_value.save.called

    def test_account_cerp_update_save_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        self.env['keychain2.account']._fields['namespace'].selection.append(
            ('provider', 'Test provider namespace'))
        account = self.env['cerp_core.account'].create(
            {'provider': provider.id,
             'namespace': provider.key_namespace})
        rec = MagicMock()

        _clog_mock = self._patch('models.account.logs')
        _logger_mock = self._patch('models.account._logger')
        _fetch_mock = self._patch('models.account.CloudERPAccount._cerp_fetch')

        def _save_error():
            raise exceptions.Warning('SOMETHING ELSE WENT WRONG')

        error = None

        with _clog_mock as clog_mock:
            with _logger_mock as logger_mock:
                with _fetch_mock as fetch_mock:
                    fetch_mock.return_value.save.side_effect = _save_error
                    try:
                        account._cerp_update(rec)
                    except exceptions.Warning as e:
                        error = e
        assert str(error) == "('SOMETHING ELSE WENT WRONG', '')"
        assert (
            list(logger_mock.warn.call_args)
            == [("Update failed for %s: ('SOMETHING ELSE WENT WRONG', '')"
                 % rec,),
                {}])
        assert (
            list(clog_mock.cerp_log.call_args)
            == [(self.env,
                 rec.provider.module.name,
                 "Update failed: ('SOMETHING ELSE WENT WRONG', '')"),
                {'log_type': 'warn', 'commit': True}])


class TestCloudERPAccountFactory(TestCloudERPModels):

    def setUp(self):
        super(TestCloudERPAccountFactory, self).setUp()
        # using return_value, side_effect kwargs with reset_mock
        # doesnt work in all python versions
        account_mock.reset_mock()
        account_mock.side_effect = None
        adapter_mock.reset_mock()
        adapter_mock.side_effect = None
        records_mock.reset_mock()
        records_mock.side_effect = None

    @property
    def _account_model(self):
        return cerp_account_factory(
            'keyname',
            'SHORTNAME',
            DummyCloudERPAccount,
            DummyCloudERPAdapter)

    @property
    def _account_model_with_validation_docs(self):
        return cerp_account_factory(
            'keyname',
            'SHORTNAME',
            DummyCloudERPAccount,
            DummyCloudERPAdapterWithDocs)

    def test_account_factory(self):
        account_model = self._account_model
        assert issubclass(account_model, DummyCloudERPAccount)
        assert (
            account_model.__name__
            == 'SHORTNAMECloudERPAccount')

    def test_account_factory_namespace(self):
        with self._patch('models.account.fields') as field_mock:
            field_mock.return_value = fields.Selection(
                selection_add=[
                    ('foo', 'Bar')])
            self._account_model
        assert (
            list(field_mock.Selection.call_args)
            == [(),
                {'selection_add': [
                    ('keyname', 'SHORTNAME')]}])

    def test_account_factory_validator(self):
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is True)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_true(self):
        account_mock.return_value = True
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is True)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_int(self):
        account_mock.return_value = 23
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is True)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_str(self):
        account_mock.return_value = 'asdfa ☠ m;aoidjfpi'
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is True)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_false(self):
        account_mock.return_value = False
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is False)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_false_doc(self):
        account_mock.return_value = False
        account_model = self._account_model_with_validation_docs
        result = None
        error = None
        try:
            result = account_model.keyname_validate_credentials('CREDENTIALS')
        except exceptions.Warning as e:
            error = e
        assert not result
        assert (
            error.args[0]
            == 'Invalid credentials:  Validation docs\n        ')
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_none(self):
        account_mock.return_value = None
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is False)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_zero(self):
        account_mock.return_value = None
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is False)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_empty_str(self):
        account_mock.return_value = ''
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is False)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_empty_list(self):
        account_mock.return_value = []
        account_model = self._account_model
        assert (
            account_model.keyname_validate_credentials('CREDENTIALS')
            is False)
        assert not adapter_mock.called
        assert (
            list(account_mock.call_args)
            == [('CREDENTIALS',), {}])

    def test_account_factory_validator_fail(self):
        # no error handling
        # this might want to handle eg ValidationError
        account_mock.side_effect = DummyException('test')
        result = None
        error = None
        try:
            result = self._account_model.keyname_validate_credentials(
                'CREDENTIALS')
        except DummyException as e:
            error = e
        assert not adapter_mock.called
        assert result is None
        assert error

    def test_account_factory_fetch(self):
        _account = self._account_model
        recordset = records.RecordCollector(_account)
        records_mock.return_value = recordset
        assert (
            _account.keyname_fetch('SELF', 'CREDENTIALS')
            is recordset)
        assert (
            list(records_mock.call_args)
            == [('CREDENTIALS',), {}])
        assert (
            list(adapter_mock.call_args)
            == [('SELF',), {}])

    def test_account_factory_fetch_str_fail(self):
        records_mock.return_value = ''
        result = None
        error = None
        try:
            result = self._account_model.keyname_fetch('SELF', 'CREDENTIALS')
        except cerp_exceptions.CloudERPFetchException as e:
            error = e
        assert result is None
        assert error
        assert (
            list(records_mock.call_args)
            == [('CREDENTIALS',), {}])
        assert (
            list(adapter_mock.call_args)
            == [('SELF',), {}])

    def test_account_factory_fetch_none_fail(self):
        records_mock.return_value = None
        result = None
        error = None
        try:
            result = self._account_model.keyname_fetch('SELF', 'CREDENTIALS')
        except cerp_exceptions.CloudERPFetchException as e:
            error = e
        assert result is None
        assert error
        assert (
            list(records_mock.call_args)
            == [('CREDENTIALS',), {}])
        assert (
            list(adapter_mock.call_args)
            == [('SELF',), {}])
