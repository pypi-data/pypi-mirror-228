# https://engineeringblog.yelp.com/2017/06/making-photos-smaller.html
from . import HandlerManager

import logging

logger = logging.getLogger(__name__)


def jpeg_minify(jpeg, settings: dict):
    """Minify JPEG main function."""
    # TODO: Implement this
    # print(f"JPEG WAS CALLED FOR {len(jpeg)}!!!!! #############################################")
    return jpeg, None


class Handler:
    """JPEG handler class"""

    def __init__(self, context: HandlerManager):
        self.context = context
        self.settings: dict = self.context.settings()

    @classmethod
    def is_binary(self):
        return True

    @classmethod
    def extensions(self):
        return ["jpeg", "jpg"]

    @classmethod
    def name(self):
        return "jpeg"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return True, raw, None
        elif "minify" == mode:
            proc, msg = jpeg_minify(raw, self.settings)
            return True, proc, msg
        else:
            return False, raw, [f"Unsupported mode '{mode}' for {self.name()} handler, skipping..."]
