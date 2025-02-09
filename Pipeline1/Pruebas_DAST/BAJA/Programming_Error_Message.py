import requests
import re
import os
import unittest
import sys
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style
from cryptography.fernet import Fernet

# Inicializar colorama
init()

# Definir el directorio donde se almacenarán los reportes
REPORT_DIR = "reportes_vulnerabilidades_Baja"
os.makedirs(REPORT_DIR, exist_ok=True)


def generate_report_name():
    return f"Programming_Error_Message_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"


def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_same_domain(url, base_url):
    return urlparse(url).netloc == urlparse(base_url).netloc


def extract_internal_links(url):
    """ Extrae enlaces internos dentro del mismo dominio. """
    internal_links = set()
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            base_url = get_base_url(url)
            links = re.findall(r'href=[\'"](.*?)[\'"]', response.text, re.IGNORECASE)
            for link in links:
                absolute_link = urljoin(base_url, link.strip())
                if is_same_domain(absolute_link, base_url):
                    internal_links.add(absolute_link)
    except requests.exceptions.RequestException:
        pass
    return internal_links


def check_programming_errors(url):
    """ Verifica si la URL contiene mensajes de error. """
    error_messages = ['syntaxerror', 'exception', 'identationerror', 'error', 'warning', 'fail', '404', '500', '400',
                      '403']
    try:
        response = requests.get(url, timeout=5)
        for error in error_messages:
            if error in response.text.lower():
                return {
                    "url": url,
                    "damage": "Exposición de información sensibleque puede ser utilizada por un atacante.",
                    "protection": "Configurar mensajes de error genéricosy registrar errores internamente.",
                    "cwe": "CWE-209:Information Exposure Through Error Message"
                }

    except requests.exceptions.RequestException:
        pass
    return None


def scan_url(url, visited_urls=None):
    """ Escanea la URL y sus enlaces internos. """
    if visited_urls is None:
        visited_urls = set()

    vulnerabilities = []

    if url in visited_urls:
        return vulnerabilities

    visited_urls.add(url)

    result = check_programming_errors(url)
    if result:
        vulnerabilities.append(result)
        print(f"{Fore.RED}Vulnerabilidad detectada en {url}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}No se encontraron vulnerabilidades en {url}{Style.RESET_ALL}")

    for link in extract_internal_links(url):
        vulnerabilities.extend(scan_url(link, visited_urls))

    return vulnerabilities


def save_report(vulnerabilities, url):
    """ Guarda el reporte en un archivo HTML si hay vulnerabilidades. """
    if vulnerabilities:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        file_name = generate_report_name()
        file_path = os.path.join(REPORT_DIR, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n")
            file.write("<title>Reporte de Vulnerabilidades Baja</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Programming Error Message</h1>")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>URL Analizada: {url}</p>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")
            for v in vulnerabilities:
                file.write(f"<li><pre>{v}</pre></li>")
            file.write("</ul></body></html>")

        with open(file_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(file_path + ".enc", 'wb') as f:
            f.write(encrypted_data)
        print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")
    else:
        print(Fore.LIGHTGREEN_EX + "No se detectaron vulnerabilidades." + Style.RESET_ALL)
        return None


def main():
    url = input("Ingrese la URL a analizar: ").strip()
    if not url.startswith("http"):
        print("URL inválida. Asegúrese de incluir 'http://' o 'https://'")
        return
    vulnerabilities = scan_url(url)
    save_report(vulnerabilities, url)


if __name__ == "__main__":
    main()
