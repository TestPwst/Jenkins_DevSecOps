import requests
import re
import os
import unittest
from urllib.parse import urlparse, urljoin
from datetime import datetime
from requests.exceptions import RequestException, Timeout, ConnectionError
from cryptography.fernet import Fernet

# Configuración de reportes
directory = "reportes_vulnerabilidades_Critica"
os.makedirs(directory, exist_ok=True)


# Función para validar la URL
def validar_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc)


# Función para verificar vulnerabilidades de seguridad
def verificar_vulnerabilidades(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code not in {200, 403}:
            return []

        vulnerabilidades = []
        cabeceras = response.headers
        if 'Strict-Transport-Security' not in cabeceras:
            vulnerabilidades.append("Falta Strict-Transport-Security (HSTS).")
        if 'X-Content-Type-Options' not in cabeceras:
            vulnerabilidades.append("Falta X-Content-Type-Options.")
        if 'Content-Security-Policy' not in cabeceras:
            vulnerabilidades.append("Falta Content-Security-Policy.")

        patrones = [r'/backup', r'/admin/backup', r'/export', r'/db_dump', r'/download/backup',
                    r'\.(sql|bak|zip|rar|tar|7z)$']
        for pattern in patrones:
            if re.search(pattern, response.text):
                vulnerabilidades.append(f"Posible archivo expuesto: {pattern}")

        return vulnerabilidades
    except (RequestException, Timeout, ConnectionError) as e:
        return [f"Error de conexión: {e}"]


# Generar reporte encriptado
def generar_reporte(vulnerabilidades, url):
    if not vulnerabilidades:
        return f"\nNo se detectaron vulnerabilidades."

    file_name = f"Ransomware_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
    file_path = os.path.join(directory, file_name)
    key = Fernet.generate_key()
    cipher = Fernet(key)

    with open(file_path, 'w') as file:
        file.write("<html><head><title>Reporte de Vulnerabilidades Críticas</title></head><body>")
        file.write("=" * 150 + "\n\n")
        file.write("<h1 style='text-align:center;'>Reporte de Vulnerabilidades Críticas</h1>")
        file.write("=" * 150 + "\n\n")
        file.write(f"<p>URL Analizada: {url}</p>")
        file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
        # Escribir cada vulnerabilidad en formato HTML
        for vulnerability in vulnerabilidades:
            file.write(f"<li><pre>{vulnerability}</pre></li>")
        file.write("</ul></body></html>")

    with open(file_path, 'rb') as f:
        encrypted_data = cipher.encrypt(f.read())
    with open(file_path + ".enc", 'wb') as f:
        f.write(encrypted_data)

    return f"Reporte generado y encriptado en {file_path}.enc"


# Clase de prueba con unittest
class TestSeguridadWeb(unittest.TestCase):
    def test_vulnerabilidades(self):
        url = input("Ingresa la URL a escanear: ")
        self.assertTrue(validar_url(url), "URL inválida")
        vulnerabilidades = verificar_vulnerabilidades(url)
        resultado = generar_reporte(vulnerabilidades, url)
        print(resultado)
        self.assertIsInstance(vulnerabilidades, list)


if __name__ == "__main__":
    unittest.main()
