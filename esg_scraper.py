import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# List of filler words and stop words to be removed
FILLER_WORDS = {
    'um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 'seriously',
    'literally', 'well', 'just', 'actually', 'right', 'i mean'
}

STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
    'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been', 'before', 'being',
    'below', 'between', 'both', 'but', 'by', 'can', 'could', 'did', 'didn\'t', 'do',
    'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 'each', 'few', 'for',
    'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having',
    'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if',
    'in', 'into', 'is', 'isn\'t', 'it', 'its', 'itself', 'just', 'll', 'm', 'me',
    'might', 'must', 'my', 'myself', 'need', 'needn\'t', 'no', 'nor', 'not', 'now',
    'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves',
    'out', 'over', 'own', 're', 's', 'same', 'shan\'t', 'she', 'should', 'should\'ve',
    'so', 'some', 'such', 't', 'than', 'that', 'the', 'their', 'theirs', 'them',
    'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to',
    'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn\'t', 'we', 'were',
    'weren\'t', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why',
    'will', 'with', 'won\'t', 'would', 'y', 'you', 'your', 'yours', 'yourself',
    'yourselves'
}

def remove_filler_words(text):
    """
    Remove filler words and stop words from the text.
    """
    words = text.split()
    cleaned_words = [word for word in words if word.lower() not in FILLER_WORDS and word.lower() not in STOP_WORDS]
    return ' '.join(cleaned_words)

def preprocess_data(data):
    """
    Preprocess the data by removing filler words and stop words.
    """
    return remove_filler_words(data)

def scrape_data(source):
    """
    Scrape data from the given source.
    """
    if source == 'barclys':
        url = 'https://www.barclays.com/esg/'
        return scrape_barclys(url)
    elif source == 'hbsc':
        url = 'https://www.hsbc.com/sustainability'
        return scrape_hbsc(url)
    elif source == 'db':
        url = 'https://investor-relations.db.com/esg/#links'
        return scrape_db(url)
    else:
        raise ValueError("Unsupported source")

def scrape_barclys(url):
    """
    Scrape data from Barclays ESG page.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = ''
    for paragraph in soup.find_all(class_='jumbo-body-d'):
        data += paragraph.get_text() + ' '
    return preprocess_data(data.strip())

def scrape_hbsc(url):
    """
    Scrape data from HSBC sustainability page.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = ''
    for div in soup.find_all(class_='col-sm-8 col-sm-offset-2 article-sublayout__content'):
        data += div.get_text() + ' '
    return preprocess_data(data.strip())

def scrape_db(url):
    """
    Scrape data from Deutsche Bank ESG page.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = ''
    for div in soup.find_all(class_='mod-mega-tab-box-item__rich-text'):
        data += div.get_text() + ' '
    return preprocess_data(data.strip())

def get_top_words(text, top_n=10):
    """
    Get the top N most common words from the text.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

# Example usage
if __name__ == "__main__":
    sources = ['barclys', 'hbsc', 'db']
    for source in sources:
        data = scrape_data(source)
        top_words = get_top_words(data)
        print(f"Top words for {source}:")
        for word, count in top_words:
            print(f"{word}: {count}")
