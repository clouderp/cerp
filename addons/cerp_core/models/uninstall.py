# -*- coding: utf-8 -*-

import functools

from odoo import api, models, _


from ..typing import OdooModelType
from .. import utils


def _filter_affected_models(
        module_names: set,
        ir_models_xids: dict,
        model: OdooModelType) -> bool:
    #
    # this function includes all cerp_core models with exception of cerp_log
    #
    # it also includes the keychain model as uninstalling accounts removes
    # these
    #
    # as the tables are not actually being uninstalled - just documents
    # it doesnt exclude classes which are inherited from
    #
    xids = ir_models_xids.get(model.id, ())
    return bool(
        xids and (
            not any(xid.split('.')[1]
                    in ['model_cerp_core_log']
                    for xid in xids)
            and (any(xid.split('.')[0]
                     in ['keychain2']
                     for xid in xids)
                 or any(xid.split('.')[1]
                        in ['model_cerp_core_account']
                        for xid in xids)
                 or all(xid.split('.')[0]
                        in module_names
                        for xid in xids))))


class CloudERPModuleUninstall(models.TransientModel):
    _inherit = "base.module.uninstall"
    _name = "cerp_core.module.uninstall"

    def _get_models(self):
        """ Return the models (ir.model) to consider for the impact. """
        # this is necessary to prevent the mail addon clobbering
        # the uninstall functionality
        return self.env['ir.model'].search([('transient', '=', False)])

    @api.depends('module_ids')
    def _compute_model_ids(self):
        ir_models = self._get_models()
        ir_models_xids = ir_models._get_external_ids()

        for wizard in self:
            if wizard.module_id:
                module_names = set(wizard._get_modules().mapped('name'))
                module_names.add('cerp_core')
                # find the models that have all their XIDs in the given modules
                self.model_ids = ir_models.filtered(
                    functools.partial(
                        _filter_affected_models,
                        module_names,
                        ir_models_xids)).sorted('name')

    def action_uninstall(self):
        # it shouldnt be possible to uninstall multiple addons through
        # the UI
        self.ensure_one()
        module = self.module_id
        module.button_immediate_uninstall()
        return utils.success_action(
            self.env,
            _("Module (%s) uninstalled" % module.name))
