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
