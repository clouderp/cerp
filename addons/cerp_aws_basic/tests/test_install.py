# -*- coding: utf-8 -*-

from odoo.addons.cerp_core.tests._base import TestCloudERPAdapter


class TestAWSCloudERPInstall(TestCloudERPAdapter):
    addon = "cerp_aws_basic"

    def test_validator(self):
        self._test_validator()

    def test_icon(self):
        self._test_icon()

    def test_manifest(self):
        self._test_manifest()

    def test_model(self):
        self._test_model()
