import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import pandas as pd
from collections import Counter
import numpy as np

# Function to scrape ESG data from Barclays
def scrape_esg_data(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        esg_sections = soup.find_all('div', class_='jumbo-body-d')

        for section in esg_sections:
            title = section.find('h3').get_text(strip=True) if section.find('h3') else 'No Title'
            description = section.get_text(strip=True)
            data.append({'title': title, 'description': description})
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return data

# Function to generate and plot word clouds
def plot_word_cloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()

# Function to create a heat map of word frequency
def plot_heat_map(word_freq, title):
    # Convert word frequencies to a DataFrame
    df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
    df = df.sort_values(by='Frequency', ascending=False)

    # Create a heat map matrix
    matrix = np.zeros((1, len(df)))
    matrix[0] = df['Frequency']

    plt.figure(figsize=(12, 4))
    sns.heatmap(matrix, cmap='YlGnBu', annot=True, cbar=True, xticklabels=df['Word'], yticklabels=['Frequency'])
    plt.title(title)
    plt.xticks(rotation=90)
    plt.show()

# Function to analyze and visualize ESG data
def analyze_data(data):
    # Combine all descriptions into a single text
    combined_text = ' '.join(item['description'] for item in data)
    
    # Generate and plot word cloud for common words
    plot_word_cloud(combined_text, 'Word Cloud of Common Words')

    # Tokenize and count words
    words = combined_text.lower().split()
    word_freq = Counter(words)
    
    # Generate and plot heat map of word frequency
    plot_heat_map(word_freq, 'Heat Map of Word Frequency')

if __name__ == "__main__":
    # URL for Barclays ESG data (update URL if necessary)
    barclays_data = scrape_esg_data('https://home.barclays/sustainability')
    if barclays_data:
        analyze_data(barclays_data)
    else:
        print("No data found for Barclays.")
