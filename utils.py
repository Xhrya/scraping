import requests

def fetch_pdf_from_server(pdf_name):
    try:
        response = requests.get(f'http://127.0.0.1:5000/get_pdf/{pdf_name}')
        response.raise_for_status()  # Check if request was successful
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the PDF: {e}")
        return None
