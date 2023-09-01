import os

from .consts import AZURE_CREDS_FILE

from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient

AZURE_CREDS_FILE = os.environ.get("AZURE_CREDS_FILE", AZURE_CREDS_FILE)


def get_creds() -> dict:
    azure_creds = None
    with open(AZURE_CREDS_FILE, "r") as f:
        azure_creds = json.load(f)

    return azure_creds


def connect():
    azure_creds = get_creds()

    credential = ClientSecretCredential(
        azure_creds["tenant_id"], azure_creds["client_id"], azure_creds["client_secret"]
    )
    scopes = ["https://graph.microsoft.com/.default"]
    client = GraphServiceClient(credentials=credential, scopes=scopes)
    return client
