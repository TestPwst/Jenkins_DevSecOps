import requests
import re
import os
import unittest
from datetime import datetime
from colorama import Fore, Style, init

# Inicializa colorama
init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Informacion"
os.makedirs(report_directory, exist_ok=True)

# Rutas internas comunes para verificar
internal_paths = [
    '/etc/', '/var/', '/proc/', '/sys/', '/root/', '/home/', '/tmp/', '/srv/',
    '/usr/local/', '/usr/bin/', '/usr/sbin/', '/lib/', '/lib64/', '/boot/',
    '/dev/', '/run/', '/media/', '/mnt/', '/opt/', '/bin/', '/sbin/',
    '/windows/', '/winnt/', '/program files/', '/documents and settings/', '/recycler/'
]

# Patrones comunes para detectar posibles divulgaciones de datos de tarjetas de crédito
credit_card_keywords = re.compile(
    r'\b(credit\s*card|card\s*number|credit\s*card\s*number|cvv|cvv2|expiration\s*date|card\s*security\s*code)\b',
    re.IGNORECASE
)


def check_internal_path_disclosure(url):
    """ Verifica la divulgación de rutas internas en una página web."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error al hacer la solicitud a {url}: {e}{Style.RESET_ALL}")
        return False

    for path in internal_paths:
        if path in response.text:
            return True
    return False


def check_credit_card_disclosure(url):
    """ Verifica si hay divulgación de datos de tarjetas de crédito en una página web."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error al hacer la solicitud a {url}: {e}{Style.RESET_ALL}")
        return False

    return bool(credit_card_keywords.search(response.text))


class TestVulnerabilityScanner(unittest.TestCase):
    """ Clase de pruebas unitarias para la detección de vulnerabilidades. """

    def test_internal_path_disclosure(self):
        url = "https://example.com"
        result = check_internal_path_disclosure(url)
        self.assertIsInstance(result, bool)

    def test_credit_card_disclosure(self):
        url = "https://example.com"
        result = check_credit_card_disclosure(url)
        self.assertIsInstance(result, bool)


if __name__ == "__main__":
    url = input("Ingrese la URL a escanear: ")
    vulnerabilities_detected = []

    if check_internal_path_disclosure(url):
        vulnerabilities_detected.append(f"Divulgación de Rutas Internas en: {url}")
    if check_credit_card_disclosure(url):
        vulnerabilities_detected.append(f"Divulgación de Datos de Tarjeta de Crédito en: {url}")

    if vulnerabilities_detected:
        report_name = f"Internal_Path_Disclosure_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(report_directory, report_name)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<html><body><h1>Reporte de Vulnerabilidades</h1><ul>")
            for vulnerability in vulnerabilities_detected:
                file.write(f"<li>{vulnerability}</li>")
            file.write("</ul></body></html>")

        print(f"{Fore.RED}Se detectaron vulnerabilidades. Reporte generado: {file_path}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}No se detectaron vulnerabilidades.{Style.RESET_ALL}")

    unittest.main()
