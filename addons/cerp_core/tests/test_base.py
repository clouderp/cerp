# -*- coding: utf-8 -*-

from unittest.mock import patch

from odoo.tests.common import SavepointCase


class TestCloudERPBase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestCloudERPBase, cls).setUpClass()

    def _patch(self, path):
        return patch(
            'odoo.addons.cerp_core.%s'
            % (path))
