# -*- coding: utf-8 -*-

import logging

import requests

from odoo import api, exceptions, models, fields, _

try:
    from odoo.addons.base.module.module import assert_log_admin_access
except ImportError:
    from odoo.addons.base.models.ir_module import assert_log_admin_access

from .. import utils
from ..constants import VERSIONS_URL


_logger = logging.getLogger(__name__)


class CloudERPModule(models.Model):
    _inherit = 'ir.module.module'

    cerp_providers = fields.One2many(
        'cerp_core.account_provider',
        'module')
    cerp_is_visible = fields.Boolean(
        compute='compute_cerp_is_visible',
        search='_cerp_is_visible_search')
    cerp_can_upgrade = fields.Boolean(
        compute='compute_cerp_can_upgrade',
        search='_cerp_can_upgrade_search')
    cerp_can_immediate_upgrade = fields.Boolean(
        compute='compute_cerp_can_immediate_upgrade',
        search='_cerp_can_immediate_upgrade_search')
    cerp_provider = fields.Many2one(
        'cerp_core.account_provider',
        compute='compute_cerp_provider',
        search='search_cerp_provider',
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

    def _cerp_is_visible_search(self, operator, value):
        _search = [
            ('name', '=like', 'cerp_%'),
            ('name', 'not in', ['cerp_basic', 'cerp_core', 'cerp_pro'])]
        recs = self.search(_search).filtered(
            lambda x: x.cerp_is_visible is True)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    def _cerp_can_upgrade_search(self, operator, value):
        _search = [
            ('name', '=like', 'cerp_%'),
            ('name', 'not in', ['cerp_basic', 'cerp_core', 'cerp_pro']),
            ('sequence', '>', '100')]
        recs = self.search(_search)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    def _cerp_can_immediate_upgrade_search(self, operator, value):
        _search = [
            ('name', '=like', 'cerp_%'),
            ('name', 'not in', ['cerp_basic', 'cerp_core', 'cerp_pro']),
            ('sequence', '<=', '100'),
            ('state', '!=', 'installed')]
        recs = self.search(_search)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    @api.depends()
    def compute_cerp_can_immediate_upgrade(self):
        _search = [
            ('name', '=like', 'cerp_%'),
            ('name', 'not in', ['cerp_basic', 'cerp_core', 'cerp_pro']),
            ('sequence', '>', '100'),
            ('state', '=', 'installed')]
        basic_modules = [x.name.split('_')[1] for x in self.search(_search)]
        for rec in self:
            cerp_type = rec.name.split('_')[1]
            rec.cerp_can_immediate_upgrade = (
                rec.sequence <= 100
                and cerp_type in basic_modules
                and rec.state != "installed")

    @api.depends()
    def compute_cerp_can_upgrade(self):
        for rec in self:
            rec.cerp_can_upgrade = rec.sequence > 100

    @api.depends()
    def compute_cerp_is_visible(self):
        _records = {}
        for rec in self:
            cerp_type = rec.name.split('_')[1]
            name, sequence = _records.get(cerp_type, (None, None))
            if name is None or (sequence > rec.sequence):
                _records[cerp_type] = (rec.name, rec.sequence)
        visible = [x[0] for x in _records.values()]
        for rec in self:
            rec.cerp_is_visible = rec.name in visible

    @api.depends('cerp_providers')
    def compute_cerp_provider(self):
        for rec in self:
            if len(rec.cerp_providers) > 0:
                rec.cerp_provider = rec.cerp_providers[0]
            else:
                rec.cerp_provider = None

    def cerp_provider_inverse(self):
        if len(self.cerp_providers) > 0:
            # provider.module cannot be empty and so module.cerp_provider
            # cannot be changed
            raise exceptions.Warning(
                'Cloud ERP provider (%s) is already associated '
                'with this module (%s), and cannot be empty. Not '
                'setting provider (%s)'
                % (self.cerp_providers[0].name,
                   self.name,
                   self.cerp_provider.name))
        self.cerp_provider.module = self

    def search_cerp_provider(self, operator, value):
        # not sure at all if this is correct
        return [('id', operator, value)]

    def button_cerp_install(self):
        self.button_immediate_install()
        return self.button_configure_cerp_account()

    @assert_log_admin_access
    def button_cerp_uninstall_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': _('Uninstall Cloud ERP module'),
            'view_mode': 'form',
            'res_model': 'cerp_core.module.uninstall',
            'context': {'default_module_id': self.id}}

    def button_configure_cerp_account(self):
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
            target='new',
            context=context)
        if provider.account:
            context.update(
                dict(form_view_initial_mode='edit',
                     force_detailed_view='true'))
            form['res_id'] = provider.account.id
        return form

    def cerp_update_module_versions(self):
        versions = requests.get(VERSIONS_URL).json()
        for addon, versions in versions.items():
            print(addon)
        return utils.success_action(
            self.env,
            _("Module versions updated"))
