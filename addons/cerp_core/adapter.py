# -*- coding: utf-8 -*-

from typing import Iterable

from odoo.addons.keychain2.models.keychain import Keychain2Account

from . import records


class Adapter(object):
    collector = records.RecordCollector

    def __init__(
            self,
            keychain: Keychain2Account):
        self.keychain = keychain
        self.account = keychain.env['cerp_core.account'].search(
            [('keychain2', '=', keychain.id)])

    @property
    def metricsets(self):
        return self.account.metricsets

    @classmethod
    def validate_credentials(cls, credentials) -> bool:
        raise NotImplementedError

    def fetch(self, credentials) -> records.RecordCollector:
        raise NotImplementedError

    def collect(self, records: Iterable) -> records.RecordCollector:
        return self.collector(self.account, records)
