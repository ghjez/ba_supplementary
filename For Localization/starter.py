from flask import Flask, request, jsonify, send_file
import json
from app import doing
import os
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/outputData'

PROCESING_TIMEOUT = 600 # seconds

# Receive a POST request from a server with an image
@app.route('/localize', methods=['POST'])
def process_stage():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Save the file to the configured upload folder
    input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    try:
        file.save(input_filepath)
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
    
    # Ensure output folder exists
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    # Perform localization
    output_filepath = os.path.join(app.config['OUTPUT_FOLDER'])

    if not os.path.exists(input_filepath):
        return jsonify({'error': f'Input file {input_filepath} not found'}), 500
    
    # The result is written to a variable in case we want to return just the results.json file
    processed_data = doing([input_filepath], output_filepath)  

    # Configure path to the output file
    # output_filepath_final = os.path.join(app.config['OUTPUT_FOLDER'], 'final', 'results.json')
    output_filepath_final = os.path.join(app.config['OUTPUT_FOLDER'], 'results.zip')

    # Wait max PROCESSING_TIMEOUT seconds until results.json/results.zip exists 
    time_counter = 0
    while not os.path.exists(output_filepath_final):
        time.sleep(1)
        time_counter += 1
        if time_counter > PROCESING_TIMEOUT:break

    if not os.path.exists(output_filepath_final):
        return jsonify({'error': 'Output file not found'}), 500

    # Read results.json
    #  with open(output_filepath_final, 'r') as f:
    #     processed_data = json.load(f)

    # return jsonify(processed_data)

    # Send results.zip
    return send_file(output_filepath_final, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

