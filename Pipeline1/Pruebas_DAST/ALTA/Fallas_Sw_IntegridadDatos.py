import unittest
from unittest.mock import patch
import requests
import re
import os
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style

# Inicializar colorama
init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Alta"
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"Fallas_Software_Integridad_Datos_ {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
file_path = os.path.join(report_directory, name)

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
        print(f"{Fore.YELLOW}Error al intentar extraer enlaces en {url}: {e}{Style.RESET_ALL}")
    return internal_links


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc


def perform_data_integrity_checks(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text

            # Chequeo de formularios sin validación
            input_fields = re.findall(r'<input.*?>', page_content, flags=re.IGNORECASE)
            for input_field in input_fields:
                if 'type="text"' in input_field or 'type="password"' in input_field:
                    vulnerability = {
                        'description': f"Campo sin validación detectado en {url}: {input_field}",
                        'cwe': "CWE-20: Validación de entrada insuficiente",
                        'protection': "Implementar validaciones del lado del servidor para todas las entradas del usuario.",
                        'damage': "Puede permitir que un atacante ingrese datos maliciosos."
                    }
                    vulnerabilities_detected.append(vulnerability)

            # Exposición de datos sensibles
            sensitive_data_exposure = re.findall(r'password|ssn|credit card|email', page_content, flags=re.IGNORECASE)
            if sensitive_data_exposure:
                vulnerability = {
                    'description': f"Exposición de datos sensibles detectada en {url}.",
                    'cwe': "CWE-200: Exposición de información sensible",
                    'protection': "Encriptar los datos sensibles y no exponerlos.",
                    'damage': "Puede resultar en la divulgación no autorizada de información."
                }
                vulnerabilities_detected.append(vulnerability)

            # Validar uso de HTTPS
            if urlparse(url).scheme != "https":
                vulnerability = {
                    'description': f"Conexión no segura (HTTP) detectada en {url}.",
                    'cwe': "CWE-319: Uso de transporte inseguro",
                    'protection': "Asegurar el uso de HTTPS.",
                    'damage': "La falta de cifrado expone los datos."
                }
                vulnerabilities_detected.append(vulnerability)

    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error al intentar verificar la URL: {url} - {e}{Style.RESET_ALL}")

    # Obtener y escanear enlaces internos
    internal_links = extract_internal_links(url)
    for link in internal_links:
        if link not in visited_urls:
            visited_urls.add(link)
            perform_data_integrity_checks(link)


def start_data_integrity_scan(url):
    global vulnerabilities_detected
    vulnerabilities_detected = []  # Reseteamos la lista de vulnerabilidades
    perform_data_integrity_checks(url)
    if vulnerabilities_detected:
        with open(file_path, 'w') as file:
            file.write("<html><head><title>Reporte de Vulnerabilidades Alta</title></head><body>")
            file.write("<h1>Reporte de Vulnerabilidades Alta</h1>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
            for vulnerability in vulnerabilities_detected:
                file.write(f"<li><strong>{vulnerability['description']}</strong></li>")
                file.write(f"<ul><li><b>CWE:</b> {vulnerability['cwe']}</li>")
                file.write(f"<li><b>Protección recomendada:</b> {vulnerability['protection']}</li>")
                file.write(f"<li><b>Daño potencial:</b> {vulnerability['damage']}</li></ul>")
            file.write("</ul></body></html>")


# Clase de pruebas con unittest
class TestDataIntegrityScan(unittest.TestCase):

    @patch('builtins.input', return_value='https://client.qa.powerstreet.cloud/')  # Simula el input de la URL
    @patch('requests.get')
    def test_data_integrity_scan(self, mock_get, mock_input):
        # Simulamos una respuesta de HTTP exitosa
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html><input type="text" name="username"></html>'

        # Ejecutamos el escaneo con la URL proporcionada por el input simulado
        start_data_integrity_scan(input())  # Se utiliza el input simulado

        # Verificar que las vulnerabilidades fueron detectadas
        self.assertGreater(len(vulnerabilities_detected), 0)
        self.assertIn('Campo sin validación detectado', vulnerabilities_detected[0]['description'])


if __name__ == '__main__':
    unittest.main()
