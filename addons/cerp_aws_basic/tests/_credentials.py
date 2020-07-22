# -*- coding: utf-8 -*-

VALID_CREDENTIALS = (
    ["xxxxxxxxxxxxxxxxxxxxx", "zzzzzzzzzzzzzzzzzzzzz"],
    ["aaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbb"])
INVALID_CREDENTIALS = (
    {}, dict(foo="bar"), "somestring",
    ["xxxxxxxxxxxxxxxxxxxxx"],
    ["xxxxxxxxxxxxxxxxxxxxx",
     "zzzzzzzzzzzzzzzzzzzzz",
     "zzzzzzzzzzzzzzzzzzzzz"])
