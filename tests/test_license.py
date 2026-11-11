"""Every shipped source file carries the GPL v2 header that LICENSE matches."""

import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
HEADER = "# Copyright (C) 2025 OETIKER+PARTNER AG - License: GNU General Public License v2"


@pytest.mark.parametrize(
    "path",
    sorted((ROOT / "local").rglob("*.py")),
    ids=lambda p: p.relative_to(ROOT / "local").as_posix(),
)
def test_source_file_has_license_header(path):
    assert path.read_text().splitlines()[0] == HEADER
