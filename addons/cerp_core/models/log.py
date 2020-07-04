# -*- coding: utf-8 -*-

from odoo import models, fields


class CloudERPLog(models.Model):
    _name = 'cerp_core.log'
    _description = 'Cloud ERP log'

    log_type = fields.Selection(
        [('info', 'INFO'),
         ('warn', 'WARN'),
         ('error', 'ERROR')],
        default='info',
        required=True)
    message = fields.Char()
