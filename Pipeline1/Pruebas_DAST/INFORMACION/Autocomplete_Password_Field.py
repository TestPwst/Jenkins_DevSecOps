import requests
import re
from urllib.parse import urlparse, urljoin
import colorama
import os
from colorama import Fore, Style
from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock

colorama.init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Mejores_Practicas"
os.makedirs(report_directory, exist_ok=True)


def get_user_url():
    return input("Ingrese la URL a escanear: ")


def extract_internal_links(url):
    internal_links = set()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            base_url = get_base_url(url)
            links = re.findall(r'href=[\'\"](.*?)[\'\"]', page_content, flags=re.IGNORECASE)
            for link in links:
                absolute_link = urljoin(base_url, link.strip())
                if is_same_domain(absolute_link, base_url):
                    internal_links.add(absolute_link)
    except requests.RequestException:
        print(f"{Fore.YELLOW}Error en el servidor al acceder a {url}{Style.RESET_ALL}")
    return internal_links


def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_same_domain(url, base_url):
    return urlparse(url).netloc == urlparse(base_url).netloc


def perform_autocomplete_checks(url, vulnerabilities_detected):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            password_fields = re.findall(r'<input.*?type=["\']password["\'].*?>', page_content, flags=re.IGNORECASE)
            for password_field in password_fields:
                if 'autocomplete="on"' in password_field.lower() or 'autocomplete' not in password_field.lower():
                    vulnerabilities_detected.append(f"Vulnerable: {password_field} en {url}")
    except requests.RequestException:
        print(f"{Fore.YELLOW}Error en el servidor al acceder a {url}{Style.RESET_ALL}")


def scan_internal_links_autocomplete(url, vulnerabilities_detected):
    visited_urls = set()
    internal_links = extract_internal_links(url)
    for link in internal_links:
        if link not in visited_urls:
            visited_urls.add(link)
            perform_autocomplete_checks(link, vulnerabilities_detected)


class TestVulnerabilityScanner(unittest.TestCase):
    @patch('requests.get')
    def test_extract_internal_links(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<a href="/internal">Internal Link</a>'
        links = extract_internal_links("http://example.com")
        self.assertIn("http://example.com/internal", links)

    @patch('requests.get')
    def test_perform_autocomplete_checks_vulnerable(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<input type="password" autocomplete="on">'
        vulnerabilities_detected = []
        perform_autocomplete_checks("http://example.com", vulnerabilities_detected)
        self.assertTrue(len(vulnerabilities_detected) > 0)

    @patch('requests.get')
    def test_perform_autocomplete_checks_secure(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<input type="password" autocomplete="off">'
        vulnerabilities_detected = []
        perform_autocomplete_checks("http://example.com", vulnerabilities_detected)
        self.assertTrue(len(vulnerabilities_detected) == 0)


if __name__ == "__main__":
    url = get_user_url()
    vulnerabilities_detected = []
    scan_internal_links_autocomplete(url, vulnerabilities_detected)
    unittest.main()
