import requests
import re
import os
import unittest
from datetime import datetime
import colorama
from colorama import Fore, Style
from unittest.mock import patch

colorama.init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Informacion"
os.makedirs(report_directory, exist_ok=True)

# Lista de versiones vulnerables conocidas
vulnerable_versions = ['1.12.1', '1.12.0', '1.11.4']


def check_jquery_ui_autocomplete_version(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        jquery_version_pattern = r'jquery-ui-autocomplete.*?v?(\d+\.\d+\.\d+)'
        matches = re.findall(jquery_version_pattern, response.text, re.IGNORECASE)

        found_vulnerabilities = [version for version in matches if version in vulnerable_versions]
        return found_vulnerabilities
    except requests.RequestException:
        return None


def run_tests_autocomplete_version(url):
    print("--- jQuery UI Autocomplete Version ---")
    print(f"Probando URL: {url}")
    vulnerabilities_detected = check_jquery_ui_autocomplete_version(url)

    if vulnerabilities_detected:
        name = f"jQuery_UI_Autocomplete_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(report_directory, name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html><html lang='en'><head>")
            file.write("<meta charset='UTF-8'><title>Reporte de Vulnerabilidades</title>")
            file.write("</head><body><h1>Reporte de Vulnerabilidades</h1><ul>")
            for version in vulnerabilities_detected:
                file.write(f"<li>Vulnerable: jQuery UI Autocomplete versión {version} en {url}</li>")
            file.write("</ul></body></html>")
        print(f"{Fore.LIGHTRED_EX}Se detectaron vulnerabilidades. Reporte generado en {file_path}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTGREEN_EX}No se detectaron vulnerabilidades en {url}.{Style.RESET_ALL}")


class TestJQueryUIAutocomplete(unittest.TestCase):

    @patch('requests.get')
    def test_vulnerable_version_detected(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<script src=\"jquery-ui-autocomplete-1.12.1.js\"></script>"

        result = check_jquery_ui_autocomplete_version("http://example.com")
        self.assertIn('1.12.1', result)

    @patch('requests.get')
    def test_no_vulnerable_version_detected(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<script src=\"jquery-ui-autocomplete-2.0.0.js\"></script>"

        result = check_jquery_ui_autocomplete_version("http://example.com")
        self.assertEqual(result, [])

    @patch('requests.get')
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException

        result = check_jquery_ui_autocomplete_version("http://example.com")
        self.assertIsNone(result)


if __name__ == "__main__":
    url = input("Ingrese la URL a analizar: ")
    run_tests_autocomplete_version(url)
    unittest.main(exit=False)
