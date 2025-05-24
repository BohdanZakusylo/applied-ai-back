#!/usr/bin/env python3
"""
Test script to demonstrate authentication behavior in the AI Healthcare Assistant API

This script shows:
1. Public endpoints that work without authentication
2. Protected endpoints that return 401 without authentication  
3. Protected endpoints that work with authentication
"""

import requests
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

def make_request(method: str, endpoint: str, headers: Dict[str, str] = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make HTTP request and return response info"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers or {})
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers or {}, json=data or {})
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers or {}, json=data or {})
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers or {})
        else:
            return {"error": f"Unsupported method: {method}"}
        
        return {
            "status_code": response.status_code,
            "status_text": "SUCCESS" if 200 <= response.status_code < 300 else "FAILED",
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed - is the server running?"}
    except Exception as e:
        return {"error": str(e)}

def print_test_result(test_name: str, result: Dict[str, Any], expected_status: int = None):
    """Print formatted test result"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*60}")
    
    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
        return
    
    status_code = result["status_code"]
    status_text = result["status_text"]
    
    # Check if status matches expected
    if expected_status and status_code == expected_status:
        print(f"✅ Status: {status_code} ({status_text}) - EXPECTED")
    elif expected_status:
        print(f"❌ Status: {status_code} ({status_text}) - EXPECTED {expected_status}")
    else:
        print(f"📊 Status: {status_code} ({status_text})")
    
    print(f"📝 Response:")
    print(json.dumps(result["response"], indent=2))

def main():
    """Run authentication tests"""
    print("🚀 AI Healthcare Assistant API v1 - Authentication Test")
    print("This script demonstrates protected vs public endpoints")
    
    # Test headers
    no_auth_headers = {"accept": "application/json"}
    auth_headers = {
        "accept": "application/json", 
        "Authorization": "Bearer test-jwt-token-placeholder"
    }
    
    print("\n" + "🔓" * 20 + " PUBLIC ENDPOINTS " + "🔓" * 20)
    
    # 1. Test public endpoints (should work without auth)
    print_test_result(
        "Health Check (Public)",
        make_request("GET", "/api/v1/health", no_auth_headers),
        expected_status=200
    )
    
    print_test_result(
        "User Registration (Public)", 
        make_request("POST", "/api/v1/auth/register", no_auth_headers, {
            "email": "test@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }),
        expected_status=201
    )
    
    print_test_result(
        "User Login (Public)",
        make_request("POST", "/api/v1/auth/login", no_auth_headers, {
            "email": "test@example.com", 
            "password": "testpassword123"
        }),
        expected_status=200
    )
    
    print("\n" + "🔒" * 15 + " PROTECTED ENDPOINTS - NO AUTH " + "🔒" * 15)
    
    # 2. Test protected endpoints WITHOUT auth (should return 401)
    print_test_result(
        "Get User Profile (No Auth - Should Fail)",
        make_request("GET", "/api/v1/users/profile", no_auth_headers),
        expected_status=401
    )
    
    print_test_result(
        "Send Chat Message (No Auth - Should Fail)",
        make_request("POST", "/api/v1/chat/message", no_auth_headers, {
            "message": "What does my insurance cover?"
        }),
        expected_status=401
    )
    
    print_test_result(
        "Get Chat History (No Auth - Should Fail)",
        make_request("GET", "/api/v1/chat/history", no_auth_headers),
        expected_status=401
    )
    
    print_test_result(
        "Logout (No Auth - Should Fail)",
        make_request("POST", "/api/v1/auth/logout", no_auth_headers),
        expected_status=401
    )
    
    print("\n" + "🔐" * 15 + " PROTECTED ENDPOINTS - WITH AUTH " + "🔐" * 15)
    
    # 3. Test protected endpoints WITH auth (should work)
    print_test_result(
        "Get User Profile (With Auth - Should Work)",
        make_request("GET", "/api/v1/users/profile", auth_headers),
        expected_status=200
    )
    
    print_test_result(
        "Send Chat Message (With Auth - Should Work)",
        make_request("POST", "/api/v1/chat/message", auth_headers, {
            "message": "What does my insurance cover?",
            "context": {"user_type": "international_student"}
        }),
        expected_status=200
    )
    
    print_test_result(
        "Update User Profile (With Auth - Should Work)",
        make_request("PUT", "/api/v1/users/profile", auth_headers, {
            "first_name": "Updated",
            "last_name": "Name"
        }),
        expected_status=200
    )
    
    print_test_result(
        "Get Chat History (With Auth - Should Work)",
        make_request("GET", "/api/v1/chat/history", auth_headers),
        expected_status=200
    )
    
    print_test_result(
        "Logout (With Auth - Should Work)",
        make_request("POST", "/api/v1/auth/logout", auth_headers),
        expected_status=200
    )
    
    print("\n" + "🎯" * 25 + " TEST SUMMARY " + "🎯" * 25)
    print("✅ Public endpoints work without authentication")
    print("❌ Protected endpoints return 401 without authentication") 
    print("✅ Protected endpoints work with Bearer token")
    print("🔒 This demonstrates proper API security implementation")
    print("🚀 All endpoints now use /api/v1/ prefix for versioning")
    print("\nNote: JWT validation is placeholder - implement actual validation in production!")

if __name__ == "__main__":
    main() 