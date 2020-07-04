
from odoo import api, SUPERUSER_ID


def install_provider(cr, key_namespace, short_name, module_name):
    env = api.Environment(cr, SUPERUSER_ID, {})
    module = env['ir.module.module'].search(
        [('name', '=', module_name)])[0]
    env['cerp_core.account_provider'].create(
        {'name': short_name,
         'key_namespace': key_namespace,
         'module': module.id})
    cerp_log(env, '[%s] installed' % module_name)


def uninstall_provider(cr, module_name):
    env = api.Environment(cr, SUPERUSER_ID, {})
    module = env['ir.module.module'].search(
        [('name', '=', module_name)])[0]
    providers = env['cerp_core.account_provider'].search(
        [('module', '=', module.id)])

    for provider in providers:
        env['cerp_core.account'].search(
            [('provider', '=', provider.id)]).unlink()
        provider.unlink()
    cerp_log(env, '[%s] uninstalled' % module_name)


def cerp_log(env, message, log_type='info', commit=False):
    env['cerp_core.log'].create(
        dict(message=message,
             log_type=log_type))
    if commit:
        env.cr.commit()
