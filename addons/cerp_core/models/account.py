# -*- coding: utf-8 -*-

import logging

from odoo import api, exceptions, fields, models

from ..utils import cerp_log


_logger = logging.getLogger(__name__)


class CloudERPAccount(models.Model):
    _inherits = {'keychain2.account': 'keychain2'}
    _name = 'cerp_core.account'
    _description = 'Cloud ERP account'

    name = fields.Char()

    keychain2 = fields.Many2one(
        'keychain2.account',
        ondelete='cascade',
        required=True)

    # provider
    provider = fields.Many2one(
        'cerp_core.account_provider',
        required=True)
    provider_name = fields.Char(
        'Provider name',
        related='provider.name')
    provider_module = fields.Char(
        'Provider module',
        related='provider.module_name')
    provider_icon = fields.Char(
        'Provider icon',
        related='provider.module_icon')
    provider_type = fields.Selection(
        'Provider type',
        related='provider.module_type')

    _sql_constraints = [
        ('provider_unique',
         'unique(provider, name)',
         'Only one account per provider')]

    @api.model
    def create(self, vals):
        res = super(CloudERPAccount, self).create(vals)
        cerp_log(self.env, '[%s] account created' % 'acc name')
        return res

    def write(self, vals):
        res = super(CloudERPAccount, self).write(vals)
        cerp_log(
            self.env,
            ('[%s] account updated'
             % self.provider.module.name))
        return res

    def _update(self, rec):
        try:
            update = getattr(
                rec.keychain2,
                '%s_update' % rec.keychain2.namespace)(
                    rec.keychain2._parse_credentials(
                        rec.keychain2.get_credentials()))
        except exceptions.Warning as warn:
            message = '[%s] Update failed: %s' % (
                rec.provider.module.name, str(warn))
            cerp_log(
                self.env,
                message,
                log_type="warn",
                commit=True)
            raise warn
        print(update)
        message = '[%s] Update successful' % (
            rec.provider.module.name)
        cerp_log(
            self.env,
            message)

    def button_update(self):
        return self._update(self)

    @api.model
    def cron_update(self):
        _logger.warn("RUNNING CRON UPDATE")
        for rec in self.search([]):
            _logger.warn("RUNNING CRON UPDATE FOR RECORD: %s" % rec)
            try:
                self._update(rec)
            except exceptions.Warning as warn:
                _logger.warn("Update failed for %s: %s" % (rec, warn))


def cerp_account_factory(key_namespace, short_name, Model, Adapter):

    class BaseCloudERPAccount(Model):
        __name__ = "%sCloudERPAccount" % short_name

        namespace = fields.Selection(
            selection_add=[
                (key_namespace, short_name)])

    def _update(self, credentials):
        Adapter(self).update(credentials)

    setattr(
        BaseCloudERPAccount,
        "%s_validate_credentials" % key_namespace,
        Adapter.validate_credentials)
    setattr(
        BaseCloudERPAccount,
        "%s_update" % key_namespace,
        _update)
    return BaseCloudERPAccount
