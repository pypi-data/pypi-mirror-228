"""
Tests for Taegis Alerts Triage Dashboard.
"""
from taegis_sdk_python.services.preferences.types import TicketingType
from taegis_magic.pandas.alerts import normalize_creator_name


def test_dashboard_preferences_parent(ip):
    """Test Preferences Parent."""
    ip.run_line_magic("taegis", "preferences parent --assign parter_prefs_df")

    parter_prefs_df = ip.user_ns["parter_prefs_df"]

    assert parter_prefs_df.loc[0, "partner_id"] == "5000"
    assert parter_prefs_df.loc[0, "display_name"] == "Secureworks"
    assert parter_prefs_df.loc[0, "support_phone_number"] == "855-525-7497"


def test_dashboard_preferences_ticketing_settings(ip):
    """Test Preferences Ticketing Settings."""
    ip.run_line_magic("taegis", "preferences ticketing-settings --assign ticketing_df")

    ticketing_df = ip.user_ns["ticketing_df"]

    assert ticketing_df.loc[0, "tenant_id"] == "5000"
    assert ticketing_df.loc[0, "display_name"] == "Secureworks"
    assert ticketing_df.loc[0, "ticketing_type"] == TicketingType.ZENDESK
    assert (
        ticketing_df.loc[0, "view_ticket_url"]
        == "https://support.ctpx.secureworks.com/hc/en-us/requests"
    )


def test_dashboard_preferences_user_email(ip):
    """Test Preferences User Preference - Email."""
    ip.run_line_magic(
        "taegis", "preferences user-preference email --assign email_prefs_df"
    )

    email_prefs_df = ip.user_ns["email_prefs_df"]

    assert not email_prefs_df.empty


def test_dashboard_preferences_user_severity(ip):
    """Test Preferences User Preference - alertTriage.severities."""
    ip.run_line_magic(
        "taegis",
        "preferences user-preference alertTriage.severities --assign severities_df",
    )

    severities_df = ip.user_ns["severities_df"]

    assert not severities_df.empty


def test_dashboard_recent_alerts(ip):
    """Test Recent Alerts."""
    ip.run_cell_magic(
        "taegis",
        "alerts search --limit 5 --tenant 5000 --assign recent_alerts_df",
        """
        FROM alert
        WHERE
            status = 'OPEN' AND
            investigation_ids IS NULL AND
            metadata.creator.detector.detector_id != 'app:event-filter-ql' AND
            (
                metadata.severity >= 0.8 OR
                (
                    metadata.severity >= 0.6 AND
                    metadata.severity < 0.8
                )
            )
        EARLIEST=-3d
        """,
    )

    recent_alerts_df = ip.user_ns["recent_alerts_df"]

    assert recent_alerts_df.shape[0] <= 5


def test_dashboard_alerts_by_detector(ip):
    """Test Alerts by Detector."""
    ip.run_cell_magic(
        "taegis",
        "alerts search --limit 5 --tenant 5000 --assign alerts_by_detector_df",
        """
        FROM alert
        WHERE
            status = 'OPEN' AND
            investigation_ids IS NULL AND
            metadata.creator.detector.detector_id != 'app:event-filter-ql' AND
            (
                metadata.severity >= 0.8 OR
                (
                    metadata.severity >= 0.6 AND
                    metadata.severity < 0.8
                )
            )
        EARLIEST=-3d | aggregate count by creator
        """,
    )

    alerts_by_detector_df = ip.user_ns["alerts_by_detector_df"]

    recent_alerts_pretty_df = alerts_by_detector_df.pipe(normalize_creator_name)

    assert all(
        recent_alerts_pretty_df.columns
        == ["creator", "count", "taegis_magic.creator.display_name"]
    )


def test_dashboard_recent_investigations(ip):
    """Test Recent Investigations."""
    ip.run_cell_magic(
        "taegis",
        "investigations search --limit 5 --assign inv_df",
        """
        status in ('Open', 'Active', 'Awaiting Action') AND
        deleted_at is null
        """,
    )

    inv_df = ip.user_ns["inv_df"]

    assert inv_df.shape[0] <= 5


def test_dashboard_recent_threat_publications(ip):
    """Test Recent Threat Publications."""
    ip.run_line_magic(
        "taegis",
        "threat publications latest 10 --assign latest_tips_df",
    )

    latest_tips_df = ip.user_ns["latest_tips_df"]

    assert latest_tips_df.shape[0] <= 10
