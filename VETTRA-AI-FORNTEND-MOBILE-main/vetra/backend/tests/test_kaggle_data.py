import requests
import json

# Sample data extracted from the Kaggle Milk Quality Dataset
# pH,Temprature,Taste,Odor,Fat ,Turbidity,Colour,Grade
kaggle_data = [
    {"pH": 6.6, "temp": 35.0, "grade": "high", "odor": 0},
    {"pH": 6.6, "temp": 36.0, "grade": "high", "odor": 1},
    {"pH": 6.6, "temp": 37.0, "grade": "medium", "odor": 0},
    {"pH": 6.6, "temp": 38.0, "grade": "high", "odor": 1},
    {"pH": 6.7, "temp": 41.0, "grade": "medium", "odor": 0},
    {"pH": 6.8, "temp": 40.0, "grade": "high", "odor": 1},
    {"pH": 6.5, "temp": 37.0, "grade": "medium", "odor": 0},
    {"pH": 6.4, "temp": 40.0, "grade": "low", "odor": 1},
]

def map_to_backend(row, index):
    return {
        "animal_id": f"COW-{index:03d}",
        "milk_yield": 25.0 if row["grade"] == "high" else (15.0 if row["grade"] == "medium" else 5.0),
        "feed_intake": "high" if row["grade"] == "high" else ("medium" if row["grade"] == "medium" else "low"),
        "activity_level": "high" if row["odor"] == 0 else "low",
        "temperature": row["temp"]
    }

def test_backend():
    url = "http://127.0.0.1:8000/api/v1/predict/"
    print(f"Testing backend with {len(kaggle_data)} rows from Kaggle...\n")
    
    for i, row in enumerate(kaggle_data):
        payload = map_to_backend(row, i+1)
        print(f"Sending Request for {payload['animal_id']} (Temp: {payload['temperature']})...")
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Risk Level: {result['risk_level']}, Score: {result['risk_score']}")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error connecting to backend: {e}")
        print("-" * 30)

if __name__ == "__main__":
    test_backend()
