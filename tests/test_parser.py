import pytest
import argparse
from unittest.mock import patch, MagicMock
from dotcop.app.cli import Parser


class TestParser:
    @pytest.fixture
    def parser(self):
        """Create a Parser instance for testing."""
        with patch("dotcop.parser.Logger"):
            return Parser()

    # Tests for initialization
    def test_parser_initialization(self, parser):
        """Test that parser initializes correctly."""
        assert parser.parser is not None
        assert isinstance(parser.parser, argparse.ArgumentParser)

    def test_parser_has_subparsers(self, parser):
        """Test that subparsers are created and command is required."""
        with pytest.raises(SystemExit):
            parser.parser.parse_args([])

    # Tests for subcommands without arguments
    @pytest.mark.parametrize("command", ["help", "status", "list", "create", "edit"])
    def test_simple_commands_parsing(self, parser, command):
        """Test that simple commands parse correctly."""
        args = parser.parser.parse_args([command])
        assert args.command == command

    # Tests for install command argument parsing
    def test_install_command_single_package(self, parser):
        """Test install command parses single package."""
        args = parser.parser.parse_args(["install", "@user/pkg:1.0.0"])
        assert args.command == "install"
        assert args.packages == ["@user/pkg:1.0.0"]
        assert args.force is False

    def test_install_command_multiple_packages(self, parser):
        """Test install command parses multiple packages."""
        args = parser.parser.parse_args(["install", "@user/pkg1:1.0.0", "@user/pkg2:2.0.0"])
        assert args.command == "install"
        assert len(args.packages) == 2
        assert "@user/pkg1:1.0.0" in args.packages
        assert "@user/pkg2:2.0.0" in args.packages

    def test_install_command_with_force_flag(self, parser):
        """Test install command parses --force flag."""
        args = parser.parser.parse_args(["install", "@user/pkg:1.0.0", "--force"])
        assert args.command == "install"
        assert args.force is True

    def test_install_command_requires_packages(self, parser):
        """Test install command fails without package arguments."""
        with pytest.raises(SystemExit):
            parser.parser.parse_args(["install"])

    # Tests for remove command argument parsing
    def test_remove_command_single_package(self, parser):
        """Test remove command parses single package."""
        args = parser.parser.parse_args(["remove", "@user/pkg:1.0.0"])
        assert args.command == "remove"
        assert args.packages == ["@user/pkg:1.0.0"]
        assert args.force is False

    def test_remove_command_multiple_packages(self, parser):
        """Test remove command parses multiple packages."""
        args = parser.parser.parse_args(["remove", "@user/pkg1:1.0.0", "@user/pkg2:2.0.0"])
        assert args.command == "remove"
        assert len(args.packages) == 2
        assert "@user/pkg1:1.0.0" in args.packages
        assert "@user/pkg2:2.0.0" in args.packages

    def test_remove_command_with_force_flag(self, parser):
        """Test remove command parses --force flag."""
        args = parser.parser.parse_args(["remove", "@user/pkg:1.0.0", "--force"])
        assert args.command == "remove"
        assert args.force is True

    def test_remove_command_requires_packages(self, parser):
        """Test remove command fails without package arguments."""
        with pytest.raises(SystemExit):
            parser.parser.parse_args(["remove"])

    # Tests for check_pkgformat method (validation logic)
    def test_check_pkgformat_calls_formatter(self, parser):
        """Test that check_pkgformat calls Formatter.check_pkgformat."""
        args = MagicMock()
        args.packages = ["@user/pkg:1.0.0"]

        with patch("dotcop.parser.Formatter") as MockFormatter:
            mock_formatter = MockFormatter.return_value
            mock_formatter.check_pkgformat.return_value = True

            parser.check_pkgformat(args)
            mock_formatter.check_pkgformat.assert_called_once_with("@user/pkg:1.0.0")

    def test_check_pkgformat_keeps_valid_packages(self, parser):
        """Test that check_pkgformat retains valid packages."""
        args = MagicMock()
        args.packages = ["@user/pkg1:1.0.0", "@user/pkg2:2.0.0"]

        with patch("dotcop.parser.Formatter") as MockFormatter:
            mock_formatter = MockFormatter.return_value
            mock_formatter.check_pkgformat.return_value = True

            parser.check_pkgformat(args)
            assert args.packages == ["@user/pkg1:1.0.0", "@user/pkg2:2.0.0"]

    def test_check_pkgformat_filters_invalid_packages(self, parser):
        """Test that check_pkgformat filters out invalid packages."""
        args = MagicMock()
        args.packages = ["@user/pkg1:1.0.0", "invalid", "@user/pkg2:2.0.0"]

        with patch("dotcop.parser.Formatter") as MockFormatter:
            mock_formatter = MockFormatter.return_value
            # First call returns True, second False, third True
            mock_formatter.check_pkgformat.side_effect = [True, False, True]

            parser.check_pkgformat(args)
            assert args.packages == ["@user/pkg1:1.0.0", "@user/pkg2:2.0.0"]
            assert "invalid" not in args.packages

    def test_check_pkgformat_raises_when_all_invalid(self, parser):
        """Test that check_pkgformat raises RuntimeError when all packages are invalid."""
        args = MagicMock()
        args.packages = ["invalid1", "invalid2"]

        with patch("dotcop.parser.Formatter") as MockFormatter:
            mock_formatter = MockFormatter.return_value
            mock_formatter.check_pkgformat.return_value = False

            with pytest.raises(RuntimeError):
                parser.check_pkgformat(args)

    def test_check_pkgformat_logs_critical_on_all_invalid(self, parser):
        """Test that critical log is called when all packages are invalid."""
        args = MagicMock()
        args.packages = ["invalid1", "invalid2"]

        with patch("dotcop.parser.Formatter") as MockFormatter:
            mock_formatter = MockFormatter.return_value
            mock_formatter.check_pkgformat.return_value = False

            with patch.object(parser.logger, "critical") as mock_critical:
                with pytest.raises(RuntimeError):
                    parser.check_pkgformat(args)

                mock_critical.assert_called_once()
                call_args = mock_critical.call_args[0][0]
                assert "Invalid packages" in call_args

    def test_parse_arguments_calls_check_pkgformat_when_packages_present(self, parser):
        """Test that parse_arguments validates packages when present."""
        with patch.object(parser.parser, "parse_args") as mock_parse:
            mock_args = MagicMock()
            mock_args.command = "install"
            mock_args.packages = ["@user/pkg:1.0.0"]
            mock_parse.return_value = mock_args

            with patch.object(parser, "check_pkgformat") as mock_check:
                parser.parse_arguments()
                mock_check.assert_called_once_with(mock_args)

    def test_parse_arguments_skips_validation_without_packages(self, parser):
        """Test that parse_arguments skips validation when no packages attribute."""
        with patch.object(parser.parser, "parse_args") as mock_parse:
            mock_args = MagicMock(spec=["command"])
            mock_args.command = "status"
            mock_parse.return_value = mock_args

            with patch.object(parser, "check_pkgformat") as mock_check:
                parser.parse_arguments()
                mock_check.assert_not_called()

    def test_parse_arguments_propagates_exceptions(self, parser):
        """Test that exceptions during parsing are propagated."""
        with patch.object(parser.parser, "parse_args") as mock_parse:
            mock_parse.side_effect = ValueError("Test error")

            with pytest.raises(ValueError, match="Test error"):
                parser.parse_arguments()

    # Edge case tests
    def test_invalid_command_rejected(self, parser):
        """Test that invalid commands are rejected by argparse."""
        with pytest.raises(SystemExit):
            parser.parser.parse_args(["invalid_command"])

    def test_force_flag_defaults_to_false(self, parser):
        """Test that --force flag defaults to False when not provided."""
        args = parser.parser.parse_args(["install", "@user/pkg"])
        assert args.force is False

        args = parser.parser.parse_args(["remove", "@user/pkg"])
        assert args.force is False

    def test_multiple_packages_with_various_formats(self, parser):
        """Test parsing multiple packages with different format styles."""
        args = parser.parser.parse_args(["install", "@user/pkg1:1.0.0", "@another/pkg2", "@test/pkg3:2.3.4-beta"])
        assert len(args.packages) == 3
        assert args.packages[0] == "@user/pkg1:1.0.0"
        assert args.packages[1] == "@another/pkg2"
        assert args.packages[2] == "@test/pkg3:2.3.4-beta"
