import requests
import re
import os
import unittest
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style

# Inicializar colorama
init()

# Directorio para los reportes
report_directory = "reportes_vulnerabilidades_Critica"
os.makedirs(report_directory, exist_ok=True)

# Nombre del reporte basado en la fecha
name = f"Backdoor_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
file_path = os.path.join(report_directory, name)

# Almacenar vulnerabilidades detectadas
vulnerabilities_detected = []
visited_urls = set()

# Solicitar la URL al usuario
def get_url():
    return input("Ingrese la URL a analizar: ").strip()

# Extraer enlaces internos de una página
def extract_internal_links(url):
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

# Obtener el dominio base
def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

# Verificar si el enlace pertenece al mismo dominio
def is_same_domain(url, base_url):
    return urlparse(url).netloc == urlparse(base_url).netloc

# Revisar posibles puertas traseras
def perform_backdoor_checks(url):
    backdoor_patterns = [
        r'eval\([^)]+', r'base64_decode\([^)]+', r'system\([^)]+',
        r'shell_exec\([^)]+', r'exec\([^)]+', r'passthru\([^)]+',
        r'popen\([^)]+', r'proc_open\([^)]+', r'assert\([^)]+',
        r'phpinfo\(', r'preg_replace.*?/e', r'apache_child_terminate\(',
        r'pcntl_exec\('
    ]

    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text

            for pattern in backdoor_patterns:
                matches = re.findall(pattern, page_content, flags=re.IGNORECASE)
                if matches:
                    vulnerabilities_detected.append(f"- {pattern} encontrado en {url}\n")
                    print(f"{Fore.RED}Vulnerabilidad detectada en {url}: {pattern}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}Seguro: {pattern} no encontrado en {url}{Style.RESET_ALL}")

    except requests.RequestException:
        print(f"{Fore.YELLOW}Error al analizar {url}{Style.RESET_ALL}")

# Escaneo recursivo de enlaces internos
def perform_recursive_backdoor_checks(url):
    internal_links = extract_internal_links(url)
    for link in internal_links:
        if link not in visited_urls:
            visited_urls.add(link)
            perform_backdoor_checks(link)
            perform_recursive_backdoor_checks(link)

# Iniciar el escaneo
def start_scan():
    url = get_url()
    if url:
        print(f"{Fore.CYAN}Escaneando {url}...{Style.RESET_ALL}")
        perform_recursive_backdoor_checks(url)

        if vulnerabilities_detected:
            with open(file_path, 'w') as file:
                file.write("<html><head><title>Reporte de Vulnerabilidades</title></head><body>")
                file.write("<h1>Reporte de Vulnerabilidades</h1>")
                file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
                file.write("<ul>")
                for vulnerability in vulnerabilities_detected:
                    file.write(f"<li>{vulnerability}</li>")
                file.write("</ul></body></html>")
            print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado: {file_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTGREEN_EX}No se encontraron vulnerabilidades.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No ingresó una URL válida.{Style.RESET_ALL}")

# ---- PRUEBAS UNITARIAS ----
class TestBackdoorScanner(unittest.TestCase):

    def test_get_base_url(self):
        self.assertEqual(get_base_url("https://example.com/page"), "https://example.com")

    def test_is_same_domain(self):
        self.assertTrue(is_same_domain("https://example.com/test", "https://example.com"))
        self.assertFalse(is_same_domain("https://evil.com/test", "https://example.com"))

    def test_extract_internal_links(self):
        mock_html = '<a href="/about">About</a> <a href="https://example.com/contact">Contact</a>'
        url = "https://example.com"
        requests.get = lambda _: type('Response', (), {"status_code": 200, "text": mock_html})()
        links = extract_internal_links(url)
        self.assertIn("https://example.com/about", links)
        self.assertIn("https://example.com/contact", links)


# ---- EJECUCIÓN ----
if __name__ == "__main__":
    modo_pruebas = input("¿Quieres ejecutar las pruebas unitarias? (s/n): ").strip().lower()

    if modo_pruebas == "s":
        unittest.main()
    else:
        start_scan()
