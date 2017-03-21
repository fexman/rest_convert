#!flask/bin/python
from flask import Flask, request, abort, make_response, jsonify

from converter.app.conversion_service import ConversionException, Converter
from converter.app.form_validator import FormValidationException, Validator

app = Flask(__name__)
form_validator = Validator()
converter = Converter()

@app.route('/convert', methods=['POST'])
def create_task():
    print(request.form)
    if not request.form:
        return jsonify({'message': 'Invalid request!', 'errors': { 'request': 'Be form encoded'}}), 400
    try:
        form_validator.validate_structure(request.form)
        form_validator.validate_content(request.form)

        return jsonify({'message': 'Welcome!'})

    except FormValidationException as e:
        return jsonify({'message': 'Invalid form data!', 'errors': e.errors}), 400
    except ConversionException as e:
        return jsonify({'message': 'Invalid input!', 'errors': e.errors}), 400

if __name__ == '__main__':
    app.run(debug=True)