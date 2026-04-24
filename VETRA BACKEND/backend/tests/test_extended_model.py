import requests
import json

def test_extended_prediction():
    url = "http://127.0.0.1:8000/api/v1/predict/"
    
    # Sample scenarios with pH and Heart Rate
    scenarios = [
        {
            "name": "Healthy Cow",
            "payload": {
                "animal_id": "COW-001",
                "milk_yield": 20.0,
                "feed_intake": "high",
                "activity_level": "high",
                "temperature": 38.5,
                "pH": 6.6,
                "heart_rate": 70.0
            }
        },
        {
            "name": "Fever & High Heart Rate",
            "payload": {
                "animal_id": "COW-002",
                "milk_yield": 15.0,
                "feed_intake": "medium",
                "activity_level": "low",
                "temperature": 40.5,
                "pH": 6.8,
                "heart_rate": 110.0
            }
        },
        {
            "name": "Mastitis Risk (High pH)",
            "payload": {
                "animal_id": "COW-003",
                "milk_yield": 10.0,
                "feed_intake": "medium",
                "activity_level": "medium",
                "temperature": 39.0,
                "pH": 7.5,
                "heart_rate": 85.0
            }
        }
    ]

    print("Testing Backend with Extended Features (pH, Heart Rate)...\n")
    
    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")
        try:
            response = requests.post(url, json=scenario['payload'])
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Result: Risk={result['risk_level']}, Score={result['risk_score']}")
                # print(f"Reasons: {result['reasons']}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        print("-" * 40)

if __name__ == "__main__":
    test_extended_prediction()
