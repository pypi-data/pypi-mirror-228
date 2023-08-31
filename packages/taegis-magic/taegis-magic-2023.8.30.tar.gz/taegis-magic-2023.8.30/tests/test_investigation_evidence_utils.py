"""Test Taegis Investigation Evidence Utils."""

import pandas as pd
import pytest
from taegis_magic.commands.utils.investigations import (
    InvestigationEvidence,
    InvestigationEvidenceChanges,
    InvestigationEvidenceNormalizer,
    InvestigationEvidenceType,
    find_database,
    find_dataframe,
    get_investigation_evidence,
    get_or_create_database,
    read_database,
    stage_investigation_evidence,
    unstage_investigation_evidence,
)


def test_investigation_evidence_normalizer():
    """Test InvestigationEvidenceNormalizer."""
    normalizer = InvestigationEvidenceNormalizer(
        raw_results=InvestigationEvidenceChanges(
            action="stage",
            evidence_type=InvestigationEvidenceType.Alert,
            investigation_id="1",
            before=3,
            after=5,
            difference=2,  # property?
        ),
        service="investigations",
        tenant_id="N/A",
        region="N/A",
        arguments={},
    )

    assert "**Investigation ID**: 1" in normalizer._repr_markdown_()
    assert set(["raw_results", "service", "tenant_id", "region", "arguments"]) == set(
        normalizer.to_dict().keys()
    )
    assert set(
        ["action", "evidence_type", "investigation_id", "before", "after", "difference"]
    ) == set(normalizer.results[0].keys())


def test_get_or_create_database():
    """Test get_or_create_database."""
    db = get_or_create_database()

    tables = db.execute(
        """
        SELECT name
        FROM sqlite_schema
        WHERE
            type = 'table'
        ;"""
    ).fetchall()
    # The investigation_evidence table should be present
    assert any(
        ["investigation_evidence" in table for table in tables]
    ), "investigation_evidence table missing from database"

    column_metadata = db.execute(
        "PRAGMA table_info(investigation_evidence);"
    ).fetchall()
    # There are four columns in the schema
    assert (
        len(column_metadata) == 4
    ), "The wrong number of columns was found in the database"

    col_names = ["evidence_type", "id", "tenant_id", "investigation_id"]
    # Column order matters for INSERT operations
    for idx, col_name in enumerate(col_names):
        assert (
            column_metadata[idx][1] == col_name,
            f"Column '{col_name}' in wrong order, should be in position {idx}",
        )


def test_stage_investigation_evidence():
    db = get_or_create_database()

    df1 = pd.DataFrame(
        [
            {
                "id": "alert://abc123",
                "tenant_id": "99999",
            },
            {
                "id": "alert://xyz789",
                "tenant_id": "11111",
            },
        ]
    )

    evidence_changes = stage_investigation_evidence(
        df1, db, InvestigationEvidenceType.Alert
    )

    assert evidence_changes.action == "stage"
    assert evidence_changes.before == 0
    assert evidence_changes.after == 2
    assert evidence_changes.difference == 2

    staged_evidence = read_database(
        db,
        evidence_type=InvestigationEvidenceType.Alert,
    )

    assert len(staged_evidence) == len(df1)

    df2 = pd.DataFrame(
        [
            # This one is intentionally a duplicate from df1!
            {
                "id": "alert://abc123",
                "tenant_id": "99999",
            },
            {
                "id": "alert://qwert456",
                "tenant_id": "22222",
            },
        ]
    )

    evidence_changes = stage_investigation_evidence(
        df2, db, InvestigationEvidenceType.Alert
    )

    assert evidence_changes.action == "stage"
    assert evidence_changes.before == 2
    assert evidence_changes.after == 3
    assert evidence_changes.difference == 1

    staged_evidence = read_database(
        db,
        evidence_type=InvestigationEvidenceType.Alert,
    )

    assert len(staged_evidence) == 3


def test_unstage_investigation_evidence():
    db = get_or_create_database()

    df1 = pd.DataFrame(
        [
            {
                "id": "alert://abc123",
                "tenant_id": "99999",
            },
            {
                "id": "alert://xyz789",
                "tenant_id": "11111",
            },
            {
                "id": "alert://qwert456",
                "tenant_id": "22222",
            },
        ]
    )

    stage_investigation_evidence(df1, db, InvestigationEvidenceType.Alert)

    df2 = pd.DataFrame(
        [
            {
                "id": "alert://qwert456",
                "tenant_id": "22222",
            }
        ]
    )

    evidence_changes = unstage_investigation_evidence(
        df2, db, InvestigationEvidenceType.Alert
    )

    assert evidence_changes.action == "unstage"
    assert evidence_changes.before == 3
    assert evidence_changes.after == 2
    assert evidence_changes.difference == -1

    staged_evidence = read_database(
        db,
        evidence_type=InvestigationEvidenceType.Alert,
    )

    assert len(staged_evidence) == 2


def test_get_investigation_evidence(on_disk_database):
    evidence = get_investigation_evidence("investigation_input.db", "99999")
    assert isinstance(evidence, InvestigationEvidence)
    assert evidence.tenant_id == "99999"
    assert evidence.investigation_id == "NEW"
    assert evidence.search_queries is None
    assert evidence.events is not None
    assert len(evidence.events) == 3
    assert evidence.alerts is not None
    assert len(evidence.alerts) == 2


def test_read_database(on_disk_database):
    all_rows = read_database(on_disk_database)

    assert len(all_rows) == 11
    # Test for filtering by evidence type
    alerts_rows = read_database(
        on_disk_database,
        InvestigationEvidenceType.Alert,
    )

    assert len(alerts_rows) == 3

    # Test for evidence type and tenant ID
    events_rows = read_database(
        on_disk_database,
        InvestigationEvidenceType.Event,
        tenant_id="99999",
    )

    assert len(events_rows) == 6

    # Test for evidence type, tenant ID, and investigation ID
    events_for_specific_investigation_rows = read_database(
        on_disk_database,
        InvestigationEvidenceType.Event,
        tenant_id="99999",
        investigation_id="investigation-id-12345",
    )

    assert len(events_for_specific_investigation_rows) == 3


def test_find_database_on_disk(on_disk_database):
    import sqlite3

    db = find_database("investigation_input.db")
    assert isinstance(db, sqlite3.Connection)


def test_find_database_in_notebook_namespace(ip):
    import sqlite3

    _db = get_or_create_database()
    ip.user_ns["investigation_input_db"] = _db
    db = find_database(None)
    assert isinstance(db, sqlite3.Connection)


def test_find_dataframe_in_notebook_namespace(ip):
    df = pd.DataFrame(
        [
            {
                "id": "alert://abc123",
                "tenant_id": "99999",
            },
            {
                "id": "alert://xyz789",
                "tenant_id": "11111",
            },
        ]
    )
    df.attrs["my_custom_attribute"] = "betcha didn't know you could do this"

    ip.user_ns["my_target_dataframe"] = df

    df = find_dataframe("my_target_dataframe")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df.attrs["my_custom_attribute"] == "betcha didn't know you could do this"


def test_find_dataframe_without_ipython(ip):
    """Test find_dataframe for on-disk JSON DataFrame."""
    df = find_dataframe("tests/test_reference.json")
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 3


def test_find_dataframe_not_found(ip):
    """Test find_dataframe when DataFrame is not found."""
    with pytest.raises(ValueError):
        find_dataframe("tests/test_reference_not_found.json")
