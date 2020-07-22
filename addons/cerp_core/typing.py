# -*- coding: utf-8 -*-

from typing import TypeVar

from odoo import models

from . import adapter


AdapterType = TypeVar(
    'AdapterType',
    bound='.'.join(
        [adapter.Adapter.__module__,
         adapter.Adapter.__name__]))


OdooModelType = TypeVar(
    'ModelType',
    bound='.'.join(
        [models.Model.__module__,
         models.Model.__name__]))
