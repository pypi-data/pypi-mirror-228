"""Test taegis tenants commands."""

import pytest
import time
from click.exceptions import BadOptionUsage
from numpy import dtype
from taegis_magic.pandas.tenants import inflate_environments


def test_tenants_search_by_name(ip):
    """Test %taegis tenants search --filter-by-name."""
    ip.run_line_magic(
        "taegis", "tenants search --filter-by-name '%Dark Cloud%' --assign dataframe"
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.shape[0] == 1
    assert dataframe.loc[0, "id"] == "50530"


def test_tenants_search_by_region(ip):
    """Test %taegis tenants search --filter-by-name."""
    ip.run_line_magic(
        "taegis", "tenants search --filter-by-region 'production' --assign dataframe"
    )

    dataframe = ip.user_ns["dataframe"]
    inflated_environments = dataframe.pipe(inflate_environments)

    assert inflated_environments["environments.production"].dtype == dtype("bool")
    assert inflated_environments["environments.production"].nunique() == 1
    assert inflated_environments["environments.production"].unique().all()


def test_tenants_search_by_label_name(ip):
    """Test %taegis tenants search --filter-by-label-name."""
    ip.run_line_magic(
        "taegis",
        "tenants search --filter-by-label-name red_cloak_id --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["labels"].apply(
                lambda x: len([label for label in x if label["name"] == "red_cloak_id"])
                > 0
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_label_value(ip):
    """Test %taegis tenants search --filter-by-label-value."""
    ip.run_line_magic(
        "taegis",
        "tenants search --filter-by-label-name red_cloak_id "
        "--filter-by-label-value 085bc176 --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.loc[0, "id"] == "50530"


def test_tenants_search_by_label_value_without_name(ip):
    """Test %taegis tenants search --filter-by-label-value without --filter-by-label-name."""

    with pytest.raises(BadOptionUsage):
        ip.run_line_magic(
            "taegis",
            "tenants search --filter-by-label-value 085bc176 --assign dataframe",
        )


def test_tenants_search_by_partner_subscription(ip):
    """Test %taegis tenants search --filter-by-partner-subscription."""
    ip.run_line_magic(
        "taegis",
        "tenants search --filter-by-partner-subscription 'Dell MDR Delivery' --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["partnership.subscriptions"].apply(
                lambda x: len([sub for sub in x if sub["name"] == "Dell MDR Delivery"])
                > 0
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_requested_service(ip):
    """Test %taegis tenants search --filter-by-requested-service."""
    ip.run_line_magic(
        "taegis",
        "tenants search --filter-by-requested-service 'test MXDR' --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["requested_services"].apply(
                lambda x: len([sub for sub in x if sub["name"] == "test MXDR"]) > 0
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_created_start_time(ip):
    """Test %taegis tenants search --filter-by-created-start-time --filter-by-created-end-time."""
    ip.run_line_magic(
        "taegis",
        "tenants search --filter-by-created-start-time '2020-01-01T00:00:00Z' --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["created_at"]
            .apply(lambda x: time.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
            .apply(
                lambda x: x
                >= time.strptime("2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_created_end_time(ip):
    """Test %taegis tenants search --filter-by-created-end-time."""

    ip.run_line_magic(
        "taegis",
        "tenants search --filter-by-created-end-time '2020-12-31T23:59:59Z' --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["created_at"]
            .apply(lambda x: time.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
            .apply(
                lambda x: x
                <= time.strptime("2020-12-31T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ"),
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_created_start_end_time(ip):
    """Test %taegis tenants search --filter-by-created-start-time --filter-by-created-end-time."""
    ip.run_line_magic(
        "taegis",
        "tenants search --assign dataframe "
        "--filter-by-created-start-time '2020-01-01T00:00:00Z' "
        "--filter-by-created-end-time '2020-12-31T23:59:59Z'",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["created_at"]
            .apply(lambda x: time.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
            .between(
                time.strptime("2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
                time.strptime("2020-12-31T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ"),
            )
        ].shape
        == dataframe.shape
    )


@pytest.mark.xfail
def test_fail():
    """Test a failure."""
    ip.run_line_magic(
        "taegis",
        "tenants search --assign dataframe "
        "--filter-by-created-start-time '2020-01-01T00:00:00Z' "
        "--filter-by-created-end-time '2022-12-31T23:59:59Z'",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["created_at"]
            .apply(lambda x: time.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
            .between(
                time.strptime("2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
                time.strptime("2020-12-31T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ"),
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_modified_start_time(ip):
    """Test %taegis tenants search --filter-by-modified-start-time."""
    ip.run_line_magic(
        "taegis",
        "tenants search --filter-by-modified-start-time '2020-01-01T00:00:00Z' --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["updated_at"]
            .apply(lambda x: time.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
            .apply(
                lambda x: x
                >= time.strptime("2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_modified_end_time(ip):
    """Test %taegis tenants search --filter-by-modified-end-time."""

    ip.run_line_magic(
        "taegis",
        "tenants search --filter-by-modified-end-time '2020-12-31T23:59:59Z' --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["updated_at"]
            .apply(lambda x: time.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
            .apply(
                lambda x: x
                <= time.strptime("2020-12-31T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ"),
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_modified_start_end_time(ip):
    """Test %taegis tenants search --filter-by-modified-start-time --filter-by-modified-end-time."""
    ip.run_line_magic(
        "taegis",
        "tenants search --assign dataframe "
        "--filter-by-modified-start-time '2020-01-01T00:00:00Z' "
        "--filter-by-modified-end-time '2020-12-31T23:59:59Z'",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe[
            dataframe["updated_at"]
            .apply(lambda x: time.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
            .between(
                time.strptime("2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
                time.strptime("2020-12-31T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ"),
            )
        ].shape
        == dataframe.shape
    )


def test_tenants_search_by_tenant_hierarchy(ip):
    ...
