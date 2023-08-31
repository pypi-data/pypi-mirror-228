"""Test %taegis configure commands."""

import pytest
from taegis_magic.commands.configure import (
    LOGGING_SECTION,
    QUERIES_SECTION,
    REGIONS_SECTION,
    ConfigureLogging,
    LoggingOptions,
)
from taegis_sdk_python.config import get_config


def test_configure_regions_add(ip):
    """Test %taegis configure regions add."""
    ip.run_line_magic(
        "taegis", "configure regions add pilot https://api.pilot.8labs.io"
    )

    config = get_config()

    for name, url in config[REGIONS_SECTION].items():
        assert name == "pilot"
        assert url == "https://api.pilot.8labs.io"

    ip.run_line_magic("taegis", "configure regions remove pilot")


def test_configure_regions_remove(ip):
    """Test %taegis configure regions add."""
    ip.run_line_magic(
        "taegis", "configure regions add pilot https://api.pilot.8labs.io"
    )
    config = get_config()
    assert len(config[REGIONS_SECTION]) == 1

    ip.run_line_magic("taegis", "configure regions remove pilot")
    config = get_config()
    assert len(config[REGIONS_SECTION]) == 0


def test_configure_regions_list(ip):
    """Test %taegis configure regions add."""
    ip.run_line_magic(
        "taegis", "configure regions add pilot https://api.pilot.8labs.io"
    )
    ip.run_line_magic(
        "taegis", "configure regions add pilot2 https://api.pilot2.8labs.io"
    )
    ip.run_line_magic("taegis", "configure regions list --assign dataframe")

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.shape[0] == 2

    for _, row in dataframe.iterrows():
        ip.run_line_magic("taegis", f"configure regions remove {row['name']}")


def test_configure_regions_add_for_update(ip):
    """Test %taegis configure regions add."""
    ip.run_line_magic(
        "taegis", "configure regions add pilot https://api.pilot.8labs.io"
    )

    config = get_config()

    for name, url in config[REGIONS_SECTION].items():
        assert name == "pilot"
        assert url == "https://api.pilot.8labs.io"

    ip.run_line_magic("taegis", "configure regions add pilot http://localhost")

    config = get_config()

    for name, url in config[REGIONS_SECTION].items():
        assert name == "pilot"
        assert url == "http://localhost"

    ip.run_line_magic("taegis", "configure regions remove pilot")


def test_queries_track(ip):
    """Test %taegis configure queries track."""
    ip.run_line_magic("taegis", "configure queries track --status yes")

    config = get_config()

    assert config[QUERIES_SECTION].getboolean("track") is True


def test_queries_list(ip):
    """Test %taegis configure queries list."""
    ip.run_line_magic("taegis", "configure queries track --status yes")
    ip.run_line_magic("taegis", "configure queries list --assign queries_config")

    queries_config = ip.user_ns["queries_config"]

    assert queries_config.loc[0, "name"] == "track"
    assert queries_config.loc[0, "value"] == "yes"


@pytest.mark.parametrize("option", [member.value for member in LoggingOptions])
@pytest.mark.parametrize("status", [member.value for member in ConfigureLogging])
def test_logging_defaults(ip, option, status):
    """Test %taegis configure logging defaults."""
    ip.run_line_magic(
        "taegis", f"configure logging defaults {option} --status {status}"
    )

    config = get_config()

    truthy = True if status == "true" else False

    assert config[LOGGING_SECTION].getboolean(option) is truthy
