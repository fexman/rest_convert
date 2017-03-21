#!flask/bin/python
from flask import Flask, request, abort, make_response, jsonify

app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def create_task():
    print(request.form)
    if not request.form or not 'date' in request.form or not 'format' in request.form:
        return jsonify({'message': 'Invalid form data!', 'errors': { 'form-data': 'Must contain fields date and format'}}), 400
    return jsonify({'message':'Welcome!'})

if __name__ == '__main__':
    app.run(debug=True)