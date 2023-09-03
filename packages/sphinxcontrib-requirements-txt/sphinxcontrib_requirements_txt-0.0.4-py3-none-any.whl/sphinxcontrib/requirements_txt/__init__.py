r"""Sphinx extension: requirements-txt
======================================
"""
from sphinx.application import Sphinx

from ._version import __version__, __version_tuple__  # type: ignore
from .directive import RequirementsDirective


def setup(app: Sphinx) -> None:
    r"""Set up.

    :param app:
    :type app: Sphinx
    :rtype: None
    """
    app.add_config_value(
        name="requirements_title", default="{title}", rebuild="env"
    )
    app.add_directive(name="requirements", cls=RequirementsDirective)
