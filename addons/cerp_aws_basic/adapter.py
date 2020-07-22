# -*- coding: utf-8 -*-

from datetime import date

from odoo.addons.cerp_core import adapter, records, utils
from odoo.addons.cerp_core.decorators import arg


class AWSRecord(records.Record):
    pass


class AWSRecordCollector(records.RecordCollector):
    record_class = AWSRecord


class CloudERPAdapter(adapter.Adapter):
    collector = AWSRecordCollector

    @classmethod
    @arg.typed(list)
    @arg.length(2)
    def validate_credentials(cls, credentials: list) -> bool:
        """
        Example:
        [
           "xxxxxxxxxxxxxxxxx",
           "yyyyyyyyyyyyyyyyy"
        ]
        """
        return (
            len(credentials[0]) > 2
            and len(credentials[1]) > 2)

    def fetch(
            self,
            credentials: list,
            metricset=None) -> AWSRecordCollector:
        this_month = utils.get_month_range(date.today())
        aws_cost_monthly = self.account.provider.metric_types.search(
            [('name', '=', 'aws.costs.monthly')])
        return self.collect(
            [dict(metric_type=aws_cost_monthly.id,
                  value=23,
                  start=this_month[0],
                  end=this_month[1])])
