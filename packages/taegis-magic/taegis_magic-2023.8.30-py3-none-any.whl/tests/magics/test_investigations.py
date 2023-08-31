"""Test Taegis Investigations Magics."""

import pytest
import pandas as pd

from pathlib import Path

from taegis_sdk_python.services.investigations2.types import (
    InvestigationV2,
    InvestigationsV2,
)
from taegis_magic.commands.investigations import (
    InvestigationsSearchResultsNormalizer,
    InvestigationsCreatedResultsNormalizer,
)
from taegis_magic.commands.utils.investigations import (
    get_or_create_database,
    read_database,
    InvestigationEvidenceType,
)


def test_investigations_search_results_normalizer():
    """Test InvestigationsSearchResultsNormalizer functionality."""
    investigations_v2 = InvestigationsV2.from_json(
        Path("tests/magics/investigations_v2.json").read_text(encoding="utf-8")
    )
    normalized_results = InvestigationsSearchResultsNormalizer(
        raw_results=[investigations_v2],
        service="investigations",
        tenant_id="50530",
        region="charlie",
        arguments={
            "cell": "archived_at IS NOT NULL",
            "limit": 1,
            "region": "charlie",
            "tenant": "50530",
        },
    )

    assert len(normalized_results._shareable_url) == 1
    assert normalized_results._shareable_url == [None]
    assert (
        normalized_results.results[0].get("id")
        == "04cfff95-730e-453a-a8a8-a1f7d5b99034"
    )
    assert normalized_results.status == "SUCCESS"
    assert normalized_results.total_results == 354
    assert normalized_results.results_returned == 1

    share_link = normalized_results.get_shareable_url(0)
    assert share_link.startswith("https://")
    assert normalized_results.get_shareable_url(0) == share_link


def test_investigations_create_results_normalizer():
    """Test InvestigationsCreatedResultsNormalizer functionality."""
    investigation_v2 = InvestigationV2.from_json(
        Path("tests/magics/create_investigation_v2.json").read_text(encoding="utf-8")
    )
    normalized_results = InvestigationsCreatedResultsNormalizer(
        raw_results=investigation_v2,
        service="investigations",
        tenant_id="50530",
        region="charlie",
        arguments={
            "title": "mpegman - test investigation [do not delete/archive]",
            "key_findings": "This is for a test.  Please do not delete.",
            "priority": 1,
            "type": "SECURITY_INVESTIGATION",
            "status": "OPEN",
            "assignee_id": "auth0|5d3783714ba1270de8ebef08",
            "database": None,
            "dry_run": False,
            "region": "charlie",
            "tenant": "50530",
        },
        dry_run=False,
    )

    share_link = normalized_results.shareable_url

    assert (
        normalized_results.results[0].get("id")
        == "74051731-eded-474e-a16b-556a9fd56e6d"
    )
    assert normalized_results.status == "SUCCESS"
    assert normalized_results.total_results == 1
    assert normalized_results.results_returned == 1
    assert share_link.startswith("https://")
    assert normalized_results.shareable_url == share_link


def test_stage(ip):
    """Test %taegis investigations evidence stage."""
    alerts_df = pd.DataFrame(
        [
            {
                "id": "alert://abc123",
                "tenant_id": "99999",
            },
            {
                "id": "alert://xyz789",
                "tenant_id": "99999",
            },
            {
                "id": "alert://qwert456",
                "tenant_id": "22222",
            },
        ]
    )

    db = get_or_create_database()

    ip.user_ns["investigation_input_db"] = db
    ip.user_ns["alerts_df"] = alerts_df

    ip.run_line_magic("taegis", "investigations evidence stage alerts alerts_df")

    staged_evidence = read_database(db, evidence_type=InvestigationEvidenceType.Alert)

    assert len(alerts_df) == len(staged_evidence)


def test_unstage(ip, in_memory_database):
    """Test %taegis investigations evidence unstage."""
    alerts_to_remove = pd.DataFrame(
        [
            {
                "id": "alert://abc123",
                "tenant_id": "99999",
            },
            {
                "id": "alert://xyz789",
                "tenant_id": "99999",
            },
        ]
    )

    ip.user_ns["investigation_input_db"] = in_memory_database
    ip.user_ns["alerts_to_remove"] = alerts_to_remove

    ip.run_line_magic(
        "taegis", "investigations evidence unstage alerts alerts_to_remove"
    )

    remaining_alert_evidence = read_database(
        in_memory_database, evidence_type=InvestigationEvidenceType.Alert
    )
    assert len(remaining_alert_evidence) == 1

    unrelated_event_evidence = read_database(
        in_memory_database, evidence_type=InvestigationEvidenceType.Event
    )
    # Should remain unchanged/unaffected
    assert len(unrelated_event_evidence) == 4


def test_investigations_evidence_show(ip, in_memory_database):
    """Test %taegis investigations evidence show."""
    ip.user_ns["investigation_input_db"] = in_memory_database
    ip.run_line_magic(
        "taegis", "investigations evidence show --assign all_staged_evidence"
    )
    all_staged_evidence = ip.user_ns["all_staged_evidence"]
    assert len(all_staged_evidence) == 7

    ip.run_line_magic(
        "taegis",
        "investigations evidence show --evidence-type events --assign staged_events",
    )
    staged_events = ip.user_ns["staged_events"]
    assert len(staged_events) == 4

    ip.run_line_magic(
        "taegis",
        "investigations evidence show --tenant 99999 --assign staged_for_tenant",
    )
    staged_for_tenant = ip.user_ns["staged_for_tenant"]
    assert len(staged_for_tenant) == 5


def test_investigations_create_dry_run(ip):
    """Test %taegis investigations create."""
    ip.run_line_magic(
        "taegis",
        "investigations create --tenant 50530 --region charlie "
        "--title 'Test Title' --key-findings tests/magics/test_keyfindings.md "
        "--type SECURITY_INVESTIGATION --status OPEN "
        "--assignee-id auth0|5d3783714ba1270de8ebef08 --dry-run "
        "--assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.shape[0] == 1


@pytest.mark.parametrize("head", [3, 100, 150, 301, 500])
def test_investigations_search(ip, head):
    """Test %taegis investigations search."""
    ip.run_cell_magic(
        "taegis",
        "investigations search --tenant 50530 --region charlie --assign dataframe",
        f"archived_at IS NOT NULL | head {head}",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.shape[0] <= head


def test_investigations_search_queries_add(ip):
    """Test %taegis investigations search-queries add."""
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 12345 --tenant-id 00000 "
        "--query 'FROM alert EARLIEST=-1d | head 5' --results-returned 5 --total-results 5 "
        "--assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.loc[0, "id"] == "12345"
    assert dataframe.loc[0, "tenant_id"] == "00000"
    assert dataframe.loc[0, "query"] == "FROM alert EARLIEST=-1d | head 5"
    assert dataframe.loc[0, "results_returned"] == 5
    assert dataframe.loc[0, "total_results"] == 5


def test_investigations_search_queries_remove(ip):
    """Test %taegis investigations search-queries add."""
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 12345 --tenant-id 00000 "
        "--query 'FROM alert EARLIEST=-1d | head 5' --results-returned 5 --total-results 5 "
        "--assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert not dataframe.empty

    ip.run_line_magic(
        "taegis",
        "investigations search-queries remove --query-id 12345 --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.empty


def test_investigations_search_queries_list(ip):
    """Test %taegis investigations search-queries add."""
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 12345 --tenant-id 00000 "
        "--query 'FROM alert EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 23456 --tenant-id 00000 "
        "--query 'FROM auth EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 34567 --tenant-id 00000 "
        "--query 'FROM process EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )

    ip.run_line_magic(
        "taegis",
        "investigations search-queries list --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.shape[0] == 3

    ip.run_line_magic(
        "taegis",
        "investigations search-queries clear",
    )


def test_investigations_search_queries_clear(ip):
    """Test %taegis investigations search-queries add."""
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 12345 --tenant-id 00000 "
        "--query 'FROM alert EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 23456 --tenant-id 00000 "
        "--query 'FROM auth EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 34567 --tenant-id 00000 "
        "--query 'FROM process EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )

    ip.run_line_magic(
        "taegis",
        "investigations search-queries list --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.shape[0] == 3

    ip.run_line_magic(
        "taegis",
        "investigations search-queries clear",
    )

    ip.run_line_magic(
        "taegis",
        "investigations search-queries list --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.empty


def test_investigations_search_queries_stage(ip):
    """Test %taegis investigations search-queries add."""
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 12345 --tenant-id 00000 "
        "--query 'FROM alert EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 23456 --tenant-id 00000 "
        "--query 'FROM auth EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )
    ip.run_line_magic(
        "taegis",
        "investigations search-queries add --query-id 34567 --tenant-id 00000 "
        "--query 'FROM process EARLIEST=-1d | head 5' --results-returned 5 --total-results 5",
    )

    ip.run_line_magic(
        "taegis",
        "investigations search-queries list --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.shape[0] == 3

    ip.run_line_magic(
        "taegis",
        "investigations search-queries stage",
    )

    ip.run_line_magic(
        "taegis",
        "investigations search-queries list --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.empty

    ip.run_line_magic("taegis", "investigations evidence show --assign dataframe")

    dataframe = ip.user_ns["dataframe"]

    assert dataframe[dataframe["evidence_type"] == "search_queries"].shape[0] == 3


@pytest.mark.skip("documentation test")
def test_investigations_create(ip):
    """Test showcasing how investigations create works."""

    ### Investigating Alerts ###
    from taegis_magic.pandas.alerts import inflate_raw_events

    ip.run_cell_magic(
        "taegis",
        "alerts search --tenant 50530 --region charlie --assign alerts_evidence --track",
        """
        FROM alert
        WHERE
            metadata.title = 'Suspicious AWS Account Enumeration' AND
            status = 'OPEN' AND
            metadata.severity > 0.2 AND
            investigation_ids IS NULL
        EARLIEST=-3d | head 2
        """,
    )

    ip.run_line_magic("taegis", "investigations evidence stage alerts alerts_evidence")

    ### Showcase Alerts->Events pivot ###
    alerts_evidence = ip.user_ns["alerts_evidence"]
    alerts_evidence = alerts_evidence.pipe(inflate_raw_events)
    username = alerts_evidence["event_data.user_name"].unique()[0]

    ### Investigating Events ###
    ip.run_cell_magic(
        "taegis",
        "events search --tenant 50530 --region charlie --assign events_evidence --track",
        f"""
        FROM cloudaudit 
        WHERE 
            user_name = '{username}' 
        EARLIEST=-3d | head 2
        """,
    )

    ip.run_line_magic("taegis", "investigations evidence stage events events_evidence")

    ip.run_line_magic(
        "taegis",
        "investigations search-queries list --assign queries --display queries",
    )

    # optional
    # ip.run_line_magic("taegis", "investigations search-queries remove --query-id <uuid>")

    ip.run_line_magic("taegis", "investigations search-queries stage")

    ### Review Evidence ###
    ip.run_line_magic("taegis", "investigations evidence show")

    ### Create the Investigation
    ip.run_line_magic(
        "taegis",
        "investigations create --title 'Micah Magic Test' --key-findings 'test_keyfindings.md' "
        "--priority LOW --type SECURITY_INVESTIGATION --status DRAFT "
        "--assignee-id 'auth0|5d3783714ba1270de8ebef08' --region charlie --tenant 50530",
    )
