import requests
import re
import os
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style
from cryptography.fernet import Fernet
import unittest
from unittest import mock

# Inicializar colorama
init()

# Directorio para reportes
report_directory = "reportes_vulnerabilidades_Media"
os.makedirs(report_directory, exist_ok=True)

# Lista de vulnerabilidades detectadas
vulnerabilities_detected = []
visited_urls = set()


def extract_internal_links(url):
    """Extrae enlaces internos de una URL."""
    internal_links = set()
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            page_content = response.text
            base_url = get_base_url(url)
            links = re.findall(r'href=[\'"](.*?)[\'"]', page_content, flags=re.IGNORECASE)
            for link in links:
                absolute_link = urljoin(base_url, link.strip())
                if is_same_domain(absolute_link, base_url):
                    internal_links.add(absolute_link)
    except requests.RequestException:
        pass  # Ignorar errores de conexión
    return internal_links


def get_base_url(url):
    """Extrae la base de la URL."""
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_same_domain(url, base_url):
    """Verifica si la URL pertenece al mismo dominio."""
    return urlparse(url).netloc == urlparse(base_url).netloc


def perform_logging_monitoring_checks(url):
    """Verifica vulnerabilidades de registro y monitoreo en una URL."""
    try:
        response = requests.get(url, timeout=5)
        print(f"{Fore.CYAN}Verificando: {url} (HTTP {response.status_code}){Style.RESET_ALL}")

        if response.status_code != 200:
            return False

        headers = response.headers
        logging_issues = []

        if "X-Content-Type-Options" not in headers:
            logging_issues.append("Falta la cabecera X-Content-Type-Options.\n")

        if "Audit-Log" not in headers:
            logging_issues.append("Falta un sistema de registro de auditoría.\n")

        if "Server" in headers and re.search(r"\d", headers["Server"]):
            logging_issues.append(f"Exposición de la versión del servidor: {headers['Server']}.\n")

        if logging_issues:
            vulnerabilities_detected.append(f"- {url}: {', '.join(logging_issues)}")
            print(f"{Fore.RED}Vulnerabilidades detectadas en {url}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.GREEN}Sin problemas de registro y monitoreo en {url}{Style.RESET_ALL}")
        return False

    except requests.RequestException:
        print(f"{Fore.YELLOW}Error al analizar: {url}{Style.RESET_ALL}")
        return False


def start_logging_monitoring_scan():
    """Solicita la URL al usuario y realiza el escaneo."""
    url = input("Ingrese la URL a analizar: ").strip()
    print(f"{Fore.CYAN}Iniciando escaneo en: {url}{Style.RESET_ALL}")

    perform_logging_monitoring_checks(url)
    internal_links = extract_internal_links(url)

    for link in internal_links:
        if link not in visited_urls:
            visited_urls.add(link)
            perform_logging_monitoring_checks(link)

    if vulnerabilities_detected:
        filename = f"Fallas_Registro_Monitoreo_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(report_directory, filename)
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n")
            file.write("<title>Reporte de Vulnerabilidades Media</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Fallas de Registro y Monitoreo</h1>")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>URL Analizada: {url}</p>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
            for vulnerability in vulnerabilities_detected:
                file.write(f"<li>{vulnerability}</li>\n")
            file.write("</ul>\n</body>\n</html>")
        with open(file_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(file_path + ".enc", 'wb') as f:
            f.write(encrypted_data)

        print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}No se encontraron vulnerabilidades.{Style.RESET_ALL}")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    start_logging_monitoring_scan()

class TestLoggingMonitoring(unittest.TestCase):

    def setUp(self):
        """Solicita la URL al usuario antes de ejecutar las pruebas."""
        global user_url
        if not hasattr(self, 'user_url'):
# --- PRUEBAS UNITARIAS ---
            self.user_url = input("Ingrese una URL para las pruebas: ").strip()

    def test_get_base_url(self):
        """Prueba la extracción de la base de la URL."""
        self.assertEqual(get_base_url(self.user_url),
                         f"{urlparse(self.user_url).scheme}://{urlparse(self.user_url).netloc}")

    def test_is_same_domain(self):
        """Prueba si dos URLs pertenecen al mismo dominio."""
        base_url = get_base_url(self.user_url)
        test_url = urljoin(base_url, "/test")
        self.assertTrue(is_same_domain(test_url, base_url))
        self.assertFalse(is_same_domain("https://otherdomain.com", base_url))

    def test_extract_internal_links(self):
        """Simula una página HTML con enlaces internos y prueba su extracción."""
        html_content = '<a href="/about">About</a><a href="/contact">Contact</a>'
        base_url = get_base_url(self.user_url)
        with unittest.mock.patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = html_content
            links = extract_internal_links(base_url)
            self.assertIn(urljoin(base_url, "/about"), links)
            self.assertIn(urljoin(base_url, "/contact"), links)

    def test_perform_logging_monitoring_checks(self):
        """Prueba que la función retorna un booleano al analizar la URL."""
        with unittest.mock.patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.headers = {"X-Content-Type-Options": "nosniff"}
            result = perform_logging_monitoring_checks(self.user_url)
            self.assertIsInstance(result, bool)
