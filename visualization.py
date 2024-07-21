import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import pandas as pd
from collections import Counter
import numpy as np

# Function to scrape ESG data (same as before)

def scrape_esg_data_barclays(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        esg_sections = soup.find_all('div', class_='jumbo-body-d')

        for section in esg_sections:
            description = section.get_text(strip=True)
            if description:
                data.append({'description': description})
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return data

# Function to scrape ESG data from HSBC
def scrape_esg_data_hsbc(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        esg_sections = soup.find_all('div', class_='col-sm-8 col-sm-offset-2 article-sublayout__content')

        for section in esg_sections:
            description = section.get_text(strip=True)
            if description:
                data.append({'description': description})
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return data

# Function to scrape ESG data from Deutsche Bank
def scrape_esg_data_deutsche_bk(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        esg_sections = soup.find_all('div', class_='mod-mega-tab-box-item__rich-text')

        for section in esg_sections:
            description = section.get_text(strip=True)
            if description:
                data.append({'description': description})
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return data
# Function to generate and save word cloud image
def save_word_cloud(text, filename):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'static/{filename}', bbox_inches='tight')
    plt.close()

# Function to create and save heat map image
def save_heat_map(word_freq, filename):
    df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
    df = df.sort_values(by='Frequency', ascending=False)
    
    matrix = np.zeros((1, len(df)))
    matrix[0] = df['Frequency']
    
    plt.figure(figsize=(12, 4))
    sns.heatmap(matrix, cmap='YlGnBu', annot=True, cbar=True, xticklabels=df['Word'], yticklabels=['Frequency'])
    plt.title('Heat Map of Word Frequency')
    plt.xticks(rotation=90)
    plt.savefig(f'static/{filename}', bbox_inches='tight')
    plt.close()

# Function to generate and save all graphs
def generate_and_save_graphs():
    # URLs for ESG data
    barclays_url = 'URL_FOR_BARCLAYS_ESG'
    hsbc_url = 'URL_FOR_HSBC_ESG'
    deutsche_bk_url = 'https://investor-relations.db.com/esg/#links'
    
    # Scrape and analyze data
    barclays_data = scrape_esg_data_barclays(barclays_url)
    if barclays_data:
        combined_text = ' '.join(item['description'] for item in barclays_data)
        words = combined_text.lower().split()
        word_freq = Counter(words)
        save_word_cloud(combined_text, 'barclays_wordcloud.png')
        save_heat_map(word_freq, 'barclays_heatmap.png')

    hsbc_data = scrape_esg_data_hsbc(hsbc_url)
    if hsbc_data:
        combined_text = ' '.join(item['description'] for item in hsbc_data)
        words = combined_text.lower().split()
        word_freq = Counter(words)
        save_word_cloud(combined_text, 'hsbc_wordcloud.png')
        save_heat_map(word_freq, 'hsbc_heatmap.png')

    deutsche_bk_data = scrape_esg_data_deutsche_bk(deutsche_bk_url)
    if deutsche_bk_data:
        combined_text = ' '.join(item['description'] for item in deutsche_bk_data)
        words = combined_text.lower().split()
        word_freq = Counter(words)
        save_word_cloud(combined_text, 'deutsche_bk_wordcloud.png')
        save_heat_map(word_freq, 'deutsche_bk_heatmap.png')

if __name__ == "__main__":
    generate_and_save_graphs()
