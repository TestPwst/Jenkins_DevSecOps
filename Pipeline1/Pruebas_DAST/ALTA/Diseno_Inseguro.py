import unittest
import requests
import re
import os
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style

# Inicializar colorama
init()

# Función para obtener la URL base
def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

# Función para verificar si la URL pertenece al mismo dominio
def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc

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
        print(f"{Fore.YELLOW}Error al intentar extraer enlaces en {url}: {e}{Style.RESET_ALL}")
    return internal_links

# Función para realizar las comprobaciones de diseño inseguro
def perform_insecure_design_checks(url, vulnerabilities_detected, visited_urls):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            input_fields = re.findall(r'<input.*?type=["\']text["\'].*?>', page_content, flags=re.IGNORECASE)
            for input_field in input_fields:
                vulnerable = False
                issues = [
                    "CSRF token no presente",
                    "Campos de entrada de contraseña con autocomplete habilitado",
                    "Campos de entrada sin validación adecuada"
                ]
                for issue in issues:
                    if "autocomplete" in input_field.lower() and "password" in input_field.lower():
                        vulnerable = True
                        damage = "Exposición de datos sensibles, riesgo de robo de credenciales."
                        protections = [
                            "\n1. Deshabilitar el autocompletado en campos de contraseña.",
                            "\n2. Implementar tokens CSRF en formularios sensibles.",
                            "\n3. Asegurar que todos los datos sean validados en el lado del servidor."
                        ]
                        cwe = "CWE-352: Cross-Site Request Forgery (CSRF)"
                        vulnerabilities_detected.append(
                            f"- Vulnerable: {input_field} en {url}\nDaño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\n")
                        break

            # Verificar cabeceras de seguridad
            security_headers = {
                "X-Frame-Options": "CWE-1021: Restricción inadecuada de capas o marcos de la interfaz de usuario renderizados.",
                "Content-Security-Policy": "CWE-693: Falla del mecanismo de protección.",
                "X-Content-Type-Options": "CWE-16: Configuración. Protección contra MIME sniffing faltante.",
                "Referrer-Policy": "CWE-200: Exposición de información confidencial a un actor no autorizado.",
                "Strict-Transport-Security": "CWE-319: Transmisión de información confidencial en texto claro.",
                "Permissions-Policy": "CWE-732: Asignación incorrecta de permisos para recursos críticos."
            }
            for header, cwe in security_headers.items():
                if header not in response.headers:
                    vulnerabilities_detected.append(
                        f"- Cabecera de seguridad ausente: {header} en {url}\nProtección recomendada: Configurar la cabecera {header} para mitigar ataques como clickjacking y MITM\nCWE: {cwe}\n"
                    )

    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error al intentar verificar la URL: {url} - {e}{Style.RESET_ALL}")

    # Obtener y escanear enlaces internos
    internal_links = extract_internal_links(url)
    for link in internal_links:
        if link not in visited_urls:
            visited_urls.add(link)
            perform_insecure_design_checks(link, vulnerabilities_detected, visited_urls)

# Función principal que recibe la URL como parámetro
def start_insecure_design_scan(url, vulnerabilities_detected, visited_urls):
    perform_insecure_design_checks(url, vulnerabilities_detected, visited_urls)

    return vulnerabilities_detected

# Clase de pruebas con unittest
class TestInsecureDesignScan(unittest.TestCase):

    def test_insecure_design_scan(self):
        url = input("Ingresa la URL a probar: ")  # Aquí se obtiene la URL desde input()

        # Lista para almacenar vulnerabilidades detectadas
        vulnerabilities_detected = []
        visited_urls = set()

        # Llamamos a la función que realiza el escaneo
        result = start_insecure_design_scan(url, vulnerabilities_detected, visited_urls)

        # Validación: Si se detectan vulnerabilidades, deberíamos tener algo en 'result'
        self.assertIsInstance(result, list)  # Debe devolver una lista de vulnerabilidades
        if result:
            print("Se han detectado vulnerabilidades:")
            for vulnerability in result:
                print(vulnerability)
        else:
            print("No se han detectado vulnerabilidades.")

if __name__ == "__main__":
    unittest.main()
