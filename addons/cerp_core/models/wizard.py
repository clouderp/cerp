# -*- coding: utf-8 -*-

from odoo import models, fields


class MessageWizard(models.TransientModel):
    _name = 'cerp_core.message.wizard'

    message = fields.Text('Message', required=True)

    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}
