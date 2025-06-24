import subprocess
import json
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

import ssl

# Your Azure Key Vault name
KEY_VAULT_NAME = ""
KV_URI = f""

# credential = DefaultAzureCredential()
# client = SecretClient(vault_url=KV_URI, credential=credential)

# Function to retrieve secrets dynamically
def get_secret(secret_name):
    """Fetch secret value from Azure Key Vault."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KV_URI, credential=credential)

    secret = client.get_secret(secret_name)
    return secret.value

# Function to set secrets dynamically (if needed)
def set_secret(secret_name, secret_value):
    """Fetch secret value from Azure Key Vault."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KV_URI, credential=credential)
    client.set_secret(secret_name, secret_value)

# Function to get Azure CLI token
def get_cli_token():
    result = subprocess.run(
        ["C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd", "account", "get-access-token", "--resource", "https://management.azure.com"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check = True,
        text = True
    )
    token_data = json.loads(result.stdout)
    return token_data["accessToken"]

token = get_cli_token()
# print(token)
# Function to run a Databricks notebook using the Databricks REST API
def run_databricks_notebook():

    DATABRICKS_TOKEN = get_secret("Databricks-Token")
    DATABRICKS_INSTANCE = get_secret("Databricks-Instance")

    headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}"
    }

    payload = {
    "job_id": "123",
    "notebook_params": {
            "azure_access_token": token
        }
    }

    response = requests.post(
    f"{DATABRICKS_INSTANCE}/api/2.0/jobs/run-now",
    headers=headers,
    json=payload
)

    print(response.json())

# Run the function to execute the Databricks notebook
run_databricks_notebook()
