import requests
import re
import colorama
import os
import unittest
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style
from datetime import datetime
from cryptography.fernet import Fernet

colorama.init()

report_directory = "reportes_vulnerabilidades_Critica"
os.makedirs(report_directory, exist_ok=True)

name = f"SSRF_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
file_path = os.path.join(report_directory, name)

vulnerabilities_detected = []
visited_urls = set()

def extract_internal_links(url):
    """Extrae enlaces internos desde la URL proporcionada."""
    try:
        response = requests.get(url, timeout=10)
        internal_links = re.findall(r'href=["\'](https?://[^"\'>]+)', response.text)
        return [link for link in internal_links if url in link]
    except requests.RequestException:
        return []

def perform_ssrf_checks(url):
    """Realiza pruebas de SSRF en la URL proporcionada."""
    payloads = [
        "http://localhost", "http://127.0.0.1", "http://169.254.169.254",
        "http://metadata.google.internal", "http://169.254.169.254/latest/meta-data/"
    ]

    headers = {"User-Agent": "Mozilla/5.0"}

    for payload in payloads:
        try:
            response = requests.get(url, headers=headers, params={"test": payload}, timeout=10)
            response_time = response.elapsed.total_seconds()

            if response.status_code == 200 and re.search(r"(localhost|127\.0\.0\.1|169\.254\.169\.254)", response.text):
                vulnerabilities_detected.append(f"- {url} con payload {payload}, tiempo: {response_time}s")
                print(f'{Fore.RED}Vulnerable{Style.RESET_ALL}: {url} con payload {payload}')
                break
        except requests.RequestException as e:
            print(f"{Fore.YELLOW}Error en {url} con payload {payload}: {e}{Style.RESET_ALL}")

    for link in extract_internal_links(url):
        if link not in visited_urls:
            visited_urls.add(link)
            perform_ssrf_checks(link)

def ssrf(url):
    """Función principal para iniciar el escaneo SSRF."""
    visited_urls.add(url)
    perform_ssrf_checks(url)

    if vulnerabilities_detected:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<h1>Reporte de Vulnerabilidades</h1><ul>")
            for v in vulnerabilities_detected:
                file.write(f"<li>{v}</li>")
            file.write("</ul>")
        print(Fore.LIGHTRED_EX + "Vulnerabilidades detectadas." + Style.RESET_ALL)
    else:
        print(Fore.LIGHTGREEN_EX + "No se detectaron vulnerabilidades." + Style.RESET_ALL)


# --- PRUEBAS UNITARIAS ---
class TestSSRFScanner(unittest.TestCase):
    def test_extract_internal_links(self):
        """Verifica extracción de enlaces internos."""
        html = '<a href="https://example.com/page1">Link1</a>'
        with requests_mock.Mocker() as m:
            m.get("https://example.com", text=html)
            links = extract_internal_links("https://example.com")
            self.assertIn("https://example.com/page1", links)

    def test_perform_ssrf_checks(self):
        """Simula un ataque SSRF y detecta respuestas vulnerables."""
        with requests_mock.Mocker() as m:
            m.get("https://malicious.com", text="127.0.0.1 detected")
            perform_ssrf_checks("https://malicious.com")
            self.assertTrue(any("127.0.0.1" in v for v in vulnerabilities_detected))

# --- EJECUCIÓN NORMAL ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:  # Solo pedirá la URL si NO se está ejecutando como prueba unitaria
        url = input("Ingrese la URL a analizar: ").strip()
        ssrf(url)
    else:
        unittest.main()
