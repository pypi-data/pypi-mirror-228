import sys
import logging
from jinja2 import Environment
import magic
from . import HandlerManager, append_and_return

logger = logging.getLogger(__name__)

jinja_env = Environment()
magic_mime = magic.Magic(mime=True)


def jinja_lint(jinja, settings: dict):
    """Minify jinja main function. Does not minify, rather detects errors (lint)"""
    messages = []
    try:
        jinja_env.parse(jinja)
    except Exception as e:
        messages.append(f"jinja2 lint error: {e}")
    return messages


def detect_mime(buf):
    return magic_mime.from_buffer(buf)


def process_html(raw, name, mode, context):
    html_handler = context.get_handler_by_name("html")
    ok, processed, html_messages = html_handler.process(raw, name)
    return ok, processed, html_messages


class Handler:
    """jinja2 handler class"""

    def __init__(self, context: HandlerManager):
        self.context = context
        self.settings: dict = self.context.settings()

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["jinja", "jinja2", "j2", "tpl", "template"]

    @classmethod
    def name(self):
        return "jinja"

    def process(self, raw: str, name: str = None):
        processed = raw
        mode = self.settings.get("mode")
        mime = "NOT SUPPORTED"  # "text/html" #detect_mime(raw)
        # logger.info(f"mime {mime}")
        html_messages = []
        # logger.warn(f"Processing j2 {name}")
        # logger.warn(raw)
        if mime == "text/html":
            html_ok, processed, html_messages_add = process_html(raw, name, mode, self.context)
            if html_ok:
                html_messages = append_and_return(html_messages_add, "Did html processing: OK")
            else:
                html_messages = append_and_return(html_messages_add, "Did html processing: Fail")
        if "beautify" == mode:
            lint_messages = jinja_lint(processed, self.settings)
            return True, processed, [*lint_messages, *html_messages]
        elif "minify" == mode:
            lint_messages = jinja_lint(processed, self.settings)
            return True, processed, [*lint_messages, *html_messages]
        else:
            return False, raw, [f"Unsupported mode '{mode}' for {self.name()} handler, skipping..."]
