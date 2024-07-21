import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Function to scrape ESG data with numerical metrics
def scrape_esg_metrics(url, section_tag, section_class, title_tag, metric_tag):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all sections containing ESG metrics
        esg_sections = soup.find_all(section_tag, class_=section_class)

        for section in esg_sections:
            title = section.find(title_tag).text.strip()
            metric_text = section.find(metric_tag).text.strip()
            # Convert metric_text to a number (e.g., float or int)
            try:
                metric_value = float(metric_text.replace(',', '').replace('$', '').strip())
                data.append({'title': title, 'metric': metric_value})
            except ValueError:
                continue  # Skip if the metric is not a number
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return data

# Function to plot ESG metrics
def plot_esg_metrics(data, title):
    titles = [item['title'] for item in data]
    metrics = [item['metric'] for item in data]

    plt.figure(figsize=(12, 8))
    plt.barh(titles, metrics, color='purple')
    plt.xlabel('Metric Value')
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    # Example for Barclays
    barclays_metrics = scrape_esg_metrics('https://home.barclays/sustainability', 'div', 'promo-body', 'h3', 'span.metric')
    plot_esg_metrics(barclays_metrics, 'Barclays ESG Metrics')

    # Example for HSBC
    hsbc_metrics = scrape_esg_metrics('https://www.hsbc.com/sustainability', 'section', 'esg-section', 'h2', 'span.metric')
    plot_esg_metrics(hsbc_metrics, 'HSBC ESG Metrics')
