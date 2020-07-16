# -*- coding: utf-8 -*-

from odoo.addons.cerp_core.utils import install_provider, uninstall_provider

from .constants import KEY_NAMESPACE, SHORT_NAME, MODULE_NAME


def post_init_hook(cr, registry):
    install_provider(cr, KEY_NAMESPACE, SHORT_NAME, MODULE_NAME)


def uninstall_hook(cr, registry):
    uninstall_provider(cr, MODULE_NAME)
