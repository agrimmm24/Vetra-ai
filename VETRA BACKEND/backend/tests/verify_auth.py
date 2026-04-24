import asyncio
import httpx

async def verify():
    # Note: Assumes server is running on 8000
    base_url = "http://127.0.0.1:8000/api/v1/auth"
    
    # 1. Signup
    print("Testing Signup...")
    signup_data = {
        "phone": "9876543210",
        "name": "Test User",
        "address": "123 Street",
        "city": "Sample City",
        "state": "Sample State",
        "preferred_language": "en"
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{base_url}/signup", json=signup_data)
            print(f"Signup Response: {resp.status_code} - {resp.json()}")
        except Exception as e:
            print(f"Signup failed: {e}")

        # 2. Request OTP
        print("\nTesting Request OTP...")
        try:
            resp = await client.post(f"{base_url}/login/request-otp", json={"phone": "9876543210"})
            print(f"Request OTP Response: {resp.status_code} - {resp.json()}")
        except Exception as e:
            print(f"Request OTP failed: {e}")

        # 3. Verify OTP (Assume 1234 for mock or check logs)
        # Note: Since I'm using a mock that prints to console, I'll need to know it.
        # But for this script, I'll just check if the backend responded correctly.

if __name__ == "__main__":
    # This script requires the server to be running.
    # Since I can't guarantee the server is up in this environment, 
    # I'll just check if the code builds/lints or run a unit test if possible.
    pass
