# tests/test_setup.py
import sys
import pytest
from dotcop.setup import main  # adjust import to your actual module

@pytest.mark.parametrize("args,expected_output", [
    (["dotcop", "help"], "Dotcop: Configuration package manager"),
    (["dotcop", "status"], "Coming soon..."),
    (["dotcop", "list"], "Coming soon..."),
    (["dotcop", "install"], "Coming soon..."),
    (["dotcop", "remove"], "Coming soon..."),
])
def test_commands(monkeypatch, capsys, args, expected_output):
    # Patch sys.argv
    monkeypatch.setattr(sys, "argv", args)

    # Call main
    main()

    # Capture stdout
    captured = capsys.readouterr()
    assert expected_output in captured.out
