import requests
import re
import ssl
import socket
import os
from urllib.parse import urlparse
from datetime import datetime
from colorama import init, Fore, Style
import unittest
from unittest.mock import patch

# Inicializar colorama
init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Alta"
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"Reporte_Fallas_Criptograficas_ {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
file_path = os.path.join(report_directory, name)

# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []

# Función para verificar la configuración SSL/TLS
def check_ssl_config(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    context = ssl.create_default_context()

    try:
        with socket.create_connection((host, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cipher = ssock.cipher()
                protocol = ssock.version()  # Protocolo SSL/TLS

                # Verificar protocolos inseguros
                obsolete_protocols = ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1']
                if protocol in obsolete_protocols:
                    vulnerabilities_detected.append(
                        f"- Uso de protocolo obsoleto en {url}: {protocol}. Riesgo de interceptación de datos.\n")
                else:
                    print(f"{Fore.GREEN}Protocolo seguro detectado: {protocol}{Style.RESET_ALL}")

                # Verificar cifrados débiles
                weak_ciphers = ['3DES', 'RC4', 'DES', 'MD5', 'SHA-1']
                if any(cipher_name in cipher[0] for cipher_name in weak_ciphers):
                    vulnerabilities_detected.append(
                        f"- Cifrado débil en {url}: {cipher[0]}. Posible ataque de fuerza bruta o colisión.\n")

    except (ssl.SSLError, socket.error) as e:
        print(f"{Fore.YELLOW}Error al verificar SSL: {e}{Style.RESET_ALL}")

# Función para verificar encabezados de seguridad
def check_security_headers(url):
    headers_needed = {
        'Strict-Transport-Security': "CWE-523: Encabezado HTTP Strict Transport Security (HSTS) no detectado.",
        'Content-Security-Policy': "CWE-358: Content Security Policy no implementada.",
        'X-Content-Type-Options': "CWE-16: Protección contra MIME sniffing faltante."
    }

    try:
        response = requests.get(url)
        for header, message in headers_needed.items():
            if header not in response.headers:
                vulnerabilities_detected.append(f"- {message} en {url}\n")
            elif header == 'Strict-Transport-Security':
                hsts_header = response.headers.get(header, '')
                max_age_match = re.search(r'max-age=(\d+)', hsts_header)
                if max_age_match:
                    max_age = int(max_age_match.group(1))
                    if max_age < 31536000:
                        vulnerabilities_detected.append(f"- Configuración HSTS débil en {url}: max-age demasiado bajo.\n")
                else:
                    vulnerabilities_detected.append(f"- Configuración HSTS incorrecta en {url}.\n")

    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error al verificar encabezados de seguridad: {e}{Style.RESET_ALL}")

# Función para realizar las pruebas de fallas criptográficas
def perform_crypto_flaws_checks(url):
    vulnerabilities_detected.clear()  # Limpiar vulnerabilidades detectadas antes de cada ejecución
    check_ssl_config(url)
    check_security_headers(url)

    # Crear reporte si hay vulnerabilidades
    if vulnerabilities_detected:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>")
            file.write("<html lang='en'>")
            file.write("<head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Reporte de Vulnerabilidades Alta</title></head>")
            file.write("<body>")
            file.write("<h1 style='text-align:center;'>Reporte de Vulnerabilidades Alta</h1>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
            for vulnerability in vulnerabilities_detected:
                file.write(f"<li><pre>{vulnerability}</pre></li>")
            file.write("</ul></body></html>")

    else:
        print(f"{Fore.LIGHTGREEN_EX}No se detectaron vulnerabilidades.{Style.RESET_ALL}")

# Clase para pruebas
class TestCryptoFlawsChecks(unittest.TestCase):

    @patch('builtins.input', return_value='https://example.com')  # Usar un mock para el input
    def test_perform_crypto_flaws_checks(self, mock_input):
        # Probar la función principal
        url = mock_input()  # Recibir la URL de input (mocked)
        perform_crypto_flaws_checks(url)

        # Comprobamos que la lista de vulnerabilidades no está vacía
        self.assertIsInstance(vulnerabilities_detected, list, "Las vulnerabilidades deberían ser una lista.")
        if vulnerabilities_detected:
            self.assertTrue(len(vulnerabilities_detected) > 0, "Se deberían haber detectado vulnerabilidades.")

if __name__ == '__main__':
    unittest.main()
