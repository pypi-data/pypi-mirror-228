"""Test taegis tenant-profiles commands."""


from numpy import bool_


def test_tenant_profile_list(ip):
    """Test %taegis tenant-profiles list."""
    ip.run_line_magic(
        "taegis",
        "tenant-profiles list --tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert not dataframe.empty


def test_contacts(ip):
    """Test %taegis tenant-profiles contacts."""
    ip.run_line_magic(
        "taegis",
        "tenant-profiles contacts add --user-id 'ac1255ef-b11f-40d0-91f3-40cca57037d2' --preference CseTertiary "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    contact_id = dataframe.loc[0, "id"]

    assert dataframe.loc[0, "email"] == "core-test-user@octolabs.io"

    ip.run_line_magic(
        "taegis",
        "tenant-profiles contacts list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.loc[0, "tertiary.id"] == contact_id

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles contacts update --id '{contact_id}' --user-id '9526bca4-3b20-4b5f-ad9f-6bea40def6cf' --preference CseTertiary "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.loc[0, "email"] == "taegisxdrvalidation@octolabs.io"

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles contacts remove --id '{contact_id}' "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    ip.run_line_magic(
        "taegis",
        "tenant-profiles contacts list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert "tertiary.id" not in dataframe.columns


def test_network(ip):
    """Test %taegis tenant-profiles network."""
    ip.run_line_magic(
        "taegis",
        "tenant-profiles network add --cidr '192.0.2.0/24' --description 'RFC 5737 Documentation' "
        "--network-type Other --no-is-critical "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert not dataframe.empty

    network_id = dataframe.loc[0, "id"]

    ip.run_line_magic(
        "taegis",
        "tenant-profiles network list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert not dataframe[dataframe["id"] == network_id].empty

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles network update --id '{network_id}' --cidr '198.51.100.0/24' "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.loc[0, "id"] == network_id
    assert dataframe.loc[0, "cidr"] == "198.51.100.0/24"

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles network remove --id '{network_id}' "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    ip.run_line_magic(
        "taegis",
        "tenant-profiles network list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    if not dataframe.empty:
        assert dataframe[dataframe["id"] == network_id].empty


def test_note(ip):
    """Test %taegis tenant-profiles note."""
    ip.run_line_magic(
        "taegis",
        "tenant-profiles note list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    contents = dataframe.loc[0, "contents"]

    assert not dataframe.empty

    ip.run_line_magic(
        "taegis",
        "tenant-profiles note update --contents 'Test test test' "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.loc[0, "contents"] == "Test test test"

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles note update --contents '{contents}' "
        "--tenant 11772 --region charlie --assign dataframe",
    )


def test_security_controls(ip):
    """Test %taegis tenant-profiles security-controls."""
    ip.run_line_magic(
        "taegis",
        "tenant-profiles security-controls add "
        "--ip '192.0.2.100' --details 'Documentation Test Scanner' "
        "--service VULNERABILITY_SCANNING --source INTERNAL "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    control_id = dataframe.loc[0, "id"]

    assert dataframe.loc[0, "ip"] == "192.0.2.100"
    assert dataframe.loc[0, "details"] == "Documentation Test Scanner"
    assert dataframe.loc[0, "service"] == "VULNERABILITY_SCANNING"
    assert dataframe.loc[0, "source"] == "INTERNAL"

    ip.run_line_magic(
        "taegis",
        "tenant-profiles security-controls list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert not dataframe[dataframe["ip"] == "192.0.2.100"].empty

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles security-controls update --id {control_id} "
        "--ip '192.0.2.101' --details 'Documentation Test Pentester' "
        "--service PENETRATION_TESTING --source EXTERNAL "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.loc[0, "id"] == control_id
    assert dataframe.loc[0, "ip"] == "192.0.2.101"
    assert dataframe.loc[0, "details"] == "Documentation Test Pentester"
    assert dataframe.loc[0, "service"] == "PENETRATION_TESTING"
    assert dataframe.loc[0, "source"] == "EXTERNAL"

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles security-controls remove --id {control_id} "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    ip.run_line_magic(
        "taegis",
        "tenant-profiles security-controls list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    if not dataframe.empty:
        assert dataframe[dataframe["ip"] == "192.0.2.101"].empty


def test_mfa(ip):
    """Test %taegis tenant-profiles mfa."""
    ip.run_line_magic(
        "taegis",
        "tenant-profiles mfa add --service CITRIX --ip '192.0.2.150' "
        "--exceptions 'N/A' --details 'Citrix VPN MFA' --mfa-required "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    mfa_id = dataframe.loc[0, "id"]

    assert dataframe.loc[0, "ip"] == "192.0.2.150"
    assert dataframe.loc[0, "mfa_required"] is bool_(True)
    assert dataframe.loc[0, "exceptions"] == "N/A"
    assert dataframe.loc[0, "details"] == "Citrix VPN MFA"
    assert dataframe.loc[0, "service"] == "CITRIX"

    ip.run_line_magic(
        "taegis",
        "tenant-profiles mfa list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert not dataframe[dataframe["id"] == mfa_id].empty

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles mfa update --id {mfa_id} "
        "--service VPN --ip '192.0.2.151' "
        "--exceptions 'None' --details 'VPN MFA' --no-mfa-required "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    assert dataframe.loc[0, "id"] == mfa_id
    assert dataframe.loc[0, "ip"] == "192.0.2.151"
    assert dataframe.loc[0, "mfa_required"] is bool_(False)
    assert dataframe.loc[0, "exceptions"] == "None"
    assert dataframe.loc[0, "details"] == "VPN MFA"
    assert dataframe.loc[0, "service"] == "VPN"

    ip.run_line_magic(
        "taegis",
        f"tenant-profiles mfa remove --id {mfa_id} "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    ip.run_line_magic(
        "taegis",
        "tenant-profiles mfa list "
        "--tenant 11772 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]

    if not dataframe.empty:
        assert dataframe[dataframe["id"] == mfa_id].empty
