from google.cloud import storage

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to {destination_blob_name}.")

def download_from_gcs(bucket_name, source_blob_name, destination_file_path):
    """Downloads a file from Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    blob.download_to_filename(destination_file_path)

    print(f"File {source_blob_name} downloaded to {destination_file_path}.")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)

        # Upload to GCS
        bucket_name = 'your-bucket-name'
        upload_to_gcs(bucket_name, file_path, filename)

        return "File uploaded to Google Cloud Storage", 200

@app.route('/download/<filename>')
def download_file(filename):
    bucket_name = 'your-bucket-name'
    destination_file_path = os.path.join('/tmp', filename)
    
    # Download from GCS
    download_from_gcs(bucket_name, filename, destination_file_path)
    
    return send_file(destination_file_path)
