# -*- coding: utf-8 -*-

from odoo import models

from odoo.addons.cerp_core.models.account import cerp_account_factory

from ..adapter import CloudERPAdapter
from ..constants import KEY_NAMESPACE, SHORT_NAME


class CloudERPAccount(models.Model):
    _inherit = 'keychain2.account'


cerp_account_factory(
    KEY_NAMESPACE,
    SHORT_NAME,
    CloudERPAccount,
    CloudERPAdapter)
