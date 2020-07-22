# -*- coding: utf-8 -*-

from typing import Iterable, Iterator

from odoo.addons.keychain2.models.keychain import Keychain2Account

from .record import Record


class RecordCollector(object):
    record_type = 'cerp_core.metric'
    record_class = Record

    def __init__(
            self,
            account: Keychain2Account,
            records: Iterable = None):
        self.account = account
        self._records = []
        for record in records or []:
            self.add_record(self.record_class(record))

    def add_record(self, record: Record) -> None:
        self._records.append(record)

    @property
    def env(self):
        return self.account.env

    @property
    def records(self) -> Iterator[Record]:
        for record in self._records:
            yield record

    def save(self):
        # bulk add ?
        for record in self.records:
            self.env[self.record_type].create(record.data)
