import re
import requests
import os
from datetime import datetime
import colorama
from colorama import Fore, Style
import unittest

colorama.init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Informacion"

# Asegurarse de que el directorio existe
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"Vulnerabilidades_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"

# Crear la ruta completa del archivo
file_path = os.path.join(report_directory, name)


# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []

# Lista de versiones vulnerables de jQuery UI Tooltip
vulnerable_versions = ['1.12.1', '1.12.0', '1.11.4']  # Ejemplos, actualiza según vulnerabilidades conocidas


def check_jquery_ui_tooltip_version(url):
    print("--- jQuery UI Tooltip Version ---")

    try:
        # Realizar la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx

        # Buscar versiones de jQuery UI Tooltip en el contenido
        tooltip_version_pattern = r'jquery-ui-tooltip.*?v?(\d+\.\d+\.\d+)'
        matches = re.findall(tooltip_version_pattern, response.text, re.IGNORECASE)

        if matches:
            found_vulnerabilities = set()
            # Verificar si alguna versión encontrada está en la lista de vulnerables
            for version in matches:
                if version in vulnerable_versions:
                    found_vulnerabilities.add(version)

            if found_vulnerabilities:
                vulnerabilities_detected.append(
                    f"---JQUERY UI TOOLTIP VERSION---\n"
                    f"Versión desactualizada de jQuery UI Tooltip encontrada en: {url}\n"
                    f"Versión(es) vulnerable(s) encontrada(s): {', '.join(found_vulnerabilities)}\n"
                    f"Daño Potencial: La explotación de vulnerabilidades conocidas en versiones antiguas puede permitir a los atacantes comprometer la seguridad de la aplicación, afectar su funcionalidad o robar información.\n"
                    f"Protección: \n1.Actualiza a la última versión de jQuery UI Tooltip. \n2.Consulta el changelog y las notas de versión para conocer las actualizaciones de seguridad y correcciones de errores.\n"
                    f"CWE-1035: Injection of Sensitive Information into Logs\n"
                    f"Contenido de la página donde se encontró la versión:\n"
                    f"{response.text[:500]}\n"
                )
                print(
                    f'{Fore.RED}Vulnerabilidad detectada{Style.RESET_ALL}: {url} - Versión(es) vulnerable(s) encontrada(s): {", ".join(found_vulnerabilities)}')
            else:
                print(f'{Fore.GREEN}Seguro: No se detectaron versiones vulnerables {Style.RESET_ALL}en {url}')
        else:
            print(f'{Fore.GREEN}Seguro: No se encontraron versiones de jQuery UI Tooltip {Style.RESET_ALL}en {url}')

    except requests.RequestException as e:
        print(f'{Fore.YELLOW}Error al realizar la solicitud{Style.RESET_ALL}: {e}')


def generate_report():
    # Solo crear archivo si se detectaron vulnerabilidades
    if vulnerabilities_detected:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>")
            file.write("<html lang='en'>")
            file.write("<head>")
            file.write("<meta charset='UTF-8'>")
            file.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
            file.write("<title>Reporte de Vulnerabilidades Informacion</title>")
            file.write("</head>")
            file.write("<body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Vulnerabilidades Informacion</h1>")  #
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


def run_tests_tooltip(url):
    check_jquery_ui_tooltip_version(url)
    generate_report()


class TestVulnerabilitiesDetection(unittest.TestCase):

    def test_vulnerabilities_detection(self):
        url = input("Introduce la URL para verificar vulnerabilidades: ")
        run_tests_tooltip(url)

        # Verificar si alguna vulnerabilidad fue detectada
        self.assertTrue(vulnerabilities_detected, "No se detectaron vulnerabilidades.")
        print("Vulnerabilidades detectadas:", vulnerabilities_detected)

if __name__ == '__main__':
    unittest.main()
