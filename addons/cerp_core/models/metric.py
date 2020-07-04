# -*- coding: utf-8 -*-

from odoo import models, fields


class CloudERPMetric(models.Model):
    _name = 'cerp_core.metric'
    _description = 'Cloud metric'

    start = fields.Datetime()
    end = fields.Datetime()
    type = fields.Many2one(
        'cerp_core.metric.type',
        required=True)
    value = fields.Float()


class CloudERPMetricType(models.Model):
    _name = 'cerp_core.metric.type'
    _description = 'Cloud metric type'

    name = fields.Char()
    scope = fields.Char()
