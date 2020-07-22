# -*- coding: utf-8 -*-

import calendar
from datetime import datetime

from odoo import _


def get_month_range(_date):
    first_day = _date.replace(day=1)
    last_day = _date.replace(
        day=calendar.monthrange(
            _date.year, _date.month)[1])
    return (
        datetime.combine(first_day, datetime.min.time()),
        datetime.combine(last_day, datetime.max.time()))


def success_action(
        env,
        message,
        title=None,
        res_model=None,
        wizard_model=None):
    message = env[wizard_model or 'cerp_core.message.wizard'].create(
        {'message': message})
    return {
        'name': title or _('Success'),
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': res_model or 'cerp_core.message.wizard',
        'res_id': message.id,
        'target': 'new'}
