import requests
import re
import os
import unittest
from urllib.parse import urlparse, urljoin
from datetime import datetime
from unittest.mock import patch, MagicMock


def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def is_same_domain(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc


def extract_internal_links(url, page_content):
    internal_links = set()
    base_url = get_base_url(url)
    links = re.findall(r'href=[\'\"](.*?)[\'\"]', page_content, flags=re.IGNORECASE)
    for link in links:
        absolute_link = urljoin(base_url, link.strip())
        if is_same_domain(absolute_link, base_url):
            internal_links.add(absolute_link)
    return internal_links


def detect_email_disclosure(url, page_content):
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.IGNORECASE)
    emails = email_pattern.findall(page_content)
    return emails


def perform_email_disclosure_checks(url, visited_urls):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            emails = detect_email_disclosure(url, page_content)
            internal_links = extract_internal_links(url, page_content)
            for link in internal_links:
                if link not in visited_urls:
                    visited_urls.add(link)
                    emails.extend(perform_email_disclosure_checks(link, visited_urls))
            return emails
    except requests.RequestException:
        pass
    return []


class TestEmailDisclosure(unittest.TestCase):
    @patch('requests.get')
    def test_detect_email_disclosure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Email: test@example.com</body></html>"
        mock_get.return_value = mock_response
        emails = perform_email_disclosure_checks("http://example.com", set())
        self.assertIn("test@example.com", emails)

    @patch('requests.get')
    def test_no_email_disclosure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>No email here</body></html>"
        mock_get.return_value = mock_response
        emails = perform_email_disclosure_checks("http://example.com", set())
        self.assertEqual(emails, [])


if __name__ == "__main__":
    url = input("Ingrese la URL a escanear: ")
    visited_urls = set()
    emails = perform_email_disclosure_checks(url, visited_urls)
    if emails:
        print("Vulnerabilidades detectadas:", emails)
    else:
        print("No se detectaron vulnerabilidades.")
    unittest.main()
