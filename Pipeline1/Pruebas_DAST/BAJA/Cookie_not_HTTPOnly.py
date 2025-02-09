import requests
import os
from datetime import datetime
import colorama
from colorama import Fore, Style
from cryptography.fernet import Fernet

colorama.init()

# Definir el directorio donde se almacenarán los reportes
REPORT_DIRECTORY = "reportes_vulnerabilidades_Baja"
os.makedirs(REPORT_DIRECTORY, exist_ok=True)


def check_cookie_security(url):
    """
    Verifica las cookies en la URL dada y devuelve una lista de vulnerabilidades detectadas.
    """
    vulnerabilities_detected = []

    try:
        response = requests.get(url)
        cookies = response.headers.get('Set-Cookie', '')

        # Verificar cookies sin la bandera HttpOnly
        http_only_cookies = [cookie for cookie in cookies.split(';') if 'HttpOnly' not in cookie]
        if http_only_cookies:
            vulnerabilities_detected.append({
                "tipo": "Cookies sin la bandera HttpOnly",
                "cookie": http_only_cookies[0],
                "cwe": "CWE-1004: Insecure Cookie Handling"
            })
            print(f'{Fore.RED}Vulnerable: Cookies sin HttpOnly{Style.RESET_ALL} -> {http_only_cookies[0]}')

        # Verificar cookies sin la bandera Secure
        secure_cookies = [cookie for cookie in cookies.split(';') if 'Secure' not in cookie]
        if secure_cookies:
            vulnerabilities_detected.append({
                "tipo": "Cookies sin la bandera Secure",
                "cookie": secure_cookies[0],
                "cwe": "CWE-1004: Insecure Cookie Handling"
            })
            print(f'{Fore.RED}Vulnerable: Cookies sin Secure{Style.RESET_ALL} -> {secure_cookies[0]}')

        # Verificar cookies sin la bandera SameSite
        same_site_cookies = [cookie for cookie in cookies.split(';') if 'SameSite' not in cookie]
        if same_site_cookies:
            vulnerabilities_detected.append({
                "tipo": "Cookies sin la bandera SameSite",
                "cookie": same_site_cookies[0],
                "cwe": "CWE-1004: Insecure Cookie Handling"
            })
            print(f'{Fore.RED}Vulnerable: Cookies sin SameSite{Style.RESET_ALL} -> {same_site_cookies[0]}')

        if not vulnerabilities_detected:
            print(f'{Fore.GREEN}Seguro{Style.RESET_ALL}: No se detectaron vulnerabilidades en las cookies.')

    except requests.RequestException as e:
        print(f'{Fore.YELLOW}Error en el servidor{Style.RESET_ALL}: {e}')

    return vulnerabilities_detected


def generate_html_report(vulnerabilities_detected, url):
    """
    Genera un reporte en HTML si se detectaron vulnerabilidades.
    """
    if vulnerabilities_detected:
        filename = f"Cookie_Security_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(REPORT_DIRECTORY, filename)
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n")
            file.write("<title>Reporte de Vulnerabilidades Baja</title></head><body>")
            file.write("=" * 150 + "\n\n")
            file.write("<h1 style='text-align:center;'>Reporte de Cookie not Marked as HTTPOnly</h1>")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>URL Analizada: {url}</p>")
            file.write(f"<p>Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            file.write("<h2>Vulnerabilidades Detectadas</h2><ul>")

            for vuln in vulnerabilities_detected:
                file.write(
                    f"<li><strong>{vuln['tipo']}</strong><br>Cookie: {vuln['cookie']}<br>CWE: {vuln['cwe']}</li>\n")

            file.write("</ul>\n</body>\n</html>\n")

        with open(file_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        with open(file_path + ".enc", 'wb') as f:
            f.write(encrypted_data)

        print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")

    else:
        return print(f"\n{Fore.GREEN}No se detectaron vulnerabilidades.{Style.RESET_ALL}")


def main():
    url = input("Ingrese la URL a analizar: ")
    vulnerabilities = check_cookie_security(url)
    generate_html_report(vulnerabilities, url)


if __name__ == "__main__":
    main()
