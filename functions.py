import requests
import re
from bs4 import BeautifulSoup
import sys


def get_urls_from_page(url):
    """
    This function creates the list of links from a web page
    Args:
        url (str): the web page's url
    Returns:
        list of str: the list of links
    """
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
    
def select_urls_from_list(page, selection, extension = "csv"):
    """
    This function selects the links from a web page that matches the selection string ending by the extension.
    Args:
        page (str): the web page's url
        selection (str): the string matching in  
        extension (str): the link suffixe
    Returns:
        list of str: the list of matching links
    """
    urls = get_urls_from_page(page)
    pattern = fr".*{selection}.*\.{extension}$"
    urls_reduite = []
    for url in urls:
        if re.match(pattern, url):    
            urls_reduite.append(url)
    return urls_reduite

def generate_blob_name(link):
    """
    This function generates a file name
    Args:
        link (str): the file links
    Returns:
        str: the name of file
    """
    link_parts = re.findall(r'/([a-zA-Z0-9\-]+)', link)
    liste_reduite = []
    liste_reduite.append(link_parts[-4])
    liste_reduite.append(link_parts[-3])
    liste_reduite.append(link_parts[-1])
    name = "_".join(liste_reduite)
    name = f"{name}.csv"
    return name

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