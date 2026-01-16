# tests/test_config.py
import pytest
import yaml
from unittest.mock import patch, MagicMock


@pytest.fixture
def config_instance():
    """Fixture to create a Config instance"""
    from dotcop.data.load_dotcop_configuration import DotcopConfiguration

    return Config()


def test_test_configfile_missing_xdg_config_home(config_instance, monkeypatch):
    """Test that test_configfile raises EnvironmentError when XDG_CONFIG_HOME is not set"""
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)

    with pytest.raises(EnvironmentError):
        config_instance.test_configfile()


def test_test_configfile_invalid_xdg_config_home(config_instance, monkeypatch, tmp_path):
    """Test that test_configfile raises EnvironmentError when XDG_CONFIG_HOME is not a directory"""
    # Point to a file instead of directory
    fake_file = tmp_path / "not_a_directory"
    fake_file.touch()
    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_file))

    with pytest.raises(EnvironmentError):
        config_instance.test_configfile()


def test_test_configfile_creates_config_directory(config_instance, monkeypatch, tmp_path):
    """Test that test_configfile creates the dotcop config directory if it doesn't exist"""
    fake_config_home = tmp_path / "config"
    fake_config_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_config_home))

    # Mock RootFinder and file operations
    with (
        patch("dotcop.config.RootFinder") as mock_root_finder,
        patch("dotcop.config.shutil.copyfile"),
    ):
        mock_finder = MagicMock()
        mock_finder.find_root.return_value = tmp_path / "project_root"
        mock_root_finder.return_value = mock_finder

        # Create the source file
        src_file = tmp_path / "project_root" / "dotcop.yml"
        src_file.parent.mkdir(parents=True, exist_ok=True)
        src_file.write_text("test: config")

        config_instance.test_configfile()

        # Check that the dotcop directory was created
        config_dir = fake_config_home / "dotcop"
        assert config_dir.exists()
        assert config_dir.is_dir()


def test_test_configfile_copies_default_config(config_instance, monkeypatch, tmp_path):
    """Test that test_configfile copies the default config file from project root"""
    fake_config_home = tmp_path / "config"
    fake_config_home.mkdir(parents=True, exist_ok=True)
    config_dir = fake_config_home / "dotcop"
    config_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_config_home))

    # Create a fake project root with default config
    fake_root = tmp_path / "project_root"
    fake_root.mkdir(parents=True, exist_ok=True)
    default_config = fake_root / "dotcop.yml"
    default_config.write_text("default: configuration")

    with patch("dotcop.config.RootFinder") as mock_root_finder:
        mock_finder = MagicMock()
        mock_finder.find_root.return_value = fake_root
        mock_root_finder.return_value = mock_finder

        config_instance.test_configfile()

        # Check that config was copied
        config_path = config_dir / "dotcop.yml"
        assert config_path.exists()
        assert config_path.read_text() == "default: configuration"


def test_test_configfile_existing_config_not_overwritten(config_instance, monkeypatch, tmp_path):
    """Test that test_configfile doesn't overwrite existing config file"""
    fake_config_home = tmp_path / "config"
    fake_config_home.mkdir(parents=True, exist_ok=True)
    config_dir = fake_config_home / "dotcop"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Create existing config
    config_path = config_dir / "dotcop.yml"
    config_path.write_text("existing: configuration")

    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_config_home))

    config_instance.test_configfile()

    # Check that existing config was not overwritten
    assert config_path.read_text() == "existing: configuration"
    assert config_instance.config_path == config_path


def test_test_configfile_root_finder_fails(config_instance, monkeypatch, tmp_path):
    """Test that test_configfile raises FileNotFoundError when RootFinder fails"""
    fake_config_home = tmp_path / "config"
    fake_config_home.mkdir(parents=True, exist_ok=True)
    config_dir = fake_config_home / "dotcop"
    config_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_config_home))

    with patch("dotcop.config.RootFinder") as mock_root_finder:
        mock_finder = MagicMock()
        mock_finder.find_root.side_effect = FileNotFoundError()
        mock_root_finder.return_value = mock_finder

        with pytest.raises(FileNotFoundError):
            config_instance.test_configfile()


def test_test_configfile_missing_default_config(config_instance, monkeypatch, tmp_path):
    """Test that test_configfile raises FileNotFoundError when default config is missing"""
    fake_config_home = tmp_path / "config"
    fake_config_home.mkdir(parents=True, exist_ok=True)
    config_dir = fake_config_home / "dotcop"
    config_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_config_home))

    # Create a fake project root WITHOUT default config
    fake_root = tmp_path / "project_root"
    fake_root.mkdir(parents=True, exist_ok=True)

    with patch("dotcop.config.RootFinder") as mock_root_finder:
        mock_finder = MagicMock()
        mock_finder.find_root.return_value = fake_root
        mock_root_finder.return_value = mock_finder

        with pytest.raises(FileNotFoundError):
            config_instance.test_configfile()


def test_load_configfile_success(config_instance, monkeypatch, tmp_path):
    """Test that load_configfile successfully loads a valid YAML config"""
    fake_config_home = tmp_path / "config"
    fake_config_home.mkdir(parents=True, exist_ok=True)
    config_dir = fake_config_home / "dotcop"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Create a valid config file
    config_path = config_dir / "dotcop.yml"
    config_data = {"key": "value", "nested": {"item": 123}}
    config_path.write_text(yaml.dump(config_data))

    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_config_home))

    result = config_instance.load_configfile()

    assert result == config_data
    assert config_instance.config_path == config_path


def test_load_configfile_invalid_yaml(config_instance, monkeypatch, tmp_path):
    """Test that load_configfile raises YAMLError for invalid YAML"""
    from yaml import YAMLError

    fake_config_home = tmp_path / "config"
    fake_config_home.mkdir(parents=True, exist_ok=True)
    config_dir = fake_config_home / "dotcop"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Create an invalid YAML file
    config_path = config_dir / "dotcop.yml"
    config_path.write_text("invalid: yaml: content: [broken")

    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_config_home))

    with pytest.raises(YAMLError):
        config_instance.load_configfile()


def test_load_configfile_calls_test_configfile(config_instance, monkeypatch, tmp_path):
    """Test that load_configfile calls test_configfile first"""
    fake_config_home = tmp_path / "config"
    fake_config_home.mkdir(parents=True, exist_ok=True)
    config_dir = fake_config_home / "dotcop"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_path = config_dir / "dotcop.yml"
    config_path.write_text("test: data")

    monkeypatch.setenv("XDG_CONFIG_HOME", str(fake_config_home))

    with patch.object(config_instance, "test_configfile") as mock_test:
        mock_test.return_value = None
        config_instance.config_path = config_path

        config_instance.load_configfile()

        mock_test.assert_called_once()


def test_load_configfile_propagates_test_configfile_exceptions(config_instance):
    """Test that load_configfile propagates exceptions from test_configfile"""
    with patch.object(config_instance, "test_configfile") as mock_test:
        mock_test.side_effect = EnvironmentError("Test error")

        with pytest.raises(EnvironmentError):
            config_instance.load_configfile()
