import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_and_save_content(url, output_file):
    """
    Fetch HTML content from a URL, process it, and save it to a file.
    """
    try:
        # Fetch HTML content
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Select relevant content section
        content_section = soup.find('section', class_='content')
        if not content_section:
            print(f"Content not found: {url}")
            return

        # Remove unwanted parts (example placeholder)
        unwanted_text = content_section.find(string=lambda text: "Example Placeholder" in text if text else False)
        if unwanted_text:
            unwanted_text.extract()  # Remove unwanted parts

        # Save HTML content to file
        html_content = content_section.prettify()
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Content successfully saved to {output_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_urls_from_sitemap(sitemap_url):
    """
    Extract URLs from a sitemap.
    """
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'xml')
        urls = [loc.text for loc in soup.find_all('loc')]
        return urls
    except Exception as e:
        print(f"Failed to fetch sitemap: {e}")
        return []

def sanitize_filename(name):
    """
    Sanitize a filename to remove invalid characters.
    """
    return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()

def main():
    sitemap_url = 'https://example.com/sitemap.xml'
    output_folder = 'extracted_html'

    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Fetch URLs from sitemap
    urls = get_urls_from_sitemap(sitemap_url)

    # Process each URL and save content
    for url in urls:
        parsed_url = urlparse(url)
        page_name = sanitize_filename(parsed_url.path.split('/')[-1]) or 'index'
        output_file = os.path.join(output_folder, f"{page_name}.txt")
        fetch_and_save_content(url, output_file)

if __name__ == "__main__":
    main()
