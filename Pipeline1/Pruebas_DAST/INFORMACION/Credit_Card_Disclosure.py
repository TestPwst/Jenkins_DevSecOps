import unittest
import requests
import re
import colorama
import os
from colorama import Fore, Style
from datetime import datetime
from urllib.parse import urlparse, urljoin

colorama.init()

# Definir el directorio donde se almacenarán los reportes
REPORT_DIRECTORY = "reportes_vulnerabilidades_Informacion"
os.makedirs(REPORT_DIRECTORY, exist_ok=True)

# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []
visited_urls = set()

VULNERABILITY_TITLE = "Divulgación de Tarjetas de Crédito"


def extract_internal_links(url):
    """Extrae enlaces internos de una página web."""
    internal_links = set()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            base_url = get_base_url(url)
            links = re.findall(r'href=[\'"](.*?)[\'"]', page_content, flags=re.IGNORECASE)
            for link in links:
                absolute_link = urljoin(base_url, link.strip())
                if is_same_domain(absolute_link, base_url):
                    internal_links.add(absolute_link)
    except requests.RequestException:
        pass
    return internal_links


def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc


def luhn_check(card_number):
    """Valida un número de tarjeta de crédito usando el algoritmo de Luhn."""
    card_number = ''.join(filter(str.isdigit, card_number))
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def perform_credit_card_disclosure_checks(url):
    global visited_urls
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            card_pattern = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
            potential_cards = card_pattern.findall(page_content)
            if potential_cards:
                for card in potential_cards:
                    if luhn_check(card):
                        vulnerabilities_detected.append(f"Vulnerable: {card} en {url}")
                        print(
                            f"{Fore.RED}{VULNERABILITY_TITLE}{Style.RESET_ALL}: Tarjeta detectada {Fore.RED}{card}{Style.RESET_ALL} en {url}")

            internal_links = extract_internal_links(url)
            for link in internal_links:
                if link not in visited_urls:
                    visited_urls.add(link)
                    perform_credit_card_disclosure_checks(link)
    except requests.RequestException:
        pass


def save_report():
    """Guarda los resultados en un archivo HTML si se detectan vulnerabilidades."""
    if vulnerabilities_detected:
        name = f"CreditCardDisclosure_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(REPORT_DIRECTORY, name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<html><head><title>Reporte de Vulnerabilidades</title></head><body>")
            file.write(f"<h1>{VULNERABILITY_TITLE}</h1>")
            file.write("<ul>")
            for vulnerability in vulnerabilities_detected:
                file.write(f"<li>{vulnerability}</li>")
            file.write("</ul></body></html>")
        print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado: {file_path}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTGREEN_EX}No se detectaron vulnerabilidades.{Style.RESET_ALL}")


if __name__ == "__main__":
    url = input("Ingrese la URL a analizar: ")
    perform_credit_card_disclosure_checks(url)
    save_report()


class TestCreditCardDisclosure(unittest.TestCase):
    def test_luhn_check_valid(self):
        self.assertTrue(luhn_check("4532015112830366"))
        self.assertTrue(luhn_check("6011000990139424"))

    def test_luhn_check_invalid(self):
        self.assertFalse(luhn_check("1234567890123456"))
        self.assertFalse(luhn_check("1111222233334444"))

    def test_get_base_url(self):
        self.assertEqual(get_base_url("https://example.com/path/page.html"), "https://example.com")
        self.assertEqual(get_base_url("http://sub.example.com"), "http://sub.example.com")

    def test_is_same_domain(self):
        self.assertTrue(is_same_domain("https://example.com/page", "https://example.com"))
        self.assertFalse(is_same_domain("https://another.com/page", "https://example.com"))


if __name__ == "__main__":
    unittest.main()
