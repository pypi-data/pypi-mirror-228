from .. import HandlerManager

from .scour import scourString


import logging

logger = logging.getLogger(__name__)


def svg_minify(svg, settings: dict):
    """Minify SVG main function."""
    svg = scourString(in_string=svg, options=settings)
    return svg, None


class Handler:
    """SVG handler class"""

    def __init__(self, context: HandlerManager):
        self.context = context
        self.settings: dict = self.context.settings()

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["svg"]

    @classmethod
    def name(self):
        return "svg"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return True, raw, None
        elif "minify" == mode:
            proc, msg = svg_minify(raw, self.settings)
            return True, proc, msg
        else:
            return False, raw, [f"Unsupported mode '{mode}' for {self.name()} handler, skipping..."]
