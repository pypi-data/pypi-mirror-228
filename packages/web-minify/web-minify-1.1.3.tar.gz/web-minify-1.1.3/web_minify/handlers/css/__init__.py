#!/usr/bin/env python3
"""CSS Minifier functions for CSS-HTML-JS-Minify."""

from .variables import EXTENDED_NAMED_COLORS, CSS_PROPS_TEXT
from .css import css_minify

from .. import HandlerManager

import logging

logger = logging.getLogger(__name__)


class Handler:
    """CSS handler class"""

    def __init__(self, context: HandlerManager):
        self.context = context
        self.settings: dict = self.context.settings()

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["css"]

    @classmethod
    def name(self):
        return "css"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return True, raw, None
        elif "minify" == mode:
            proc, msg = css_minify(raw, self.settings)
            return True, proc, msg
        else:
            return False, raw, [f"Unsupported mode '{mode}' for {self.name()} handler, skipping..."]
