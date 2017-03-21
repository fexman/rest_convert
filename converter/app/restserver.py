#!flask/bin/python
from flask import Flask, request, abort, make_response, jsonify

from converter.app.conversion_service import ConversionException, Converter
from converter.app.form_validator import FormValidationException, Validator

app = Flask(__name__)
form_validator = Validator()
converter = Converter()


@app.route('/convert', methods=['POST'])
def convert():

    # initial test if form data is provided
    if not request.form:
        return jsonify({'message': 'Invalid request!', 'errors': {'request': 'Must be form encoded'}}), 400

    # ensure valid form data as input
    form_validator.validate_structure(request.form)
    form_validator.validate_content(request.form)

    input = request.form['date']

    # obtain fitting converter func
    if request.form['format'] == 'unix':
        convert_func = converter.convert_unix_to_rfc
        out_format = 'rfc3339'
    else:
        convert_func = converter.convert_rfc_to_unix
        out_format = 'unix'

    # convert and return response
    return jsonify({'input': input, 'output': convert_func(input), 'format': out_format})

@app.errorhandler(405)
def http_invalid_method(e):
    return jsonify({'message:':'http: method not allowed'}), 405

@app.errorhandler(404)
def http_invalid_method(e):
    return jsonify({'message:':'http: not found'}), 404

@app.errorhandler(FormValidationException)
def handle_invalid_usage(error):
    return jsonify({'message': 'Invalid form data!', 'errors': error.errors}), 400

@app.errorhandler(ConversionException)
def handle_invalid_usage(error):
    return jsonify({'message': 'Invalid input!', 'errors': error.errors}), 400

if __name__ == '__main__':
    app.run(debug=True)
