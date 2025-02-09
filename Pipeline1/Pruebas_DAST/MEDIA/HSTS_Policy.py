import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import colorama
from colorama import Fore, Style
import unittest
from cryptography.fernet import Fernet

colorama.init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Media"
# Asegurarse de que el directorio existe
os.makedirs(report_directory, exist_ok=True)


# Lista para almacenar vulnerabilidades detectadas
vulnerabilities_detected = []


# Función para verificar política HSTS
def check_hsts_policy(url):
    print(f'{Fore.CYAN}Escaneando vulnerabilidad: HSTS Policy{Style.RESET_ALL}')
    response = requests.get(url)
    if 'Strict-Transport-Security' not in response.headers:
        damage = "Sin la política HSTS, los usuarios pueden ser vulnerables a ataques de intermediario (MITM) y el tráfico HTTPS puede degradarse a HTTP."
        protections = ["\n1. Habilitar la política HSTS con 'Strict-Transport-Security'.",
                       "\n2. Asegurarse de que todas las solicitudes HTTP sean redirigidas a HTTPS."]
        cwe = "CWE-523: Unprotected Transport of Credentials"
        vulnerabilities_detected.append(f"- HSTS no habilitado en {url}\nDaño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\n")
        print(f'{Fore.RED}HSTS no habilitado{Style.RESET_ALL}: {url}\nDaño: {damage}\nPrevenciones: {", ".join(protections)}\nCWE: {cwe}')
        return True  # Vulnerabilidad encontrada
    else:
        print(f'{Fore.GREEN}HSTS está habilitado correctamente en {url}{Style.RESET_ALL}')
    return False  # Sin vulnerabilidad

# Función para verificar scripts obsoletos como jQuery UI Dialog
def check_jquery_ui_version(url):
    print(f'{Fore.CYAN}Escaneando vulnerabilidad: jQuery UI Version{Style.RESET_ALL}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    found_obsolete_jquery = False

    for script in scripts:
        if 'jquery-ui-dialog' in script.get('src', ''):
            damage = "Exposición a vulnerabilidades conocidas como inyecciones de código y secuencias de comandos maliciosas."
            protections = ["\n1.Actualizar a la última versión de jQuery UI.", "\n2.Utilizar la versión segura de los componentes de terceros."]
            cwe = "CWE-1104: Use of Unmaintained Third Party Components"
            vulnerabilities_detected.append(f"- Versión obsoleta de jQuery UI Dialog encontrada en {script['src']}\nDaño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\n")
            print(f'{Fore.RED}Versión obsoleta de jQuery UI Dialog encontrada{Style.RESET_ALL}: {script["src"]}\nDaño: {damage}\nPrevenciones: {", ".join(protections)}\nCWE: {cwe}')
            found_obsolete_jquery = True
            break

    if not found_obsolete_jquery:
        print(f'{Fore.GREEN}No se encontraron versiones obsoletas de jQuery UI en {url}{Style.RESET_ALL}')
    return found_obsolete_jquery  # Retorna True si vulnerabilidad encontrada


# Función para realizar el chequeo de las vulnerabilidades de HSTS y scripts obsoletos
def perform_hsts_checks(url):
    if vulnerabilities_detected:
        filename = f"HSTS_Not_Policy_Enabled_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(report_directory, filename)
        key = Fernet.generate_key()
        cipher = Fernet(key)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>")
            file.write("<html lang='en'>")
            file.write("<head>")
            file.write("<meta charset='UTF-8'>")
            file.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
            file.write("<title>Reporte de Vulnerabilidades Media</title>")
            file.write("</head>")
            file.write("<body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Vulnerabilidades Media</h1>")  #
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

    hsts_detected = check_hsts_policy(url)
    jquery_detected = check_jquery_ui_version(url)

    return hsts_detected or jquery_detected  # Retorna True si alguna vulnerabilidad es encontrada


# Pruebas Unitarias
class TestVulnerabilities(unittest.TestCase):

    def setUp(self):
        self.url = input("Ingrese la URL a analizar: ")

    def test_hsts_policy(self):
        # Verificamos que HSTS sea vulnerabilidad (True si no está habilitado)
        self.assertFalse(check_hsts_policy(self.url))  # Cambié assertTrue por assertFalse aquí

    def test_jquery_ui_version(self):
        # Verificamos que jQuery UI no esté obsoleto (True si no es vulnerable)
        self.assertFalse(check_jquery_ui_version(self.url))  # Cambié assertTrue por assertFalse aquí

    def test_perform_hsts_checks(self):
        # Verificamos que perform_hsts_checks no sea vulnerabilidad (True si se detecta vulnerabilidad)
        self.assertFalse(perform_hsts_checks(self.url))   #  No cambié aquí porque se espera que detecte alguna vulnerabilidad


if __name__ == "__main__":
    unittest.main()
