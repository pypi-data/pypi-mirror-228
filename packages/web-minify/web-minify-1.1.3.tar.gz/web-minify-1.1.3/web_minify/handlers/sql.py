import sys
import sqlparse
import logging
from . import HandlerManager, append_and_return

logger = logging.getLogger(__name__)


class Handler:
    """SQL handler class"""

    def __init__(self, context: HandlerManager):
        self.context = context
        self.settings: dict = self.context.settings()

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["sql", "pgsql"]

    @classmethod
    def name(self):
        return "sql"

    def process(self, raw: str, name: str = None):
        processed = raw
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Check out https://github.com/paetzke/format-sql as alternative
            processed = ""
            statements = sqlparse.split(raw)
            for statement in statements:
                processed += sqlparse.format(statement, reindent=True, reindent_aligned=True, indent_tabs=True, output_format="python", keyword_case="lower") + "\n\n"
            return True, processed, [f"Processed {len(statements)} SQL statements"]
        elif "minify" == mode:
            return True, raw, []
        else:
            return False, raw, [f"Unsupported mode '{mode}' for {self.name()} handler, skipping..."]
