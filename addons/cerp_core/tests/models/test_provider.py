# -*- coding: utf-8 -*-

from psycopg2 import IntegrityError

from odoo import tools

from ._base import TestCloudERPModels


class TestCloudERPProviderModel(TestCloudERPModels):

    def setUp(self):
        super(TestCloudERPProviderModel, self).setUp()

    def test_provider(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        assert module.cerp_provider == provider
        assert provider.module == module
        assert (
            provider.module_name
            == module.shortdesc)
        assert (
            provider.module_icon
            == module.icon)
        assert provider.module_type == 'basic'
        assert not provider.account.exists()
        assert not provider.account_name

    def test_provider_update_module(self):
        module = self.env['ir.module.module'].search([])[0]
        module2 = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        provider.module = module2
        assert module2.cerp_provider == provider

    def test_provider_remove(self):
        module = self.env['ir.module.module'].search([])[0]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        assert module.cerp_provider
        provider.unlink()
        assert not module.cerp_provider

    def test_provider_no_module(self):
        result = None
        error = None
        try:
            with tools.mute_logger('odoo.sql_db'), self.env.cr.savepoint():
                result = self.env['cerp_core.account_provider'].create(
                    {'name': 'PROVIDER',
                     'key_namespace': 'provider'})
        except IntegrityError as e:
            error = e
        assert not result
        assert error

    def test_provider_no_name_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        result = None
        error = None
        try:
            with tools.mute_logger('odoo.sql_db'), self.env.cr.savepoint():
                result = self.env['cerp_core.account_provider'].create(
                    {'key_namespace': 'provider',
                     'module': module.id})
        except IntegrityError as e:
            error = e
        assert not result
        assert error

    def test_provider_no_key_namespace_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        result = None
        error = None
        try:
            with tools.mute_logger('odoo.sql_db'), self.env.cr.savepoint():
                result = self.env['cerp_core.account_provider'].create(
                    {'name': 'PROVIDER',
                     'module': module.id})
        except IntegrityError as e:
            error = e
        assert not result
        assert error

    def test_provider_update_module_fail(self):
        module = self.env['ir.module.module'].search([])[0]
        module2 = self.env['ir.module.module'].search([])[1]
        provider = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER',
             'key_namespace': 'provider',
             'module': module.id})
        provider2 = self.env['cerp_core.account_provider'].create(
            {'name': 'PROVIDER 2',
             'key_namespace': 'provider2',
             'module': module2.id})
        error = None
        try:
            with tools.mute_logger('odoo.sql_db'), self.env.cr.savepoint():
                provider.write(dict(module=module2.id))
        except IntegrityError as e:
            error = e
        assert error
        # not sure how best to test this
        assert provider.module == module
        assert provider2.module == module2
        provider.invalidate_cache()
        provider2.invalidate_cache()
        assert provider.module == module
        assert provider2.module == module2
