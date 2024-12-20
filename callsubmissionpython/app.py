import os
from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Azure Blob Storage setup
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNoWJ1XDu3MSmf1234567890+FYZ1WOwYcpruEclxYYvIQ==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
CONTAINER_NAME = "callfiles"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.route('/check-container', methods=['GET'])
def check_container():
    try:
        if container_client.exists():
            return jsonify({"message": f"Container '{CONTAINER_NAME}' exists."}), 200
        else:
            return jsonify({"message": f"Container '{CONTAINER_NAME}' does not exist."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        sfi_no = request.form['sfi_no']
        program = request.form['program']
        session = request.form['session']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date = request.form['date']
        uploaded_file = request.files['file']

        # Combine first name and last name into FirstnameLastname format
        coach_name = f"{first_name}{last_name}"

        # Construct new file name
        new_file_name = f"{sfi_no}.{program}.{session}.{coach_name}.{date}.mp4"

        # Upload file to Azurite
        blob_client = container_client.get_blob_client(new_file_name)
        blob_client.upload_blob(uploaded_file)

        return jsonify({"message": f"File uploaded as {new_file_name}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
