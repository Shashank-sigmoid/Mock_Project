import unittest
import requests


class TestApis(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        print('\nSetup Class')

    @classmethod
    def teardown_class(cls):
        print("\nTearing Down Class")

    def test_api_query1(self):
        response = requests.get("http://127.0.0.1:8086/api/query1?startdate=&&enddate=")
        assert response.status_code == 200

    def test_api_query2(self):
        response = requests.get("http://127.0.0.1:8086/api/query2?startdate=&&enddate=")
        assert response.status_code == 200

    def test_api_query3(self):
        response = requests.get("http://127.0.0.1:8086/api/query3?startdate=&&enddate=")
        assert response.status_code == 200

    def test_api_query4(self):
        response = requests.get("http://127.0.0.1:8086/api/query4?startdate=&&enddate=")
        assert response.status_code == 200

    def test_api_query5(self):
        response = requests.get("http://127.0.0.1:8086/api/query5?startdate=&&enddate=")
        assert response.status_code == 200

    def test_api_query6(self):
        response = requests.get("http://127.0.0.1:8086/api/query6?startdate=&&enddate=")
        assert response.status_code == 200

    def test_api_query7(self):
        response = requests.get("http://127.0.0.1:8086/api/query7?startdate=&&enddate=")
        assert response.status_code == 200

    def test_api_query8(self):
        response = requests.get("http://127.0.0.1:8086/api/query8?startdate=&&enddate=")
        assert response.status_code == 200


if __name__ == "__main__":
    print("Testing...")
    unittest.main()
