# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class CloudERPAccountProvider(models.Model):
    _name = 'cerp_core.account_provider'
    _description = 'Cloud account provider'
    name = fields.Char(required=True)
    key_namespace = fields.Char(required=True)
    accounts = fields.One2many(
        'cerp_core.account',
        'provider')
    account = fields.Many2one(
        'cerp_core.account',
        compute='compute_account',
        inverse='account_inverse',
        search='search_account')
    account_name = fields.Char(
        'Account name',
        related='account.name')

    metricsets = fields.One2many(
        'cerp_core.metricset',
        'provider')
    metric_types = fields.One2many(
        'cerp_core.metric.type',
        'provider')

    module = fields.Many2one(
        'ir.module.module',
        string="CloudERP account provider module",
        required=True,
        ondelete='cascade')
    module_name = fields.Char(
        'Module name',
        related='module.shortdesc')
    module_icon = fields.Char(
        'Module icon',
        related='module.icon')
    module_type = fields.Selection(
        [('basic', 'Basic'),
         ('pro', 'Pro')],
        default='basic')

    _sql_constraints = [
        ('module_unique',
         'unique(module)',
         'Only one module per provider')]

    @api.depends('accounts')
    def compute_account(self):
        for rec in self:
            if len(rec.accounts) > 0:
                rec.account = rec.accounts[0]
            else:
                rec.account = None

    def account_inverse(self):
        if len(self.accounts) > 0:
            account = self.env['ir.account.account'].browse(
                self.accounts[0].id)
            account.cerp_provider = False
        self.account.provider = self

    def search_account(self, operator, value):
        # not sure at all if this is correct
        return [('id', operator, value)]

    def unlink(self):
        # todo: unlink keychain account
        res = super(CloudERPAccountProvider, self).unlink()
        return res
