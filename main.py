from flask import Flask, request, jsonify, send_file, abort
from google.cloud import storage
import os
from io import BytesIO
# for gcp stuff
app = Flask(__name__)

# Initialize Google Cloud Storage client
client = storage.Client()
bucket_name = 'your-gcp-bucket-name'
bucket = client.bucket(bucket_name)

@app.route('/get_pdf/<pdf_name>', methods=['GET'])
def get_pdf(pdf_name):
    try:
        blob = bucket.blob(pdf_name)
        if not blob.exists():
            abort(404, 'PDF not found in bucket.')

        pdf_stream = BytesIO()
        blob.download_to_file(pdf_stream)
        pdf_stream.seek(0)  # Reset stream position to the beginning

        return send_file(pdf_stream, as_attachment=True, download_name=pdf_name, mimetype='application/pdf')
    except Exception as e:
        print(f"An error occurred: {e}")
        abort(500)  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True)
