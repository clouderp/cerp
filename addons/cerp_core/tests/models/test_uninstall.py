# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, PropertyMock

from odoo import models

from odoo.addons.cerp_core.models.uninstall import (
    _filter_affected_models)

from ._base import TestCloudERPModels


_filter_affected_param_list = (
    ([], None, False),
    ([], False, False),
    ([], [], False),
    ([], ['other.foo'], False),
    ([], ['keychain2.foo'], True),
    ([], ['keychain2.foo', 'other.bar'], True),
    (['notkeychain2'], ['keychain2.foo', 'other.bar'], True),
    ([], ['other.model_cerp_core_account'], True),
    ([], ['other.model_cerp_core_account', 'other.bar'], True),
    (['baz.foo'], ['other.model_cerp_core_account', 'other.bar'], True),
    (['foo'], ['foo.bar', 'foo.baz'], True),
    (['foo', 'bar'], ['foo.bar', 'bar.baz'], True),
    (['foo'], ['foo.bar', 'foo.baz'], True),
    (['foo', 'bar'], ['foo.bar', 'baz.foo'], False))


class TestCloudERPModuleUninstall(TestCloudERPModels):

    def test_uninstall_wizard(self):
        keychain = self.env['ir.module.module'].search(
            [('name', '=', 'keychain2')])
        wizard = self.env['cerp_core.module.uninstall'].create(
            dict(module_id=keychain.id))
        assert wizard._inherit == 'base.module.uninstall'
        assert isinstance(wizard, models.TransientModel)

    def test_get_models(self):
        keychain = self.env['ir.module.module'].search(
            [('name', '=', 'keychain2')])
        wizard = self.env['cerp_core.module.uninstall'].create(
            dict(module_id=keychain.id))
        wizard.env = MagicMock()
        _models = wizard._get_models()
        assert (
            list(wizard.env.__getitem__.call_args)
            == [('ir.model',), {}])
        assert (
            list(wizard.env.__getitem__.return_value.search.call_args)
            == [([('transient', '=', False)],), {}])
        assert (
            _models
            == wizard.env.__getitem__.return_value.search.return_value)

    def test_action_uninstall(self):
        keychain = self.env['ir.module.module'].search(
            [('name', '=', 'keychain2')])
        wizard = self.env['cerp_core.module.uninstall'].create(
            dict(module_id=keychain.id))
        wizard.env = MagicMock()
        wizard.ensure_one = MagicMock()
        _module_id = type(wizard).module_id
        type(wizard).module_id = MagicMock()

        _patch = self._patch('models.uninstall.utils.success_action')
        with _patch as success_mock:
            result = wizard.action_uninstall()

        assert wizard.ensure_one.called
        assert wizard.module_id.button_immediate_uninstall.called
        assert (
            list(success_mock.call_args)
            == [(wizard.env,
                 "Module (%s) uninstalled" % (wizard.module_id.name)), {}])
        assert result == success_mock.return_value
        type(wizard).module_id = _module_id

    def test_compute_model_ids(self):
        keychain = self.env['ir.module.module'].search(
            [('name', '=', 'keychain2')])
        wizard = self.env['cerp_core.module.uninstall'].create(
            dict(module_id=keychain.id))
        wizard._get_models = MagicMock()

        assert (
            wizard._compute_model_ids._depends
            == ('module_ids',))

        _model_ids = type(wizard).model_ids
        _get_modules = type(wizard)._get_modules
        type(wizard).model_ids = MagicMock(new_callable=PropertyMock)
        get_modules_mock = MagicMock()
        type(wizard)._get_modules = get_modules_mock
        wizard._get_modules = MagicMock()

        with self._patch('models.uninstall.functools') as funct_mock:
            with self._patch('models.uninstall.set') as set_mock:
                wizard._compute_model_ids()

        assert wizard._get_models.called
        assert not wizard._get_modules.called
        assert get_modules_mock.called
        assert (
            list(get_modules_mock.return_value.mapped.call_args)
            == [('name',), {}])
        assert (
            list(set_mock.call_args)
            == [(get_modules_mock.return_value.mapped.return_value,), {}])
        assert (
            list(list(c) for c in set_mock.return_value.add.call_args_list)
            == [[('cerp_core',), {}]])

        _ir_models = wizard._get_models.return_value
        _ir_models_xids = _ir_models._get_external_ids.return_value

        assert (
            wizard.model_ids
            == _ir_models.filtered.return_value.sorted.return_value)
        assert (
            list(_ir_models.filtered.call_args)
            == [(funct_mock.partial.return_value,), {}])
        assert (
            list(funct_mock.partial.call_args)
            == [(_filter_affected_models,
                 set_mock.return_value,
                 _ir_models_xids), {}])
        type(wizard).model_ids = _model_ids
        type(wizard)._get_modules = _get_modules

    def test_filter_affected_models(self):
        _model = MagicMock()
        _xids = MagicMock()

        for _mods, _xids_return, expected in _filter_affected_param_list:
            with self.subTest():
                _xids.get.return_value = _xids_return
                assert (
                    _filter_affected_models(_mods, _xids, _model)
                    == expected)
                assert (
                    list(_xids.get.call_args)
                    == [(_model.id, ()), {}])
                _xids.reset_mock()
