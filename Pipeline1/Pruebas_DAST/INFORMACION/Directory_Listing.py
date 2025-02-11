import requests
from urllib.parse import urlparse, urljoin
import re
import os
from datetime import datetime
from colorama import Fore, Style, init
import unittest

# Inicializar colorama
init(autoreset=True)

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Informacion"
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"Directory_Listing_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
file_path = os.path.join(report_directory, name)

# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []
visited_urls = set()

def extract_internal_links(url):
    internal_links = set()
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
        base_url = get_base_url(url)
        links = re.findall(r'href=[\'\"](.*?)[\'\"]', page_content, flags=re.IGNORECASE)
        for link in links:
            absolute_link = urljoin(base_url, link.strip())
            if is_same_domain(absolute_link, base_url):
                internal_links.add(absolute_link)
    return internal_links

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc

def check_directory_listing(url):
    directories_to_test = ['/', '/admin/', '/backup/', '/config/', '/data/', '/docs/', '/graficos/', '/scripts/', '/tmp/']
    vulnerability_found = False
    for directory in directories_to_test:
        full_url = urljoin(url, directory)
        response = requests.get(full_url)
        if response.status_code == 200 and ('Index of' in response.text or re.search(r'<title>Index of', response.text, re.IGNORECASE)):
            vulnerabilities_detected.append(full_url)
            vulnerability_found = True
    return vulnerability_found

def perform_directory_listing_checks(url):
    global visited_urls
    if check_directory_listing(url):
        internal_links = extract_internal_links(url)
        for link in internal_links:
            if link not in visited_urls:
                visited_urls.add(link)
                perform_directory_listing_checks(link)

class TestDirectoryListing(unittest.TestCase):
    def test_is_same_domain(self):
        self.assertTrue(is_same_domain("https://example.com/page", "https://example.com"))
        self.assertFalse(is_same_domain("https://example2.com/page", "https://example.com"))

    def test_get_base_url(self):
        self.assertEqual(get_base_url("https://example.com/page"), "https://example.com")

    def test_check_directory_listing(self):
        self.assertIsInstance(check_directory_listing("https://httpd.apache.org/docs/"), bool)

if __name__ == "__main__":
    url = input("Ingrese la URL a escanear: ")
    perform_directory_listing_checks(url)
    unittest.main()
