# -*- coding: utf-8 -*-

from psycopg2 import IntegrityError

from odoo import exceptions, tools

from ._base import TestCloudERPModels


class TestCloudERPModuleModel(TestCloudERPModels):

    def setUp(self):
        super(TestCloudERPModuleModel, self).setUp()

    def test_module_provider(self):
        module = self.env['ir.module.module'].search([])[0]
        assert not module.cerp_provider
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        assert module.cerp_provider == provider
        assert module.cerp_provider_name == provider.module_name
        assert module.cerp_provider_type == provider.module_type
        assert module.cerp_provider_account is False
        assert (
            provider.module
            == module.cerp_provider.module
            == module)

    def test_module_provider_update(self):
        module = self.env['ir.module.module'].search([])[0]
        module2 = self.env['ir.module.module'].search([])[1]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        module2.cerp_provider = provider
        assert module2.cerp_provider_name == provider.module_name
        assert module2.cerp_provider_type == provider.module_type
        assert module2.cerp_provider_account is False
        assert (
            provider.module
            == module2.cerp_provider.module
            == module2)
        assert not module.cerp_provider

    def test_module_provider_remove_module(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        assert provider.exists()
        module.unlink()
        assert not provider.exists()

    def test_module_provider_update_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        module2 = self.env['ir.module.module'].search([])[1]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        module2.cerp_provider = provider
        assert provider.module == module2
        assert not module.cerp_provider
        provider2 = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER 2',
             'key_namespace': 'provider2',
             'module': module.id})
        error = None
        try:
            module2.cerp_provider = provider2
        except exceptions.Warning as e:
            error = e
        assert error
        module2.invalidate_cache()
        assert module2.cerp_provider == provider
        assert module.cerp_provider == provider2

    def test_module_provider_remove_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        error = None
        try:
            module.cerp_provider = None
        except exceptions.Warning as e:
            error = e
        assert error
        module.invalidate_cache()
        assert module.cerp_provider == provider
        assert provider.module == module

    def test_module_provider_unique_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        result = None
        error = None
        try:
            with tools.mute_logger('odoo.sql_db'), self.env.cr.savepoint():
                result = self.env['cerp_core.account_provider'].create(
                    {'name': 'PROVIDER 2',
                     'key_namespace': 'provider',
                     'module': module.id})
        except IntegrityError as e:
            error = e
        assert not result
        assert error
