[![pipeline status](https://gitlab.com/octomy/web-minify/badges/production/pipeline.svg)](https://gitlab.com/octomy/web-minify/-/commits/production)
<!---
                                                         
                                                         
     ## ## ## ## ## ## ## ## ## ## ##                    
        ## ## ## ## ## ## ## ## ##                       
           ## ## ## ## ## ## ##                          
              ## ## ## ## ##                             
                 ## ## ##                                
                    ##                                   
                                                         
                                                         
WARNING: This file is AUTO GENERATED from "tpl_README.md".
         Any changes you make will be OVERWRITTEN at the 
         next invocation of `make readme`                
                                                         
                                                         
                    ##                                   
                 ## ## ##                                
              ## ## ## ## ##                             
           ## ## ## ## ## ## ##                          
        ## ## ## ## ## ## ## ## ##                       
     ## ## ## ## ## ## ## ## ## ## ##                    
                                                         
                                                         
-->
# About web-minify (version 1.1.2-test-development)

<img src="https://gitlab.com/octomy/web-minify/-/raw/production/design/logo-1024.png" width="20%"/>

__web-minify__ is the all-in-one just-works-out-of-the-box does-what-you-want highly-opinionated web minifier&trade;

- web-minify is [available on gitlab](https://gitlab.com/octomy/web-minify).

## Goals of this tool:

> NOTE: We have not reached all these goals yet, please see next sections.

| Goal   |      Status |
|--------|-------------|
| All-in-one compressor/obfuscator/minifier/cruncher for most of the common static web formats | See [list of supported formats](#supported-formats). | ✅ |
| Installable via PyPi on platforms supported by Python 3+ | ✅ |
| No dependencies on large non-python tool such as nodejs | ✅ |
| Support for images formats such as [.png](https://en.wikipedia.org/wiki/Portable_Network_Graphics) and [.jpeg](https://en.wikipedia.org/wiki/JPEG) | ✅ |
| Support for vector graphics formats such as [.svg](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) | ✅ |
| Support for style sheet formats such as .css and [.sass](https://en.wikipedia.org/wiki/Sass_(stylesheet_language) | ✅ |
| Support for script formats such as .js | ✅ |
| Support for template formats such as .jinja | ✅ |
| Support for markup formats such as .html | ✅ |
| Handle intertwined formats such as JS and CSS inside HTML | ❌ |
| Does what you hoped by default (i.e. highly opinionated) | ✅ |
| Can be tweaked to do what you didn't want (i.e. flexible) | ✅ |
| Small and dependency free (i.e. implemented in pure python if possible) | Only tested/used on Linux. There is hope for OSX/BSD/Posix but YMMV on Windows. |
| Available as library as well as command-line tool | ✅ |
| Easily extensible; adding another backend can be done by writing one function | ✅ |
| Cross platform, supports many Python 3.x versions | Only tested on Python 3.7 |


# Getting started

__web-minify__ can be used and hacked on in a myriad of different ways. 

## Use web-minify as a module from your code

web-minify is [available in PyPI](https://pypi.org/project/web-minify/).

```shell
# Install web-minify into your current Python environment
pip install web-minify

```

Now you can access it's features from your code:

<details>

```Python
import web_minify

settings = {
    "input": "my_originals_dir/",
    "output": "my_processed_dir/",
}

# Instanciate processor with settings we want to use
p = web_minify.processor.Processor(settings)


# Process files as per settings (this is equivalent to the commandline mode)
p. process_file()


# Process a list of files relative to input, and output them depending on settings
p. process_files_list(["input_file.svg", "input_file.html"])


# Process a single file (disregard input/output from settings
p.process_file("some_input_file.svg", "some_output_file.svg")

```

</details>


## Use web-minify as a command line tool

web-minify is [available in PyPI](https://pypi.org/project/web-minify/).

```shell
# Install web-minify into your current Python environment
pip install web-minify

```

```shell
# Run the web-minify cli tool with help argument to see detailed usage
web-minify --help

```


The output looks like this:

<details>

```shell
$ ./web-minify.py --help

usage: web-minify.py [-h] [--version] [--mode {Mode.minify,Mode.beautify}]
                     [--format FORMAT] [--overwrite] [--on-change] [--verbose]
                     [--quiet] [--dry-run] [--copy] [--force] [--diff]
                     [--no-size-checks] [--size-max NUM] [--size-min NUM]
                     [--nproc NUM] [--gzip] [--disable-type-svg]
                     [--disable-type-sql] [--disable-type-json]
                     [--disable-type-css] [--disable-type-png]
                     [--disable-type-sass] [--disable-type-html]
                     [--disable-type-jinja] [--disable-type-js]
                     [--disable-type-jpeg] [--disable-extension-svg]
                     [--disable-extension-jinja2]
                     [--disable-extension-template] [--disable-extension-sql]
                     [--disable-extension-pgsql] [--disable-extension-jpg]
                     [--disable-extension-css] [--disable-extension-json]
                     [--disable-extension-htm] [--disable-extension-png]
                     [--disable-extension-tpl] [--disable-extension-sass]
                     [--disable-extension-html] [--disable-extension-scss]
                     [--disable-extension-j2] [--disable-extension-jinja]
                     [--disable-extension-js] [--disable-extension-jpeg]
                     [--output OUTPUT] [--sort] [--comments] [--timestamp]
                     [--wrap] [--set-precision NUM] [--set-c-precision NUM]
                     [--disable-simplify-colors] [--disable-style-to-xml]
                     [--disable-group-collapsing] [--create-groups]
                     [--keep-editor-data] [--keep-unreferenced-defs]
                     [--renderer-workaround] [--no-renderer-workaround]
                     [--strip-xml-prolog] [--remove-titles]
                     [--remove-descriptions] [--remove-metadata]
                     [--remove-descriptive-elements]
                     [--enable-comment-stripping] [--disable-embed-rasters]
                     [--enable-viewboxing] [--indent TYPE] [--nindent NUM]
                     [--no-line-breaks] [--strip-xml-space]
                     [--enable-id-stripping] [--shorten-ids]
                     [--shorten-ids-prefix PREFIX] [--protect-ids-noninkscape]
                     [--protect-ids-list LIST] [--protect-ids-prefix PREFIX]
                     [--error-on-flowtext]
                     input

optional arguments:
  -h, --help            show this help message and exit

general:
  General options for this program

  --version             show program's version number and exit
  --mode {Mode.minify,Mode.beautify}
                        Select mode of operation. Minify will prepare files
                        for deployment, beautify will prepare files for
                        development.
  --format FORMAT       Format string used to generate any output filename.
                        (Dangerous!!)
  --overwrite           Allow overwrite of existing destination files in-
                        place. Default is skip and warn. (Dangerous!!)
  --on-change           Allow overwrite files only on source changed (detected
                        by modify time).
  --verbose             Show more output during processing.
  --quiet               Show no output during processing.
  --dry-run             Never touch files, only log what would have been done
                        (for debugging purposes)
  --copy                Just copy files verbatime without processing them.
  --force               Overwrite even if destination exists and is newer.
                        (Dangerous!!)
  --diff                Log diff output for every file processed (warning:
                        will be slow and output a lot of log).
  --no-size-checks      Disable size sanity checks (detects and prevents run-
                        away processors generating huge amounts of data
  --size-max NUM        Set maximum size of files to process in bytes.
  --size-min NUM        Set minimum size of files to process in bytes.
  --nproc NUM           Set number of cores for multiprocessing (default is
                        number of cores available which is 24 on this machine)
  --gzip                Create a GZIP compressed version of every non binary
                        file processed with .gz suffix added.
  --disable-type-svg    Copy svg files verbatim instead of processing them for
                        given handler type
  --disable-type-sql    Copy sql files verbatim instead of processing them for
                        given handler type
  --disable-type-json   Copy json files verbatim instead of processing them
                        for given handler type
  --disable-type-css    Copy css files verbatim instead of processing them for
                        given handler type
  --disable-type-png    Copy png files verbatim instead of processing them for
                        given handler type
  --disable-type-sass   Copy sass files verbatim instead of processing them
                        for given handler type
  --disable-type-html   Copy html files verbatim instead of processing them
                        for given handler type
  --disable-type-jinja  Copy jinja files verbatim instead of processing them
                        for given handler type
  --disable-type-js     Copy js files verbatim instead of processing them for
                        given handler type
  --disable-type-jpeg   Copy jpeg files verbatim instead of processing them
                        for given handler type
  --disable-extension-svg
                        Copy svg files verbatim instead of processing them for
                        given filename extension
  --disable-extension-jinja2
                        Copy jinja2 files verbatim instead of processing them
                        for given filename extension
  --disable-extension-template
                        Copy template files verbatim instead of processing
                        them for given filename extension
  --disable-extension-sql
                        Copy sql files verbatim instead of processing them for
                        given filename extension
  --disable-extension-pgsql
                        Copy pgsql files verbatim instead of processing them
                        for given filename extension
  --disable-extension-jpg
                        Copy jpg files verbatim instead of processing them for
                        given filename extension
  --disable-extension-css
                        Copy css files verbatim instead of processing them for
                        given filename extension
  --disable-extension-json
                        Copy json files verbatim instead of processing them
                        for given filename extension
  --disable-extension-htm
                        Copy htm files verbatim instead of processing them for
                        given filename extension
  --disable-extension-png
                        Copy png files verbatim instead of processing them for
                        given filename extension
  --disable-extension-tpl
                        Copy tpl files verbatim instead of processing them for
                        given filename extension
  --disable-extension-sass
                        Copy sass files verbatim instead of processing them
                        for given filename extension
  --disable-extension-html
                        Copy html files verbatim instead of processing them
                        for given filename extension
  --disable-extension-scss
                        Copy scss files verbatim instead of processing them
                        for given filename extension
  --disable-extension-j2
                        Copy j2 files verbatim instead of processing them for
                        given filename extension
  --disable-extension-jinja
                        Copy jinja files verbatim instead of processing them
                        for given filename extension
  --disable-extension-js
                        Copy js files verbatim instead of processing them for
                        given filename extension
  --disable-extension-jpeg
                        Copy jpeg files verbatim instead of processing them
                        for given filename extension
  --output OUTPUT       Path to local output (file or folder).
  input                 Path to local input (file or folder).

common:
  Options common to many formats

  --sort                Alphabetically sort CSS Properties (CSS).
  --comments            Keep comments (CSS/HTML).
  --timestamp           Add a timestamp in output files (CSS/HTML/SVG).
  --wrap                Wrap output to ~80 chars per line (CSS).

svg optimization:
  Optimization options that are only available for SVG

  --set-precision NUM   set number of significant digits (default: 5)
  --set-c-precision NUM
                        set number of significant digits for control points
                        (default: same as '--set-precision')
  --disable-simplify-colors
                        won't convert colors to #RRGGBB format
  --disable-style-to-xml
                        won't convert styles into XML attributes
  --disable-group-collapsing
                        won't collapse <g> elements
  --create-groups       create <g> elements for runs of elements with
                        identical attributes
  --keep-editor-data    won't remove Inkscape, Sodipodi, Adobe Illustrator or
                        Sketch elements and attributes
  --keep-unreferenced-defs
                        won't remove elements within the defs container that
                        are unreferenced
  --renderer-workaround
                        work around various renderer bugs (currently only
                        librsvg) (default)
  --no-renderer-workaround
                        do not work around various renderer bugs (currently
                        only librsvg)

svg document:
  Document options that are only available for SVG

  --strip-xml-prolog    won't output the XML prolog (<?xml ?>)
  --remove-titles       remove <title> elements
  --remove-descriptions
                        remove <desc> elements
  --remove-metadata     remove <metadata> elements (which may contain license
                        or author information etc.)
  --remove-descriptive-elements
                        remove <title>, <desc> and <metadata> elements
  --enable-comment-stripping
                        remove all comments (<!-- -->)
  --disable-embed-rasters
                        won't embed rasters as base64-encoded data
  --enable-viewboxing   changes document width / height to 100pct / 100pct and
                        creates viewbox coordinates

svg output formatting:
  Output formatting options that are only available for SVG

  --indent TYPE         indentation of the output: none, space, tab (default:
                        space)
  --nindent NUM         depth of the indentation, i.e. number of spaces /
                        tabs: (default: 1)
  --no-line-breaks      do not create line breaks in output(also disables
                        indentation; might be overridden by
                        xml:space="preserve")
  --strip-xml-space     strip the xml:space="preserve" attribute from the root
                        SVG element

svg id attributes:
  ID attribute options that are only available for SVG

  --enable-id-stripping
                        remove all unreferenced IDs
  --shorten-ids         shorten all IDs to the least number of letters
                        possible
  --shorten-ids-prefix PREFIX
                        add custom prefix to shortened IDs
  --protect-ids-noninkscape
                        don't remove IDs not ending with a digit
  --protect-ids-list LIST
                        don't remove IDs given in this comma-separated list
  --protect-ids-prefix PREFIX
                        don't remove IDs starting with the given prefix

svg compatability checks:
  Compatibility check options that are only available for SVG

  --error-on-flowtext   exit with error if the input SVG uses non-standard
                        flowing text (only warn by default)

    ---------------------------------------------------------
             __             _      _ ___    
 _    _____ / /  ______ _  (_)__  (_) _/_ __
| |/|/ / -_) _ \/___/  ' \/ / _ \/ / _/ // /
|__,__/\__/_.__/   /_/_/_/_/_//_/_/_/ \_, / 
                                     /___/  
v1.1.2

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
    + {EXT}
    + {HASH}
    + {PATH}
    + {BASE}
 

```

</details>

## Developing web-minify

web-minify is [available on gitlab](https://gitlab.com/octomy/web-minify).

__web-minify welcomes PRs!__ If you want to contribute we welcome your code contriburtions! We are proud of the fact that this project is a true meritocracy.

Example: extending web-minify to support additional formats is done by a very simple interface:

1. Put a module under `web-minify/web_minify/handlers/your_format`. This can either be a module folder or python module source file. See [css/](web_minify/handlers/css) or [html.py](web_minify/handlers/html.py) for example implementations.
2. Include the new function in `__all__` in `web-minify/web_minify/handlers/__init__.py`
3. Register the new function in `self.processor_map` in `web-minify/web_minify/processor.py`

Easy as 🥧!


### Supported formats
Already supported Formats:


| Format   |       | minify | beautify | Tests |
|----------|-------|--------|----------|-------|
| *.html, *htm, *.tpl |  Hypertext Markup Language | ✅ | ✅ | ❌ |
| *.css | Cascading Style Sheets | ✅ | ❌ | ❌ |
| *.js | JavaScript | ✅✝ | ✅ | ❌ |
| *.json | JavaScript Object Notation | ✅ | ✅ | ❌ |
| *.sass | Syntactically Awesome Style Sheets | ✅ | ❌ | ❌ |
| *.scss | Syntactically Awesome Style Sheets (modern syntax) | ✅ | ❌ | ❌ |
| *.png | Portable Network Graphics | ✅ | ❌ | ❌ |
| *.jpg, *.jpeg | Joint Photographic Experts Group | ✅ | ❌ | ❌ |
| *.svg | Scalable Vector Graphics | ✅ | ❌ | ❌ |
| *.sql | Structured Query Language | ❌ | ✅ | ❌ |
| *.your_file | web-minify is made to be [extensible](#Developing-web-minify) | ✅✝✝ | ✅✝✝ | ✅✝✝ |

_✝Buggy for modern syntax features_
_✝✝Submit your PR!_


# License

Complete license is in the file [LICENSE](LICENSE) in the root of the git repo.

> GNU GPL and GNU LGPL or MIT.
> This work is free software: You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This work is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; Without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this work.



# Other Notable Features

1. Supports recursive scanning of directories
2. Supports spitting out .gz versions of files to speed up serving of static files
3. Supports some controls over each format's processing
4. Supports change detection and watch mode
5. Made to be somewhat [extensible](#extending-web-minify)

# Known Limitations and Problems:

1. Compression of modern .js haves some bugs. We welcome PRs!
2. Some of the usage patterns of the command line tool are not implemented yet. We welcome PRs!
3. Codebase has ZERO tests. We welcome PRs!
