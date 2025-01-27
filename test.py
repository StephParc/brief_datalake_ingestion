import requests
import re
from bs4 import BeautifulSoup
import sys


def get_urls_from_page(url):
    # Faire une requête HTTP pour obtenir le contenu de la page
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Analyser le contenu HTML de la page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver tous les éléments 'a' (liens)
        links = soup.find_all('a')

        # Extraire les URLs des liens
        urls = [link.get('href') for link in links if link.get('href')]

        return urls
    else:
        print(f"Échec de la requête: {response.status_code}")
        return []

def get_parquet_from_page(url):
    # Faire une requête HTTP pour obtenir le contenu de la page
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Analyser le contenu HTML de la page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver tous les éléments 'a' (liens)
        links = soup.find_all('a')

        # Extraire les URLs des liens
        urls = [link.get('href') for link in links if link.get('href')]

        return urls
    else:
        print(f"Échec de la requête: {response.status_code}")
        return []


def generate_parquet_name(link):
    """
    This function generates a file name
    Args:
        link (str): the file links
    Returns:
        str: the name of file
    """
    name = re.findall(r'/([a-zA-Z0-9\-]+.parquet)$', link)[0]
    return name

print(generate_parquet_name('/datasets/Marqo/amazon-products-eval/blob/main/data/data-00009-of-00105.parquet'))