# -*- coding: utf-8 -*-

# todo: put proper credential tests!
VALID_CREDENTIALS = (
    dict(foo='xxxxxxxxxxxxxx'),
    dict(foo='yyyyyyyyyyyyyy'))
INVALID_CREDENTIALS = (
    [], (), "somestring",
    dict(foo="bar"),
    dict(foo="xxxxxxxxxxxxxx",
         other="var"))
