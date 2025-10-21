import pytest
from unittest.mock import Mock, patch
from dotcop.utils.formatter import Formatter


class TestFormatter:
    @pytest.fixture
    def formatter(self):
        """Create a Formatter instance for testing."""
        with patch('dotcop.utils.formatter.Logger'):
            return Formatter()
    
    # Tests for check_version method
    def test_check_version_valid_simple(self, formatter):
        """Test valid simple semantic version."""
        assert formatter.check_version("1.0.0") is True
    
    def test_check_version_valid_with_prerelease(self, formatter):
        """Test valid version with prerelease tag."""
        assert formatter.check_version("1.0.0-alpha") is True
        assert formatter.check_version("2.1.3-beta.1") is True
    
    def test_check_version_valid_with_build(self, formatter):
        """Test valid version with build metadata."""
        assert formatter.check_version("1.0.0+20130313144700") is True
        assert formatter.check_version("1.0.0-beta+exp.sha.5114f85") is True
    
    def test_check_version_invalid_format(self, formatter):
        """Test invalid version formats."""
        assert formatter.check_version("1.0") is False
        assert formatter.check_version("v1.0.0") is False
        assert formatter.check_version("1.0.0.0") is False
        assert formatter.check_version("invalid") is False
        assert formatter.check_version("") is False
    
    # Tests for check_pkgformat method
    def test_check_pkgformat_valid_with_version(self, formatter):
        """Test valid package format with version."""
        assert formatter.check_pkgformat("@user/pkgname:1.0.0") is True
        assert formatter.check_pkgformat("@john/myapp:2.3.4") is True
        assert formatter.check_pkgformat("@dev/tool:1.0.0-alpha") is True
    
    def test_check_pkgformat_valid_without_version(self, formatter):
        """Test valid package format without version."""
        assert formatter.check_pkgformat("@user/pkgname") is True
        assert formatter.check_pkgformat("@alice/config") is True
    
    def test_check_pkgformat_invalid_version(self, formatter):
        """Test package with invalid version format."""
        assert formatter.check_pkgformat("@user/pkgname:1.0") is False
        assert formatter.check_pkgformat("@user/pkgname:invalid") is False
        assert formatter.check_pkgformat("@user/pkgname:v1.0.0") is False
    
    def test_check_pkgformat_invalid_format(self, formatter):
        """Test invalid package name formats."""
        assert formatter.check_pkgformat("user/pkgname") is False  # Missing @
        assert formatter.check_pkgformat("@user-pkgname") is False  # Missing /
        assert formatter.check_pkgformat("@user/") is False  # Missing package name
        assert formatter.check_pkgformat("@/pkgname") is False  # Missing user
        assert formatter.check_pkgformat("pkgname") is False  # No user prefix
        assert formatter.check_pkgformat("") is False  # Empty string
    
    def test_check_pkgformat_edge_cases(self, formatter):
        """Test edge cases for package format."""
        # Package names with numbers and special chars
        assert formatter.check_pkgformat("@user123/pkg-name") is True
        assert formatter.check_pkgformat("@user/pkg_name:1.0.0") is True
    
    def test_check_pkgformat_logging_invalid_format(self, formatter):
        """Test logging for invalid package format."""
        with patch.object(formatter.logger, 'error') as mock_error:
            formatter.check_pkgformat("invalid_format")
            mock_error.assert_called_once()
            assert "Invalid package name format" in mock_error.call_args[0][0]
    
    def test_check_pkgformat_logging_invalid_version(self, formatter):
        """Test logging for invalid version format."""
        with patch.object(formatter.logger, 'error') as mock_error:
            formatter.check_pkgformat("@user/pkg:badversion")
            mock_error.assert_called_once()
            assert "Invalid version format" in mock_error.call_args[0][0]
    
    @pytest.mark.parametrize("pkg,expected", [
        ("@user/pkg:1.0.0", True),
        ("@user/pkg", True),
        ("@user/pkg:2.1.3-beta.1+build", True),
        ("@user/pkg:1.0", False),
        ("user/pkg", False),
        ("@user/pkg:invalid", False),
        ("@alice/myconfig:3.2.1", True),
        ("@test/app", True),
    ])
    def test_check_pkgformat_parametrized(self, formatter, pkg, expected):
        """Parametrized test for various package formats."""
        assert formatter.check_pkgformat(pkg) is expected
