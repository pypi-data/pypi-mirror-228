import sys
import json
from . import HandlerManager

import logging

logger = logging.getLogger(__name__)


class Handler:
    """json handler class"""

    def __init__(self, context: HandlerManager):
        self.context = context
        self.settings: dict = self.context.settings()

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["json"]

    @classmethod
    def name(self):
        return "json"

    def _process(self, raw: str, do_format: bool):
        try:
            parsed = json.loads(raw)
            format_indent = 4
            return json.dumps(parsed, indent=format_indent if do_format else None, sort_keys=True), None
        except json.JSONDecodeError as jde:
            return f"Error decoding json: {jde}", None
        except Exception as e:
            return f"Unknown error processing json: {e}", None

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            proc, msg = self._process(raw, do_format=True)
            return True, proc, msg
        elif "minify" == mode:
            proc, msg = self._process(raw, do_format=False)
            return True, proc, msg
        else:
            return False, raw, [f"Unsupported mode '{mode}' for {self.name()} handler, skipping..."]
