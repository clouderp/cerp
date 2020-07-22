# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, PropertyMock

from ._base import TestCloudERPModels


_model_per_module_param_list = (
    (None, None),
    ('DOESNOTEXIST', None),
    ('cerp_core.account_provider', 1),
    ('keychain2.account', 1),
)


class TestCloudERPModel(TestCloudERPModels):

    def test_cerp_module_count(self):
        _models = self.env['ir.model'].search([])[:3]
        _models.env = MagicMock()
        _cerp_module_count = type(_models).cerp_module_count
        _cerp_count_mock = PropertyMock()
        type(_models).cerp_module_count = _cerp_count_mock
        _context = type(_models)._context
        type(_models)._context = MagicMock()
        _patch = self._patch(
            'models.model.CloudERPModel._cerp_compute_rec_count_for_module')

        assert _models._cerp_compute_count._depends == ()
        with _patch as count_mock:
            _models._cerp_compute_count()

        assert (
            list(list(c) for c in _models._context.get.call_args_list)
            == [[('active_model',), {}]])
        assert not _models._context.__getitem__.called
        assert not _models.env.__getitem__.called
        assert not count_mock.called
        assert (
            list(list(c) for c in _cerp_count_mock.call_args_list)
            == [[(0,), {}], [(0,), {}], [(0,), {}]])

        type(_models)._context = _context
        type(_models).cerp_module_count = _cerp_module_count

    def test_cerp_active_module_count(self):
        _models = self.env['ir.model'].search([])[:3]
        _models.env = MagicMock()
        _cerp_module_count = type(_models).cerp_module_count
        _cerp_count_mock = PropertyMock()
        type(_models).cerp_module_count = _cerp_count_mock
        _context = type(_models)._context
        type(_models)._context = MagicMock()
        type(_models)._context.get.return_value = 'ir.module.module'

        _patch = self._patch(
            'models.model.CloudERPModel._cerp_compute_rec_count_for_module')

        assert _models._cerp_compute_count._depends == ()
        with _patch as count_mock:
            _models._cerp_compute_count()

        assert (
            list(list(c) for c in _models._context.get.call_args_list)
            == [[('active_model',), {}]])
        assert (
            list(list(c) for c in _models._context.__getitem__.call_args_list)
            == [[('active_id',), {}]])
        assert (
            list(list(c) for c in _models.env.__getitem__.call_args_list)
            == [[('ir.module.module',), {}]])
        _env_search = _models.env.__getitem__.return_value.search
        assert (
            list(list(c) for c in _env_search.call_args_list)
            == [[([('id',
                    '=',
                    _models._context.__getitem__.return_value)],),
                 {}]])
        assert (
            list(list(c) for c in _cerp_count_mock.call_args_list)
            == [[(count_mock.return_value,), {}]] * 3)
        assert (
            list(list(c) for c in count_mock.call_args_list)
            == [[(_env_search.return_value, _models[0]), {}],
                [(_env_search.return_value, _models[1]), {}],
                [(_env_search.return_value, _models[2]), {}]])

        type(_models)._context = _context
        type(_models).cerp_module_count = _cerp_module_count

    def test_cerp_compute_rec_count(self):
        _model = self.env['ir.model'].search([])[0]

        _model.env = MagicMock()
        rec = MagicMock()
        module = MagicMock()

        for model, expected in _model_per_module_param_list:
            with self.subTest():
                rec.model = model
                assert (
                    _model._cerp_compute_rec_count_for_module(module, rec)
                    == expected)
                assert not _model.env.__getitem__.called
                assert not _model.env.cr.execute.called
                assert not _model.env.cr.fetchone.called

    def test_cerp_compute_rec_count_account(self):
        _model = self.env['ir.model'].search([])[0]

        _model.env = MagicMock()
        rec = MagicMock()
        module = MagicMock()
        rec.model = 'cerp_core.account'
        module.cerp_provider.accounts = ['ACC'] * 23
        assert _model._cerp_compute_rec_count_for_module(module, rec) == 23
        assert not _model.env.__getitem__.called
        assert not _model.env.cr.execute.called
        assert not _model.env.cr.fetchone.called

    def test_cerp_compute_rec_count_metric_type(self):
        _model = self.env['ir.model'].search([])[0]
        _model.env = MagicMock()
        rec = MagicMock()
        module = MagicMock()
        rec.model = 'cerp_core.metric.type'
        module.cerp_provider.metric_types = ['METRIC_TYPE'] * 17
        assert _model._cerp_compute_rec_count_for_module(module, rec) == 17
        assert not _model.env.__getitem__.called
        assert not _model.env.cr.execute.called
        assert not _model.env.cr.fetchone.called

    def test_cerp_compute_rec_count_metricset(self):
        _model = self.env['ir.model'].search([])[0]
        _model.env = MagicMock()
        rec = MagicMock()
        module = MagicMock()
        rec.model = 'cerp_core.metricset'
        module.cerp_provider.metricsets = ['METRICSET'] * 13
        assert _model._cerp_compute_rec_count_for_module(module, rec) == 13
        assert not _model.env.__getitem__.called
        assert not _model.env.cr.execute.called
        assert not _model.env.cr.fetchone.called

    def test_cerp_compute_rec_count_metric(self):
        _model = self.env['ir.model'].search([])[0]
        _model.env = MagicMock()
        rec = MagicMock()
        module = MagicMock()
        module.cerp_provider.metric_types.ids = [1, 2, 3]
        rec.model = 'cerp_core.metric'

        result = _model._cerp_compute_rec_count_for_module(module, rec)
        assert (
            list(_model.env.__getitem__.call_args)
            == [('cerp_core.metric',), {}])
        assert (
            list(_model.env.cr.execute.call_args)
            == [('SELECT COUNT(*) FROM "%s" WHERE "metric_type" IN (1,2,3)'
                 % _model.env.__getitem__.return_value._table,),
                {}])
        assert (
            list(_model.env.cr.fetchone.call_args)
            == [(), {}])
        assert (
            result
            == _model.env.cr.fetchone.return_value.__getitem__.return_value)
        assert (
            list(_model.env.cr.fetchone.return_value.__getitem__.call_args)
            == [(0,), {}])
