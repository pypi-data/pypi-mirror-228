r"""Test directive."""
import os

from sphinxcontrib.requirements_txt.directive import parse

PATH = os.path.dirname(os.path.dirname(__file__))


class Test:
    r"""Test."""

    @staticmethod
    def test_parse() -> None:
        result = parse(os.path.join(PATH, "requirements.txt"))
        expected = [
            {},
            {"text": "Support MyST."},
            {
                "text": "myst-parser",
                "other": "",
                "url": "https://pypi.org/project/myst-parser",
            },
            {
                "text": "sphinx",
                "other": "",
                "url": "https://pypi.org/project/sphinx",
            },
        ]
        assert result == expected
