#!flask/bin/python
from flask import Flask, request, abort, make_response, jsonify

from converter.app.conversion_service import ConversionException, Converter
from converter.app.form_validator import FormValidationException, Validator

app = Flask(__name__)
form_validator = Validator()
converter = Converter()

@app.route('/convert', methods=['POST'])
def convert():

    #initial test if form data is provided
    if not request.form:
        return jsonify({'message': 'Invalid request!', 'errors': { 'request': 'Must be form encoded'}}), 400
    try:

        #ensure valid form data as input
        form_validator.validate_structure(request.form)
        form_validator.validate_content(request.form)

        input = request.form['date']

        #obtain fitting converter func
        if request.form['format'] == 'unix':
            convert_func = converter.convert_unix_to_rfc
            out_format = 'rfc3339'
        else:
            convert_func = converter.convert_rfc_to_unix
            out_format = 'unix'

        print(input)
        #convert and return response
        return jsonify({'input':input,'output':convert_func(input),'format':out_format})

    except FormValidationException as e:
        return jsonify({'message': 'Invalid form data!', 'errors': e.errors}), 400
    except ConversionException as e:
        return jsonify({'message': 'Invalid input!', 'errors': e.errors}), 400

if __name__ == '__main__':
    app.run(debug=True)