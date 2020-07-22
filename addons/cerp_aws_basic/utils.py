# -*- coding: utf-8 -*-

from datetime import datetime


def aws_to_dt(aws):
    return datetime.strptime(aws, '%Y-%m-%dT%H:%M:%S+00:00')


def dt_to_aws(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
