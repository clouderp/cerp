# -*- coding: utf-8 -*-

import logging

from odoo import api, exceptions, fields, models

from .. import (
    exceptions as cerp_exceptions,
    logs, records, typing)


_logger = logging.getLogger(__name__)


class CloudERPAccount(models.Model):
    _inherits = {'keychain2.account': 'keychain2'}
    _name = 'cerp_core.account'
    _description = 'Cloud ERP account'

    name = fields.Char(
        required=True,
        default='default')

    keychain2 = fields.Many2one(
        'keychain2.account',
        ondelete='cascade',
        required=True)

    # provider
    provider = fields.Many2one(
        'cerp_core.account_provider',
        required=True,
        ondelete='cascade')
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

    # metrics
    metricsets = fields.Many2many(
        'cerp_core.metricset',
        'accounts_metricsets_rel',
        'cerp_core_account_id',
        'cerp_core_metricset_id',
        string='Metricsets')

    _sql_constraints = [
        ('provider_unique',
         'unique(provider, name)',
         'Only one account per provider')]

    @api.model
    def create(self, vals):
        res = super(CloudERPAccount, self).create(vals)
        res.metricsets = res.provider.metricsets
        logs.cerp_log(
            self.env,
            res.provider.module.name,
            'Account \'%s\' created'
            % res.name)
        return res

    def write(self, vals):
        res = super(CloudERPAccount, self).write(vals)
        logs.cerp_log(
            self.env,
            self.provider.module.name,
            'Account \'%s\' updated'
            % self.name)
        return res

    def unlink(self):
        recs = [
            (rec.provider.module.name, rec.name)
            for rec
            in self]
        res = super(CloudERPAccount, self).unlink()
        for module_name, name in recs:
            logs.cerp_log(
                self.env,
                module_name,
                'Account \'%s\' removed'
                % name)
        return res

    def cerp_account_save(self):
        self.env.cr.commit()
        return {
            'type': 'ir.actions.act_window',
            'target': 'self',
            'view_mode': 'kanban',
            'res_model': 'cerp_core.account'}

    def button_update(self):
        return self._cerp_update(self)

    @api.model
    def cron_update(self):
        return
        for rec in self.search([]):
            self._cerp_update(rec)

    def _cerp_adapter(self, rec):
        return getattr(
            rec.keychain2,
            '%s_fetch' % rec.keychain2.namespace)

    def _cerp_credentials(self, rec):
        return rec.keychain2._parse_credentials(
            rec.keychain2.get_credentials())

    # rec: models.Model
    # -> records.RecordCollector
    def _cerp_fetch(self, rec):
        return self._cerp_adapter(rec)(
            self._cerp_credentials(rec))

    # rec: models.Model
    # -> None or Error
    def _cerp_update(self, rec):
        try:
            records = self._cerp_fetch(rec)
        except exceptions.Warning as warn:
            _logger.warn(
                "Fetch failed for %s: %s" % (rec, warn))
            logs.cerp_log(
                self.env,
                rec.provider.module.name,
                'Fetch failed: %s' % str(warn),
                log_type="warn",
                commit=True)
            raise warn
        else:
            try:
                records.save()
            except exceptions.Warning as warn:
                _logger.warn(
                    "Update failed for %s: %s" % (rec, warn))
                logs.cerp_log(
                    self.env,
                    rec.provider.module.name,
                    'Update failed: %s' % str(warn),
                    log_type="warn",
                    commit=True)
                raise warn
            else:
                logs.cerp_log(
                    self.env,
                    rec.provider.module.name,
                    'Fetch successful')


def cerp_account_factory(
        key_namespace: str,
        short_name: str,
        Model: typing.OdooModelType,
        Adapter: typing.AdapterType) -> typing.OdooModelType:

    class BaseCloudERPAccount(Model):
        namespace = fields.Selection(
            selection_add=[
                (key_namespace, short_name)])

    def _fetch(self, credentials) -> records.RecordCollector:
        result = Adapter(self).fetch(credentials)
        try:
            assert isinstance(result, records.RecordCollector)
        except AssertionError:
            raise cerp_exceptions.CloudERPFetchException(
                'CloudERPAdapter.fetch must return a '
                'cerp_core.records.RecordCollector object')
        else:
            return result

    @classmethod
    def _validate(self, credentials) -> bool:
        if not Adapter.validate_credentials(credentials):
            if Adapter.validate_credentials.__doc__:
                raise exceptions.Warning(
                    "Invalid credentials: %s"
                    % Adapter.validate_credentials.__doc__)
            return False
        return True

    setattr(
        BaseCloudERPAccount,
        "%s_validate_credentials" % key_namespace,
        _validate)
    setattr(
        BaseCloudERPAccount,
        "%s_fetch" % key_namespace,
        _fetch)
    setattr(
        BaseCloudERPAccount,
        '__name__',
        "%sCloudERPAccount" % short_name)
    return BaseCloudERPAccount
