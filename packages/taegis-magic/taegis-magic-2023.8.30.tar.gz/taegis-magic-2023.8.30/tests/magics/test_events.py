"""Test Taegis Events Magics."""

import pandas as pd
import pytest
from taegis_magic.commands.events import (
    TaegisEventNormalizer,
    TaegisEventQueryNormalizer,
)


def test_events_search_assign(ip):
    """Test %taegis events search."""
    with pytest.raises(KeyError):
        ip.user_ns["dataframe"]

    ip.run_cell_magic(
        "taegis",
        "events search --tenant 50530 --region charlie --assign dataframe",
        "FROM process EARLIEST=-1d | head 5",
    )

    dataframe = ip.user_ns["dataframe"]

    assert isinstance(dataframe, pd.DataFrame), "--assign didn't assign as a DataFrame"

    assert dataframe.shape[0] <= 5, "dataframe shape is incorrect"


def test_events_search_aggregate_assign(ip):
    """Test %taegis events search."""
    with pytest.raises(KeyError):
        ip.user_ns["dataframe"]

    ip.run_cell_magic(
        "taegis",
        "events search --tenant 50530 --region charlie --assign dataframe",
        "FROM process EARLIEST=-1d | aggregate count by host_id, image_path | head 5",
    )

    dataframe = ip.user_ns["dataframe"]

    assert isinstance(dataframe, pd.DataFrame), "--assign didn't assign as a DataFrame"

    assert dataframe.shape[0] <= 5, "dataframe shape is incorrect"


def test_events_events_assign(ip):
    """Test %taegis events search."""
    with pytest.raises(KeyError):
        ip.user_ns["dataframe"]

    ip.run_line_magic(
        "taegis",
        "events events --tenant 50530 --region charlie --assign dataframe "
        "--resource-id event://priv:scwx.process:50530:1685648727000:0906044b-fb44-5e1e-b850-6b82edd97fae "
        "--resource-id event://priv:scwx.process:50530:1685648727000:477def73-c5a3-52a4-bc2a-3140add290fc",
    )

    dataframe = ip.user_ns["dataframe"]

    assert isinstance(dataframe, pd.DataFrame), "--assign didn't assign as a DataFrame"

    assert dataframe.shape[0] <= 2, "dataframe shape is incorrect"


def test_alerts_search_with_query_and_sharelinks(ip):
    """Test %taegis alerts search integration."""
    ip.run_cell_magic(
        "taegis",
        "events search --tenant 50530 --region charlie --assign dataframe",
        "FROM process EARLIEST=-1d | head 5",
    )

    taegis_magic_result = ip.user_ns["_taegis_magic_result"]

    assert taegis_magic_result.query_identifier is not None
    assert taegis_magic_result.shareable_url is not None
