import unittest
from unittest import mock
from bs4 import BeautifulSoup
import colorama
import os
import requests
from colorama import Fore, Style
from datetime import datetime
import hashlib
import base64
from cryptography.fernet import Fernet


colorama.init()

# Configuración de directorio de reportes
REPORT_DIR = "reportes_vulnerabilidades_Mejores_Practicas"
os.makedirs(REPORT_DIR, exist_ok=True)


def calculate_sri_hash(file_content, algorithm="sha384"):
    """Calcula el hash SRI del contenido descargado."""
    hash_function = hashlib.new(algorithm)
    hash_function.update(file_content)
    return f"{algorithm}-{base64.b64encode(hash_function.digest()).decode('utf-8')}"


def check_resource_integrity(resource_url, integrity):
    """Valida el atributo 'integrity' comparando el hash calculado."""
    try:
        response = requests.get(resource_url, timeout=10)
        response.raise_for_status()

        # Calcular el hash del contenido descargado
        calculated_hash = calculate_sri_hash(response.content)

        # Comparar hashes
        return integrity == calculated_hash

    except Exception as e:
        print(f"{Fore.YELLOW}Error al validar el recurso: {resource_url}. Detalle: {e}{Style.RESET_ALL}")
        return False


def analyze_page(url):
    """Analiza una página en busca de vulnerabilidades de SRI."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Asegurar la codificación UTF-8
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', src=True)
        links = soup.find_all('link', href=True, rel=lambda x: 'stylesheet' in x)

        vulnerabilities = []
        for tag in scripts + links:
            resource_url = tag.get('src') or tag.get('href')
            integrity = tag.get('integrity')

            if not integrity:
                vulnerabilities.append(f"Etiqueta: {tag.name}, Recurso: {resource_url}, Falta 'integrity'.")
            else:
                is_valid = check_resource_integrity(resource_url, integrity)
                if not is_valid:
                    vulnerabilities.append(f"Etiqueta: {tag.name}, Recurso: {resource_url}, 'integrity' no coincide.")

        return vulnerabilities

    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error en el servidor{Style.RESET_ALL}: {e}")
    except Exception as e:
        print(f"{Fore.YELLOW}Error inesperado{Style.RESET_ALL}: {e}")
    return []


def generate_report(url, vulnerabilities):
    """Genera un reporte en HTML con soporte UTF-8."""
    if vulnerabilities:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"SRI_Not_Implemented_{timestamp}.html"
        file_path = os.path.join(REPORT_DIR, file_name)
        key = Fernet.generate_key()
        cipher = Fernet(key)
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
            file.write("<h1 style='text-align:center;'>Reporte de SRI not Implemented</h1>")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>URL Analizada: {url}</p>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")

            for vulnerability in vulnerabilities:
                file.write(f"<li>{vulnerability}</li>")

            file.write("</ul></body></html>")

        with open(file_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(file_path + ".enc", 'wb') as f:
            f.write(encrypted_data)

        print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")

    else:
        return print(f"\n{Fore.GREEN}No se detectaron vulnerabilidades.{Style.RESET_ALL}")


def sri_not_implemented():
    """Solicita la URL al usuario y realiza el escaneo."""
    url = input("Ingrese la URL a analizar: ").strip()
    if not url.startswith("http"):
        print(f"{Fore.RED}Error: La URL debe comenzar con 'http' o 'https'.{Style.RESET_ALL}")
        return

    print(f"{Fore.LIGHTBLUE_EX}--- Escaneo de Subresource Integrity (SRI) ---{Style.RESET_ALL}")
    vulnerabilities = analyze_page(url)

    if vulnerabilities:
        print(Fore.LIGHTRED_EX + "Se detectaron vulnerabilidades:" + Style.RESET_ALL)
        for v in vulnerabilities:
            print(f"{Fore.RED}{v}{Style.RESET_ALL}")
        generate_report(url, vulnerabilities)
    else:
        print(Fore.LIGHTGREEN_EX + "No se detectaron vulnerabilidades." + Style.RESET_ALL)


# ---------------- PRUEBAS UNITARIAS ----------------
class TestSRIValidation(unittest.TestCase):

    def test_calculate_sri_hash(self):
        """Verifica que el hash SRI se calcule correctamente."""
        content = b"test content"
        expected_hash = calculate_sri_hash(content)
        self.assertTrue(expected_hash.startswith("sha384-"))

    def test_check_resource_integrity_valid(self):
        """Prueba la validación de integridad con un hash correcto."""
        content = b"test content"
        expected_hash = calculate_sri_hash(content)
        with unittest.mock.patch("requests.get") as mock_get:
            mock_get.return_value.content = content
            mock_get.return_value.status_code = 200
            self.assertTrue(check_resource_integrity("https://client.qa.powerstreet.cloud/script.js", expected_hash))

    def test_check_resource_integrity_invalid(self):
        """Prueba la validación de integridad con un hash incorrecto."""
        content = b"test content"
        different_hash = calculate_sri_hash(b"different content")
        with unittest.mock.patch("requests.get") as mock_get:
            mock_get.return_value.content = content
            mock_get.return_value.status_code = 200
            self.assertFalse(check_resource_integrity("https://client.qa.powerstreet.cloud/script.js", different_hash))

    def test_analyze_page_no_integrity(self):
        """Verifica que se detecte la falta de 'integrity' en recursos externos."""
        html_content = """<html><head></head><body>
            <script src="https://client.qa.powerstreet.cloud/script.js"></script>
            <link rel="stylesheet" href="https://client.qa.powerstreet.cloud/style.css">
        </body></html>"""
        with unittest.mock.patch("requests.get") as mock_get:
            mock_get.return_value.text = html_content
            mock_get.return_value.status_code = 200
            vulnerabilities = analyze_page("http://example.com")
            self.assertEqual(len(vulnerabilities), 2)

    def test_analyze_page_integrity_match(self):
        """Verifica que un recurso con 'integrity' correcto no se reporte como vulnerable."""
        correct_hash = calculate_sri_hash(b"test content")
        html_content = f"""<html><head></head><body>
            <script src="https://client.qa.powerstreet.cloud/script.js" integrity="{correct_hash}"></script>
        </body></html>"""
        with unittest.mock.patch("requests.get") as mock_get:
            mock_get.side_effect = [
                unittest.mock.Mock(text=html_content, status_code=200),
                unittest.mock.Mock(content=b"test content", status_code=200)
            ]
            vulnerabilities = analyze_page("https://client.qa.powerstreet.cloud")
            self.assertEqual(len(vulnerabilities), 0)


if __name__ == "__main__":
    sri_not_implemented()  # Ejecuta el análisis de SRI
    unittest.main()  # Ejecuta los tests
