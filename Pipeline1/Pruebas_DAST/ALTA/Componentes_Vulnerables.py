import unittest
from unittest.mock import patch
import requests
import re
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style
import os

# Inicializar colorama
init()

# Crear un directorio temporal para los reportes
report_directory = "reportes_vulnerabilidades_Alta"
os.makedirs(report_directory, exist_ok=True)

# Crear una lista global para almacenar vulnerabilidades
vulnerabilities_detected = []
visited_urls = set()


def check_http_status(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        return response
    except requests.exceptions.RequestException as e:
        return None


def perform_vulnerable_components_checks(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            libraries = re.findall(r'<script.*?src=[\'"](.*?)[\'"].*?>|<link.*?href=[\'"](.*?)[\'"].*?>', page_content)
            for library in libraries:
                library_url = library[0] if library[0] else library[1]
                if library_url:
                    library_name = library_url.split('/')[-1].split('.')[0]
                    version = re.search(r'(\d+\.\d+(\.\d+)?)', library_url)
                    version = version.group(0) if version else "Desconocida"

                    # Vulnerabilidad conocida de ejemplo
                    vulnerable_versions = {
                        'jquery': ['1.12.4'],
                    }

                    if library_name in vulnerable_versions and version in vulnerable_versions[library_name]:
                        vulnerabilities_detected.append(
                            f"Componente vulnerable detectado: {library_name} versión {version} en {url}"
                        )
    except requests.RequestException as e:
        pass


def check_security_headers(url):
    response = check_http_status(url)
    if not response:
        return

    headers = response.headers
    security_headers = {
        'Content-Security-Policy': 'CSP',
        'Strict-Transport-Security': 'HSTS',
    }

    for header, description in security_headers.items():
        if header not in headers:
            vulnerabilities_detected.append(f"Vulnerable: {header} faltante en {url}")


def check_insecure_cookie_settings(url):
    response = check_http_status(url)
    if not response:
        return
    cookies = response.cookies
    for cookie in cookies:
        if not cookie.has_nonstandard_attr('HttpOnly'):
            vulnerabilities_detected.append(f"Cookie {cookie.name} sin HttpOnly en {url}")


def check_directory_listing(url):
    response = check_http_status(url)
    if not response:
        return

    if 'Index of' in response.text:
        vulnerabilities_detected.append(f"Listado de directorios habilitado en {url}")


def mala_configuracion_seguridad(url):
    perform_vulnerable_components_checks(url)
    check_security_headers(url)
    check_insecure_cookie_settings(url)
    check_directory_listing(url)


class TestVulnerabilities(unittest.TestCase):

    @patch('builtins.input', return_value="https://client.qa.powerstreet.cloud")
    @patch('requests.get')
    def test_vulnerabilities_detection(self, mock_get, mock_input):
        # Simular la respuesta de la API
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html><script src="https://code.jquery.com/jquery-1.12.4.js"></script></html>'
        mock_get.return_value.headers = {'Content-Security-Policy': 'default-src *'}

        # Llamar a la función principal
        mala_configuracion_seguridad("https://client.qa.powerstreet.cloud")

        # Verificar que se detectaron vulnerabilidades
        self.assertTrue(len(vulnerabilities_detected) > 0)
        self.assertIn("Componente vulnerable detectado: jquery versión 1.12.4 en https://client.qa.powerstreet.cloud",
                      vulnerabilities_detected)


if __name__ == '__main__':
    unittest.main()
