import matplotlib
matplotlib.use('Agg')  # Set matplotlib backend to Agg

from flask import Flask, render_template, abort
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from cm,ollections import Counter
import re
from textblob import TextBlob
import PyPDF2
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words

# Import scrape_data and get_top_words from esg_scraper
from esg_scraper import scrape_data, get_top_words

app = Flask(__name__)

def create_bar_chart(labels, values, title):
    fig, ax = plt.subplots()
    ax.bar(labels, values, color='skyblue')
    ax.set_xlabel('Phrases')
    ax.set_ylabel('Scores')
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def create_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def create_pie_chart(labels, values, title):
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    buffer = BytesIO()
    plt.title(title)
    plt.savefig(buffer, format='png')
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower()

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def get_top_topics(text, n=10):
    words = [word for word in text.split() if word not in stop_words]
    word_counts = Counter(words)
    return word_counts.most_common(n)

def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity

def extract_relevant_text(text, phrases):
    relevant_text = {}
    for phrase in phrases:
        indices = [m.start() for m in re.finditer(re.escape(phrase.lower()), text)]
        relevant_text[phrase] = " ".join(text[i:i+500] for i in indices)  # Grab a snippet around each occurrence
    return relevant_text

def get_sentiment_meaning(polarity, subjectivity):
    polarity_meaning = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    subjectivity_meaning = "Subjective" if subjectivity > 0.5 else "Objective"
    return polarity_meaning, subjectivity_meaning

@app.route('/')
def index():
    try:
        barclys_data = scrape_data('barclys')
        hbsc_data = scrape_data('hbsc')
        db_data = scrape_data('db')

        if not barclys_data or not hbsc_data or not db_data:
            raise ValueError("One or more data sources are empty.")

        barclys_wordcloud = create_wordcloud(barclys_data)
        hbsc_wordcloud = create_wordcloud(hbsc_data)
        db_wordcloud = create_wordcloud(db_data)

        barclys_top_words = get_top_words(barclys_data)
        hbsc_top_words = get_top_words(hbsc_data)
        db_top_words = get_top_words(db_data)

        return render_template('index.html',
                              barclys_wordcloud=barclys_wordcloud,
                              hbsc_wordcloud=hbsc_wordcloud,
                              db_wordcloud=db_wordcloud,
                              barclys_top_words=barclys_top_words,
                              hbsc_top_words=hbsc_top_words,
                              db_top_words=db_top_words)
    except Exception as e:
        print(f"An error occurred in index route: {e}")
        abort(500)  # Internal Server Error

@app.route('/sentiment')
def sentiment():
    try:
        barclays_topics, barclays_polarity, barclays_subjectivity = analyze_pdf('files/Barclays-PLC-Annual-Report-2023.pdf')
        non_financial_topics, non_financial_polarity, non_financial_subjectivity = analyze_pdf('files/Non-Financial-Report-2023.pdf')

        barclays_pie_chart = create_pie_chart(
            ['Polarity', 'Subjectivity'],
            [barclays_polarity, barclays_subjectivity],
            'Barclays Sentiment Analysis'
        )
        non_financial_pie_chart = create_pie_chart(
            ['Polarity', 'Subjectivity'],
            [non_financial_polarity, non_financial_subjectivity],
            'Non-Financial Report Sentiment Analysis'
        )

        return render_template('sentiment.html',
                               barclays_pie_chart=barclays_pie_chart,
                               non_financial_pie_chart=non_financial_pie_chart,
                               barclays_polarity=barclays_polarity,
                               non_financial_polarity=non_financial_polarity,
                               barclays_subjectivity=barclays_subjectivity,
                               non_financial_subjectivity=non_financial_subjectivity)
    except Exception as e:
        print(f"An error occurred in sentiment route: {e}")
        abort(500)  # Internal Server Error

@app.route('/sentiment_by_phrases')
def sentiment_by_phrases():
    try:
        barclays_phrases_sentiments = analyze_phrase('files/Barclays-PLC-Annual-Report-2023.pdf', [
            'ESG innovations in emerging economies',
            'Diversity inclusion',
            'ESG performance',
            'Human rights',
            'Responsible supply chain',
            'Climate change',
            'ESG disclosures',
            'Governance issues',
            'Greenhouse gas emissions'
        ])
        non_financial_phrases_sentiments = analyze_phrase('files/Non-Financial-Report-2023.pdf', [
            'ESG innovations in emerging economies',
            'Diversity inclusion',
            'ESG performance',
            'Human rights',
            'Responsible supply chain',
            'Climate change',
            'ESG disclosures',
            'Governance issues',
            'Greenhouse gas emissions'
        ])

        barclays_labels = [phrase for phrase in barclays_phrases_sentiments.keys()]
        barclays_polarity_values = [result['polarity'] for result in barclays_phrases_sentiments.values()]
        barclays_subjectivity_values = [result['subjectivity'] for result in barclays_phrases_sentiments.values()]

        non_financial_labels = [phrase for phrase in non_financial_phrases_sentiments.keys()]
        non_financial_polarity_values = [result['polarity'] for result in non_financial_phrases_sentiments.values()]
        non_financial_subjectivity_values = [result['subjectivity'] for result in non_financial_phrases_sentiments.values()]

        barclays_polarity_chart = create_bar_chart(barclays_labels, barclays_polarity_values, 'Barclays Polarity Scores')
        barclays_subjectivity_chart = create_bar_chart(barclays_labels, barclays_subjectivity_values, 'Barclays Subjectivity Scores')

        non_financial_polarity_chart = create_bar_chart(non_financial_labels, non_financial_polarity_values, 'Non-Financial Polarity Scores')
        non_financial_subjectivity_chart = create_bar_chart(non_financial_labels, non_financial_subjectivity_values, 'Non-Financial Subjectivity Scores')

        return render_template('sentiment_by_phrases.html',
                               barclays_polarity_chart=barclays_polarity_chart,
                               barclays_subjectivity_chart=barclays_subjectivity_chart,
                               non_financial_polarity_chart=non_financial_polarity_chart,
                               non_financial_subjectivity_chart=non_financial_subjectivity_chart,
                               barclays_phrases_sentiments=barclays_phrases_sentiments,
                               non_financial_phrases_sentiments=non_financial_phrases_sentiments)
    except Exception as e:
        print(f"An error occurred in sentiment_by_phrases route: {e}")
        abort(500)  # Internal Server Error

@app.route('/sentiment-by-theme')
def sentiment_by_theme():
    try:
        barclays_text = extract_text_from_pdf('files/Barclays-PLC-Annual-Report-2023.pdf')
        non_financial_text = extract_text_from_pdf('files/Non-Financial-Report-2023.pdf')

        barclays_cleaned_text = clean_text(barclays_text)
        non_financial_cleaned_text = clean_text(non_financial_text)

        barclays_top_topics = get_top_topics(barclays_cleaned_text, n=5)
        non_financial_top_topics = get_top_topics(non_financial_cleaned_text, n=5)

        def analyze_topic_sentiment(topic):
            polarity, subjectivity = perform_sentiment_analysis(topic)
            return polarity, subjectivity

        barclays_topic_sentiments = {word: analyze_topic_sentiment(word) for word, _ in barclays_top_topics}
        non_financial_topic_sentiments = {word: analyze_topic_sentiment(word) for word, _ in non_financial_top_topics}

        barclays_sentiment_meanings = {
            word: get_sentiment_meaning(polarity, subjectivity)
            for word, (polarity, subjectivity) in barclays_topic_sentiments.items()
        }
        non_financial_sentiment_meanings = {
            word: get_sentiment_meaning(polarity, subjectivity)
            for word, (polarity, subjectivity) in non_financial_topic_sentiments.items()
        }

        return render_template('sentiment_by_theme.html',
                               barclays_topic_sentiments=barclays_topic_sentiments,
                               non_financial_topic_sentiments=non_financial_topic_sentiments,
                               barclays_sentiment_meanings=barclays_sentiment_meanings,
                               non_financial_sentiment_meanings=non_financial_sentiment_meanings)
    except Exception as e:
        print(f"An error occurred in sentiment_by_theme route: {e}")
        abort(500)  # Internal Server Error

def analyze_phrase(file_path, phrases):
    text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(text)
    relevant_text = extract_relevant_text(cleaned_text, phrases)
    sentiment_results = {}
    for phrase, snippet in relevant_text.items():
        polarity, subjectivity = perform_sentiment_analysis(snippet)
        sentiment_results[phrase] = {
            'text': snippet,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'polarity_meaning': get_sentiment_meaning(polarity, subjectivity)[0],
            'subjectivity_meaning': get_sentiment_meaning(polarity, subjectivity)[1]
        }
    return sentiment_results

if __name__ == '__main__':
    app.run(debug=True)
