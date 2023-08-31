"""Taegis magics tests for Users."""

import pytest


@pytest.mark.skip(reason="requires user token, not client credentials")
def test_users_current_user(ip):
    """Test %taegis users current-user."""
    ip.run_line_magic("taegis", "users current-user --assign dataframe")

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.shape[0] == 1


def test_users_search(ip):
    """Test %taegis users search."""

    # single email
    ip.run_line_magic(
        "taegis",
        "users search --email 'mpegman@secureworks.com' --assign  dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe.shape
        == dataframe[dataframe["email"] == "mpegman@secureworks.com"].shape
    )

    # partial single email
    ip.run_line_magic(
        "taegis",
        "users search --email 'mpegman%' --assign  dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe.shape
        == dataframe[dataframe["email"].str.contains("mpegman", case=False)].shape
    )

    # partial name match
    # does not work on given and family name (only 1 field)
    ip.run_line_magic(
        "taegis",
        "users search --name 'pegman' --assign  dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe.shape
        == dataframe[
            (dataframe["email"].str.contains("pegman", case=False))
            | (dataframe["given_name"].str.contains("pegman", case=False))
            | (dataframe["family_name"].str.contains("pegman", case=False))
        ].shape
    )

    # add role filter
    ip.run_line_magic(
        "taegis",
        "users search --email 'mpegman%' --role analyst --assign  dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe.shape
        == dataframe[dataframe["roles"].apply(lambda x: "tenantAnalyst" in x)].shape
    )

    # multiple full emails
    ip.run_line_magic(
        "taegis",
        "users search --email 'mpegman@secureworks.com' --email 'jmessinger@secureworks.com' --assign  dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe.shape
        == dataframe[
            (dataframe["email"] == "mpegman@secureworks.com")
            | (dataframe["email"] == "jmessinger@secureworks.com")
        ].shape
    )

    # multiple partial matchs
    # subsequent partial matchs will be dropped
    ip.run_line_magic(
        "taegis",
        "users search --email 'mpegman%' --email 'jmessinger%' --assign  dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe.shape == dataframe[(dataframe["email"].str.contains("mpegman"))].shape
    )
    assert dataframe[(dataframe["email"].str.contains("jmessinger"))].empty

    # full/partial match
    # full matches will be dropped
    ip.run_line_magic(
        "taegis",
        "users search --email 'mpegman%' --email 'jmessinger@secureworks.com' --assign  dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert (
        dataframe.shape == dataframe[(dataframe["email"].str.contains("mpegman"))].shape
    )
    assert dataframe[(dataframe["email"] == "jmessinger@secureworks.com")].empty


@pytest.mark.skip("documentation test")
def test_invite_users(ip):
    """Test %taegis users support-pin/verify-support-pin/validate-support-pin."""
    ip.run_line_magic(
        "taegis",
        "users invite-users "
        "--email mpegman@secureworks.com --email jmessinger@secureworks.com "
        "--role auditor --language en "
        "--assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]
    assert dataframe.shape[0] == 2


@pytest.mark.skip("documentation test")
def test_invite_trial_user(ip):
    """Test %taegis users support-pin/verify-support-pin/validate-support-pin."""
    ip.run_line_magic(
        "taegis",
        "users invite-trial-user "
        "--email mpegman@secureworks.com "
        "--trial-tenant 11772 --language en "
        "--assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]
    assert dataframe.shape[0] == 1


@pytest.mark.skip("documentation test")
def test_pin_support(ip):
    """Test %taegis users support-pin/verify-support-pin/validate-support-pin."""
    ip.run_line_magic(
        "taegis",
        "users support-pin --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert not dataframe.empty

    pin = dataframe.loc[0, "code"]

    ip.run_line_magic(
        "taegis",
        f"users verify-support-pin {pin} --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert not dataframe.empty

    email_address = dataframe.loc[0, "email_address"]

    ip.run_line_magic(
        "taegis",
        f"users validate-support-pin {email_address} {pin} --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]
    successful = dataframe.loc[0, "successful"]

    assert successful is True
