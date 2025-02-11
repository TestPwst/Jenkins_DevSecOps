import re
import requests
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style, init
import os
from datetime import datetime
import unittest

# Inicializar colorama
init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Alta"

# Asegurarse de que el directorio existe
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"Reporte_Phishing_ {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"

# Crear la ruta completa del archivo
file_path = os.path.join(report_directory, name)

vulnerabilities_detected = []
visited_urls = set()

class TestPhishing(unittest.TestCase):

    def extract_internal_links(self, url):
        internal_links = set()
        try:
            response = requests.get(url)
            if response.status_code == 200:
                page_content = response.text
                base_url = self.get_base_url(url)
                links = re.findall(r'href=[\'"](.*?)[\'"]', page_content, flags=re.IGNORECASE)
                for link in links:
                    absolute_link = urljoin(base_url, link.strip())
                    if self.is_same_domain(absolute_link, base_url):
                        internal_links.add(absolute_link)
        except requests.RequestException as e:
            print(f'{Fore.YELLOW}Error al extraer enlaces internos de {url}: {e}{Style.RESET_ALL}')
        return internal_links

    def get_base_url(self, url):
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return base_url

    def is_same_domain(self, url, base_url):
        parsed_url = urlparse(url)
        parsed_base_url = urlparse(base_url)
        return parsed_url.netloc == parsed_base_url.netloc

    def is_suspicious_domain(self, url):
        """Verifica si un dominio es sospechoso basándose en listas blancas y negras."""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        whitelist = ['@powerstreet.com.mx', '@assist.com.uy', 'https://client.assist.com.uy/', 'https://client.qa.powerstreet.cloud/']
        blacklist = ['@domain-name.com', '@google.org.com', '@paypal.com', '@apple.com']

        if domain in blacklist:
            return True
        if domain not in whitelist and 'example' in domain:  # Ajusta según el contexto
            return True
        return False

    def detect_phishing_patterns(self, url, input_fields):
        """Detecta patrones de phishing en los campos de entrada."""
        phishing_patterns = [
            r'https?://.*?client.qa.powerstreet\.cloud',
            r'javascript:redirect\(["\'](.*?)["\']\)',
            r'https?://.*?/(login|account|secure)\.php',
        ]

        for input_field in input_fields:
            for pattern in phishing_patterns:
                match = re.search(pattern, input_field, flags=re.IGNORECASE)
                if match:
                    suspected_url = match.group(0)
                    if self.is_suspicious_domain(suspected_url):
                        damage = "Posible redirección a un sitio de phishing."
                        protections = [
                            "\n1. Validar redirecciones en el backend.",
                            "\n2. Implementar CSP para prevenir redirecciones no autorizadas.",
                            "\n3. Usar validación y sanitización de entradas."
                        ]
                        cwe = "CWE-601: URL Redirection to Untrusted Site ('Open Redirect')"
                        vulnerabilities_detected.append(
                            f"Vulnerable: {input_field} en {url}\n"
                            f"Redirección sospechosa: {suspected_url}\n"
                            f"Daño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\n"
                        )
                        print(f"{Fore.RED}Vulnerable{Style.RESET_ALL}: {input_field} en {url}\n"
                              f"Redirección sospechosa: {suspected_url}\n"
                              f"Daño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}")
                        break
            else:
                print(f"{Fore.GREEN}Seguro{Style.RESET_ALL}: {input_field} en {url}")

    def perform_phishing_checks(self, url):
        """Realiza el análisis de phishing en una URL y sus enlaces internos."""
        try:
            response = requests.get(url, timeout=10)
            print(f"{Fore.CYAN}Verificando código de respuesta HTTP para {url}...{Style.RESET_ALL}")
            if response.status_code == 200:
                print(f"{Fore.GREEN}Código de respuesta 200 OK{Style.RESET_ALL}")
                page_content = response.text

                # Extraer campos de entrada en formularios
                input_fields = re.findall(r'<form.*?action=["\'](.*?)["\'].*?>', page_content, flags=re.IGNORECASE)
                self.detect_phishing_patterns(url, input_fields)

                # Verificar enlaces internos
                internal_links = self.extract_internal_links(url)
                for link in internal_links:
                    if link not in visited_urls:
                        visited_urls.add(link)
                        self.perform_phishing_checks(link)
            elif response.status_code == 404:
                print(f"{Fore.YELLOW}Error 404: Página no encontrada en {url}{Style.RESET_ALL}")
            elif response.status_code == 403:
                print(f"{Fore.YELLOW}Error 403: Acceso prohibido en {url}{Style.RESET_ALL}")
            elif response.status_code == 500:
                print(f"{Fore.RED}Error 500: Error interno del servidor en {url}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Código de respuesta {response.status_code} en {url}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error al conectar con {url}: {e}{Style.RESET_ALL}")

    def phishing(self, url):
        print(f"{Fore.LIGHTBLUE_EX}--- Escaneo de Phishing ---")
        self.perform_phishing_checks(url)
        if vulnerabilities_detected:
            with open(file_path, 'w') as file:
                file.write("<html><head><title>Reporte de Vulnerabilidades Alta</title></head><body>")
                file.write("=" * 150 + "\n\n")
                file.write("<h1 style='text-align:center;'>Reporte de Vulnerabilidades Alta</h1>")  #
                file.write("=" * 150 + "\n\n")
                file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
                file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
                # Escribir cada vulnerabilidad en formato HTML
                for vulnerability in vulnerabilities_detected:
                    file.write(f"<li><pre>{vulnerability}</pre></li>")
                # Cerrar las etiquetas HTML
                file.write("</ul></body></html>")
                print(Fore.LIGHTRED_EX + "Se detectaron vulnerabilidades." + Style.RESET_ALL)
            print(f"{Fore.LIGHTMAGENTA_EX}Reporte en HTML generado: {file_path}")
        else:
            print(Fore.LIGHTGREEN_EX + "No se detectaron vulnerabilidades." + Style.RESET_ALL)

    def test_phishing_scan(self):
        url = input("Ingresa la URL para escanear: ")
        self.phishing(url)

if __name__ == "__main__":
    unittest.main()
