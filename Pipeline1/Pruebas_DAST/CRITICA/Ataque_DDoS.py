import requests
import threading
import os
import time
from datetime import datetime
from colorama import Fore, Style, init
from collections import Counter
import unittest
import re
from cryptography.fernet import Fernet

# Inicializar colorama
init()

# Configurar directorio de reportes
report_directory = "reportes_vulnerabilidades_Critica"
os.makedirs(report_directory, exist_ok=True)

# Contador de estadísticas
stats = {"success": 0, "server_errors": 0, "client_errors": 0, "timeouts": 0, "average_response_time": []}
patterns = Counter()  # Para detectar patrones de respuesta
vulnerabilities_detected = []


# Función para enviar solicitudes con validación de patrones
def send_request(url, thread_id):
    global response_time
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response_time = time.time() - start_time

        # Validar respuesta
        if response.status_code == 200:
            stats["success"] += 1
            patterns["success"] += 1
            print(f'{Fore.GREEN}✓ Ataque DDoS - Solicitud {thread_id}: {response_time:.2f}s - Exitosa{Style.RESET_ALL}')
        elif 500 <= response.status_code < 600:
            stats["server_errors"] += 1
            patterns[f"server_error_{response.status_code}"] += 1
            print(f'{Fore.YELLOW}⚠ Ataque DDoS - Solicitud {thread_id}: {response_time:.2f}s - Error del servidor '
                  f'({response.status_code}){Style.RESET_ALL}')
        elif 400 <= response.status_code < 500:
            stats["client_errors"] += 1
            patterns[f"client_error_{response.status_code}"] += 1
            print(f'{Fore.RED}✗ Ataque DDoS - Solicitud {thread_id}: {response_time:.2f}s - Error del cliente ({response.status_code}){Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}✗ Ataque DDoS - Solicitud {thread_id}: Respuesta inesperada{Style.RESET_ALL}')

        # Almacenar tiempo de respuesta
        stats["average_response_time"].append(response_time)

    except requests.exceptions.Timeout:
        stats["timeouts"] += 1
        patterns["timeouts"] += 1
        print(f'{Fore.RED}✗ Ataque DDoS - Solicitud {thread_id}: Tiempo de espera agotado{Style.RESET_ALL}')
    except requests.exceptions.RequestException as e:
        vulnerabilities_detected.append(f"Error: Solicitud {thread_id} fallida con error {e}.")
        print(f'{Fore.RED}✗ Ataque DDoS - Solicitud {thread_id}: Fallida - Error {e}{Style.RESET_ALL}')


# Función para realizar el chequeo DDoS con control de frecuencia
def perform_ddos_check(url):
    threads = []
    num_requests = 100
    interval = 0.1  # Intervalo entre solicitudes en segundos

    print(f"{Fore.LIGHTBLUE_EX}--- Iniciando prueba de ataque DDoS ---{Style.RESET_ALL}")

    for i in range(num_requests):
        thread = threading.Thread(target=send_request, args=(url, i))
        threads.append(thread)
        thread.start()
        time.sleep(interval)  # Introducir pausa entre solicitudes

    for thread in threads:
        thread.join()

    # Calcular estadísticas promedio
    if stats["average_response_time"]:
        stats["average_response_time"] = sum(stats["average_response_time"]) / len(stats["average_response_time"])


# Clasificar impacto con base en patrones
def classify_impact():
    total_errors = stats["server_errors"] + stats["timeouts"]
    error_rate = total_errors / (stats["success"] + total_errors) if total_errors else 0

    if error_rate > 0.5:
        impact = f'{Fore.RED}Crítico: El servidor es altamente vulnerable a DDoS.{Style.RESET_ALL}'
    elif 0.2 <= error_rate <= 0.5:
        impact = f'{Fore.YELLOW}Moderado: El servidor muestra vulnerabilidad a DDoS.{Style.RESET_ALL}'
    else:
        impact = f'{Fore.GREEN}Bajo: El servidor tiene buena protección contra DDoS.{Style.RESET_ALL}'
    return impact


# Función que se usará en el input para capturar la URL
def get_url_from_input():
    return input("Por favor, ingresa la URL para la prueba de ataque DDoS: ")


# Generar reporte HTML solo si se detectan vulnerabilidades críticas
def generate_report():
    if vulnerabilities_detected:
        name = f"Ataque_DDoS_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
        file_path = os.path.join(report_directory, name)
        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(file_path, 'w') as file:
            # Cabecera HTML
            file.write(
                f"<!DOCTYPE html>\n<html lang='es'>\n<head>\n<meta charset='UTF-8'>\n<title>Reporte DDoS</title>\n")
            file.write("<style>\nbody { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }\n")
            file.write("h1 { color: #333; }\ntable { width: 100%; border-collapse: collapse; margin-top: 20px; }\n")
            file.write("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n")
            file.write("th { background-color: #f2f2f2; }\n</style>\n</head>\n<body>\n")

            # Título y descripción
            file.write("=" * 150 + "\n\n")
            file.write(f"<h1>Reporte de Ataque DDoS</h1>\n")
            file.write("=" * 150 + "\n\n")
            file.write(f"<p>Reporte generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n")
            file.write("<p>Para más información sobre ataques DDoS, consulte: <a href='https://owasp.org/www-community/"
                       "attacks/Denial_of_Service' target='_blank'>OWASP - Denial of Service</a></p>\n")

            # Resultados del ataque DDoS
            file.write("<h2>Resultados del ataque DDoS</h2>\n")
            file.write("<table>\n<tr><th>Descripción</th><th>Detalle</th></tr>\n")
            for vulnerability in vulnerabilities_detected:
                file.write(f"<tr><td>{vulnerability}</td><td>Detectado</td></tr>\n")
            file.write("</table>\n")

            # Estadísticas
            file.write("<h2>Estadísticas</h2>\n")
            file.write("<table>\n<tr><th>Estadística</th><th>Valor</th></tr>\n")
            file.write(f"<tr><td>Solicitudes exitosas</td><td>{stats['success']}</td></tr>\n")
            file.write(f"<tr><td>Errores del servidor</td><td>{stats['server_errors']}</td></tr>\n")
            file.write(f"<tr><td>Errores del cliente</td><td>{stats['client_errors']}</td></tr>\n")
            file.write(f"<tr><td>Solicitudes fallidas por tiempo de espera</td><td>{stats['timeouts']}</td></tr>\n")
            file.write(
                f"<tr><td>Tiempo promedio de respuesta</td><td>{stats['average_response_time']:.2f} segundos</td></tr>\n")
            file.write("</table>\n")

            # Impacto
            impact = classify_impact()
            file.write(f"<h2>Impacto</h2>\n<p>{impact}</p>\n")

            # Cierre del HTML
            file.write("</body>\n</html>")
            with open(file_path, 'rb') as f:
                encrypted_data = cipher.encrypt(f.read())
            with open(file_path + ".enc", 'wb') as f:
                f.write(encrypted_data)

            print(f"{Fore.LIGHTMAGENTA_EX}Reporte generado y encriptado en {file_path}.enc{Style.RESET_ALL}")

    else:
        return print(f"\n{Fore.GREEN}No se detectaron vulnerabilidades.{Style.RESET_ALL}")


# Función para limpiar ANSI antes de comparar en unittest
def remove_ansi(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)


class TestDDoSDetection(unittest.TestCase):

    def test_classify_impact(self):
        global stats
        stats["success"] = 10
        stats["server_errors"] = 10
        stats["timeouts"] = 10

        impact = classify_impact()
        impact_clean = remove_ansi(impact)  # Quitar colores ANSI para comparar

        self.assertIn("Crítico", impact_clean)

    def test_no_vulnerabilities_detected(self):
        global vulnerabilities_detected
        vulnerabilities_detected = []
        self.assertFalse(vulnerabilities_detected, "No debe haber vulnerabilidades detectadas al inicio.")

    def test_send_request_success(self):
        global stats
        stats = {"success": 0, "server_errors": 0, "client_errors": 0, "timeouts": 0, "average_response_time": []}
        send_request("https://client.qa.powerstreet.cloud", 1)
        print("Stats después de send_request:", stats)  # Depuración
        self.assertGreater(stats["success"], 0, "Debe haber al menos una solicitud exitosa.")


# Ejecutar pruebas unitarias si se ejecuta el script directamente
if __name__ == "__main__":
    unittest.main(exit=False)

    # Iniciar la prueba si no es un entorno de test
    perform_ddos_check(get_url_from_input())

    impact_result = classify_impact()
    print(f"{Fore.MAGENTA}Impacto del ataque: {impact_result}{Style.RESET_ALL}")
