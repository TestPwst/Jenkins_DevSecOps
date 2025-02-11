import unittest
from unittest.mock import patch
import requests
import re
import colorama
import os
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style
from datetime import datetime
from cryptography.fernet import Fernet

# Aquí comenzamos a simular las funcionalidades de las funciones principales
# Inicializar colorama
colorama.init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Alta"

# Asegurarse de que el directorio existe
os.makedirs(report_directory, exist_ok=True)

# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []
visited_urls = set()  # Inicializar aquí


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
        else:
            print(f"{Fore.YELLOW}Código de respuesta HTTP {response.status_code} en {url}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f'{Fore.YELLOW}Error en el servidor al procesar {url}: {e}{Style.RESET_ALL}')
    return internal_links


# Función para obtener la URL base
def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


# Función para verificar si la URL es del mismo dominio
def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc


# Función para realizar las verificaciones de Path Traversal
def perform_path_traversal_checks(url):
    payloads = [
        '../../../etc/passwd', '../../etc/passwd', '/etc/passwd', '/proc/self/environ', '/../etc/passwd',
        '/../../../etc/passwd', '/../../../../etc/passwd', '/..%2f..%2f..%2f..%2fetc%2fpasswd',
        "../../windows/system32/drivers/etc/hosts",
        "../%2e%2e/%2e%2e/etc/passwd",
        "%2e%2e%2f%2e%2e%2fetc/passwd",
    ]
    for payload in payloads:
        test_url = f"{url}file?path={payload}"
        try:
            headers = {
                'Authorization': 'Bearer tu_token_aqui',
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.get(test_url, headers=headers, timeout=5)
            if response.status_code == 200:
                if 'root:x:' in response.text or '"127.0.0.1"' in response.text:
                    damage = ("Exposición de archivos sensibles del sistema, como /etc/passwd, "
                              "que puede permitir obtener información crítica o control del servidor.")
                    protections = [
                        "\n1. Validar y sanitizar todas las entradas del usuario.",
                        "\n2. No permitir rutas de archivo arbitrarias.",
                        "\n3. Usar rutas absolutas y proteger archivos sensibles del sistema."
                    ]
                    cwe = "CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')"
                    vulnerabilities_detected.append(
                        f"{Fore.LIGHTRED_EX}- Vulnerable: {test_url} con payload: {payload}\nDanio: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\n")
                    print(f'{Fore.RED}Vulnerable{Style.RESET_ALL}: {test_url} con payload: {payload}')
                else:
                    print(f'{Fore.GREEN}Seguro{Style.RESET_ALL}: {test_url} con payload: {payload}')
            elif response.status_code == 403:
                print(
                    f'{Fore.LIGHTYELLOW_EX}Acceso denegado: Código 403 en {test_url}. \nPuede requerir autenticación o ajustes en las cabeceras.{Style.RESET_ALL}')
            else:
                print(
                    f'{Fore.LIGHTYELLOW_EX}Código de respuesta HTTP {response.status_code} para {test_url}{Style.RESET_ALL}')
        except requests.RequestException as e:
            print(f'{Fore.YELLOW}No se pudo conectar: {test_url}: {e}{Style.RESET_ALL}')

    internal_links = extract_internal_links(url)
    for link in internal_links:
        if link not in visited_urls:
            visited_urls.add(link)
            perform_path_traversal_checks(link)


# Función que se ejecuta en el escaneo
def perform_path_transversal(url):
    print("--- Path Traversal ---")
    perform_path_traversal_checks(url)


def generate_report(url):
    if vulnerabilities_detected:
        filename = f"Camino_Traversal_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(report_directory, filename)
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>")
            file.write("<html lang='en'>")
            file.write("<head>")
            file.write("<meta charset='UTF-8'>")
            file.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
            file.write("<title>Reporte de Vulnerabilidades Alta</title>")
            file.write("</head>")
            file.write("<body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Camino Traversal</h1>")  #
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


# Test con unittest para verificar la función perform_path_transversal
class TestPathTraversal(unittest.TestCase):

    @patch('builtins.input', return_value='https://client.qa.powerstreet.cloud/')
    def test_perform_path_traversal(self, mock_input):
        url = input("Introduce una URL: ")  # Simula la entrada del usuario
        with patch('requests.get') as mock_get:
            # Simulamos la respuesta para una URL
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = 'root:x:'  # Simulamos una respuesta que contiene la vulnerabilidad
            perform_path_transversal(url)

            # Verificamos si se detectó una vulnerabilidad
            self.assertGreater(len(vulnerabilities_detected), 0, "No se detectaron vulnerabilidades")

    @patch('builtins.input', return_value='https://client.qa.powerstreet.cloud/')
    def test_no_vulnerabilities(self, mock_input):
        url = input("Introduce una URL: ")  # Simula la entrada del usuario
        with patch('requests.get') as mock_get:
            # Simulamos la respuesta para una URL no vulnerable
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = 'normal content'
            perform_path_transversal(url)

            # Verificamos si no se detectaron vulnerabilidades
            self.assertEqual(len(vulnerabilities_detected), 0, "Se detectaron vulnerabilidades cuando no deberían")


if __name__ == '__main__':
    unittest.main()