#!/usr/bin/env python3
"""
Simple test script to debug the API connection
"""
import requests
import json

def test_api():
    url = "http://localhost:8000/api/chat"
    
    # Test data
    data = {
        "developer_message": "You are a helpful AI assistant.",
        "user_message": "Hello, how are you?",
        "model": "gpt-4o-mini",
        "api_key": "your-actual-api-key-here"  # Replace with your real API key
    }
    
    try:
        print("Testing API connection...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ API is working! Response:")
            print(response.text)
        else:
            print("❌ API Error:")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_api()
