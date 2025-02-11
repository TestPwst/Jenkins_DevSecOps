import requests
import re
import colorama
import os
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style
from datetime import datetime
import unittest
from cryptography.fernet import Fernet

colorama.init()

# Directorio para reportes
report_directory = "reportes_vulnerabilidades_Critica"
os.makedirs(report_directory, exist_ok=True)

# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []
visited_urls = set()

# Función para extraer enlaces internos
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
    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error al extraer enlaces: {e}{Style.RESET_ALL}")
    return internal_links

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def is_same_domain(url, base_url):
    return urlparse(url).netloc == urlparse(base_url).netloc

# Probar control de acceso con autenticación
def test_access_control_with_auth(page_url, cookies=None, headers=None):
    try:
        response = requests.get(page_url, cookies=cookies, headers=headers, allow_redirects=False)
        if response.status_code == 200 and not contains_sensitive_content(response.text):
            return 'vulnerable'
        return 'secure'
    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error en el servidor: {e}{Style.RESET_ALL}")
        return 'error'

# Buscar contenido sensible en la respuesta
def contains_sensitive_content(response_text):
    sensitive_keywords = ['admin', 'dashboard', 'confidential', 'restricted']
    return any(keyword.lower() in response_text.lower() for keyword in sensitive_keywords)

# Extraer rutas restringidas
def extract_restricted_pages(url):
    common_paths = ['/admin', '/dashboard', '/settings', '/user/profile', '/api/secure', '/private']
    return [url + path for path in common_paths]

# Realizar pruebas de control de acceso
def perform_access_control_checks(url, cookies=None, headers=None):
    restricted_pages = extract_restricted_pages(url)
    for page in restricted_pages:
        response = test_access_control_with_auth(page, cookies=cookies, headers=headers)
        if response == 'vulnerable':
            damage = "El fallo de control de acceso permite a usuarios no autorizados acceder a áreas restringidas."
            protections = ["\n1. Implementar roles de acceso estrictos.", "\n2. Validar permisos antes de conceder acceso a recursos."]
            cwe = "CWE-284: Improper Access Control"
            vulnerabilities_detected.append(
                f"- Vulnerable: {page}\nDaño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\n")
            print(f"{Fore.RED}Vulnerable{Style.RESET_ALL}: {page}\nDaño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}")
        elif response == 'error':
            print(f"{Fore.YELLOW}Error en el servidor{Style.RESET_ALL}: {page}")
        else:
            print(f"{Fore.GREEN}Seguro{Style.RESET_ALL}: {page}")

# Función principal para iniciar el escaneo
def perform_access_control_checks_all(url, cookies=None, headers=None):
    print(f"{Fore.LIGHTBLUE_EX}--- Escaneo de Control de Acceso Defectuoso ---")
    perform_access_control_checks(url, cookies=cookies, headers=headers)

    internal_links = extract_internal_links(url)
    for link in internal_links:
        if link not in visited_urls:
            visited_urls.add(link)
            perform_access_control_checks(link, cookies=cookies, headers=headers)


# Función para generar el reporte
def generate_report():
    # Crear reporte si hay vulnerabilidades detectadas
    if vulnerabilities_detected:
        filename = f"Control de Acceso Defectuoso {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(report_directory, filename)
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, 'w') as file:
            file.write("<html><head><title>Reporte de Vulnerabilidades Críticas</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Acceso Defectuoso</h1>")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
            # Escribir cada vulnerabilidad en formato HTML
            for vulnerability in vulnerabilities_detected:
                file.write(f"<li><pre>{vulnerability}</pre></li>")
            # Cerrar las etiquetas HTML
            file.write("</ul></body></html>")
            with open(file_path, 'rb') as f:
                encrypted_data = cipher.encrypt(f.read())
            with open(file_path + ".enc", 'wb') as f:
                f.write(encrypted_data)

            print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")

    else:
        return print(f"\n{Fore.GREEN}No se detectaron vulnerabilidades.{Style.RESET_ALL}")

# Pruebas unitarias
class TestVulnerabilities(unittest.TestCase):
    def test_url_input(self):
        url = input("Ingrese la URL a analizar: ").strip()
        self.assertTrue(url.startswith("http://") or url.startswith("https://"), "La URL debe comenzar con 'http://' o 'https://'")

    def test_access_control_check(self):
        url = input("Ingrese la URL a analizar: ").strip()
        self.assertIn("http", url, "La URL debe contener 'http'")

# Ejecutar las pruebas unitarias
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # Aquí solicitamos la URL al usuario
    url = input("Ingrese la URL a analizar: ").strip()

    # Ejecutamos las funciones principales
    perform_access_control_checks_all(url)
    generate_report()
