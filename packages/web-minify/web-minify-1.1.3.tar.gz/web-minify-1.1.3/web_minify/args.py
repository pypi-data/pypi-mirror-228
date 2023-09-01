#!/usr/bin/env python3

import argparse

import logging

from pathos.multiprocessing import cpu_count

from .modes import Mode
from .logo import logo
from .handlers import HandlerManager

from . import __version__


logger = logging.getLogger(__name__)

nproc = cpu_count()


##############################################################################


def parse_arguments(defaults):
    """Build and return a command line agument parser."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
    ---------------------------------------------------------
{logo}

    Process all CSS/SASS/HTML/JS/SVG/PNG/JPEG found at input,
    either in single file or recursively through a directory.

    Will output in place, to specified file or folder depending
    on what output was specified.

    Will apply transformation to each file according to
    selected mode:

    Mode = minify (for optimizing production):
     + Compile (SASS -> CSS)
     + Strip whitespace
     + Strip comments
     + Strip metadata
     + Increase compression ratio (PNG, JPEG)
     + Sort (CSS)
     + Add timestamp (CSS, HTML)
     + Obfuscate (CSS, JS)
     + Hash

    Mode = beautify (for aiding development):
     + lint (JS, HTML)
     + normalize format (JS, HTML)

    Provides some options for processing:
    + Process files in-place
    + Process files renaming to new form
    + Compress results to .gz (all non-binary files)

    Available variables in format string are:
    + {{EXT}}
    + {{HASH}}
    + {{PATH}}
    + {{BASE}}
 
""",
    )

    _option_group_general = parser.add_argument_group("general", "General options for this program")
    _option_group_general.add_argument("--version", action="version", version=__version__)
    _option_group_general.add_argument("--mode", type=Mode, choices=list(Mode), help="Select mode of operation. Minify will prepare files for deployment, beautify will prepare files for development.", default=defaults.get("mode"))
    _option_group_general.add_argument("--format", type=str, help="Format string used to generate any output filename. (Dangerous!!)", default=defaults.get("format"))
    _option_group_general.add_argument("--overwrite", action="store_true", help="Allow overwrite of existing destination files in-place. Default is skip and warn. (Dangerous!!)", default=defaults.get("overwrite"))
    _option_group_general.add_argument("--on-change", action="store_true", help="Allow overwrite files only on source changed (detected by modify time).", default=defaults.get("on_change"))
    _option_group_general.add_argument("--verbose", action="store_true", help="Show more output during processing.", default=defaults.get("verbose"))
    _option_group_general.add_argument("--quiet", action="store_true", help="Show no output during processing.", default=defaults.get("quiet"))
    _option_group_general.add_argument("--dry-run", action="store_true", help="Never touch files, only log what would have been done (for debugging purposes)", default=defaults.get("dry_run"))
    _option_group_general.add_argument("--copy", action="store_true", help="Just copy files verbatime without processing them.", default=defaults.get("copy"))
    _option_group_general.add_argument("--force", action="store_true", help="Overwrite even if destination exists and is newer. (Dangerous!!)", default=defaults.get("force"))
    _option_group_general.add_argument("--diff", action="store_true", help="Log diff output for every file processed (warning: will be slow and output a lot of log).", default=defaults.get("diff"))
    _option_group_general.add_argument("--no-size-checks", action="store_true", help="Disable size sanity checks (detects and prevents run-away processors generating huge amounts of data", default=defaults.get("no_size_checks"))
    _option_group_general.add_argument("--size-max", action="store", type=int, dest="size_max", default=defaults.get("size_max"), metavar="NUM", help=f"Set maximum size of files to process in bytes.")
    _option_group_general.add_argument("--size-min", action="store", type=int, dest="size_min", default=defaults.get("size_min"), metavar="NUM", help=f"Set minimum size of files to process in bytes.")
    _option_group_general.add_argument("--nproc", action="store", type=int, dest="nproc", default=nproc, metavar="NUM", help=f"Set number of cores for multiprocessing (default is number of cores available which is {nproc} on this machine)")
    _option_group_general.add_argument("--gzip", action="store_true", help="Create a  GZIP compressed version of every non binary file processed with .gz suffix added.", default=defaults.get("gzip"))

    handlers = HandlerManager()
    valid_extensions = handlers.get_supported_extensions()
    handler_names = handlers.get_handler_names()

    for name in set(handler_names):
        _option_group_general.add_argument(f"--disable-type-{name}", action="store_true", dest=f"disable_type_{name}", default=False, help=f"Copy {name} files verbatim instead of processing them for given handler type")

    for name in set(valid_extensions):
        _option_group_general.add_argument(f"--disable-extension-{name}", action="store_true", dest=f"disable_extension_{name}", default=False, help=f"Copy {name} files verbatim instead of processing them for given filename extension")

    _option_group_general.add_argument("--output", type=str, help="Path to local output (file or folder).", default=defaults.get("output"))
    _option_group_general.add_argument("input", metavar="input", type=str, help="Path to local input (file or folder).", default=defaults.get("input"))

    _option_group_common = parser.add_argument_group("common", "Options common to many formats")
    _option_group_common.add_argument("--sort", action="store_true", help="Alphabetically sort CSS Properties (CSS).", default=defaults.get("sort"))
    _option_group_common.add_argument("--comments", action="store_true", help="Keep comments (CSS/HTML).", default=defaults.get("comments"))
    _option_group_common.add_argument("--timestamp", action="store_true", help="Add a timestamp in output files (CSS/HTML/SVG).", default=defaults.get("timestamp"))
    _option_group_common.add_argument("--wrap", action="store_true", help="Wrap output to ~80 chars per line (CSS).", default=defaults.get("wrap"))

    _option_group_optimization = parser.add_argument_group("svg optimization", "Optimization options that are only available for SVG")
    _option_group_optimization.add_argument("--set-precision", action="store", type=int, dest="digits", default=5, metavar="NUM", help="set number of significant digits (default: 5)")
    _option_group_optimization.add_argument("--set-c-precision", action="store", type=int, dest="cdigits", default=-1, metavar="NUM", help="set number of significant digits for control points " "(default: same as '--set-precision')")
    _option_group_optimization.add_argument("--disable-simplify-colors", action="store_false", dest="simple_colors", default=True, help="won't convert colors to #RRGGBB format")
    _option_group_optimization.add_argument("--disable-style-to-xml", action="store_false", dest="style_to_xml", default=True, help="won't convert styles into XML attributes")
    _option_group_optimization.add_argument("--disable-group-collapsing", action="store_false", dest="group_collapse", default=True, help="won't collapse <g> elements")
    _option_group_optimization.add_argument("--create-groups", action="store_true", dest="group_create", default=False, help="create <g> elements for runs of elements with identical attributes")
    _option_group_optimization.add_argument("--keep-editor-data", action="store_true", dest="keep_editor_data", default=False, help="won't remove Inkscape, Sodipodi, Adobe Illustrator " "or Sketch elements and attributes")
    _option_group_optimization.add_argument("--keep-unreferenced-defs", action="store_true", dest="keep_defs", default=False, help="won't remove elements within the defs container that are unreferenced")
    _option_group_optimization.add_argument("--renderer-workaround", action="store_true", dest="renderer_workaround", default=True, help="work around various renderer bugs (currently only librsvg) (default)")
    _option_group_optimization.add_argument("--no-renderer-workaround", action="store_false", dest="renderer_workaround", default=True, help="do not work around various renderer bugs (currently only librsvg)")

    _option_group_document = parser.add_argument_group("svg document", "Document options that are only available for SVG")
    _option_group_document.add_argument("--strip-xml-prolog", action="store_true", dest="strip_xml_prolog", default=False, help="won't output the XML prolog (<?xml ?>)")
    _option_group_document.add_argument("--remove-titles", action="store_true", dest="remove_titles", default=False, help="remove <title> elements")
    _option_group_document.add_argument("--remove-descriptions", action="store_true", dest="remove_descriptions", default=False, help="remove <desc> elements")
    _option_group_document.add_argument("--remove-metadata", action="store_true", dest="remove_metadata", default=False, help="remove <metadata> elements " "(which may contain license or author information etc.)")
    _option_group_document.add_argument("--remove-descriptive-elements", action="store_true", dest="remove_descriptive_elements", default=False, help="remove <title>, <desc> and <metadata> elements")
    _option_group_document.add_argument("--enable-comment-stripping", action="store_true", dest="strip_comments", default=False, help="remove all comments (<!-- -->)")
    _option_group_document.add_argument("--disable-embed-rasters", action="store_false", dest="embed_rasters", default=True, help="won't embed rasters as base64-encoded data")
    _option_group_document.add_argument("--enable-viewboxing", action="store_true", dest="enable_viewboxing", default=False, help="changes document width / height to 100pct / 100pct and creates viewbox coordinates")

    _option_group_formatting = parser.add_argument_group("svg output formatting", "Output formatting options that are only available for SVG")
    _option_group_formatting.add_argument("--indent", action="store", type=str, dest="indent_type", default="space", metavar="TYPE", help="indentation of the output: none, space, tab (default: space)")
    _option_group_formatting.add_argument("--nindent", action="store", type=int, dest="indent_depth", default=1, metavar="NUM", help="depth of the indentation, i.e. number of spaces / tabs: (default: 1)")
    _option_group_formatting.add_argument("--no-line-breaks", action="store_false", dest="newlines", default=True, help="do not create line breaks in output" '(also disables indentation; might be overridden by xml:space="preserve")')
    _option_group_formatting.add_argument("--strip-xml-space", action="store_true", dest="strip_xml_space_attribute", default=False, help='strip the xml:space="preserve" attribute from the root SVG element')

    _option_group_ids = parser.add_argument_group("svg id attributes", "ID attribute options that are only available for SVG")
    _option_group_ids.add_argument("--enable-id-stripping", action="store_true", dest="strip_ids", default=False, help="remove all unreferenced IDs")
    _option_group_ids.add_argument("--shorten-ids", action="store_true", dest="shorten_ids", default=False, help="shorten all IDs to the least number of letters possible")
    _option_group_ids.add_argument("--shorten-ids-prefix", action="store", type=str, dest="shorten_ids_prefix", default="", metavar="PREFIX", help="add custom prefix to shortened IDs")
    _option_group_ids.add_argument("--protect-ids-noninkscape", action="store_true", dest="protect_ids_noninkscape", default=False, help="don't remove IDs not ending with a digit")
    _option_group_ids.add_argument("--protect-ids-list", action="store", type=str, dest="protect_ids_list", metavar="LIST", help="don't remove IDs given in this comma-separated list")
    _option_group_ids.add_argument("--protect-ids-prefix", action="store", type=str, dest="protect_ids_prefix", metavar="PREFIX", help="don't remove IDs starting with the given prefix")

    _option_group_compatibility = parser.add_argument_group("svg compatability checks", "Compatibility check options that are only available for SVG")
    _option_group_compatibility.add_argument("--error-on-flowtext", action="store_true", dest="error_on_flowtext", default=False, help="exit with error if the input SVG uses non-standard flowing text " "(only warn by default)")

    return parser.parse_args()
