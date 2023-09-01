# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
#
# natural_sort filter
#
from __future__ import annotations


import re

from jinja2.runtime import Undefined
from jinja2.utils import Namespace


def convert(text):
    return int(text) if text.isdigit() else text.lower()


def natural_sort(iterable, sort_key=None):
    if isinstance(iterable, Undefined) or iterable is None:
        return []

    def alphanum_key(key):
        if sort_key is not None and isinstance(key, dict):
            return [convert(c) for c in re.split("([0-9]+)", str(key.get(sort_key, key)))]
        elif sort_key is not None and isinstance(key, Namespace):
            return [convert(c) for c in re.split("([0-9]+)", getattr(key, sort_key))]
        else:
            return [convert(c) for c in re.split("([0-9]+)", str(key))]

    return sorted(iterable, key=alphanum_key)


class FilterModule(object):
    def filters(self):
        return {
            "natural_sort": natural_sort,
        }
