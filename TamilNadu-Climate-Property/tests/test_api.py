import unittest

from fastapi.testclient import TestClient

from app.main import app


class TestClimatePropertyAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_health(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tamil Nadu Climate", response.json()["message"])

    def test_predict_route(self):
        payload = {
            "district": "Pudukkottai",
            "city": "Pudukkottai",
            "latitude": 10.3797,
            "longitude": 78.8208,
            "area_sqft": 1200,
            "market_rate_per_sqft": 2800,
        }

        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("valuation", response.json())
        self.assertIn("base_value", response.json()["valuation"])


if __name__ == "__main__":
    unittest.main()
