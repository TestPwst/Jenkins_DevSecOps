import requests
import re
import os
from urllib.parse import urlparse, urljoin
from datetime import datetime
from colorama import init, Fore, Style

# Inicializar colorama
init()

# Definir el directorio donde se almacenarán los reportes
report_directory = "reportes_vulnerabilidades_Alta"

# Asegurarse de que el directorio existe
os.makedirs(report_directory, exist_ok=True)

# Generar nombre de archivo basado en la fecha y hora actual
name = f"Configuracion_Seguridad_Incorrecta{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"

# Crear la ruta completa del archivo
file_path = os.path.join(report_directory, name)

# Lista para almacenar vulnerabilidades detectadas
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
        print(f"{Fore.YELLOW}Error al intentar extraer enlaces en {url}: {e}{Style.RESET_ALL}")
    return internal_links

def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc

# Función para verificar configuraciones de seguridad
def perform_security_misconfiguration_checks(url):
    try:
        response = requests.get(url)
        print(f"{Fore.CYAN}Verificando la URL: {url} (HTTP {response.status_code}){Style.RESET_ALL}")
        if response.status_code == 200:
            headers = response.headers
            misconfigurations = []

            if "X-Content-Type-Options" not in headers:
                misconfigurations.append("Falta la cabecera X-Content-Type-Options (Protección contra ataques MIME).")
            if "Content-Security-Policy" not in headers:
                misconfigurations.append("Falta la cabecera Content-Security-Policy (Protección contra inyecciones).")
            if "X-Frame-Options" not in headers:
                misconfigurations.append("Falta la cabecera X-Frame-Options (Protección contra ataques de clickjacking).")
            if "Strict-Transport-Security" not in headers and urlparse(url).scheme == "https":
                misconfigurations.append("Falta la cabecera Strict-Transport-Security (HSTS para conexiones seguras).")
            if "Referrer-Policy" not in headers:
                misconfigurations.append("Falta la cabecera Referrer-Policy (Protección contra fugas de información referencial).")
            if "Permissions-Policy" not in headers:
                misconfigurations.append("Falta la cabecera Permissions-Policy (Control sobre permisos del navegador, como ubicación y cámara).")

            # Verificar la exposición de versiones
            server = headers.get("Server", "")
            if server and re.search(r"\d", server):
                misconfigurations.append(f"Exposición de la versión del servidor: {server} (Puede permitir enumeración de versiones vulnerables).")

            # Chequear si se utiliza HTTPS
            if urlparse(url).scheme != "https":
                misconfigurations.append("Conexión no segura (HTTP). Se recomienda usar HTTPS.")

            # Guardar vulnerabilidades detectadas
            if misconfigurations:
                damage = "Configuraciones inseguras pueden permitir ataques de inyección, secuestro de sesión o filtrado de datos."
                protections = [
                    "\n1. Implementar cabeceras de seguridad (CSP, X-Content-Type-Options, X-Frame-Options, etc.).",
                    "\n2. Utilizar HTTPS y configurar HSTS.",
                    "\n3. Evitar la exposición de versiones de servidor y configurar cabeceras correctamente."
                ]
                cwe = "CWE-16: Security Misconfiguration"
                vulnerabilities_detected.append(
                    f"- Configuración de seguridad incorrecta detectada en {url}\nDaño: {damage}\nPrevenciones: {', '.join(protections)}\nCWE: {cwe}\nDetalles: {'; '.join(misconfigurations)}\n")
                print(f"{Fore.RED}Vulnerabilidad de configuración de seguridad detectada en {url}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Configuración segura en {url}{Style.RESET_ALL}")

    except requests.RequestException as e:
        print(f"{Fore.YELLOW}Error al intentar verificar la URL: {url} - {e}{Style.RESET_ALL}")

    # Obtener y escanear enlaces internos
    internal_links = extract_internal_links(url)
    for link in internal_links:
        if link not in visited_urls:
            visited_urls.add(link)
            perform_security_misconfiguration_checks(link)

# Función principal que puede ser llamada desde otro archivo
def start_security_misconfiguration_scan(url):
    print(f"{Fore.LIGHTBLUE_EX}--- Escaneo de Configuración de Seguridad Incorrecta ---")
    perform_security_misconfiguration_checks(url)
    if vulnerabilities_detected:
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
            file.write("<h1 style='text-align:center;'>Reporte de Vulnerabilidades Alta</h1>")  #
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
