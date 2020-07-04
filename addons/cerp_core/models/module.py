# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class CloudERPModule(models.Model):
    _inherit = 'ir.module.module'

    cerp_providers = fields.One2many(
        'cerp_core.account_provider',
        'module')
    cerp_provider = fields.Many2one(
        'cerp_core.account_provider',
        compute='compute_cerp_provider',
        inverse='cerp_provider_inverse')
    cerp_provider_name = fields.Char(
        'Provider name',
        related='cerp_provider.module_name')
    cerp_provider_type = fields.Selection(
        'Provider type',
        related='cerp_provider.module_type')
    cerp_provider_account = fields.Char(
        'Account name',
        related='cerp_provider.account_name')

    @api.depends('cerp_providers')
    def compute_cerp_provider(self):
        for rec in self:
            if len(rec.cerp_providers) > 0:
                rec.cerp_provider = rec.cerp_providers[0]
            else:
                rec.cerp_provider = None

    def cerp_provider_inverse(self):
        if len(self.cerp_providers) > 0:
            cerp_provider = self.env['cerp_core.account_provider'].browse(
                self.cerp_providers[0].id)
            cerp_provider.module = False
        self.cerp_provider.module = self

    def button_configure_account(self):
        provider = self.env['cerp_core.account_provider'].search(
            [('module', '=', self.id)])
        context = dict(
            default_namespace=provider.key_namespace,
            default_provider=provider.id,
            default_name="default")
        form = dict(
            type='ir.actions.act_window',
            view_mode='form',
            view_type='form',
            res_model='cerp_core.account',
            target='self',
            context=context)
        if provider.account:
            context.update(
                dict(form_view_initial_mode='edit',
                     force_detailed_view='true'))
            form['res_id'] = provider.account.id
        return form
