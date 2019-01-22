# -*- coding=utf-8 -*-

import os

import pytest
import vistir

import pythonfinder.utils

from pythonfinder import Finder


os.environ["ANSI_COLORS_DISABLED"] = "1"


def _get_python_versions():
    finder = Finder(global_search=True, system=False, ignore_unsupported=True)
    pythons = finder.find_all_python_versions()
    for v in pythons:
        py = v.py_version
        comes_from = getattr(py, "comes_from", None)
        if comes_from is not None:
            comes_from_path = getattr(comes_from, "path", v.path)
        else:
            comes_from_path = v.path
    return sorted(list(pythons))


PYTHON_VERSIONS = _get_python_versions()


versions = [
    (pythonfinder.utils.get_python_version(python.path.as_posix()), python.as_python.version)
    for python in PYTHON_VERSIONS
]

version_dicts = [
    (pythonfinder.utils.parse_python_version(str(python.as_python.version)), python.as_python.as_dict())
    for python in PYTHON_VERSIONS
]

test_paths = [
    (python.path.as_posix(), True)
    for python in PYTHON_VERSIONS
]

@pytest.mark.parse
@pytest.mark.parametrize("python, expected", versions)
def test_get_version(python, expected):
    assert python == str(expected)


@pytest.mark.parse
@pytest.mark.parametrize("python, expected", version_dicts)
def test_parse_python_version(python, expected):
    for key in ["comes_from", "architecture", "executable", "name"]:
        if key in expected:
            del expected[key]
        if key in python:
            del python[key]
    assert python == expected


@pytest.mark.is_python
@pytest.mark.parametrize("python, expected", test_paths)
def test_is_python(python, expected):
    assert pythonfinder.utils.path_is_known_executable(python)
    assert pythonfinder.utils.looks_like_python(os.path.basename(python))
    assert pythonfinder.utils.path_is_python(vistir.compat.Path(python))