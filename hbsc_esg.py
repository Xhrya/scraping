import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import pandas as pd
from collections import Counter
import numpy as np

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

# Function to analyze and visualize HSBC ESG data
def analyze_data_hsbc(data):
    # Combine all descriptions into a single text
    combined_text = ' '.join(item['description'] for item in data)
    
    # Generate and plot word cloud for common words
    plot_word_cloud(combined_text, 'Word Cloud of Common Words - HSBC')

    # Tokenize and count words
    words = combined_text.lower().split()
    word_freq = Counter(words)
    
    # Generate and plot heat map of word frequency
    plot_heat_map(word_freq, 'Heat Map of Word Frequency - HSBC')

if __name__ == "__main__":
    # URL for HSBC ESG data (update URL if necessary)
    hsbc_data = scrape_esg_data_hsbc('https://www.hsbc.com/sustainability')
    if hsbc_data:
        analyze_data_hsbc(hsbc_data)
    else:
        print("No data found for HSBC.")
