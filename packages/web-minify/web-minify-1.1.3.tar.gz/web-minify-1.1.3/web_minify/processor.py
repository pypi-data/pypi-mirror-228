import os
import pprint
import datetime
import time
import zlib
import difflib
import colorama
from .files import path_is_in_path, generate_file_list, determine_file_extension
from .handlers import HandlerManager, append_and_return
from pathos.multiprocessing import cpu_count
from .time import human_delta
from .modes import Mode

import resource

# resource.setrlimit(resource.RLIMIT_NOFILE, (5000,-1))

now = time.time()
now_ns = time.time_ns()

# from multiprocessing import Pool, cpu_count
from pathos.multiprocessing import ProcessingPool as Pool

import logging

logger = logging.getLogger(__name__)


gzip_suffix = ".gz"


try:
    colorama.init()
except ImportError:  # fallback so that the imported classes always exist

    class ColorFallback:
        __getattr__ = lambda self, name: ""

    colorama.Fore = colorama.Back = colorama.Style = ColorFallback()


def b2s(b):
    # return "✅" if b else "❌"
    return "☑️" if b else "-"


def vertical_header(sp, stati):
    logger.info("")
    # stati=["success", "gzip"]
    longest = 0
    for s in stati:
        longest = len(s) if len(s) > longest else longest
    r = list(range(longest))
    # logger.info(f"longest={longest}, r={r}")
    for y in r:
        line = ""
        for s in stati:
            sl = len(s)
            d = longest - len(s)
            cond = y >= d
            # logger.info(f"s={s}, sl={sl}, y={y}, longest={longest}, d={d}, cond={cond}")
            line += s[y - d] if cond else " "
            line += sp
        logger.info(line)


def table_heads(table):
    heads = set()
    for row_key, row_value in table.items():
        heads.update(row_value.keys())
    return heads


def normalize_tabdata(table, heads, remove=[]):
    out = []
    for row_key, row_value in table.items():
        row_out = []
        for head in heads:
            if not head in remove:
                value = row_value.get(head, "")
            row_out.append(value)
        out.append(row_out)
    return out


def table_widts(table, heads=[]):
    num = 0
    for row in table:
        c = len(row)
        num = max(c, num)
    c = len(heads)
    num = max(c, num)
    cols = [0] * num
    for index, col in enumerate(heads):
        l = len(f"{col}")
        m = max(l, cols[index])
        cols[index] = m
    for row in table:
        for index, col in enumerate(row):
            l = len(f"{col}")
            m = max(l, cols[index])
            cols[index] = m
    return cols


def log_table(name, table, remove=[]):
    # fmt:off
    heads_short_table = {
        "extension": "ext"
        , "type": "typ"
        , "success": "OK"
        , "failed": "E"
        , "written": "💾"
        , "changed": "Δ"
        , "copied": "cp"
        , "overwritten": "✏️"
        , "new": "🆕"
        , "processed": "🏭"
        , "binary": "bin"
        , "gzip": "gz"
        , "skipped": "⏭"
        , "handler_disabled": "hX"
        , "extension_disabled": "eX"
        , "empty": "Ø"
        , "size_error": "ES"
        , "time": "⏲"
        , "slow":"zzz"
        }
    # fmt:on
    heads = [head for head in heads_short_table.keys() if head not in remove]
    heads_short = [heads_short_table[head] for head in heads if head not in remove]
    use_heads = heads
    norm = normalize_tabdata(table, heads)
    widths = table_widts(norm, use_heads)
    fmt = ""
    lt = 0
    inner_wall = " "
    inner_wall_len = len(inner_wall)
    outer_wall = "|"
    outer_wall_len = len(outer_wall)
    fmt += outer_wall
    lt += outer_wall_len
    for index, head in enumerate(use_heads):
        l = widths[index]  # len(head)
        lt += l + inner_wall_len + 1
        fmt += f"{inner_wall}{{:<{l}}} "
    fmt += outer_wall
    lt += outer_wall_len
    logger.info("+" + "-" * (lt - 2) + "+")
    logger.info(fmt.format(*use_heads))
    logger.info("+" + "-" * (lt - 2) + "+")
    for row_value in norm:
        vals = []
        for value in row_value:
            t = type(value)
            if t is datetime.timedelta:
                value = human_delta(value)
            elif t is bool:
                value = b2s(value)
            vals.append(value)
        logger.info(fmt.format(*vals))
    logger.info("+" + "-" * (lt - 2) + "+")


def log_summary(summary):
    ft = {"by_extension": ["type"], "by_type": ["extension"]}
    for k, v in ft.items():
        table = summary.get(k, {}.copy())
        logger.info(f"")
        logger.info(f"{k}:")
        log_table(k, table, v)
        logger.info(f"")


def log_files(results):
    # fmt:off
    keys=[
      'success'
    , 'copied'
    , 'written'
    , 'overwritten'
    , 'new'
    , 'processed'
    , 'changed'
    , 'empty'
    , 'skipped'
    , "handler_disabled"
    , "extension_disabled"
    , 'size_error'
    , 'binary'
    , 'gzip'
    , 'slow'
    , 'size'
    ]
    # fmt:on
    sp = " " * 2
    # logger.info(f"Processing '{input_path}' -->[{self.mode.value}]--> '{output_path}'")
    vertical_header(sp, keys)
    keys.remove("size")
    fct = 0
    header_interval = 10
    for result in results:
        if fct > header_interval:
            fct -= header_interval
            vertical_header()
        s = result.get("status")
        output_path = result.get("output_path")
        size_percentage = result.get("size_percentage", "N/A")
        line = ""
        for k in keys:
            v = b2s(s[k])
            line += f"{v}{sp}"
        line += f"{size_percentage: <3.1f}%{sp}'{output_path}'"
        logger.info(line)
        fct += 1


def color_diff(diff):
    for line in diff:
        if line.startswith("+"):
            yield colorama.Fore.GREEN + line + colorama.Fore.RESET
        elif line.startswith("-"):
            yield colorama.Fore.RED + line + colorama.Fore.RESET
        elif line.startswith("^"):
            yield colorama.Fore.BLUE + line + colorama.Fore.RESET
        else:
            yield line


def sanity_bounds(handler_name: str):
    K = 1024
    M = K * K
    G = M * K
    # fmt:off
    bounds = {
        "html": {
              "max": 1 * M
            , "min": 0
            , "offset": 64
            , "percentage": 100
        }
    }
    # fmt:on
    # Trivial reject on types we don't care about
    return bounds.get(handler_name, None)


def size_sanity_check(original_size: int, processed_size: int, handler_name: str):
    bounds = sanity_bounds(handler_name)
    percentage = (processed_size * 100) / (original_size if original_size > 0 else 1)
    offset = bounds.get("offset", 0) if bounds else 0
    check_percentage = ((processed_size + offset) * 100) / ((original_size if original_size > 0 else 1) + offset)
    if False:
        logger.info(f"### Size sanity check for {original_size} vs. {processed_size} with {handler_name} had percentage {percentage: <3.1f}%")
        logger.info(pprint.pformat(bounds))
        logger.info("### Bounds:")
        logger.info(pprint.pformat(bounds))
    # Trivial reject on missing bounds (we only test for types we care about)
    if not bounds:
        return True, percentage, None
    # Reject on max/min bound
    if processed_size > bounds["max"]:
        return False, percentage, f"Processed size {processed_size} was above type max {bounds['max']}"
    if processed_size < bounds["min"]:
        return False, percentage, f"Processed size {processed_size} was below type min {bounds['min']}"
    # Reject on percentage min/max bound
    if check_percentage > 100 + bounds["percentage"]:
        return False, percentage, f"Processed size percentage {percentage: <3.1f}% was above type max {100 + bounds['percentage']: <3.1f}%"
    if check_percentage < 100 - bounds["percentage"]:
        return False, percentage, f"Processed size percentage {percentage: <3.1f}% was below type min {100 - bounds['percentage']: <3.1f}%"
    # All tests passed
    return True, percentage, None


class Processor:
    def __init__(self, settings: dict):
        self.settings: dict = settings
        self.input: str = settings.get("input", None)
        self.output: str = settings.get("output", None)
        self.input_is_dir: bool = self.input and os.path.isdir(self.input)
        self.input_exists: bool = self.input and os.path.exists(self.input)
        self.output_is_dir: bool = self.output and os.path.isdir(self.output)
        self.output_exists: bool = self.output and os.path.exists(self.output)
        self.mode: Mode = Mode(settings.get("mode", "minify"))
        self.copy: bool = settings.get("copy", False)
        self.diff: bool = settings.get("diff", False)
        self.format: bool = settings.get("format", False)
        self.overwrite: bool = settings.get("overwrite", False)
        self.on_change: bool = settings.get("on_change", False)
        self.prefix: bool = settings.get("prefix", False)
        self.gzip: bool = settings.get("gzip", False)
        self.hash: bool = settings.get("hash", False)
        self.verbose: bool = settings.get("verbose", False)
        self.quiet: bool = settings.get("quiet", False)
        self.force: bool = settings.get("force", False)
        self.dry_run: bool = settings.get("dry_run", False)
        self.nproc: int = settings.get("nproc", 1)
        self.ncore: int = cpu_count()
        self.size_min: int = settings.get("size_min", 0)
        self.size_max: int = settings.get("size_max", 0)
        self.no_size_checks: bool = settings.get("no_size_checks", False)

        self.handlers = HandlerManager()
        self.handlers.prepare_handlers(self.settings)

        self.valid_extensions = self.handlers.get_supported_extensions()
        self.handler_names = self.handlers.get_handler_names()
        self.string_type = type("")
        self.bytes_type = type(b"")

        if self.verbose:
            logger.info("### Settings:")
            logger.info(pprint.pformat(self.settings))
            logger.info("### Handlers & extensions:")
            for handler_name in self.handler_names:
                handler = self.handlers.get_handler_by_name(handler_name)
                extensions = handler.extensions()
                logger.info(f"# {handler_name}:")
                for extension in extensions:
                    logger.info(f"   .{extension}:")
        self.pool = None
        self.sane, self.sane_message = self._sanity_checks()

    def sanity_checks(self):
        return self.sane, self.sane_message

    def _sanity_checks(self):
        valid_modes = list(Mode)
        if not self.mode in valid_modes:
            return (False, f"The specified mode {self.mode} was not valid. NOTE: Valid modes are {pprint.pformat(valid_modes)}")
        if not self.input or not self.input_exists:
            return (False, f"The input specified '{self.input}' did not exist. Input must be an existing directory or file")
        if not self.overwrite and self.on_change:
            return (False, f"On-change will not have an effect so long as overwrite is not enabled")
        if not self.output and not self.overwrite and not self.format:
            return (False, f"Only input '{self.input}' was specified. Without a setting for 'output', 'overwrite' and/or 'format' all processing will fail")
        if self.output_is_dir and path_is_in_path(self.input, self.output):
            return (False, f"The output '{self.output}' is a subpath of input '{self.input}'")
        if self.input_is_dir and path_is_in_path(self.output, self.input):
            return (False, f"The input '{self.input}' is a subpath of output '{self.output}'")
        return True, None

    def process_file(self, input_path: str, output_path: str, now_ns=now_ns):
        encoding = "utf-8"
        # fmt:off
        status={
              "gzip": False
            , "changed": False
            , "copied": False
            , "processed": False
            , "overwritten": False
            , "new": False
            , "written": False
            , "binary": False
            , "skipped": False
            , "handler_disabled": False
            , "extension_disabled": False
            , "empty": False
            , "size_error": False
            , "size_percentage": 100
            , "extension": ""
            , "type": ""
        }
        # fmt:on
        messages = []
        if not input_path:
            return False, status, append_and_return(messages, "No input path specified")
        if not output_path:
            return False, status, append_and_return(messages, "No output path specified")
        handler = None
        is_binary = True
        extension, extension_recognized = determine_file_extension(input_path)
        status["extension"] = extension
        handler = self.handlers.get_handler_by_extension(extension)
        if handler:
            status["type"] = handler.name()
            is_binary = handler.is_binary()
            status["binary"] = is_binary
        input_stat = os.stat(input_path)
        output_stat = None
        if os.path.isfile(output_path):
            if not self.overwrite:
                return False, status, append_and_return(messages, "Trying to overwrite without overwrite enabled")
            if self.on_change:
                output_stat = os.stat(output_path)
                if not self.force:
                    if input_stat.st_mtime_ns == output_stat.st_mtime_ns:
                        status["skipped"] = True
                        return True, status, append_and_return(messages, "File not changed, skipping")
                    elif output_stat.st_mtime_ns > input_stat.st_mtime_ns:
                        status["skipped"] = True
                        return True, status, append_and_return(messages, f"Destination file newer than input, skipping ({output_stat.st_mtime_ns} >= {input_stat.st_mtime_ns})")
                else:
                    status["overwritten"] = True
        elif os.path.isdir(output_path):
            return False, status, append_and_return(messages, f"Output path {output_path} was a directory")
        else:
            output_dir = os.path.dirname(output_path)
            if not os.path.isdir(output_dir):
                os.makedirs(name=output_dir, exist_ok=True)
            if not os.path.isdir(output_dir):
                return False, status, append_and_return(messages, "Output directory did not exist or could not be created")
            status["new"] = True
        is_vip_file = False
        if not extension_recognized:
            # Skip well known files with unsupported file extensions
            base_name = os.path.basename(input_path)
            if base_name in ["sitemap.xml", "favicon.ico", "robots.txt"]:
                is_vip_file = True
            else:
                return False, status, append_and_return(messages, f"Unknown extension '{extension}' for input file")
        elif not handler:
            return False, status, append_and_return(messages, f"Could not find handler for input file with extension {extension}")
        # TODO: refactor to use stat instead of individual calls to getmsize and similar
        original_content = None
        original_file_size = os.path.getsize(input_path)
        if original_file_size < self.size_min:
            status["skipped"] = True
            return True, status, append_and_return(messages, "File size less than minimum {self.size_min}")
        elif original_file_size > self.size_max:
            status["skipped"] = True
            return True, status, append_and_return(messages, "File size more than maximum {self.size_max}")
        try:
            with open(input_path, "rb") if is_binary else open(input_path, "r", encoding=encoding) as in_file:
                original_content = in_file.read()
        except Exception as err:
            return False, status, append_and_return(messages, f"Could not load data from input file: {err}")
        if not original_content:
            messages = append_and_return(messages, f"Input file was empty")
            status["empty"] = True
        original_size = len(original_content)
        processed_content = None
        handler_status = False
        handler_messages = None
        handler_name = handler.name() if handler else None
        if not handler_name:
            return False, status, append_and_return(messages, f"Handler had no name")
        handler_disabled = handler_name in self.handler_names and self.settings.get(f"disable_type_{handler_name}", False)
        extension_disabled = extension in self.valid_extensions and self.settings.get(f"disable_suffix_{extension}", False)
        status["handler_disabled"] = handler_disabled
        status["extension_disabled"] = extension_disabled
        do_copy = self.copy or handler is None or is_vip_file or handler_disabled or extension_disabled
        processed_size = 0
        if do_copy:
            # Perform copy
            if self.verbose:
                logger.info(f"Supposed to copy: {input_path} ({extension})")
            processed_content = original_content
            processed_size = original_size
            status["copied"] = True
        else:
            # logger.info(f"SUPPOSED TO PROCESS: {input_path} ({extension})")
            ret_tup = "NON"
            try:
                ret_tup = handler.process(original_content, input_path)
                handler_status, processed_content, handler_messages = ret_tup
            except Exception as e:
                logger.exception(f"Handler {handler_name} failed with return {ret_tup}")
                return False, status, append_and_return(messages, f"Handler {handler_name} failed with exception: '{e}'")
            messages = append_and_return(messages, handler_messages)
            if None == processed_content:
                messages = append_and_return(messages, f"Processed file was empty")
                status["empty"] = True
            else:
                processed_size = len(processed_content)
            status["processed"] = True
        # logger.info(f"Content of file {input_path} was of type {type(original_content)} while processed {type(processed_content)}")
        if not handler_status:
            return False, status, append_and_return(messages, f"Handler {handler_name} returned fatal error")
        content_type = type(processed_content)
        expected_type = self.bytes_type if is_binary else self.string_type
        if content_type is not expected_type:
            if self.verbose:
                logger.error(f"processed_content: {processed_content}")
            return False, status, append_and_return(messages, f"Processed content in unexpected type: '{content_type}' instead of '{expected_type}'")
        if self.diff:
            if self.verbose:
                logger.info(f"NAME diff: \nIN= {input_path}\nOUT={output_path}")
                logger.info(f"TYPE diff: {type(original_content)} vs. {type(processed_content)}")
                logger.info(f"SIZE diff: {len(original_content)} vs. {len(processed_content)}")
            logger.info(f"CONTENT diff:")
            sep = "\n"
            logger.info("\n".join(color_diff(difflib.ndiff(original_content.split(sep), processed_content.split(sep)))))
            diffed_path = input_path + ".diffed.html"
            with open(diffed_path, "wb") if is_binary else open(diffed_path, "w", encoding=encoding) as diff_file:
                written = diff_file.write(processed_content)
                logger.info("WRITE {written} bytes of diffed file")
        size_status, size_percentage, size_message = size_sanity_check(original_size, processed_size, handler_name)
        status["size_percentage"] = size_percentage
        if not size_status:
            status["size_error"] = True
            processed_size = original_size
            messages = append_and_return(messages, size_message)
            if not self.no_size_checks:
                processed_content = original_content
        if None == processed_content:
            messages = append_and_return(messages, f"Processed file was empty")
            status["empty"] = True
        status["changed"] = original_content != processed_content
        try:
            if not self.dry_run:
                with open(output_path, "wb") if is_binary else open(output_path, "w", encoding=encoding) as out_file:
                    written = out_file.write(processed_content)
                    if written != len(processed_content):
                        return False, status, append_and_return(messages, f"Partially written output ({written} of {len(processed_content)} bytes)")
                    status["written"] = True
        except Exception as err:
            return False, status, append_and_return(messages, f"Could not write data to output file: {err}")
        try:
            if not self.dry_run:
                # If source and destination is identical then there will be no change in time, so in that case we induce it  by using "now"
                final_time = input_stat.st_mtime_ns if output_path is not input_path else now_ns
                os.utime(output_path, ns=(final_time, final_time))
        except Exception as err:
            return False, status, append_and_return(messages, f"Could not modify date of output file: {err}")
        if self.gzip:
            gzip_path = f"{output_path}{gzip_suffix}"
            try:
                if not self.dry_run and not is_binary:
                    with open(gzip_path, "wb") as gzip_file:
                        gzip_content = zlib.compress(processed_content.encode(encoding), level=9)
                        if self.verbose:
                            logger.info(f"Producing gzip file'{gzip_path}'")
                        gzip_written = gzip_file.write(gzip_content)
                        if gzip_written != len(gzip_content):
                            return False, status, append_and_return(messages, f"Partially written gzip output ({gzip_written} of {len(gzip_content)} bytes)")
                        status["gzip"] = True
            except Exception as err:
                return False, status, append_and_return(messages, f"Could not write gzip data to output file: {err}")
            try:
                if not self.dry_run and status.get("gzip", False):
                    os.utime(gzip_path, ns=(input_stat.st_mtime_ns, input_stat.st_mtime_ns))
            except Exception as err:
                return False, status, append_and_return(messages, f"Could not modify date of gzip file: {err}")
        # All went well, go home happy!
        return True, status, messages

    def process_files_list_item_wrapper(self, item):
        input_path = item["input_path"]
        output_path = item["output_path"]
        single_start_time = datetime.datetime.now()
        result = {}
        result["success"], result["status"], result["messages"] = self.process_file(input_path=input_path, output_path=output_path)
        result["status"]["success"] = result.get("success", False)
        result["status"]["failed"] = not result.get("success", False)
        result["input_path"] = input_path
        result["size_percentage"] = result["status"].get("size_percentage", "N/A")
        result["output_path"] = output_path
        result["single_start_time"] = single_start_time
        single_end_time = datetime.datetime.now()
        single_interval = single_end_time - single_start_time
        result["single_end_time"] = single_end_time
        result["single_interval"] = single_interval
        slow = single_interval > datetime.timedelta(seconds=1)
        result["status"]["slow"] = slow
        result["status"]["time"] = single_interval
        if slow:
            result["messages"].extend([f"Processing was slow ({human_delta(result.get('single_interval'))})"])
        return result

    def process_files_list(self, files_list):
        start_time = datetime.datetime.now()
        messages = {}
        results = []
        summary = {}
        if self.dry_run:
            if not self.quiet:
                logger.info(f"Dry run enabled, changes will NOT be commited to filesystem")
        if self.nproc > 1:
            if not self.quiet:
                logger.info(f"Doing multiprocessing on {len(files_list)} files with {self.nproc} threads in {self.ncore} cores...")
            with Pool(self.nproc) as pool:
                results = pool.map(self.process_files_list_item_wrapper, files_list)
        else:
            if not self.quiet:
                logger.info(f"Doing sequential processing on {len(files_list)} files...")
            for item in files_list:
                result = self.process_files_list_item_wrapper(item)
                results.append(result)
        if not self.quiet:
            logger.info(f"\n")
            logger.info(f"DONE!\n")
        # Summarize results
        by_extension = {}
        by_type = {}
        if self.verbose:
            log_files(results)
        no_time = datetime.timedelta(seconds=0)
        # fmt:off
        def_item={
              "extension": ""
            , "type": ""
            , "success": 0
            , "failed": 0
            , "copied": 0
            , "processed": 0
            , "overwritten": 0
            , "new": 0
            , "written": 0
            , "changed": 0
            , "skipped": 0
            , "handler_disabled": 0
            , "extension_disabled": 0
            , "empty": 0
            , "size_error": 0
            , "binary": 0
            , "gzip": 0
            , "slow": 0
            , "time": no_time
        }
        # fmt:on
        # fmt:off
        order=[
            "extension"
          , "type"
          , "success"
          , 'failed'
          , "copied"
          , "processed"
          , "overwritten"
          , "new"
          , "written"
          , "changed"
          , "skipped"
          , "handler_disabled"
          , "extension_disabled"
          , "empty"
          , "size_error"
          , "binary"
          , "gzip"
          , "slow"
          , "time"
        ]
        # fmt:on
        time_cols = ["time"]
        keys = order.copy()
        keys.remove("extension")
        keys.remove("type")
        by_key = {}
        failed_ct = 0
        total = "total"
        for result in results:
            status = result.get("status")
            failed = status.get("failed")
            if failed:
                failed_ct += 1
            extension = status.get("extension") or "?"
            handler_type = status.get("type") or "?"
            extension_item = by_extension.get(extension, def_item.copy())
            type_item = by_type.get(handler_type, def_item.copy())
            for key in keys:
                extension_item["extension"] = extension
                if key in time_cols:
                    extension_item[key] = extension_item.get(key, no_time) + status.get(key, no_time)
                else:
                    extension_item[key] = extension_item.get(key, 0) + (1 if status.get(key, False) else 0)
            for key in keys:
                type_item["type"] = handler_type
                if key in time_cols:
                    type_item[key] = type_item.get(key, no_time) + status.get(key, no_time)
                else:
                    type_item[key] = type_item.get(key, 0) + (1 if status.get(key, False) else 0)

            for key in keys:
                by_key[key] = by_key.get(key, 0) + (1 if status.get(key, False) else 0)

            by_extension[extension] = extension_item
            by_type[handler_type] = type_item

            input_path = f"{result.get('input_path')}"

            for message in result.get("messages"):
                all = messages.get(message, [])
                messages[message] = [*all, input_path]

        if not self.quiet:
            for result in results:
                status = result.get("status")
                extension = status.get("extension") or "?"
                handler_type = status.get("type") or "N/A"

                extension_keys = by_key.copy()
                extension_keys["extension"] = total
                by_extension[total] = extension_keys

                type_keys = by_key.copy()
                type_keys["type"] = total
                by_type[total] = type_keys

            summary = {"by_extension": by_extension, "by_type": by_type}
            end_time = datetime.datetime.now()
            interval = end_time - start_time
            if messages:
                logger.warning(f"Messages encountered were:")
                for message, all in messages.items():
                    logger.warning(f"{len(all)} x {message}")
                    show_count = 5
                    count = len(all)
                    for index in range(min(show_count, count)):
                        logger.warning(f"    {all[index]}")
                    if show_count < count:
                        logger.warning(f"    ... and {count-show_count} more")
                    logger.warning("")

            log_summary(summary)
            logger.info(f"Performing {self.mode.value} on {len(files_list)} file(s) generated {len(messages)} message(s) and took {human_delta(interval)} total\n")
            if failed_ct > 0:
                logger.error(f"NOTE: {failed_ct} errors occured\n")
        return True

    def _process_existing_dir_to_existing_dir(self):
        input_paths = generate_file_list(self.input, tuple(self.valid_extensions))
        files_list = []
        for input_path in input_paths:
            common = os.path.commonpath((os.path.abspath(self.output), os.path.abspath(input_path)))
            rel = os.path.relpath(os.path.abspath(input_path), os.path.abspath(self.input))
            output_path = os.path.join(os.path.abspath(self.output), rel)
            files_list.append({"input_path": input_path, "output_path": output_path})
        return files_list

    def _process_existing_dir_to_new_dir(self):
        # This is same as _process_existing_dir_to_existing_dir but with a mkdir first
        os.mkdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)
        return self._process_existing_dir_to_existing_dir()

    def _process_existing_dir_overwrite(self):
        input_paths = generate_file_list(self.input, tuple(self.valid_extensions))
        files_list = []
        for input_path in input_paths:
            files_list.append({"input_path": input_path, "output_path": input_path})
        return files_list

    def _process_existing_file(self):
        files_list = [{"input_path": os.path.abspath(self.input), "output_path": os.path.abspath(self.output)}]
        return files_list

    def _process_existing_file_overwrite(self):
        files_list = [{"input_path": os.path.abspath(self.input), "output_path": os.path.abspath(self.input)}]
        return files_list

    def _process_existing_file_to_dir(self):
        head, tail = os.path.split(os.path.abspath(self.input))
        files_list = [{"input_path": os.path.abspath(self.input), "output_path": os.path.join(os.path.abspath(self.output), tail)}]
        return files_list

    def process_files(self):
        if self.input_is_dir:
            if self.output:
                if self.output_is_dir:
                    files_list = self._process_existing_dir_to_existing_dir()
                    if self.verbose:
                        logger.info("transfer: exdir -> exdir")
                    return self.process_files_list(files_list), None
                elif not self.output_exists:
                    files_list = self._process_existing_dir_to_new_dir()
                    if self.verbose:
                        logger.info("transfer: exdir -> nudir")
                    return self.process_files_list(files_list), None
                else:
                    return None, f"Processsing of multiple files into one single output file is not possible"
            elif self.overwrite:
                files_list = self._process_existing_dir_overwrite()
                if self.verbose:
                    logger.info("transfer: exdir -> overwrite")
                return self.process_files_list(files_list), None
            elif self.format:
                return None, "format option was specified, it is currently not implemented for the input specified (A)"
            else:
                return None, f"input dir specified without valid output option"
        else:
            if self.output:
                if self.output_is_dir:
                    files_list = self._process_existing_file_to_dir()
                    if self.verbose:
                        logger.info("transfer: exfil -> exdir")
                    return self.process_files_list(files_list), None
                elif not self.output_exists:
                    files_list = self._process_existing_file()
                    if self.verbose:
                        logger.info("transfer: exfil -> exfil 1")
                    return self.process_files_list(files_list), None
                else:
                    if self.overwrite:
                        files_list = self._process_existing_file()
                        if self.verbose:
                            logger.info("transfer: exfil -> exfil 2")
                        return self.process_files_list(files_list), None
                    else:
                        return None, f"Cannot overwrite existing file when --overwrite is not enabled"
            elif self.overwrite:
                files_list = self._process_existing_file_overwrite()
                if self.verbose:
                    logger.info("transfer: exfil -> exfil 3")
                return self.process_files_list(files_list), None
            elif self.format:
                return None, "format option was specified, it is currently not implemented for the input specified (B)"
            else:
                return None, f"input file specified without valid output option 2"
