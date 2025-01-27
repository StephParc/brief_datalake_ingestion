from azure.storage.blob import ContainerClient
import requests
import functions

# Exécution du script princpal script.py
with open("script.py") as f:
    code = f.read()
exec(code)

# Chargement des fichiers csv Airbnb
## Télécharger le fichier depuis l'URL
source = "https://insideairbnb.com/get-the-data/"
response = requests.get(source)
response.raise_for_status()

## Chargement des fichiers
link_list = functions.select_urls_from_list(source, "spain", "csv")

## Génération des noms de fichiers
for link in link_list:
    name = functions.generate_blob_name(link)

    ## Créer le client de blob
    blob_client = container_client.get_blob_client(name)

    ## Télécharger le fichier dans le conteneur blob
    blob_client.upload_blob(response.content, overwrite=True)