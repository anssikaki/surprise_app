"""Tests for functions in ``surprise_app``.

When this file is executed directly (for example via ``streamlit run``), the
parent directory is not on ``sys.path`` which results in ``ModuleNotFoundError``
for ``surprise_app``.  To make the tests runnable in that scenario we insert the
repository root onto ``sys.path`` before importing the module.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the repository root is importable when the tests are executed directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from surprise_app import build_prompt, read_log_file


def test_build_prompt():
    text = build_prompt("GadgetPro", "the buttons are too small")
    assert "GadgetPro" in text
    assert "buttons are too small" in text
    assert text.startswith("Generate a fun action plan")


def test_read_log_file(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("line1\nline2\nline3\n")
    result = read_log_file(str(log_file), max_lines=2)
    assert result == "line2\nline3\n"


def test_read_log_file_missing(tmp_path):
    missing = tmp_path / "missing.log"
    assert read_log_file(str(missing)) == "Log file does not exist."
