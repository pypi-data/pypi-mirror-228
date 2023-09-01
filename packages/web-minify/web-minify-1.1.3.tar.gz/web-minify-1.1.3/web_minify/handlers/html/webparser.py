from html.parser import HTMLParser
import re
import pprint

import logging

logger = logging.getLogger(__name__)

whitespace_combinator_re = re.compile(r"\s+")


"""
GOAL:
    
    1. Support html soups (unbalanced/missing/wrong tags) without changing them structurally to support templates
    2. Support minify
    3. Support beautify
    4. Support lint (generate warnings about errors found in the document)

"""


def process_data(raw):
    stripped = raw.strip()
    # Remove nonsequitur space completely
    if len(stripped) <= 0:
        return ""
    # Remove interleaved space from actual content
    data = whitespace_combinator_re.sub(" ", raw)
    return data


def is_empty_content_model_tag(tag):
    return tag in ["meta", "link", "base", "hr", "img"]


class Node:
    def __init__(self, pos=None, parent=None, tag=None, attrs=[], data=None, ref=None, decl=None, comment=None):
        self.line = None
        self.col = None
        if pos:
            self.line, self.col = pos
        self.messages = []
        self.parent = parent
        self.tag = tag
        self.attrs = attrs
        self.data = data
        self.ref = ref
        self.decl = decl
        self.comment = comment
        self.children = []
        self.content_model = "any"
        self.on_content_model_violation = "allow"
        self.allow_skip_end_tag = False
        self.had_end_tag = True
        self.had_start_tag = True
        self.verbatim_data = False
        if not tag:
            self.content_model = "empty"
        if tag in ["pre", "code", "textarea"]:
            self.verbatim_data = True
        if tag in ["title"]:
            self.content_model = "text"
            self.on_content_model_violation = "close_tag"
        elif is_empty_content_model_tag(tag):
            self.content_model = "empty"
            self.on_content_model_violation = "close_tag"
        elif tag in ["html", "head", "body"]:
            self.allow_skip_end_tag = True

    def pos(self):
        if self.line and self.col:
            return f"<{self.line}, {self.col}>"
        return "<unknown>"

    def adopt(self, child):
        if child.tag and not self.tag:
            self.messages.append(f"Trying to add child tag {child.tag} to non-tag node at {self.pos()}")
            return False
        if self.content_model == "empty":
            if self.on_content_model_violation == "close_tag":
                # Implicitly close tag
                return True
            elif self.on_content_model_violation == "allow":
                self.children.append(child)
                return False
        elif self.content_model == "text" and not child.tag:
            self.children.append(child)
        else:
            if not child.tag and self.verbatim_data:
                child.verbatim_data = True
            # TODO: Not implemented:
            self.children.append(child)
        # Don't implicitly close tag
        return False

    def generate(self, indent=0, config={}):
        out = ""
        out_messages = []
        out_messages.extend(self.messages)
        sp = config.get("indent", "X") * indent
        nl = config.get("newline", "\n")
        if self.tag:
            if self.had_start_tag or config.get(f"insert_opening_{self.tag}", False) or config.get("insert_opening_tags", False):
                # logger.info("RAW:")            logger.info(pprint.pformat(self.attrs))            logger.info("SORTED:")            logger.info(pprint.pformat(sorted_attrs))
                attrstr = ""
                for attr, val in dict(sorted(self.attrs)).items() if config.get("attr_sort", False) else self.attrs:
                    attr = attr.strip()
                    val = val.strip()
                    skip = False
                    if attr == "type" and val == "text/javascript" and not config.get("include_script_type", True):
                        skip = True
                    if config.get("attr_cull_empty", False) and not val:
                        skip = True
                    if not skip:
                        qt = config.get("attr_quote", '"')
                        attrstr += f" {attr}={qt}{val}{qt}"
                end = " /" if self.content_model == "empty" else ""
                out += f"{sp}<{self.tag}{attrstr}{end}>{'' if self.verbatim_data else nl}"
            elif config.get("comment_missing_tags", False):
                out += f"{sp}<!-- <{self.tag}{attrstr}{end}> -->{'' if self.verbatim_data else nl}"
        elif self.data:
            if self.verbatim_data:
                out += self.data
            else:
                out += (sp if config.get("indent_text", False) else "") + process_data(self.data) + ("" if self.verbatim_data else nl)
        elif self.ref:
            out += f"&{self.ref};"
        elif self.decl:
            out += f"<{self.decl}>"
        elif self.comment:
            comment = self.comment.strip()
            out += f"<!-- {comment} -->{nl}"
        if config.get("debug_messages", False) and self.messages:
            out += f"<!-- | DEBUG MESSAGES for position {self.pos()}{nl}"
            for message in self.messages:
                out += f"     | {message}{nl}"
            out += f"-->{nl}"
        for child in self.children:
            child_out, child_messages = child.generate(indent + 1, config)
            out += child_out
            out_messages.extend(child_messages)
        if self.tag and not self.content_model == "empty":
            if self.had_end_tag or config.get(f"insert_closing_{self.tag}", False) or config.get("insert_closing_tags", False):
                # and not (config.get("tag_cull_empty_closing", False) and self.children)
                out += f"{'' if self.verbatim_data else sp}</{self.tag}>{nl}"
            elif config.get("comment_missing_tags", False):
                out += f"{'' if self.verbatim_data else sp}<!-- </{self.tag}> -->{nl}"
        return out, out_messages

    def __repr__(self):
        out = ""
        if self.tag:
            sorted_attrs = dict(sorted(self.attrs))
            # logger.info("RAW:")            logger.info(pprint.pformat(self.attrs))            logger.info("SORTED:")            logger.info(pprint.pformat(sorted_attrs))
            attrstr = ""
            for attr, val in sorted_attrs.items():
                attrstr += f' {attr}="{val}"'
            end = " /" if self.content_model == "empty" else ""
            cd = f" c={len(self.children)}" if len(self.children) > 0 else ""
            out += f"<{self.tag}{attrstr}{cd}{end}>"
        elif self.data:
            out += f"[{process_data(self.data)}]"
        elif self.comment:
            comment = self.comment.strip()
            out += f"<!-- {comment} -->"
        return out


class MyHTMLParser(HTMLParser):
    def __init__(self, boss, do_debug=False):
        self.boss = boss
        self.do_debug = do_debug
        # initialize the base class
        HTMLParser.__init__(self, convert_charrefs=False)

    def handle_starttag(self, tag, attrs):
        if self.do_debug:
            logger.info(f"starttag({tag, attrs})")
        return self.boss.handle_starttag(self, tag, attrs)

    def handle_endtag(self, tag):
        if self.do_debug:
            logger.info(f"endtag({tag})")
        return self.boss.handle_endtag(self, tag)

    def handle_data(self, data):
        if self.do_debug:
            logger.info(f"data({data})")
        return self.boss.handle_data(self, data)

    def handle_comment(self, comment):
        if self.do_debug:
            logger.info(f"comment({comment})")
        return self.boss.handle_comment(self, comment)

    def handle_entityref(self, ref):
        if self.do_debug:
            logger.info(f"entityref({ref})")
        return self.boss.handle_entityref(self, ref)

    def handle_charref(self, ref):
        if self.do_debug:
            logger.info(f"charref({ref})")
        return self.boss.handle_charref(self, ref)

    def handle_decl(self, decl):
        if self.do_debug:
            logger.info(f"decl({decl})")
        return self.boss.handle_decl(self, decl)

    def handle_pi(self, decl):
        if self.do_debug:
            logger.info(f"pi({decl})")
        return self.boss.handle_pi(self, decl)

    def unknown_decl(self, decl):
        if self.do_debug:
            logger.info(f"unknown({decl})")
        return self.boss.unknown_decl(self, decl)


class WebParser:
    def __init__(self):
        # fmt: off
        self.default_config={
              "indent": "\t"
            , "newline": "\n"
            , "attr_quote": "\""
            , "attr_sort": False
            , "attr_cull_empty": False
            , "tag_cull_empty_closing": False # NOTE: Not implemented, do not use!
            , "debug_messages": False
            , "include_script_type": True
            , "include_timestamp": True
            , "indent_text": True
            , "insert_head": False
            , "insert_html": False
            , "insert_doctype": False
            , "insert_body": False
            , "comment_missing_tags": False
            , "insert_opening_tags": False
            , "insert_closing_tags": False
            , "insert_opening_html": False
            , "insert_closing_html": False
            , "insert_opening_head": False
            , "insert_closing_head": False
            , "insert_opening_body": False
            , "insert_closing_body": False
            , "debug_print": False
        }
        # fmt: on
        # fmt: off
        self.beautify_config={
              "indent": "\t"
            , "newline": "\n"
            , "attr_quote": "\""
            , "attr_sort": True
            , "debug_print": True
            }
        # fmt: on
        # fmt: off
        self.minify_config={
              "indent": ""
            , "newline": ""
            , "attr_quote": ""
            , "attr_cull_empty": True
            , "tag_cull_empty_closing": True
            , "indent_text": False
            , "include_script_type": False
        }
        # fmt: on
        self.debug_config = {**self.beautify_config, "debug_messages": True, "debug_print": True}
        self.config = {**self.default_config}

    def parse(self, buf: str):
        self.stack = []
        self.pre_nodes = []
        self.post_nodes = []
        self.current_root = None
        self.roots = []
        parser = MyHTMLParser(self, self.config.get("debug_print", False))
        parser.feed(buf.strip() if buf else "")

    def generate(self, config={}):
        self.config = {**self.default_config, **config}
        # logger.info(pprint.pformat(self.config))
        if self.roots:
            out = ""
            messages = []
            for pre_node in self.pre_nodes:
                pre_out, pre_messages = pre_node.generate(0, self.config)
                out += pre_out
                messages.extend(pre_messages)
            for root in self.roots:
                gen_out, gen_messages = root.generate(0, self.config)
                out += gen_out
                messages.extend(gen_messages)
            for post_node in self.post_nodes:
                post_out, post_messages = post_node.generate(0, self.config)
                out += post_out
                messages.extend(post_messages)
            return out, messages
        else:
            return "", ["Output was empty"]

    def beautify(self):
        return self.generate(self.beautify_config)

    def debugify(self):
        return self.generate(self.debug_config)

    def minify(self):
        return self.generate(self.minify_config)

    #
    #

    #
    #           https://dev.w3.org/html5/html-author/#the-pre-element
    # https://docs.python.org/3/library/html.parser.html

    #

    def inject_parent(self, tag=None):
        parent = Node(pos=None, parent=None, tag=tag)
        parent.messages.append(f"Inserted dummy parent {tag} to balance DOM")
        parent.had_start_tag = False
        self.stack.insert(0, parent)
        if self.current_root:
            self.current_root.parent = parent
            parent.adopt(self.current_root)
        self.current_root = parent
        return self.current_root

    def submit_node(self, pos=None, tag=None, attrs=[], data=None, ref=None, decl=None, comment=None):
        parent = self.stack[-1] if len(self.stack) > 0 else None
        child = Node(pos=pos, parent=parent, tag=tag, attrs=attrs, data=data, ref=ref, decl=decl, comment=comment)
        if not self.current_root:
            if not tag:
                self.pre_nodes.append(child)
            else:
                self.current_root = child
        elif not parent:
            child.messages.append(f"New root found: {child}")
            self.roots.append(self.current_root)
            self.current_root = child
        implicitly_close_tag = False
        if parent:
            implicitly_close_tag = parent.adopt(child)
        if not implicitly_close_tag:
            self.stack.append(child)
        # TODO: Handle post_nodes
        # if not tag:
        #    self.post_nodes.append(child)
        return child

    def pop_node(self, end_tag=None):
        if len(self.stack) <= 0:
            parent = self.inject_parent(end_tag)
            parent.messages.append("Stack empty on pop_node")
            return None
        parent = self.stack[-1]
        if not parent.tag:
            self.stack.pop()
            return parent
        if parent.content_model == "empty":
            self.stack.pop()
            return parent
        if end_tag and parent.tag:
            if parent.tag == end_tag:
                parent.had_end_tag = True
                if not parent.content_model == "empty":
                    self.stack.pop()
            else:
                message = f"Tag close mismatch: {parent.tag} != {end_tag}"
                parent = self.inject_parent(end_tag)
                parent.messages.append(message)
        else:
            self.stack.pop()
        return parent

    def handle_starttag(self, parser: MyHTMLParser, tag, attrs):
        # logger.info(f"<START: {tag}")
        child = self.submit_node(pos=parser.getpos(), tag=tag, attrs=attrs)

    def handle_endtag(self, parser: MyHTMLParser, tag):
        # logger.info(f"/END: {tag}")
        self.pop_node(tag)

    def handle_data(self, parser: MyHTMLParser, data):
        # logger.info(f"DATA: {data}")
        child = self.submit_node(pos=parser.getpos(), data=data)
        self.pop_node()

    def handle_entityref(self, parser: MyHTMLParser, ref):
        # logger.info(f"DATA: {data}")
        child = self.submit_node(pos=parser.getpos(), ref=ref)
        self.pop_node()

    def handle_charref(self, parser: MyHTMLParser, ref):
        # logger.info(f"DATA: {data}")
        child = self.submit_node(pos=parser.getpos(), ref=ref)
        self.pop_node()

    def handle_comment(self, parser: MyHTMLParser, comment):
        # logger.info(f"# Comment: {comment}")
        child = self.submit_node(pos=parser.getpos(), comment=comment)
        self.pop_node()

    def handle_decl(self, parser: MyHTMLParser, decl):
        child = self.submit_node(pos=parser.getpos(), decl=f"!{decl}")
        self.pop_node()

    def handle_pi(self, parser: MyHTMLParser, decl):
        child = self.submit_node(pos=parser.getpos(), decl=f"?{decl}")
        self.pop_node()

    def unknown_decl(self, parser: MyHTMLParser, decl):
        child = self.submit_node(pos=parser.getpos(), decl=f"{decl}")
        self.pop_node()
