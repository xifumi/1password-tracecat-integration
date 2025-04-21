from typing import Annotated
from pydantic import Field
from tracecat_registry import registry, RegistrySecret, secrets

from onepassword import *

api_token = RegistrySecret(name="onepassword", keys=["ONEPASSWORD_TOKEN"])

def _create_onepassword_client(api_token: str):
    """
    Create a 1Password client using the provided API token.
    """
    from onepassword import OnePassword

    # Initialize the OnePassword client with the API token
    client = Client.authenticate(
        auth=api_token,
        integration_name ="Tracecat 1Password Integration",
        integration_version="1.0.0",)
    return client

@registry.register(
    default_title="1Password List Vaults",
    display_group="1Password",
    description="Lists all Vaults in your 1Password account",
    namespace="integrations.onepassword",
)
def onepass_list_vaults(api_token: Annotated[str, Field(description="OnePassword Client Object")]):
    """
    Args: client, 1Password Client Object
    Returns: dict, JSON searializable object

    Note: `return` can be any JSON serializable python object (e.g. str, int, float, dict of str of int)
    """
    client = _create_onepassword_client(api_token=api_token)
    vaults = await client.vaults.list_all()
    return {"message": f"List of vaults: {vaults}!"}

"""
@registry.register(
    default_title="1Password Get Secret",
    display_group="1Password",
    description="Loads a Secret from a Item in a Vault",
    namespace="integrations.onepassword",
)
def onepass_load_secret(name: Annotated[str, Field(description="Loads a Secret from a Item in a Vault")]):
    return {"message": f"Hello, {name}!"}


@registry.register(
    default_title="1Password List Items",
    display_group="1Password",
    description="Lists items in your 1Password Vault",
    namespace="integrations.onepassword",
    secrets=[api_token],
)
def onepass_list_items(
    name: Annotated[str, Field(description="Lists items in your 1Password Vault")],
):
    secret = secrets.get("apitoken")
    # For demonstration purposes, we're just returning the secret here.
    return {"message": f"Goodbye, {name}! Secret: {secret}"}
"""