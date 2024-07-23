import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import datetime
from flask import Flask, render_template, abort, request, jsonify
import base64
import sys
from io import BytesIO
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import os
from textblob import TextBlob
import PyPDF2
from dash.dependencies import Input, Output, State

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words

# Add the backend directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Import scrape_data and get_top_words from esg_scraper
from esg_scraper import scrape_data, get_top_words

# Initialize the server with Flask and then use it for Dash
server = Flask(__name__)
app = Dash(__name__, server=server)

# storage_client = storage.Client.from_service_account_json('path/to/your/service-account-key.json')
# bucket_name = 'your-bucket-name'
# bucket = storage_client.bucket(bucket_name)

# @server.route('/get_pdf/<filename>')
# def get_pdf(filename):
#     try:
#         blob = bucket.blob(filename)
#         pdf_content = blob.download_as_bytes()
#         return send_file(BytesIO(pdf_content), attachment_filename=filename, as_attachment=True)
#     except Exception as e:
#         print(f"An error occurred while fetching the PDF: {e}")
#         abort(500)


# from flask import Flask, render_template, send_file
# from utils import fetch_pdf_from_server
# ________________________________
# app = Flask(__name__)

# @app.route('/some_route')
# def some_view():
#     pdf_content = fetch_pdf_from_server('example.pdf')
#     if pdf_content:
#         # Do something with the PDF content
#         return send_file(BytesIO(pdf_content), attachment_filename='example.pdf', as_attachment=True)
#     else:
#         return "Failed to retrieve PDF", 500

# if __name__ == '__main__':
#     app.run(debug=True)




def extract_text_from_pdf(file_path):
    text = ""
    try:
        # Print current working directory and file path for debugging
        print("Current working directory:", os.getcwd())
        print("File path:", file_path)
        
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ""
    except FileNotFoundError as e:
        print(e)
        raise
    except Exception as e:
        print(f"An error occurred while extracting text from PDF: {e}")
        raise
    return text

# barclays_text = extract_text_from_pdf('../backend/files/Barclays-PLC-Annual-Report-2023.pdf')
# non_financial_text = extract_text_from_pdf('../backend/files/Non-Financial-Report-2023.pdf')

barclays_file_path = os.path.abspath('../backend/files/Barclays-PLC-Annual-Report-2023.pdf')
non_financial_file_path = os.path.abspath('../backend/files/Non-Financial-Report-2023.pdf')

barclays_text = extract_text_from_pdf(barclays_file_path)
non_financial_text = extract_text_from_pdf(non_financial_file_path)

# Navbar definition with additional links
navbar = html.Nav([
    html.Div([
        html.Strong("ESG", style={"font-weight": "bold", "font-size": "20px", "color": "white", "margin-right": "20px"}),
        html.Ul([
            html.Li(html.A("Home", href="/", style={"color": "white"})),
            html.Li(html.A("Scrape", href="/scrape", style={"color": "white"})),
            html.Li(html.A("Sentiment by Theme", href="/sentiment_by_theme", style={"color": "white"})),
            html.Li(html.A("Sentiment by Phrases", href="/sentiment_by_phrases", style={"color": "white"})),
            html.Li(html.A("About", href="/about", style={"color": "white"})),
            html.Li(html.A("Contact", href="/contact", style={"color": "white"}))
        ], style={"list-style": "none", "display": "flex", "padding": 0, "margin": 0})
    ], style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "50px"})
], style={"background-color": "blue", "padding": "10px"})

# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    html.Hr(),
])

# Define a callback to update the page content based on the URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/about':
        return html.Div([
            html.H2("About Page"),
            html.P("This is the About page content.")
        ])
    elif pathname == '/contact':
        return html.Div([
            html.H2("Contact Page"),
            html.P("This is the Contact page content.")
        ])
    elif pathname == '/scrape':
        return html.Div([
            html.H2("Scrape Data"),
            html.P("This page will trigger the scraping process.")
        ])
    elif pathname == '/sentiment_by_theme':
        return html.Div([
            html.H2("Sentiment by Theme"),
            html.P("This page displays sentiment analysis by theme.")
        ])
    elif pathname == '/sentiment_by_phrases':
        return html.Div([
            html.H2("Sentiment by Phrases"),
            html.P("This page displays sentiment analysis by phrases.")
        ])
    else:
        return html.Div([
            html.H2("Home Page"),
            html.P("This is the Home page content.")
        ])

# Flask Routes
@server.route('/scrape')
def scrape():
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

@server.route('/analyze_pdf', methods=['POST'])
def analyze_pdf():
    file_path = request.json.get('file_path')
    if not file_path:
        abort(400, 'File path is required')

    text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(text)
    top_topics = get_top_topics(cleaned_text)
    polarity, subjectivity = perform_sentiment_analysis(cleaned_text)
    return jsonify({
        'top_topics': top_topics,
        'polarity': polarity,
        'subjectivity': subjectivity
    })

@server.route('/sentiment_by_theme')
def sentiment_by_theme():
    try:
        # barclays_blob = bucket.blob('Barclays-PLC-Annual-Report-2023.pdf')
        # non_financial_blob = bucket.blob('Non-Financial-Report-2023.pdf')

        # barclays_text = barclays_blob.download_as_text()
        # non_financial_text = non_financial_blob.download_as_text()

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

@server.route('/sentiment_by_phrases')
def sentiment_by_phrases():
    try:
        barclays_phrases_sentiments = analyze_phrase('../backend/files/Barclays-PLC-Annual-Report-2023.pdf', [
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
        non_financial_phrases_sentiments = analyze_phrase('../backend/files/Non-Financial-Report-2023.pdf', [
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
                               non_financial_subjectivity_chart=non_financial_subjectivity_chart)
    except Exception as e:
        print(f"An error occurred in sentiment_by_phrases route: {e}")
        abort(500)  # Internal Server Error


def analyze_phrase(file_path, phrases):
    text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(text)
    relevant_text = extract_relevant_text(cleaned_text, phrases)
    
    phrase_sentiments = {}
    for phrase, snippet in relevant_text.items():
        polarity, subjectivity = perform_sentiment_analysis(snippet)
        phrase_sentiments[phrase] = {
            'polarity': polarity,
            'subjectivity': subjectivity
        }
    return phrase_sentiments

# Backend Functions (continued)
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
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ""
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        raise
    except Exception as e:
        print(f"An error occurred while extracting text from PDF: {e}")
        raise
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

if __name__ == '__main__':
    app.run_server(debug=True)
