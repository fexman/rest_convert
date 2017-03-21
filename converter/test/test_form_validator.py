import unittest
from converter.app.form_validator import FormValidationException, Validator


class TestFormValidator(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()

    def test_wrong_structure(self):
        with self.assertRaises(FormValidationException):
            self.validator.validate_structure({'apple': 'red'})

    def test_partial_structure(self):
        with self.assertRaises(FormValidationException):
            self.validator.validate_structure({'format': ''})

    def test_valid_structure(self):
        self.validator.validate_structure({'format': '', 'date': ''})

    def test_wrong_content(self):
        with self.assertRaises(FormValidationException):
            self.validator.validate_content({'format': 'un1x'})

    def test_valid_content(self):
        self.validator.validate_content({'format': 'unix'})


if __name__ == '__main__':
    unittest.main()
