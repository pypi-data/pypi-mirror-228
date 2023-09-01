from enum import Enum


class Mode(Enum):
    minify = "minify"
    beautify = "beautify"

    def __repr__(self):
        return f"{self.value}"


def mode2emoji(mode):
    emojis = {"minify": "🗜", "beautify": "✨"}
    return emojis.get(mode, "?")
