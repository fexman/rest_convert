import unittest
import converter.app.restserver as server


class TestRestServer(unittest.TestCase):
    def setUp(self):
        self.app = server.app.test_client()
        self.app.testing = True

    def test_invalid_path(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)

    def test_invalid_method(self):
        response = self.app.get('/convert')
        self.assertEqual(response.status_code, 405)

    def test_invalid_form_format(self):
        response = self.app.post('/convert', data={'pie': ''})
        self.assertRegex(str(response.data), r'Invalid form data')
        self.assertEqual(response.status_code, 400)

    def test_incomplete_form_format(self):
        response = self.app.post('/convert', data={'format': ''})
        self.assertRegex(str(response.data), r'Invalid form data')
        self.assertEqual(response.status_code, 400)

    def test_invalid_form_content(self):
        response = self.app.post('/convert', data={'format': 'unix', 'date': 'test'})
        self.assertEqual(response.status_code, 400)
        self.assertRegex(str(response.data), r'unix-formatted')

    def test_unix_to_rfc(self):
        response = self.app.post('/convert', data={'format': 'unix', 'date': '1490107042'})
        self.assertEqual(response.status_code, 200)
        self.assertRegex(str(response.data), r'rfc3339.+2017-03-21T15:37:22Z')

    def test_rfc_to_unix(self):
        response = self.app.post('/convert', data={'format': 'rfc3339', 'date': '2017-03-21T15:37:22Z'})
        self.assertEqual(response.status_code, 200)
        self.assertRegex(str(response.data), r'unix.+1490107042')


if __name__ == '__main__':
    unittest.main()
