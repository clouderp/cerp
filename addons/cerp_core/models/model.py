# -*- coding: utf-8 -*-

import logging

from odoo import api, models, fields


_logger = logging.getLogger(__name__)


class CloudERPModel(models.Model):
    _inherit = 'ir.model'

    cerp_module_count = fields.Integer(
        compute='_cerp_compute_count',
        string="Document count (Incl. Archived)",
        help="Total number of records in this model")

    def _cerp_compute_rec_count_for_module(self, module, rec):
        one2one_modules = [
            'cerp_core.account_provider',
            'keychain2.account']

        if rec.model in one2one_modules:
            return 1
        elif rec.model == 'cerp_core.account':
            return len(module.cerp_provider.accounts)
        elif rec.model == 'cerp_core.metric.type':
            return len(module.cerp_provider.metric_types)
        elif rec.model == 'cerp_core.metricset':
            return len(module.cerp_provider.metricsets)
        elif rec.model == 'cerp_core.metric':
            # surely this can be done with ORM ?
            if not module.cerp_provider.metric_types.ids:
                return 0
            self.env.cr.execute(
                'SELECT COUNT(*) FROM "%s" '
                'WHERE "metric_type" IN (%s)'
                % (self.env[rec.model]._table,
                   ','.join(
                       str(id)
                       for id
                       in module.cerp_provider.metric_types.ids)))
            return self.env.cr.fetchone()[0]

    @api.depends()
    def _cerp_compute_count(self):
        active_module = (
            self.env['ir.module.module'].search(
                [('id', '=', self._context['active_id'])])
            if self._context.get('active_model') == 'ir.module.module'
            else None)

        for rec in self:
            rec.cerp_module_count = (
                self._cerp_compute_rec_count_for_module(active_module, rec)
                if active_module
                else 0)
