# sphinxcontrib-requirements-txt

[![readthedocs](https://shields.io/readthedocs/sphinxcontrib-requirements-txt)](https://sphinx-contrib-requirements-txt.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sphinx-contrib/requirements-txt/main.svg)](https://results.pre-commit.ci/latest/github/sphinx-contrib/requirements-txt/main)
[![github/workflow](https://github.com/sphinx-contrib/requirements-txt/actions/workflows/main.yml/badge.svg)](https://github.com/sphinx-contrib/requirements-txt/actions)
[![codecov](https://codecov.io/gh/sphinx-contrib/requirements-txt/branch/main/graph/badge.svg)](https://codecov.io/gh/sphinx-contrib/requirements-txt)

[![github/downloads](https://shields.io/github/downloads/sphinx-contrib/requirements-txt/total)](https://github.com/sphinx-contrib/requirements-txt/releases)
[![github/downloads/latest](https://shields.io/github/downloads/sphinx-contrib/requirements-txt/latest/total)](https://github.com/sphinx-contrib/requirements-txt/releases/latest)
[![github/issues](https://shields.io/github/issues/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/discussions)
[![github/milestones](https://shields.io/github/milestones/all/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/milestones)
[![github/forks](https://shields.io/github/forks/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/network/members)
[![github/stars](https://shields.io/github/stars/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/stargazers)
[![github/watchers](https://shields.io/github/watchers/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/watchers)
[![github/contributors](https://shields.io/github/contributors/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/commits)
[![github/release-date](https://shields.io/github/release-date/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/releases/latest)

[![github/license](https://shields.io/github/license/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt)
[![github/languages/top](https://shields.io/github/languages/top/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt)
[![github/directory-file-count](https://shields.io/github/directory-file-count/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt)
[![github/code-size](https://shields.io/github/languages/code-size/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt)
[![github/repo-size](https://shields.io/github/repo-size/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt)
[![github/v](https://shields.io/github/v/release/sphinx-contrib/requirements-txt)](https://github.com/sphinx-contrib/requirements-txt)

[![pypi/status](https://shields.io/pypi/status/sphinxcontrib-requirements-txt)](https://pypi.org/project/sphinxcontrib-requirements-txt/#description)
[![pypi/v](https://shields.io/pypi/v/sphinxcontrib-requirements-txt)](https://pypi.org/project/sphinxcontrib-requirements-txt/#history)
[![pypi/downloads](https://shields.io/pypi/dd/sphinxcontrib-requirements-txt)](https://pypi.org/project/sphinxcontrib-requirements-txt/#files)
[![pypi/format](https://shields.io/pypi/format/sphinxcontrib-requirements-txt)](https://pypi.org/project/sphinxcontrib-requirements-txt/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/sphinxcontrib-requirements-txt)](https://pypi.org/project/sphinxcontrib-requirements-txt/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/sphinxcontrib-requirements-txt)](https://pypi.org/project/sphinxcontrib-requirements-txt/#files)

A sphinx extension to generate a rst/markdown to display the dependencies of
a python package from `requirement.txt`.

## Usage

Take MyST as an example. rst is similar.

`requirement.txt`:

````kconfig
# To complete package names, a cache is needed.
# Every time you change template, the cache must be regenerated.
#
# ```shell
# $ pkgbuild-language-server --print-config cache
# /home/wzy/.cache/pacman.json
# ```

pyalpm
# See <https://wiki.archlinux.org/title/Namcap>.
git+git://gitlab.archlinux.org/pacman/namcap
````

`docs/conf.py`:

```python
# ...
extensions = [
    "myst_parser",
    "sphinxcontrib.requirements_txt",
]
# ...
```

`docs/index.md`:

````markdown
```{requirements} ../requirements.txt
```
````

Then:

```shell
cd docs && sphinx-build . _build/html
cd -
xdg-open docs/_build/html/index.html
```

A generated markdown will be inserted and rendered. You see:

![screenshot](https://github.com/Freed-Wu/pkgbuild-language-server/assets/32936898/c64ba56f-e2d5-4755-be50-632bd65d431c)

## Customize

````markdown
```{requirements} /the/path/of/requirements.txt
---
title: Dependence
template: /the/path/of/template.j2
---
```
````

- `/the/path/of/requirements.txt` can be a glob expression.
- `title` can contain `{title}`, which will be converted to the base name of
  requirement file. Such as `requirements/dev.txt` will be converted to `dev`.
- `template` is a jinja2 file. See [jinja2 syntax](https://docs.jinkan.org/docs/jinja2/templates.html)
  and
  [examples](https://github.com/sphinx-contrib/requirements-txt/blob/main/src/sphinxcontrib/requirements_txt/assets/jinja2).

## Alternatives

- [sphinxcontrib-eval](https://github.com/sphinx-contrib/eval#generate-requirements-document)

See
[![readthedocs](https://shields.io/readthedocs/sphinxcontrib-requirements-txt)](https://sphinxcontrib-requirements-txt.readthedocs.io)
to know more.
