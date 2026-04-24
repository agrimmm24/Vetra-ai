import requests
import json

BASE_URL = "http://127.0.0.1:8081/api/v1"

def test_3d_triggers():
    print("🎮 Testing 3D Cow Simulation Triggers (Worst-Case Logic)\n")
    
    user_data = {
        "name": "Arjun",
        "phone": "9876543210",
        "address": "Test",
        "city": "Test",
        "state": "Test",
        "preferred_language": "hi"
    }
    
    # 1. Signup (Expect 201 or 400 if exists)
    requests.post(f"{BASE_URL}/auth/signup", json=user_data)
    
    # 2. Request OTP
    requests.post(f"{BASE_URL}/auth/login/request-otp", json={"phone": user_data["phone"]})
    
    # 3. Verify OTP
    login_resp = requests.post(f"{BASE_URL}/auth/login/verify-otp", json={"phone": user_data["phone"], "otp": "1234"})
    
    if login_resp.status_code != 200:
        print(f"❌ Login Failed: {login_resp.text}")
        return
    
    token = login_resp.json().get("access_token")
    if not token:
        print(f"❌ No token in response: {login_resp.json()}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    scenarios = [
        {
            "name": "CRITICAL: Fever > 55C (Worst Case)",
            "payload": {"animal_id": "3D-1", "milk_yield": 28, "feed_intake": "high", "activity_level": "medium", "temperature": 56.0}
        },
        {
            "name": "WARNING: Low Milk 10.5L (Worst Case)",
            "payload": {"animal_id": "3D-2", "milk_yield": 10.5, "feed_intake": "high", "activity_level": "medium", "temperature": 38.5}
        },
        {
            "name": "NORMAL: Everything Perfect",
            "payload": {"animal_id": "3D-3", "milk_yield": 30, "feed_intake": "high", "activity_level": "high", "temperature": 18.0}
        }
    ]

    for s in scenarios:
        print(f"Testing Scenario: {s['name']}")
        resp = requests.post(f"{BASE_URL}/predict/", json=s["payload"], headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ Final Score: {data.get('score')}")
            print(f"✅ Risk Level: {data.get('level')}")
            print(f"🔥 Health Rank (3D TRIGGER): {data.get('health_rank')}")
            print(f"Reasons: {[r['en'] for r in data['reasons']]}")
        else:
            print(f"❌ Prediction Failed ({resp.status_code}): {resp.text}")
        print("-" * 40)

if __name__ == "__main__":
    test_3d_triggers()
