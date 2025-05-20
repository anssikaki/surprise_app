from surprise_app import build_prompt, read_log_file


def test_build_prompt():
    text = build_prompt("Acme", 2100, "space expansion")
    assert "Acme" in text
    assert "2100" in text
    assert "space expansion" in text
    assert text.startswith("Write a press release")


def test_read_log_file(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text("line1\nline2\nline3\n")
    result = read_log_file(str(log_file), max_lines=2)
    assert result == "line2\nline3\n"


def test_read_log_file_missing(tmp_path):
    missing = tmp_path / "missing.log"
    assert read_log_file(str(missing)) == "Log file does not exist."
