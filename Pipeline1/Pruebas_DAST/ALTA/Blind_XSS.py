import logging
import requests
import unittest
import os
from datetime import datetime
from cryptography.fernet import Fernet
import sys

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("Blind_XSS.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


class BlindXSSScanner:
    def __init__(self, url):
        self.url = url
        self.payloads = [
            "<script>alert('XSS')</script>",
            "'\"><script>alert('XSS')</script>",
            "javascript:alert('XSS')"
        ]
        self.vulnerabilities = []

    def test_xss(self):
        """Prueba vulnerabilidades Blind XSS en la URL."""
        logging.info(f"Escaneando URL: {self.url}")
        for payload in self.payloads:
            test_url = f"{self.url}?input={payload}"
            try:
                response = requests.get(test_url, timeout=10)
                if payload in response.text:
                    vulnerability = f"Blind XSS detectado en {test_url}"
                    self.vulnerabilities.append(vulnerability)
                    logging.warning(vulnerability)
            except requests.RequestException as e:
                logging.error(f"Error al hacer la petición: {e}")

    def generate_report(self):
        """Genera y encripta un reporte en HTML si se encuentran vulnerabilidades."""
        if not self.vulnerabilities:
            logging.info("No se detectaron vulnerabilidades XSS.")
            return "No se detectaron vulnerabilidades XSS."

        # Nombre del archivo con fecha y hora
        file_name = f"Blind_XSS_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(os.getcwd(), file_name)

        # Generar clave de cifrado
        key = Fernet.generate_key()
        cipher = Fernet(key)

        # Escribir reporte en HTML
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n")
            file.write("<title>Reporte de Vulnerabilidades Blind XSS</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Blind XSS</h1>")
            file.write("<hr>\n")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p><strong>URL Analizada:</strong> {self.url}</p>")
            file.write(f"<p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")

            for vuln in self.vulnerabilities:
                file.write(f"<li>{vuln}</li>")
            file.write("</ul></body></html>")

        # Encriptar reporte
        encrypted_file_path = file_path + ".enc"
        with open(file_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_data)

        logging.info(f"Reporte generado y encriptado en: {encrypted_file_path}")

        return f"Reporte generado y encriptado en {encrypted_file_path}"


class TestBlindXSSScanner(unittest.TestCase):
    def test_valid_url(self):
        """Prueba si la URL es válida."""
        scanner = BlindXSSScanner("https://client.qa.powerstreet.cloud")
        self.assertTrue(scanner.url.startswith("http"))

    def test_xss_payloads(self):
        """Verifica que los payloads existan."""
        scanner = BlindXSSScanner("https://client.qa.powerstreet.cloud")
        self.assertTrue(len(scanner.payloads) > 0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_url = sys.argv[1]
    else:
        input_url = input("Ingrese la URL a escanear: ").strip()

    if input_url.startswith(("http://", "https://")):
        scanner = BlindXSSScanner(input_url)
        scanner.test_xss()
        print(scanner.generate_report())
    else:
        logging.error("URL inválida. Asegúrate de incluir 'http://' o 'https://'.")
        print("URL inválida.")

    unittest.main(exit=False)
