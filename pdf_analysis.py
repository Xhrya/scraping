import PyPDF2
from collections import Counter
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
from textblob import TextBlob

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower()

def get_top_topics(text, n=10):
    words = [word for word in text.split() if word not in stop_words]
    word_counts = Counter(words)
    return word_counts.most_common(n)

def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity

def analyze_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(text)
    top_topics = get_top_topics(cleaned_text)
    polarity, subjectivity = perform_sentiment_analysis(cleaned_text)
    return top_topics, polarity, subjectivity
