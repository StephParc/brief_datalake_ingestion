#!/bin/bash
set -o allexport
source .env
set +o allexport

echo $SP_ID_SECONDARY
# Connection to secondary service principal to obtain main service principal password
az login --service-principal --username $SP_ID_SECONDARY --password $SP_SECONDARY_PASSWORD --tenant $TENANT_ID 

# Get the Key Vault secret value
secret_value=$(az keyvault secret show --name $SECRET_NAME --vault-name $KEYVAULT_URL --query value -o tsv)

# Connection to main service principal
az login --service-principal -u $SP_ID_PRINCIPAL -p $secret_value --tenant $TENANT_ID

# Generate token
token_sas = $(az storage container generate-sas \
    --account-name $STORAGE_ACCOUNT_NAME \
    --name $BLOB_CONTAINER \
    --permissions w \
    --expiry 1hour \
    --https-only \
    --output tsv)

file_source = "https://data.insideairbnb.com/spain/catalonia/barcelona/2024-09-06/visualisations/reviews.csv"
blob_name = "barcelona_2024-09-06_reviews.csv"
destination = "https://$STORAGE_ACCOUNT_NAME.blob.core.windows.net/$BLOB_CONTAINER/input_data_azcopy?sp=w"

# Load file
az storage blob upload \
    --account-name $STORAGE_ACCOUNT_NAME \
    --container-name $BLOB_CONTAINER \
    --file $file_source \
    --name $blob_name \
    --overwrite

