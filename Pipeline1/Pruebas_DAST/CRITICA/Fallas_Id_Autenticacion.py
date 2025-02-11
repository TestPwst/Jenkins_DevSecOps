import requests
import re
import os
import unittest
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style
from unittest.mock import patch, MagicMock
from cryptography.fernet import Fernet


# Inicializar colorama
init()

# Definir directorio de reportes
report_directory = "reportes_vulnerabilidades_Critica"
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en fecha y hora
name = f"Fallas_Identificacion_Autenticacion_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
file_path = os.path.join(report_directory, name)

# Lista de vulnerabilidades detectadas
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
        print(f"{Fore.YELLOW}Error extrayendo enlaces en {url}: {e}{Style.RESET_ALL}")
    return internal_links


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc


# Función para verificar fallas de autenticación
def perform_authentication_flaws_checks(url):
    try:
        response = requests.get(url)
        print(f"{Fore.CYAN}Verificando {url} (HTTP {response.status_code}){Style.RESET_ALL}")

        if response.status_code == 200:
            page_content = response.text

            if re.search(r'<form.*?action=["\'].*?["\'].*?>', page_content, flags=re.IGNORECASE):
                if re.search(r'<input.*?name=["\'](username|email|user)["\']', page_content, flags=re.IGNORECASE) and \
                        re.search(r'<input.*?name=["\']password["\']', page_content, flags=re.IGNORECASE):
                    print(f"{Fore.YELLOW}Formulario de inicio de sesión encontrado en {url}{Style.RESET_ALL}")
                    # Probar fuerza bruta
                    # check_for_brute_force_protection(url)

            error_patterns = [r'Invalid username or password', r'Incorrect credentials', r'Login failed', r'authentication failed']
            for pattern in error_patterns:
                if re.search(pattern, page_content, flags=re.IGNORECASE):
                    vulnerabilities_detected.append(f"- Mensaje de error revelador en {url}: {pattern}\n")
                    print(f"{Fore.RED}Vulnerabilidad detectada en {url}: {pattern}{Style.RESET_ALL}")

            # Chequear contraseñas sin complejidad mínima en las políticas visibles
            check_password_complexity(page_content)

    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error en {url}: {e}{Style.RESET_ALL}")

    # Escaneo de enlaces internos limitado para evitar bucles infinitos
    internal_links = extract_internal_links(url)
    for link in list(internal_links)[:10]:  # Limitar enlaces a revisar
        if link not in visited_urls:
            visited_urls.add(link)
            perform_authentication_flaws_checks(link)


def check_password_complexity(page_content):
    # Comprobar si las políticas de contraseñas visibles son débiles
    weak_password_patterns = [
        r'password must be at least 4 characters',
        r'password should not exceed 8 characters',
        r'no special characters required',
        r'numeric passwords allowed'
    ]
    for pattern in weak_password_patterns:
        if re.search(pattern, page_content, flags=re.IGNORECASE):
            vulnerabilities_detected.append(
                f"- Políticas de contraseña débiles detectadas: {pattern}\n")
            print(f"{Fore.RED}Vulnerabilidad de complejidad de contraseña detectada: {pattern}{Style.RESET_ALL}")


# Función principal para iniciar escaneo en ambas URLs
def start_authentication_flaws_scan(url):
    print("--- Escaneo de Fallas de Identificación y Autenticación ---")
    perform_authentication_flaws_checks(url)

    if vulnerabilities_detected:
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n")
            file.write("<title>Reporte de Vulnerabilidades Critica</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Fallas de Identificación y Autenticación</h1>")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>URL Analizada: {url}</p>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
            for vulnerability in vulnerabilities_detected:
                file.write(f"<li><pre>{vulnerability}</pre></li>")
            file.write("</ul></body></html>")
        with open(file_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(file_path + ".enc", 'wb') as f:
            f.write(encrypted_data)

        print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")

    else:
        return print(f"\n{Fore.GREEN}No se detectaron vulnerabilidades.{Style.RESET_ALL}")


# 🔹 Solicitar las URLs al usuario 🔹
if __name__ == "__main__":
    url1 = input("Ingresa la primera URL a analizar: ")
    # url2 = input("Ingresa la segunda URL a analizar: ")
    start_authentication_flaws_scan(url1)


# ------------------ PRUEBAS UNITARIAS ------------------
# class TestAuthenticationFlaws(unittest.TestCase):
#
#     @patch('requests.get')
#     def test_extract_internal_links(self, mock_get):
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.text = '<a href="/internal">Enlace</a>'
#         url = "https://client.qa.powerstreet.cloud"
#         internal_links = extract_internal_links(url)
#         self.assertIn("https://client.qa.powerstreet.cloud/internal", internal_links)
#
#     @patch('requests.get')
#     def test_perform_authentication_flaws_checks(self, mock_get):
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.text = '<form action="/login"><input name="username"><input name="password"></form>'
#         url = "https://client.qa.powerstreet.cloud"
#         perform_authentication_flaws_checks(url)
#         self.assertTrue(any("Formulario de inicio de sesión encontrado" in v for v in vulnerabilities_detected))
#
#     @patch('requests.get')
#     def test_multiple_urls(self, mock_get):
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.text = "Página de prueba sin errores"
#         urls = ["https://client.qa.powerstreet.cloud", "https://client.assist.com.uy/"]
#         start_authentication_flaws_scan(urls)
#         self.assertTrue(len(vulnerabilities_detected) == 0)  # No se encontraron vulnerabilidades
#
#
# # Ejecutar las pruebas
# if __name__ == '__main__':
#     unittest.main()
