"""Test Taegis Rules commands."""

from datetime import datetime, timedelta

import pytest
from numpy import bool_
from taegis_sdk_python.services.rules.types import RuleAction, RuleEventType


def test_rules_type(ip):
    """Test %taegis rules type."""
    ip.run_line_magic("taegis", "rules type --rule-type QL --assign ql_rules")

    ql_rules = ip.user_ns["ql_rules"]

    assert "ql_filter.id" in ql_rules.columns

    ip.run_line_magic("taegis", "rules type --rule-type REGEX --assign regex_rules")

    regex_rules = ip.user_ns["regex_rules"]

    assert "ql_filter.id" not in regex_rules.columns
    assert (
        regex_rules[regex_rules["filters"].apply(lambda x: len(x) > 0)].shape
        == regex_rules.shape
    )


def test_rules_all(ip):
    """Test %taegis rules all."""
    ip.run_line_magic("taegis", "rules all --assign all_rules")

    all_rules = ip.user_ns["all_rules"]

    # not sure what to test here besides command success
    assert not all_rules.empty


def test_rules_suppression(ip):
    """Test %taegis rules suppression."""
    ip.run_line_magic("taegis", "rules suppression --assign suppression_rules")

    suppression_rules = ip.user_ns["suppression_rules"]

    assert suppression_rules["rule_action"].nunique() == 1
    assert suppression_rules["rule_action"].unique()[0] == RuleAction.SUPPRESS


def test_rules_deleted(ip):
    """Test %taegis rules deleted."""
    ip.run_line_magic(
        "taegis", "rules deleted --rule-type REGEX --assign deleted_regex_rules"
    )

    deleted_regex_rules = ip.user_ns["deleted_regex_rules"]

    assert deleted_regex_rules["deleted"].nunique() == 1
    assert deleted_regex_rules["deleted"].unique()[0] is bool_(True)


@pytest.mark.parametrize("event_type", [item.value for item in list(RuleEventType)])
def test_rules_filters(ip, event_type):
    """Test %taegis rules filters."""
    ip.run_line_magic(
        "taegis",
        f"rules filters --event-type {event_type} --rule-type REGEX --assign event_filter_rules",
    )

    event_filter_rules = ip.user_ns["event_filter_rules"]

    if not event_filter_rules.empty:
        assert event_filter_rules["event_type"].nunique() == 1
        assert event_filter_rules["event_type"].unique()[0] == RuleEventType(event_type)


def test_rules_id(ip):
    """Test %taegis rules rule."""
    ip.run_line_magic(
        "taegis",
        "rules rule --rule-id 9f26c30d-f26d-45bb-8314-dd6dba68b169 --assign rule_by_id",
    )

    rule_by_id = ip.user_ns["rule_by_id"]

    assert rule_by_id.loc[0, "id"] == "9f26c30d-f26d-45bb-8314-dd6dba68b169"


@pytest.mark.parametrize("event_type", [item.value for item in list(RuleEventType)])
def test_rules_changes_since(ip, event_type):
    """Test %taegis rules changes-since."""
    yesterday = datetime.utcnow() - timedelta(days=1)

    ip.run_line_magic(
        "taegis",
        f"rules changes-since --timestamp '{yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')}' "
        f"--event-type {event_type} --rule-type REGEX --assign changes_since",
    )

    changes_since = ip.user_ns["changes_since"]

    if not changes_since.empty:
        assert (
            changes_since[
                changes_since["updated_at"]
                .apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"))
                .apply(lambda x: x >= yesterday)
            ].shape
            == changes_since.shape
        )


def test_rules_search(ip):
    """Test %taegis rules search."""
    ip.run_cell_magic(
        "taegis", "rules search --assign rules_search", "name CONTAINS 'Test 2'"
    )

    rules_search = ip.user_ns["rules_search"]

    assert (
        rules_search[rules_search["name"].str.lower().str.contains("test 2")].shape
        == rules_search.shape
    )


@pytest.mark.skip(reason="documentation test")
def test_rules_enable(ip):
    """Test %taegis rules enable."""
    ip.run_line_magic(
        "taegis",
        "rules enable --rule-id abd49642-cf06-40ed-9ff6-c8ff44d36962 "
        "--tenant 50530 --region charlie --assign rule",
    )

    rule = ip.user_ns["rule"]

    assert rule.loc[0, "enabled"] is bool_(True)


@pytest.mark.skip(reason="documentation test")
def test_rules_disable(ip):
    """Test %taegis rules disable."""
    ip.run_line_magic(
        "taegis",
        "rules disable --rule-id abd49642-cf06-40ed-9ff6-c8ff44d36962 "
        "--tenant 50530 --region charlie --assign rule",
    )

    rule = ip.user_ns["rule"]

    assert rule.loc[0, "enabled"] is bool_(False)


@pytest.mark.skip(reason="documentation test")
def test_rules_create_custom_rule(ip):
    """Test %taegis rules create custom."""
    ip.run_cell_magic(
        "taegis",
        "rules create custom --name 'Magics Test Rule' --description 'Magics Test Rule Description' "
        "--severity low --mitre-category T2000 --mitre-category T800 "
        "--tenant 50530 --region charlie --assign rule",
        "FROM cloudaudit WHERE user_name CONTAINS 'zz9pluralzalpha'",
    )

    rule = ip.user_ns["rule"]

    assert rule.loc[0, "name"] == "Magics Test Rule"
    assert rule.loc[0, "description"] == "Magics Test Rule Description"
    assert (
        rule.loc[0, "ql_filter.query"]
        == "SEARCH FROM cloudaudit WHERE user_name CONTAINS 'jupiter'"
    )
    assert len(rule.loc[0, "attack_categories"]) == 2
    assert rule.loc[0, "severity"] == 0.2


@pytest.mark.skip(reason="documentation test")
def test_rules_create_suppression_rule(ip):
    """Test %taegis rules create suppression."""
    ip.run_line_magic(
        "taegis",
        "rules create suppression --name 'Magics Suppression Test' --description 'Magics Suppression Test Description' "
        "--key alert_title --pattern 'zz9pluralzalpha' --key entity --pattern 'host:zz9pluralzalpha' "
        "--tenant 50530 --region charlie",
    )

    rule = ip.user_ns["rule"]

    assert rule.loc[0, "name"] == "Magics Suppression Test"
    assert rule.loc[0, "description"] == "Magics Suppression Test Description"
    assert len(rule.loc[0, "filters"]) == 2
    assert rule.loc[0, "severity"] == 0
    assert rule.loc[0, "rule_action"] == RuleAction.SUPPRESS
