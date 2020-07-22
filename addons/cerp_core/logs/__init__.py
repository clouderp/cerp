# -*- coding: utf-8 -*-

from odoo import api


def cerp_log(
        env: api.Environment,
        module_name: str,
        message: str,
        log_type='info',
        commit=False):
    env['cerp_core.log'].create(
        dict(message=message,
             module_name=module_name,
             log_type=log_type))
    if commit:
        env.cr.commit()
