"""Magic Test Fixtures."""

import pytest

import pandas as pd

from taegis_magic.commands.utils.investigations import (
    get_or_create_database,
    stage_investigation_evidence,
    InvestigationEvidenceType,
)


@pytest.fixture
def in_memory_database():
    """Create an in-memory database for testing."""
    db = get_or_create_database()
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
                "resource_id": "event://abc123",
                "tenant_id": "99999",
            },
            {
                "resource_id": "event://xyz789",
                "tenant_id": "99999",
            },
            {
                "resource_id": "event://ghjk234",
                "tenant_id": "99999",
            },
            {
                "resource_id": "event://qwert456",
                "tenant_id": "22222",
            },
        ]
    )

    stage_investigation_evidence(alerts_df, db, InvestigationEvidenceType.Alert)
    stage_investigation_evidence(events_df, db, InvestigationEvidenceType.Event)

    yield db
    db.close()
