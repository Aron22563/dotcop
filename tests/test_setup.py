# tests/test_setup.py
import sys
import re
import pytest
from dotcop.setup import main, Core

VERSION_PATTERN = r"^\d+\.\d+\.\d+$"

@pytest.mark.parametrize(
    "args,expected_package,expected_force,expected_version_pattern",
    [
        (["dotcop", "install", "anypackage"], "anypackage", False, None),  # no version provided
        (["dotcop", "install", "mypkg", "--version", "1.2.3"], "mypkg", False, VERSION_PATTERN),
        (["dotcop", "install", "pkgX", "--force"], "pkgX", True, None),
        (["dotcop", "install", "pkgY", "--version", "0.0.1", "--force"], "pkgY", True, VERSION_PATTERN),
        (["dotcop", "remove", "pkgZ"], "pkgZ", None, None),
    ]
)
def test_cli_generic(monkeypatch, args, expected_package, expected_force, expected_version_pattern):
    captured_args = {}

    core = Core()
    
    def mock_install(package, version, force):
        captured_args.update({"package": package, "version": version, "force": force})

    def mock_remove(package):
        captured_args.update({"package": package})

    core.install = mock_install
    core.remove = mock_remove

    import dotcop.setup
    original_core = dotcop.setup.Core
    dotcop.setup.Core = lambda: core

    monkeypatch.setattr(sys, "argv", args)
    main()

    dotcop.setup.Core = original_core

    # Assertions
    assert captured_args["package"] == expected_package
    if "force" in captured_args and expected_force is not None:
        assert captured_args["force"] == expected_force
    if "version" in captured_args and expected_version_pattern:
        assert re.match(expected_version_pattern, captured_args["version"])

import sys
import pytest
from dotcop.setup import main, Core

def test_help_command(monkeypatch, capsys):
    """Test the help command"""
    core = Core()
    
    import dotcop.setup
    original_core = dotcop.setup.Core
    dotcop.setup.Core = lambda: core

    monkeypatch.setattr(sys, "argv", ["dotcop", "help"])
    main()
    
    dotcop.setup.Core = original_core
    
    captured = capsys.readouterr()
    assert "Dotcop" in captured.out
    assert "Configuration package manager" in captured.out

def test_status_command(monkeypatch):
    """Test the status command"""
    status_called = {"called": False}
    
    core = Core()
    
    def mock_status():
        status_called["called"] = True
    
    core.status = mock_status
    
    import dotcop.setup
    original_core = dotcop.setup.Core
    dotcop.setup.Core = lambda: core

    monkeypatch.setattr(sys, "argv", ["dotcop", "status"])
    main()
    
    dotcop.setup.Core = original_core
    
    assert status_called["called"] is True


def test_list_command(monkeypatch):
    """Test the list command"""
    list_called = {"called": False}
    
    core = Core()
    
    def mock_list():
        list_called["called"] = True
    
    core.list = mock_list
    
    import dotcop.setup
    original_core = dotcop.setup.Core
    dotcop.setup.Core = lambda: core

    monkeypatch.setattr(sys, "argv", ["dotcop", "list"])
    main()
    
    dotcop.setup.Core = original_core
    
    assert list_called["called"] is True


def test_missing_required_command(monkeypatch):
    """Test that missing command raises SystemExit"""
    monkeypatch.setattr(sys, "argv", ["dotcop"])
    
    with pytest.raises(SystemExit):
        main()


def test_install_with_none_version(monkeypatch, capsys):
    """Test install with version=None explicitly"""
    core = Core()
    
    import dotcop.setup
    original_core = dotcop.setup.Core
    dotcop.setup.Core = lambda: core

    monkeypatch.setattr(sys, "argv", ["dotcop", "install", "testpkg"])
    main()
    
    dotcop.setup.Core = original_core
    
    captured = capsys.readouterr()
    assert "testpkg" in captured.out
    assert "None" in captured.out
    assert "False" in captured.out


def test_core_methods_default_behavior(capsys):
    """Test Core class methods with default implementation"""
    core = Core()
    
    # Test status (should do nothing)
    core.status()
    
    # Test list (should do nothing)
    core.list()
    
    # Test install
    core.install("pkg1", "1.0.0", True)
    captured = capsys.readouterr()
    assert "pkg1" in captured.out
    assert "1.0.0" in captured.out
    assert "True" in captured.out
    
    # Test remove
    core.remove("pkg2")
    captured = capsys.readouterr()
    assert "pkg2" in captured.out

