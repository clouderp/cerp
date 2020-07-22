# -*- coding: utf-8 -*-

from unittest.mock import MagicMock

from odoo.addons.cerp_core import records

from .test_base import TestCloudERPBase


class TestCloudERPRecordCollector(TestCloudERPBase):

    def setUp(self):
        super(TestCloudERPRecordCollector, self).setUp()
        self._rec_mock = self._patch(
            'records.recordset.RecordCollector.record_class')
        self._add_rec_mock = self._patch(
            'records.recordset.RecordCollector.add_record')

    def test_constructor(self):
        account = MagicMock()
        with self._rec_mock as rec_mock, self._add_rec_mock as add_rec_mock:
            collector = records.RecordCollector(account)
        assert collector.account == account
        assert collector.env == account.env
        assert collector._records == []
        assert collector.record_type == 'cerp_core.metric'
        assert collector.record_class == records.Record
        assert not add_rec_mock.called
        assert not rec_mock.called

    def test_constructor_iterable(self):

        def _records():
            for x in range(3):
                yield x

        account = MagicMock()
        with self._rec_mock as rec_mock, self._add_rec_mock as add_rec_mock:
            collector = records.RecordCollector(account, _records())
        assert collector.account == account
        assert collector.env == account.env
        assert (
            list(list(c) for c in rec_mock.call_args_list)
            == [[(0,), {}], [(1,), {}], [(2,), {}]])
        assert (
            list(list(c) for c in add_rec_mock.call_args_list)
            == [[(rec_mock.return_value,), {}],
                [(rec_mock.return_value,), {}],
                [(rec_mock.return_value,), {}]])

    def test_add_record(self):
        account = MagicMock()
        with self._rec_mock, self._add_rec_mock:
            collector = records.RecordCollector(account)
        collector._records = MagicMock()
        collector.add_record("RECORD")
        assert (
            list(collector._records.append.call_args)
            == [('RECORD',), {}])

    def test_records(self):
        account = MagicMock()
        with self._rec_mock, self._add_rec_mock:
            collector = records.RecordCollector(account)
        collector._records = ['x', 'y', 'z']
        _records = []
        for record in collector.records:
            _records.append(record)
        assert _records == collector._records

    def test_save(self):
        account = MagicMock()
        with self._rec_mock, self._add_rec_mock:
            collector = records.RecordCollector(account)
        collector._records = [MagicMock(), MagicMock(), MagicMock()]
        collector.save()
        assert (
            list(list(c) for c in account.env.__getitem__.call_args_list)
            == [[('cerp_core.metric',), {}],
                [('cerp_core.metric',), {}],
                [('cerp_core.metric',), {}]])
        _create = account.env.__getitem__.return_value.create.call_args_list
        assert (
            list(list(c) for c in _create)
            == [[(collector._records[0].data,), {}],
                [(collector._records[1].data,), {}],
                [(collector._records[2].data,), {}]])


class TestCloudERPRecord(TestCloudERPBase):

    def test_constructor(self):
        record = records.Record('DATA')
        assert record.data == 'DATA'
