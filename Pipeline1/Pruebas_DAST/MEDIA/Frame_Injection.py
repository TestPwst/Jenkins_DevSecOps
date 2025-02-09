import requests
import os
from datetime import datetime
import colorama
from colorama import Fore, Style
import unittest
from unittest.mock import patch, MagicMock

colorama.init()

# Directorio de reportes
REPORT_DIRECTORY = "reportes_vulnerabilidades_Media"
os.makedirs(REPORT_DIRECTORY, exist_ok=True)

# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []


def check_frame_injection(url):
    """
    Verifica si una URL es vulnerable a Frame Injection (Clickjacking)
    """
    global vulnerabilities_detected
    vulnerabilities_detected = []  # Reset de vulnerabilidades detectadas

    try:
        response = requests.get(url)
        if response.status_code == 200:
            headers = response.headers
            if 'X-Frame-Options' not in headers or headers['X-Frame-Options'].upper() not in ['DENY', 'SAMEORIGIN']:
                damage = "El daño puede incluir ataques de clickjacking..."
                protections = ["Configurar 'X-Frame-Options' en 'DENY' o 'SAMEORIGIN'.",
                               "Usar 'Content-Security-Policy: frame-ancestors'."]
                cwe = "CWE-1021: Improper Restriction of Rendered UI Layers or Frames"
                cve = "No disponible"

                vulnerabilities_detected.append({
                    "url": url,
                    "damage": damage,
                    "protections": protections,
                    "cwe": cwe,
                    "cve": cve
                })

                print(f"\n{Fore.YELLOW}Título de la Vulnerabilidad:{Style.RESET_ALL} Frame Injection")
                print(f"{Fore.RED}Vulnerabilidad detectada{Style.RESET_ALL}: {url}")
            else:
                print(f"{Fore.GREEN}Seguro:{Style.RESET_ALL} No se detectaron problemas en {url}")
        else:
            print(f"Error: No se pudo acceder a {url} (Código: {response.status_code})")

    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")


def generate_report():
    """
    Genera un archivo HTML si se detectan vulnerabilidades
    """
    if vulnerabilities_detected:
        file_name = f"Frame_Injection_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(REPORT_DIRECTORY, file_name)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n")
            file.write("<title>Reporte de Vulnerabilidades Media</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Frame Injection</h1>")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>URL Analizada: {url}</p>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")

            for vuln in vulnerabilities_detected:
                file.write(f"<li><b>URL:</b> {vuln['url']}<br>")
                file.write(f"<b>Daño:</b> {vuln['damage']}<br>")
                file.write(f"<b>Prevenciones:</b> {', '.join(vuln['protections'])}<br>")
                file.write(f"<b>CWE:</b> {vuln['cwe']}<br>")
                file.write(f"<b>CVE:</b> {vuln['cve']}</li><br><br>")

            file.write("</ul></body></html>")

        with open(file_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(file_path + ".enc", 'wb') as f:
            f.write(encrypted_data)

        print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")

    else:
        return print(f"\n{Fore.GREEN}No se detectaron vulnerabilidades.{Style.RESET_ALL}")


if __name__ == "__main__":
    url = input("Ingrese la URL a analizar: ")
    check_frame_injection(url)
    generate_report()


class TestFrameInjection(unittest.TestCase):

    @patch("requests.get")
    def test_vulnerable_frame_injection(self, mock_get):
        """Prueba si la función detecta la vulnerabilidad cuando falta 'X-Frame-Options'."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}  # No tiene 'X-Frame-Options'
        mock_get.return_value = mock_response

        check_frame_injection("https://client.assist.com.uy/")

        self.assertEqual(len(vulnerabilities_detected), 1)
        self.assertIn("client.assist.com.uy/", vulnerabilities_detected[0]["url"])

    @patch("requests.get")
    def test_safe_site(self, mock_get):
        """Prueba si la función reconoce un sitio seguro con 'X-Frame-Options'."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'X-Frame-Options': 'DENY'}
        mock_get.return_value = mock_response

        check_frame_injection("https://client.assist.com.uy/")

        self.assertEqual(len(vulnerabilities_detected), 0)

    @patch("requests.get")
    def test_http_error(self, mock_get):
        """Prueba si maneja errores de HTTP correctamente."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        check_frame_injection("https://client.assist.com.uy/")

        self.assertEqual(len(vulnerabilities_detected), 0)

    @patch("requests.get", side_effect=requests.RequestException("Connection error"))
    def test_request_exception(self, mock_get):
        """Prueba si maneja excepciones de conexión."""
        check_frame_injection("https://client.assist.com.uy/")

        self.assertEqual(len(vulnerabilities_detected), 0)


if __name__ == '__main__':
    unittest.main()
