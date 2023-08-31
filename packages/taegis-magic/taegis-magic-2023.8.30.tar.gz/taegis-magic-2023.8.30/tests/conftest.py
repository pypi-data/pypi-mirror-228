import pytest

from taegis_magic.commands.utils.investigations import (
    get_or_create_database,
    stage_investigation_evidence,
    InvestigationEvidenceType,
)
import pandas as pd
from pathlib import Path


@pytest.fixture(scope="function")
def on_disk_database():
    """Create an on-disk database for investigations."""
    db_file_path = Path("investigation_input.db")
    db = get_or_create_database(db_file_path.name)
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

    events_df = pd.DataFrame(
        [
            {
                "id": "event://abc123",
                "tenant_id": "99999",
            },
            {
                "id": "event://xyz789",
                "tenant_id": "99999",
            },
            {
                "id": "event://ghjk234",
                "tenant_id": "99999",
            },
            {
                "id": "event://qwert456",
                "tenant_id": "22222",
            },
        ]
    )

    events_for_diff_investigation_id_df = pd.DataFrame(
        [
            {
                "id": "event://abc123",
                "tenant_id": "99999",
            },
            {
                "id": "event://xyz789",
                "tenant_id": "99999",
            },
            {
                "id": "event://ghjk234",
                "tenant_id": "99999",
            },
            {
                "id": "event://qwert456",
                "tenant_id": "22222",
            },
        ]
    )

    stage_investigation_evidence(alerts_df, db, InvestigationEvidenceType.Alert)
    stage_investigation_evidence(events_df, db, InvestigationEvidenceType.Event)
    stage_investigation_evidence(
        events_for_diff_investigation_id_df,
        db,
        InvestigationEvidenceType.Event,
        "investigation-id-12345",
    )

    yield db

    db.close()
    db_file_path.unlink()
