import requests
import re
import os
from urllib.parse import urlparse, urljoin
import colorama
from colorama import Fore, Style
from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock
from cryptography.fernet import Fernet

colorama.init()

REPORT_DIR = "reportes_vulnerabilidades_Media"
os.makedirs(REPORT_DIR, exist_ok=True)


def get_user_input():
    return input("Ingrese la URL a analizar: ").strip()




def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_same_domain(url, base_url):
    return urlparse(url).netloc == urlparse(base_url).netloc


def extract_internal_links(url):
    internal_links = set()
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            base_url = get_base_url(url)
            links = re.findall(r'href=[\'"](.*?)[\'"]', response.text, flags=re.IGNORECASE)
            for link in links:
                absolute_link = urljoin(base_url, link.strip())
                if is_same_domain(absolute_link, base_url):
                    internal_links.add(absolute_link)
    except requests.exceptions.RequestException:
        pass
    return internal_links


def check_hsts(url):
    try:
        response = requests.get(url, timeout=5)
        if 'strict-transport-security' not in response.headers:
            return {
                "url": url,
                "daño": "Ataques de 'man-in-the-middle' que pueden interceptar y modificar la comunicación.",
                "prevención": [
                    "Implementar HSTS con 'Strict-Transport-Security'.",
                    "Asegurar que HSTS esté habilitado para todas las páginas.",
                    "Usar certificados SSL/TLS válidos y no caducados."
                ],
                "cwe": "CWE-319: Cleartext Transmission of Sensitive Information"
            }
        return None
    except requests.exceptions.RequestException:
        return None


def generate_html_report(vulnerabilities, url):
    if vulnerabilities:
        filename = f"HSTS_Error_Warnings_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(REPORT_DIR, filename)
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n")
            file.write("<title>Reporte de Vulnerabilidades Baja</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Cookie not Marked as HTTPOnly</h1>")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>URL Analizada: {url}</p>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
        for vuln in vulnerabilities:
            file.write(f"<li><pre>{vuln}</pre></li>")
        file.write("</ul></body></html>")
        with open(file_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(file_path + ".enc", 'wb') as f:
            f.write(encrypted_data)

        print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")

    else:
        return print(f"\n{Fore.GREEN}No se detectaron vulnerabilidades.{Style.RESET_ALL}")

def perform_hsts_checks(url):
    visited_urls = set()
    vulnerabilities_detected = []

    def scan(url):
        if url in visited_urls:
            return
        visited_urls.add(url)
        vuln = check_hsts(url)
        if vuln:
            vulnerabilities_detected.append(vuln)
        for link in extract_internal_links(url):
            scan(link)

    scan(url)
    if vulnerabilities_detected:
        generate_html_report(vulnerabilities_detected, url)


if __name__ == "__main__":
    user_url = get_user_input()
    perform_hsts_checks(user_url)


class TestHSTSChecker(unittest.TestCase):

    @patch("requests.get")
    def test_check_hsts_vulnerable(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, headers={})
        result = check_hsts("https://test.com")
        self.assertIsNotNone(result)
        self.assertEqual(result["cwe"], "CWE-319: Cleartext Transmission of Sensitive Information")

    @patch("requests.get")
    def test_check_hsts_secure(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, headers={"strict-transport-security": "max-age=63072000"})
        result = check_hsts("https://client.assist.com.uy/")
        self.assertIsNone(result)

    @patch("requests.get")
    def test_extract_internal_links(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, text='<a href="/about">About</a>')
        links = extract_internal_links("https://client.assist.com.uy/")
        self.assertIn("https://client.assist.com.uy/about", links)  # Corrección aquí

    def test_get_base_url(self):
        self.assertEqual(get_base_url("https://client.assist.com.uy/"),
                         "https://client.assist.com.uy")  # Sin la barra final

    def test_is_same_domain(self):
        self.assertTrue(is_same_domain("https://client.assist.com.uy/about", "https://client.assist.com.uy/"))
        self.assertFalse(is_same_domain("https://client.qa.powerstreet.cloud/", "https://client.assist.com.uy/"))


if __name__ == "__main__":
    unittest.main()
