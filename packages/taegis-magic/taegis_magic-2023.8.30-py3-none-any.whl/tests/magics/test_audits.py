"""Test Taegis audits commands."""

from datetime import datetime, timedelta


def test_audits_audit(ip):
    """Test %taegis audits audit."""
    ip.run_line_magic(
        "taegis",
        "audits audit --audit-id 'd2c9c9e5-cb4e-48bb-b668-10317b11f88c' --tenant 50530 --assign audit",
    )

    audit = ip.user_ns["audit"]

    assert audit.loc[0, "id"] == "d2c9c9e5-cb4e-48bb-b668-10317b11f88c"


def test_audits_all(ip):
    """Test %taegis audits all."""
    ip.run_line_magic(
        "taegis",
        "audits all --assign audits",
    )

    audits = ip.user_ns["audits"]

    assert not audits.empty


def test_audits_search(ip):
    """Test %taegis audits search."""
    after = datetime.utcnow() - timedelta(days=3)
    after_str = after.strftime("%Y-%m-%dT%H:%M:%SZ")

    ip.run_line_magic(
        "taegis",
        f"audits search --after '{after_str}' --email mpegman@secureworks.com --tenant 50530 --assign audits",
    )

    audits = ip.user_ns["audits"]

    if not audits.empty:
        assert (
            audits[
                audits["timestamp"]
                .apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"))
                .apply(lambda x: x >= after)
            ].shape
            == audits.shape
        )
        assert audits["email"].unique()[0] == "mpegman@secureworks.com"


def test_audits_application_events(ip):
    """Test %taegis audits application-events."""
    ip.run_line_magic(
        "taegis",
        "audits application-events --event-type alerts --assign app_events --display app_events",
    )

    app_events = ip.user_ns["app_events"]

    assert not app_events.empty
