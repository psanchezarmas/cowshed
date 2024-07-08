import unittest

from cowshed.app import app


class CowshedTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_cows(self):
        response = self.app.get('/cows')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_create_cow(self):
        response = self.app.post('/cows', json={
            'name': 'Daisy',
            'sex': 'Female'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Daisy')
        self.assertEqual(response.json['sex'], 'Female')

    def test_update_cow(self):
        # First, create the cow
        self.app.post('/cows', json={
            'name': 'Daisy',
            'sex': 'Female'
        })
        
        # Update the cow
        response = self.app.put('/cows/Daisy', json={
            'sex': 'Male',
            'condition': 'Healthy'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Daisy')
        self.assertEqual(response.json['sex'], 'Male')
        self.assertEqual(response.json['condition'], 'Healthy')

    def test_delete_cow(self):
        # First, create the cow
        self.app.post('/cows', json={
            'name': 'Daisy',
            'sex': 'Female'
        })
        
        # Delete the cow
        response = self.app.delete('/cows/Daisy')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], True)
        
        # Verify that the cow is deleted
        response = self.app.get('/cows/Daisy')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
