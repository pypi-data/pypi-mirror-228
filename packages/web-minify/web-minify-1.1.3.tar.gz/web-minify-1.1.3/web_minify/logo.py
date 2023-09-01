from . import __version__

from pyfiglet import figlet_format


logo = figlet_format("web-minify", font="smslant") + f"v{__version__}"
