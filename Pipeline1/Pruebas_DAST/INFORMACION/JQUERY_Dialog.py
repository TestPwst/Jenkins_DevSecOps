import requests
import re
import os
import unittest
from datetime import datetime
import colorama
from colorama import Fore, Style

# Inicializar colorama
colorama.init(autoreset=True)

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Media"
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"jQuery_UI_Dialog_Vulnerabilities_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
file_path = os.path.join(report_directory, name)

# Lista global para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []


def check_jquery_ui_dialog_version(url):
    """
    Escanea la URL en busca de una versión vulnerable de jQuery UI Dialog.
    """
    vulnerability_title = "--- jQuery UI Dialog Version ---"
    print(f"--- {vulnerability_title} ---")

    try:
        url = url.strip()
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            page_content = response.text

            # Buscar versión de jQuery UI Dialog en la página
            version_match = re.search(r'jquery-ui-dialog\.js.*?(\d+\.\d+\.\d+)', page_content, re.IGNORECASE)
            if version_match:
                version = version_match.group(1)
                print(f"Versión detectada: {version} en {url}")

                # Lista de versiones vulnerables
                vulnerable_versions = ['1.12.0', '1.12.1']
                if version in vulnerable_versions:
                    damage = "Esta versión es vulnerable a ataques como Cross-Site Scripting (XSS)."
                    protections = [
                        "Actualizar jQuery UI Dialog a la última versión disponible.",
                        "Implementar controles de seguridad como Content Security Policy (CSP)."
                    ]
                    cwe = "CWE-79: Cross-site Scripting (XSS)"
                    vulnerabilities_detected.append(
                        f"- Vulnerable: jQuery UI Dialog versión {version} en {url}\n"
                        f"Daño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\n"
                    )
                    print(f"{Fore.RED}Vulnerable: {Style.RESET_ALL}jQuery UI Dialog versión {version} en {url}")
                else:
                    print(f"{Fore.GREEN}Seguro: {Style.RESET_ALL}jQuery UI Dialog versión {version} en {url}")
            else:
                print(f"{Fore.GREEN}Seguro: No se detectó la versión de jQuery UI Dialog {Style.RESET_ALL}en {url}")

        else:
            print(f"{Fore.YELLOW}Error al acceder a {url}: {response.status_code}{Style.RESET_ALL}")

    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error al realizar la solicitud: {e}{Style.RESET_ALL}")


def generate_html_report():
    """ Genera un archivo HTML con las vulnerabilidades detectadas. """
    if vulnerabilities_detected:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html><html lang='en'><head>")
            file.write("<meta charset='UTF-8'>")
            file.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
            file.write("<title>Reporte de Vulnerabilidades</title></head><body>")
            file.write("<h1 style='text-align:center;'>Reporte de Vulnerabilidades</h1>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")

            for vulnerability in vulnerabilities_detected:
                file.write(f"<li><pre>{vulnerability}</pre></li>")

            file.write("</ul></body></html>")
            print(f"{Fore.LIGHTRED_EX}Se detectaron vulnerabilidades.{Style.RESET_ALL}")
            print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado: {file_path}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTGREEN_EX}No se detectaron vulnerabilidades.{Style.RESET_ALL}")


import unittest
from unittest.mock import patch, MagicMock
from main import check_jquery_ui_dialog_version


class TestJQueryUIDialogScanner(unittest.TestCase):

    @patch("requests.get")
    def test_vulnerable_version_detected(self, mock_get):
        """ Verifica que se detecten versiones vulnerables de jQuery UI Dialog. """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<script src="jquery-ui-dialog.js?1.12.0"></script>'
        mock_get.return_value = mock_response

        check_jquery_ui_dialog_version("https://example.com")

        self.assertTrue(any("Vulnerable" in v for v in vulnerabilities_detected))

    @patch("requests.get")
    def test_safe_version_detected(self, mock_get):
        """ Verifica que las versiones seguras no se marquen como vulnerables. """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<script src="jquery-ui-dialog.js?1.13.2"></script>'
        mock_get.return_value = mock_response

        check_jquery_ui_dialog_version("https://example.com")

        self.assertFalse(any("Vulnerable" in v for v in vulnerabilities_detected))

    @patch("requests.get")
    def test_no_version_detected(self, mock_get):
        """ Verifica que cuando no se encuentra una versión, se marque como seguro. """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<script src="other-library.js"></script>'
        mock_get.return_value = mock_response

        check_jquery_ui_dialog_version("https://example.com")

        self.assertFalse(any("Vulnerable" in v for v in vulnerabilities_detected))

    @patch("requests.get")
    def test_http_error_handling(self, mock_get):
        """ Verifica que los errores HTTP sean manejados correctamente. """
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        check_jquery_ui_dialog_version("https://example.com")

        self.assertFalse(any("Vulnerable" in v for v in vulnerabilities_detected))


if __name__ == "__main__":
    unittest.main()


# Entrada del usuario
if __name__ == "__main__":
    url = input("Ingrese la URL a escanear: ").strip()
    check_jquery_ui_dialog_version(url)
    generate_html_report()

