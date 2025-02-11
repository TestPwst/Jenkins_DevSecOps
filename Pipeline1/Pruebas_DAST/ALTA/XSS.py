import unittest
from unittest.mock import patch
import requests
import re
import colorama
import os
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style
from datetime import datetime
import html  # Importar para escapar caracteres HTML

colorama.init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Alta"

# Asegurarse de que el directorio exista
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"XSS_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"

# Crear la ruta completa del archivo
file_path = os.path.join(report_directory, name)

# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []
visited_urls = set()


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
        print(f'{Fore.YELLOW}Error al extraer enlaces internos de {url}: {e}{Style.RESET_ALL}')
    return internal_links


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netnetloc


def perform_xss_checks_input(url, input_fields):
    vulnerability_title = "Cross-Site Scripting (XSS) en áreas de entrada"
    print(f'{Fore.BLUE}--- {vulnerability_title} ---{Style.RESET_ALL}')

    payloads = [
        "<script>alert('XSS')</script>",
        "><script>alert('XSS')</script>",
        "><img src=x onerror=alert('XSS')>",
        "><svg/onload=alert('XSS')>",
        "<img src='javascript:alert('XSS')'>",
        "javascript:alert('XSS')",
        "<iframe src='javascript:alert('XSS')'></iframe>",
        "</script><script>alert('XSS')</script>",
        "><img src=x onerror='alert('XSS')>",
        "><svg onload='alert('XSS')'>",
        "><body onload='alert('XSS')'>",
    ]

    for input_field in input_fields:
        vulnerable = False
        for payload in payloads:
            modified_input_field = re.sub(r'value\s*?=\s*?".*?"', f'value="{payload}"', input_field,
                                          flags=re.IGNORECASE)
            if payload in modified_input_field:
                vulnerable = True
                damage = f"Ejecutar scripts maliciosos en el navegador del usuario."
                protections = [f"\n1. Escapar caracteres especiales.", "\n2. Utilizar CSP.", "\n3. Validar entradas."]
                cwe = f"CWE-79: Neutralización incorrecta de la entrada durante la generación de páginas web ('Cross-site Scripting')"

                # Escapar el payload para que se vea correctamente en el HTML
                escaped_input_field = html.escape(modified_input_field)

                vulnerabilities_detected.append(
                    f"- Vulnerable: {escaped_input_field} \nen {url} payload: {escaped_input_field}\nDaño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\n")
                print(
                    f'{Fore.RED}Vulnerable{Style.RESET_ALL}: {escaped_input_field} \nen {url} payload: {escaped_input_field}\nDaño: {damage}\nPrevenciones: {", ".join(protections)}\nCWE: {cwe}')
                break
        if not vulnerable:
            print(f'{Fore.GREEN}Seguro{Style.RESET_ALL}: {input_field} en {url}')


def xss_scan(url):
    print(f"{Fore.LIGHTBLUE_EX}--- Escaneo de Cross Site Scripting ---")
    if url in visited_urls:
        return
    visited_urls.add(url)

    internal_links = extract_internal_links(url)
    print(f'Enlaces Internos en {url}:')
    for link in internal_links:
        print(f'- {link}')

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page_content = response.text

            # Imprimir contenido de los campos encontrados
            input_fields = re.findall(r'<input\s+[^>]*>', page_content, re.IGNORECASE)
            print(f'Campos de entrada encontrados: {input_fields}')
            textarea_fields = re.findall(r'<textarea[^>]*>.*?</textarea>', page_content, re.IGNORECASE | re.DOTALL)
            print(f'Campos de textarea encontrados: {textarea_fields}')

            perform_xss_checks_input(url, input_fields)
        else:
            print(
                f'{Fore.YELLOW}Error en la solicitud al URL: {url} - Código de estado: {response.status_code} - Mensaje: {response.reason}{Style.RESET_ALL}')
    except requests.RequestException as e:
        print(f'{Fore.YELLOW}Error en la solicitud al URL: {url} - {e}{Style.RESET_ALL}')

    if vulnerabilities_detected:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>")
            file.write("<html lang='en'>")
            file.write("<head>")
            file.write("<meta charset='UTF-8'>")
            file.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
            file.write("<title>Reporte de Vulnerabilidades Mejores Prácticas</title>")
            file.write("</head>")
            file.write("<body>")
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


# Test con unittest

class TestXSSScanner(unittest.TestCase):

    @patch('builtins.input', return_value='https://example.com')
    @patch('requests.get')  # Mocking the requests.get call
    def test_xss_scan(self, mock_get, mock_input):
        # Simula una respuesta exitosa de requests.get
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html><input type="text" value=""/></html>'  # HTML de ejemplo

        # Llamamos a la función para probar
        xss_scan(input())

        # Verificamos que las funciones relevantes se hayan llamado
        mock_input.assert_called_once_with()  # Verifica que el input se haya solicitado
        mock_get.assert_called_once_with('https://example.com', headers={"User-Agent": "Mozilla/5.0"})


if __name__ == '__main__':
    unittest.main()
