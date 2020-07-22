# -*- coding: utf-8 -*-

import json
import os

from odoo.addons.cerp_core import context
from .test_base import TestCloudERPBase


class SecretException(Exception):
    pass


class TestCloudERPContext(TestCloudERPBase):

    @property
    def _secrets(self):
        return dict(
            secretfoo="x",
            secretbar="y",
            verysecret="☠")

    def test_secretenv(self):
        with context.secretenv(**self._secrets):
            for k, v in self._secrets.items():
                assert os.environ[k] == v
        for k in self._secrets:
            assert k not in os.environ

    def test_secretenv_failure(self):
        try:
            with context.secretenv(**self._secrets):
                raise SecretException
        except SecretException:
            pass
        for k in self._secrets:
            assert k not in os.environ

    def test_secretfile(self):
        with context.secretfile(json.dumps(self._secrets)) as path:
            with open(path) as f:
                secrets = json.loads(f.read())
            for k, v in self._secrets.items():
                assert secrets[k] == v
        assert not os.path.exists(path)

    def test_secretfile_failure(self):
        try:
            with context.secretfile(json.dumps(self._secrets)) as path:
                raise SecretException
        except SecretException:
            pass
        assert not os.path.exists(path)
