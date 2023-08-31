"""Test Taegis Alerts Magics."""

import pytest
import pandas as pd
from taegis_magic.commands.alerts import AlertsResultsNormalizer
from taegis_magic.pandas.alerts import get_alerts_from_aggregation


def test_alerts_search_assign(ip):
    """Test %taegis alerts search."""
    with pytest.raises(KeyError):
        ip.user_ns["dataframe"]

    ip.run_cell_magic(
        "taegis",
        "alerts search --assign dataframe",
        "FROM alert EARLIEST=-1d | head 10",
    )

    dataframe = ip.user_ns["dataframe"]

    assert isinstance(dataframe, pd.DataFrame), "--assign didn't assign as a DataFrame"

    assert dataframe.shape[0] <= 10, "dataframe shape is incorrect"


def test_alerts_search_aggregate(ip):
    """Test %taegis alerts search with aggregates."""
    with pytest.raises(KeyError):
        ip.user_ns["dataframe"]

    ip.run_cell_magic(
        "taegis",
        "alerts search --assign dataframe",
        "FROM alert EARLIEST=-1d | aggregate count by metadata.title | head 10",
    )

    dataframe = ip.user_ns["dataframe"]

    assert isinstance(dataframe, pd.DataFrame), "--assign didn't assign as a DataFrame"

    assert dataframe.shape[0] <= 10, "dataframe shape is incorrect"


def test_alerts_normalizer(ip):
    """Test %taegis alerts search."""
    with pytest.raises(KeyError):
        ip.user_ns["_taegis_magic_result"]

    ip.run_cell_magic(
        "taegis",
        "alerts search --assign dataframe",
        "FROM alert EARLIEST=-1d | head 10",
    )

    taegis_magic_result = ip.user_ns["_taegis_magic_result"]

    assert isinstance(
        taegis_magic_result, AlertsResultsNormalizer
    ), "results not normalized properly"
    assert taegis_magic_result.status == "OK"
    assert taegis_magic_result.total_results <= 10
    assert taegis_magic_result.results_returned <= 10


def test_alerts_search_pagination(ip):
    """Test %taegis alerts search integration."""
    ip.run_cell_magic(
        "taegis",
        "--debug alerts search --tenant 5000 --limit 30000 --assign dataframe",
        "FROM alert EARLIEST=-1d",
    )

    dataframe = ip.user_ns["dataframe"]

    # shape[0] is the number of rows
    assert dataframe.shape[0] <= 30000


def test_alerts_search_with_query_and_sharelinks(ip):
    """Test %taegis alerts search integration."""
    ip.run_cell_magic(
        "taegis",
        "alerts search --tenant 5000 --limit 5 --assign dataframe",
        "FROM alert WHERE severity >= 0.6 EARLIEST=-1d",
    )

    taegis_magic_result = ip.user_ns["_taegis_magic_result"]

    assert taegis_magic_result.query_identifier is not None
    assert taegis_magic_result.shareable_url is not None


def test_raw_alerts_from_aggregation(ip):
    """Test alerts.pandas get_alerts_from_aggregation."""
    ip.run_cell_magic(
        "taegis",
        "alerts search --tenant 5000 --assign aggregate",
        """
        FROM alert 
        WHERE 
            severity >= 0.6
        EARLIEST=-1d
         | aggregate count by metadata.title, tenant_id
         | head 5
        """,
    )

    aggregate = ip.user_ns["aggregate"]

    raw_alerts = aggregate.pipe(get_alerts_from_aggregation)

    assert (
        raw_alerts["metadata.title"]
        .str.lower()
        .isin(aggregate["metadata.title"].unique())
        .all()
    )
    assert (
        raw_alerts["tenant_id"].str.lower().isin(aggregate["tenant_id"].unique()).all()
    )
