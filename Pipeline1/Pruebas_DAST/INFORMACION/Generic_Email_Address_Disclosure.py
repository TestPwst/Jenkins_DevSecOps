import re
import requests
import colorama
import os
import unittest
from datetime import datetime
from colorama import Fore, Style

colorama.init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Informacion"
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"Generic_Email_Disclosure_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
file_path = os.path.join(report_directory, name)

# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []


def check_generic_email_disclosure(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        generic_email_regex = r'\b(?:example|info|support|contact|admin|sales)@\w+\.\w+\b'
        emails_found = re.findall(generic_email_regex, response.text, re.IGNORECASE)

        if emails_found:
            vulnerabilities_detected.append(
                f"- {emails_found} en {url}\nCWE-200: Exposure of Sensitive Information\n")
            return True
        return False
    except requests.RequestException:
        return None


def run_tests_generic_email(url):
    print(f"Probando URL: {url}")
    vulnerable = check_generic_email_disclosure(url)
    if vulnerable:
        print(f"{Fore.RED}Vulnerable: {url}{Style.RESET_ALL}")
    elif vulnerable is None:
        print(f"{Fore.YELLOW}Error al acceder a la URL: {url}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}No vulnerable: {url}{Style.RESET_ALL}")
    print('-' * 50)


class TestEmailDisclosure(unittest.TestCase):
    def test_vulnerable_url(self):
        self.assertTrue(check_generic_email_disclosure("https://admin@powerstreet.cloud"))

    def test_non_vulnerable_url(self):
        self.assertFalse(check_generic_email_disclosure("https://example.com"))

    def test_invalid_url(self):
        self.assertIsNone(check_generic_email_disclosure("https://invalid-url-test.com"))


if __name__ == "__main__":
    user_url = input("Ingrese la URL a analizar: ")
    run_tests_generic_email(user_url)
    unittest.main()
