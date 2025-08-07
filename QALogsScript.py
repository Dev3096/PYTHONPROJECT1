import subprocess
import json
import requests
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Your Azure Key Vault name
KEY_VAULT_NAME = "abcdataengineering"
KV_URI = f"https://{KEY_VAULT_NAME}.vault.azure.net"

# Initialize Azure Key Vault client once
_credential = DefaultAzureCredential()
_secret_client = SecretClient(vault_url=KV_URI, credential=_credential)

def get_secret(secret_name):
    """Fetch secret value from Azure Key Vault."""
    try:
        secret = _secret_client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        logging.error(f"Error fetching secret '{secret_name}': {e}")
        raise

def set_secret(secret_name, secret_value):
    """Set secret value in Azure Key Vault."""
    try:
        _secret_client.set_secret(secret_name, secret_value)
    except Exception as e:
        logging.error(f"Error setting secret '{secret_name}': {e}")
        raise

def get_cli_token():
    """Get Azure CLI access token."""
    try:
        result = subprocess.run(
            ["C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd", "account", "get-access-token", "--resource", "https://management.azure.com"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        token_data = json.loads(result.stdout)
        return token_data["accessToken"]
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting CLI token: {e.stderr}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error getting CLI token: {e}")
        raise



def run_databricks_notebook(token):
    """Run a Databricks notebook using the Databricks REST API."""
    try:
        DATABRICKS_TOKEN = get_secret("Databricks-Token")
        DATABRICKS_INSTANCE = "https://adb-2641938447887677.17.azuredatabricks.net"

        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}"
        }

        payload = {
            "job_id": 1069551125400883,
            "notebook_params": {
                "azure_access_token": token
            }
        }

        response = requests.post(
            f"{DATABRICKS_INSTANCE}/api/2.0/jobs/run-now",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        print(response.json())
    except requests.RequestException as e:
        logging.error(f"Databricks API request failed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error running Databricks notebook: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        token = get_cli_token()
        run_databricks_notebook(token)
    except Exception as e:
        logging.error(f"Script failed: {e}")
