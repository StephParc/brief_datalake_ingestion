from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import ContainerClient, generate_container_sas, ContainerSasPermissions, BlobServiceClient
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import requests
import re
from bs4 import BeautifulSoup
import sys
import functions

load_dotenv()

# Env variables
sp_id_secondary = os.getenv("SP_ID_SECONDARY") # client_id_keyvault
sp_secondary_password = os.getenv("SP_SECONDARY_PASSWORD") # client_secret_keyvault
sp_id_principal = os.getenv("SP_ID_PRINCIPAL") # client_id_storage
tenant_id = os.getenv("TENANT_ID")
keyvault_url = os.getenv("KEYVAULT_URL")
secret_name = os.getenv("SECRET_NAME")
account_name = os.getenv("STORAGE_ACCOUNT_NAME")
container_name = os.getenv("BLOB_CONTAINER")
permissions = ContainerSasPermissions(read=False, add=False, create=False, write=True, delete=False)
expiry_time = datetime.now() + timedelta(hours=1)


# Authentification avec le principal de service
credential_keyvault = ClientSecretCredential(tenant_id, sp_id_secondary, sp_secondary_password)
secret_client = SecretClient(vault_url=keyvault_url, credential=credential_keyvault)

# Récupérer le secret
secret = secret_client.get_secret(secret_name)
secret_value = secret.value

# Variables pour le principal de service Storage
credential_storage = ClientSecretCredential(tenant_id, sp_id_principal, secret_value)

# Créer le client de conteneur
container_client = ContainerClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                  container_name=container_name,
                                  credential=credential_storage)

# Générer le SAS
# sas_token = generate_container_sas(account_name=account_name,
#                                   container_name=container_name,
#                                   credential=credential_storage,
#                                   permission=permissions,
#                                   expiry=expiry_time,
#                                   https_only=True)


# Créer le client de service blob
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=credential_storage)

# Créer le client de conteneur
container_client = blob_service_client.get_container_client(container_name)

# # Chargement des fichiers csv Airbnb
# ## Télécharger le fichier depuis l'URL
# source1 = "https://insideairbnb.com/get-the-data/"
# response = requests.get(source1)
# response.raise_for_status()

# ## Chargement des fichiers
# link_list = functions.select_urls_from_list(source1, "spain", "csv")

# ## Génération des noms de fichiers
# for link in link_list:
#     name = functions.generate_blob_name(link)

#     ## Créer le client de blob
#     blob_client = container_client.get_blob_client(name)

#     ## Télécharger le fichier dans le conteneur blob
#     blob_client.upload_blob(response.content, overw=True)


# # Chargement des fichiers parquet Hugging Face
# ## Télécharger le fichier depuis l'URL
# source2 = "https://huggingface.co/datasets/Marqo/amazon-products-eval/tree/main/data"
# response = requests.get(source2)rite
# response.raise_for_status()

# ## Chargement des fichiers
# link_list = functions.select_urls_from_list(source2, "data-0001", "parquet")

# ## Génération des noms de fichiers
# for link in link_list:
#     name = functions.generate_parquet_name(link)

#     ## Créer le client de blob
#     blob_client = container_client.get_blob_client(name)

#     ## Télécharger le fichier dans le conteneur blob
#     blob_client.upload_blob(response.content, overwrite=True)