# -*- coding: utf-8 -*-

from datetime import date, timedelta

import boto3
# from botocore import errorfactory

from odoo import exceptions

from odoo.addons.cerp_core import adapter, context


class CloudERPAdapter(adapter.Adapter):

    @classmethod
    def validate_credentials(cls, credentials):
        return (
            isinstance(credentials, list)
            and len(credentials) == 2)

    def update(self, credentials):
        start = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        end = date.today().strftime("%Y-%m-%d")
        secrets = dict(
            AWS_ACCESS_KEY_ID=credentials[0],
            AWS_SECRET_ACCESS_KEY=credentials[1])
        with context.secretenv(**secrets):
            return self._get_cost_and_usage(start, end)

    def _get_cost_and_usage(self, start, end):
        client = boto3.client('ce')
        try:
            client.get_cost_and_usage(
                Granularity="DAILY",
                Metrics=["BlendedCost"],
                TimePeriod=dict(
                    Start=start,
                    End=end))
        except client.exceptions.DataUnavailableException as e:
            raise exceptions.Warning("Data unavailable: %s" % e)
