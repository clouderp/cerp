# -*- coding: utf-8 -*-

from odoo.addons.cerp_core import adapter, records

from odoo.addons.cerp_core.decorators import arg


class AzureRecordCollector(records.RecordCollector):
    pass


class CloudERPAdapter(adapter.Adapter):
    collector = AzureRecordCollector

    @classmethod
    @arg.typed(dict)
    @arg.length(1)
    @arg.contains('foo')
    def validate_credentials(cls, credentials: list) -> bool:
        """
        Example:
        {
           "foo": "barrrrr"
        }
        """
        return len(credentials.get('foo', '')) > 3

    def fetch(
            self,
            credentials: dict,
            metricset=None) -> AzureRecordCollector:
        return self.collect([])
