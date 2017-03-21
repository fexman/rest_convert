class Validator:
    def validate_structure(self, form):
        if not 'date' in form or not 'format' in form:
            raise FormValidationException({'form-data': 'Must contain fields date and format'})

    def validate_content(self, form):
        if 'unix' != form['format'] and 'rfc3339' != form['format']:
            raise FormValidationException({'form-data': 'Format must be either unix or rfc3339'})


class FormValidationException(Exception):
    def __init__(self, errors):
        self.errors = errors
