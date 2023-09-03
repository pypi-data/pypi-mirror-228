r"""Directive
=============
"""
import os
import re

from docutils import nodes
from docutils.nodes import Node
from docutils.statemachine import StringList
from jinja2 import Template
from myst_parser.mdit_to_docutils.sphinx_ import SphinxRenderer
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nested_parse_with_titles

TEMPLATE_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), "assets"), "jinja2"
)


def parse(file: str) -> list[str]:
    r"""Parse requirements.txt. ``text`` will be displayed as a url, ``other``
    will be displayed normally.

    :param file:
    :type file: str
    :rtype: list[str]
    """
    with open(file) as f:
        lines = f.readlines()
    items = []
    for line in lines:
        if line.startswith("#!"):
            continue
        item = {}
        line = line.strip()
        if line.startswith("#"):
            line = line[1:].strip()
            item["text"] = line
        else:
            # ignore trailing comments
            line = line.split(" #")[0].strip()
            pos = line.find("://")
            if pos >= 0:
                item["text"] = line
                item["url"] = "https" + line[pos:]
            else:
                captures = re.match(r"[\w-]+", line)
                # ignore -r/...
                if captures:
                    item["text"] = captures[0]
                    # other is `> X.Y.Z`
                    item["other"] = line.strip(captures[0])
                    item["url"] = "https://pypi.org/project/" + captures[0]
        items += [item]
    return items


class RequirementsDirective(SphinxDirective):
    r"""Requirementsdirective."""

    has_content = True

    def run(self) -> list[Node]:
        r"""Run.

        :rtype: list[Node]
        """
        content = self.content[0]
        fmt = self.options.get("format", self.config["requirements_format"])
        template = self.options.get("template")
        if isinstance(self.state._renderer, SphinxRenderer):
            template_ext = "md"
        else:
            template_ext = "rst"
        if template is None:
            template = os.path.join(
                TEMPLATE_DIR, f"template.{template_ext}.j2"
            )
        with open(template) as f:
            template_text = f.read()
        title = os.path.basename(content).split(os.path.extsep)[0]
        if fmt.find("{title}") >= 0:
            title = fmt.format(title=title)
        else:
            title = fmt
        path = self.content.items[0][0]
        items = parse(os.path.join(os.path.dirname(path), content))
        new_content = Template(template_text).render(title=title, items=items)
        new_content = StringList(new_content.splitlines(), source="")
        node = nodes.Element()
        nested_parse_with_titles(self.state, new_content, node)

        return node.children
