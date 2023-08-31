"""Taegis Magics clients tests."""

import uuid


def test_clients_create_remove(ip):
    """Test %taegis clients create/remove commands."""
    ip.run_line_magic(
        "taegis",
        f"clients create magics-test-{uuid.uuid4()} --role auditor "
        "--tenant 50530 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]
    client_id = dataframe.loc[0, "client.client_id"]

    ip.run_line_magic(
        "taegis", f"clients remove {client_id} --tenant 50530 --region charlie"
    )


def test_clients_search(ip):
    """Test %taegis clients search command."""
    ip.run_line_magic(
        "taegis",
        f"clients create magics-test-{uuid.uuid4()} --role auditor "
        "--tenant 50530 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]
    client_id = dataframe.loc[0, "client.client_id"]
    client_name = dataframe.loc[0, "client.name"]

    # search by id
    ip.run_line_magic(
        "taegis",
        f"clients search --client-id {client_id} --tenant 50530 --region charlie --assign by_client_id",
    )
    by_client_id = ip.user_ns["by_client_id"]

    # search by name
    ip.run_line_magic(
        "taegis",
        f"clients search --name {client_name} --tenant 50530 --region charlie --assign by_client_name",
    )
    by_client_name = ip.user_ns["by_client_name"]

    # search by role
    ip.run_line_magic(
        "taegis",
        f"clients search --role auditor --tenant 50530 --region charlie --assign by_client_role",
    )
    by_client_role = ip.user_ns["by_client_role"]

    assert by_client_id.loc[0, "client_id"] == client_id
    assert by_client_name.loc[0, "name"] == client_name
    assert not by_client_role[by_client_role["client_id"] == client_id].empty

    ip.run_line_magic(
        "taegis", f"clients remove {client_id} --tenant 50530 --region charlie"
    )


def test_clients_rotate_secret(ip):
    """Test %taegis clients rotate secret command."""
    ip.run_line_magic(
        "taegis",
        f"clients create magics-test-{uuid.uuid4()} --role auditor "
        "--tenant 50530 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]
    client_id = dataframe.loc[0, "client.client_id"]
    client_secret = dataframe.loc[0, "client_secret"]

    ip.run_line_magic(
        "taegis",
        f"clients rotate secret {client_id} --tenant 50530 --region charlie --assign new_secret_df",
    )

    new_secret_df = ip.user_ns["new_secret_df"]
    new_client_id = new_secret_df.loc[0, "client.client_id"]
    new_secret = new_secret_df.loc[0, "client_secret"]

    assert client_id == new_client_id
    assert client_secret != new_secret

    ip.run_line_magic(
        "taegis", f"clients remove {client_id} --tenant 50530 --region charlie"
    )


def test_clients_role_append_remove(ip):
    """Test %taegis clients role append/remove commands."""
    ip.run_line_magic(
        "taegis",
        f"clients create magics-test-{uuid.uuid4()} "
        "--tenant 50530 --region charlie --assign dataframe",
    )

    dataframe = ip.user_ns["dataframe"]
    client_id = dataframe.loc[0, "client.client_id"]
    client_roles = dataframe.loc[0, "client.roles"]

    ip.run_line_magic(
        "taegis",
        f"clients role append {client_id} --role auditor "
        "--tenant 50530 --region charlie --assign append_df",
    )
    append_df = ip.user_ns["append_df"]
    append_roles = append_df.loc[0, "roles"]

    ip.run_line_magic(
        "taegis",
        f"clients role remove {client_id} --role auditor "
        "--tenant 50530 --region charlie --assign remove_df",
    )
    remove_df = ip.user_ns["remove_df"]
    remove_roles = remove_df.loc[0, "roles"]

    assert client_roles == "tenantAnalyst"
    assert append_roles == "tenantAnalyst,tenantAuditor"
    assert remove_roles == "tenantAnalyst"

    ip.run_line_magic(
        "taegis", f"clients remove {client_id} --tenant 50530 --region charlie"
    )
