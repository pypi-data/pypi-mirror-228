#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML Minifier functions for CSS-HTML-JS-Minify."""

from html.parser import HTMLParser

import logging
import pprint

from .. import HandlerManager

from .minify import html_minify
from .beautify import html_beautify
from .webparser import WebParser

logger = logging.getLogger(__name__)


class Handler:
    """HTML handler class"""

    def __init__(self, context: HandlerManager):
        self.context = context
        self.settings: dict = self.context.settings()
        self.webparser = WebParser()

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["html", "htm"]

    @classmethod
    def name(self):
        return "html"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        return False, raw, [f"Unsupported mode '{mode}' for {self.name()} handler, skipping..."]

    def nu_process(self, raw: str, name: str = None):
        # logger.warn("processing")
        mode = self.settings.get("mode")
        self.webparser.parse(raw)
        if "beautify" == mode:
            processed, messages = self.webparser.beautify()
            # logger.warn(f"processed({mode})={processed}")
            return True, processed, messages
            # return html_beautify(raw, self.settings)
        elif "minify" == mode:
            processed, messages = self.webparser.minify()
            # logger.warn(f"processed({mode})={processed}")
            return True, processed, messages
            # return html_minify(raw, self.settings)
        else:
            return False, raw, [f"Unsupported mode '{mode}' for {self.name()} handler, skipping..."]
