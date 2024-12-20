import os
from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Azure Blob Storage setup
AZURE_STORAGE_CONNECTION_STRING = "AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
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
        new_file_name = f"SFI-{sfi_no}.{program}.{session}.{coach_name}.{date}.mp4"

        # Upload file to Azurite
        blob_client = container_client.get_blob_client(new_file_name)
        blob_client.upload_blob(uploaded_file)

         # Render the success page with form data
        return render_template('success.html', sfi_no=sfi_no, program=program, session=session, first_name=first_name, last_name=last_name, date=date)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
