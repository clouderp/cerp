# -*- coding: utf-8 -*-

from functools import wraps


def length(_length, onerror=None):

    try:
        _length = int(_length)
    except ValueError:
        pass

    def _onerror(obj, fun, arg, _length):
        if onerror:
            return onerror(obj, fun, arg, _length)
        return False

    def wrapper(fun):

        @wraps(fun)
        def wrapped(obj, arg):
            wrong_length = (
                (isinstance(_length, str)
                 and ((_length.startswith('<')
                       and not _length.startswith('<=')
                       and len(arg) >= int(_length[1:].strip()))
                      or (_length.startswith('>')
                          and not _length.startswith('>=')
                          and len(arg) <= int(_length[1:].strip()))
                      or (_length.startswith('>=')
                          and len(arg) < int(_length[2:].strip()))
                      or (_length.startswith('<=')
                          and len(arg) > int(_length[2:].strip()))))
                or (isinstance(_length, int)
                    and not len(arg) == _length))
            if wrong_length:
                return _onerror(obj, fun, arg, _length)
            return fun(obj, arg)
        return wrapped
    return wrapper


def typed(_type, onerror=None):

    def _onerror(obj, fun, arg, _type):
        if onerror:
            return onerror(obj, fun, arg, _type)
        return False

    def wrapper(fun):

        @wraps(fun)
        def wrapped(obj, arg):
            if not isinstance(arg, _type):
                return _onerror(obj, fun, arg, _type)
            return fun(obj, arg)
        return wrapped
    return wrapper


def contains(needle, onerror=None):

    def _onerror(obj, fun, arg, needle):
        if onerror:
            return onerror(obj, fun, arg, needle)
        return False

    def wrapper(fun):

        @wraps(fun)
        def wrapped(obj, arg):
            needles = (
                needle
                if isinstance(needle, (tuple, list))
                else [needle])
            for _needle in needles:
                if _needle not in arg:
                    return _onerror(obj, fun, arg, needle)
            return fun(obj, arg)
        return wrapped
    return wrapper
