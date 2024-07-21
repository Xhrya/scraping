import requests
from bs4 import BeautifulSoup

def scrape_esg_data(url, section_tag, section_class, title_tag, description_tag):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all sections containing ESG data
        esg_sections = soup.find_all(section_tag, class_=section_class)

        for section in esg_sections:
            title = section.find(title_tag).text.strip()
            description = section.find(description_tag).get_text(strip=True)
            print(f"Title: {title}")
            print(f"Description: {description}")
            print("-" * 80)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    # Example usage for Barclays
    scrape_esg_data('https://home.barclays/sustainability', 'div', 'promo-body', 'h3', 'div.aem-rte')

    # Example usage for HSBC
    scrape_esg_data('https://www.hsbc.com/sustainability', 'section', 'esg-section', 'h2', 'p')
