# -*- coding: utf-8 -*-

from odoo import models, fields


class CloudERPMetric(models.Model):
    _name = 'cerp_core.metric'
    _description = 'Cloud metric'

    time_start = fields.Datetime(required=True)
    time_end = fields.Datetime(required=True)
    metric_type = fields.Many2one(
        'cerp_core.metric.type',
        required=True)
    value = fields.Float(required=True)

    _sql_constraints = [
        ('metric_start_end_unique',
         'unique(metric_type, time_start, time_end)',
         'No duplicate metrics')]


class CloudERPMetricType(models.Model):
    _name = 'cerp_core.metric.type'
    _description = 'Cloud metric type'

    name = fields.Char(required=True)

    provider = fields.Many2one(
        'cerp_core.account_provider',
        required=True)


class CloudERPMetricset(models.Model):
    _name = 'cerp_core.metricset'
    _description = 'Cloud metricset'

    name = fields.Char(required=True)

    accounts = fields.Many2many(
        'cerp_core.account',
        'accounts_metricsets_rel',
        'cerp_core_metricset_id',
        'cerp_core_account_id',
        string='Accounts')

    provider = fields.Many2one(
        'cerp_core.account_provider',
        required=True)
