import requests
import unittest
from urllib.parse import urljoin

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
        for payload in self.payloads:
            test_url = f"{self.url}?input={payload}"
            response = requests.get(test_url, timeout=10)
            if payload in response.text:
                self.vulnerabilities.append(f"XSS detectado en {test_url}")

    def generate_report(self):
        """Genera un reporte si se encuentran vulnerabilidades."""
        if not self.vulnerabilities:
            return "No se detectaron vulnerabilidades XSS."
        return "\n".join(self.vulnerabilities)


class TestBlindXSSScanner(unittest.TestCase):
    def test_valid_url(self):
        scanner = BlindXSSScanner("https://client.qa.powerstreet.cloud")
        self.assertTrue(scanner.url.startswith("https"))

    def test_xss_payloads(self):
        scanner = BlindXSSScanner("https://client.qa.powerstreet.cloud")
        self.assertTrue(len(scanner.payloads) > 0)


if __name__ == "__main__":
    input_url = input("Ingrese la URL a escanear: ").strip()
    if input_url.startswith(("http://", "https://")):
        scanner = BlindXSSScanner(input_url)
        scanner.test_xss()
        print(scanner.generate_report())
    else:
        print("URL inválida.")

    unittest.main(exit=False)
