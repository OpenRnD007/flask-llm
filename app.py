from flask import Flask, request, jsonify
import requests
import os
from llmlib import llm_app

app = Flask(__name__)
# Define the directory where files will be stored
local_dir = 'download'
os.makedirs(local_dir, exist_ok=True)

@app.route('/processllm', methods=['POST'])
def handle_request():
    data = request.get_json()
    file_type = data.get('filetype')
    file_path = data.get('filepath')
    questions = data.get('questions')

    # Check if the file type is valid
    if file_type not in ['PDF', 'JSON']:
        return jsonify({'error': 'Unsupported file type'}), 400

    # Check if the file exists at the given path
    try:
        response = requests.head(file_path)
        if response.status_code != 200:
            return jsonify({'error': 'File does not exist at the provided path'}), 404
    except requests.ConnectionError:
        return jsonify({'error': 'Failed to connect to the file path'}), 500

    # Download the file
    response = requests.get(file_path)
    local_file_path = os.path.join(local_dir, os.path.basename(file_path))
    with open(local_file_path, 'wb') as file:
        file.write(response.content)

    # Call the process_file function and get answers
    answers = llm_app(file_type, local_file_path, questions)

    # Return the answers in the response
    return jsonify(answers), 200

if __name__ == '__main__':
    app.run(debug=True)