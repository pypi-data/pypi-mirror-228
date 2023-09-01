#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging
from bs4 import BeautifulSoup
from html5print import HTMLBeautifier
import html

logger = logging.getLogger(__name__)


space_re = re.compile(r"^(\s*)", re.MULTILINE)

# default_formatter = 'html5lib'
default_formatter = "html.parser"
too_long_line = 1000


def html_beautify(raw, settings, encoding=None, formatter=default_formatter, indents=4):
    stripped = raw.strip()
    if len(stripped) <= 0:
        return True, stripped, None
    s = BeautifulSoup(raw, formatter)
    formatted = s.prettify(encoding=encoding)
    formatted = formatted.strip() + "\n"
    parts = formatted.split("\n")
    for part in parts:
        if len(part) > too_long_line:
            return True, raw, [f"Something wrong in html output! A line was generated with a length above the limit of {too_long_line} characters"]
    return True, formatted, None
    # spaced = space_re.sub(r"\1" * indents, formatted)
    # return spaced.strip() + "\n", None


def html_beautify_bob(raw, settings, encoding=None, formatter=default_formatter, indents=4):
    ret = raw
    try:
        ret = HTMLBeautifier.beautify(raw, indents).strip() + "\n"
    except Exception as e:
        False, raw, [f"Error beautifying HTML: {e}"]
    return True, ret, None
