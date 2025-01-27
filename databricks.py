from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import ContainerClient, generate_container_sas, ContainerSasPermissions, BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

# Env variables
sp_id_secondary = os.getenv("SP_ID_SECONDARY") # client_id_keyvault
sp_secondary_password = os.getenv("SP_SECONDARY_PASSWORD") # client_secret_keyvault
sp_id_principal = os.getenv("SP_ID_PRINCIPAL") # client_id_storage
tenant_id = os.getenv("TENANT_ID")
keyvault_url = os.getenv("KEYVAULT_URL")
secret_name = os.getenv("SECRET_NAME")
account_name = os.getenv("STORAGE_ACCOUNT_NAME")
scope = os.getenv("SCOPE")
databricks_secret = os.getenv("DATABRICKS_SECRET")
databricks_app_id = os.getenv("DATABRICKS_APP_ID")

service_credential = dbutils.secrets.get(scope=scope,key=databricks_secret)

spark.conf.set("fs.azure.account.auth.type.{account_name}.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.{account_name}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.{account_name}.dfs.core.windows.net", databricks_app_id)
spark.conf.set("fs.azure.account.oauth2.client.secret.{account_name}.dfs.core.windows.net", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.{account_name}.dfs.core.windows.net", "https://login.microsoftonline.com/{tenant_id}/oauth2/token")