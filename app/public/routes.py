import base64
from flask import Response,render_template, jsonify, request, flash, redirect, url_for, session, abort, send_from_directory
import os
import uuid
import zipfile
from generate_web_page import main
import shutil

from . import public_bp

"""
# Load favicon
@public_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(public_bp.root_path, '../static/images/favicon_io'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
"""

# Load main web page
@public_bp.route("/")
@public_bp.route("/index")
def index():
    return render_template("index.html")

# Chowlk application
@public_bp.route("/api", methods=["POST"])
def api():

    # Path where the files related to a request are stored
    requests_path = os.path.join(os.getcwd(), 'data', 'requests')
    os.makedirs(requests_path, exist_ok=True)

    # Generate an unique identifier for this request
    request_id = str(uuid.uuid4())

    # Path where the files related to this request are stored
    request_path = os.path.join(requests_path, request_id)
    os.makedirs(request_path, exist_ok=True)

    patterns_type = request.form["patterns_type"]
    flatten_lists = request.form["flatten_lists"]

    ontology_path = os.path.join(request_path, 'ontologies')

    if 'ontologiesZip' in request.files:
        file = request.files['ontologiesZip']
        zip_path = os.path.join(request_path, 'ontologies.zip')
        file.save(zip_path)
        csv_path = ''

        # Extract the contents of the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(request_path)
    
    elif 'ontologiesCsv' in request.files:
        file = request.files['ontologiesCsv']
        csv_path = os.path.join(request_path, 'ontologies.csv')
        file.save(csv_path)
    
    main(ontology_path, csv_path, request_path, patterns_type, flatten_lists)
    shutil.make_archive(request_path, 'zip', request_path)

    with open(f'{request_path}.zip', "rb") as f:
        bytes = f.read()
        encoded = base64.b64encode(bytes)

    response = Response(encoded, mimetype='application/zip')
    response.headers['Content-Disposition'] = 'attachment; filename=name.zip'

    # Remove request files
    shutil.rmtree(request_path)
    os.remove(f'{request_path}.zip')

    return response

    