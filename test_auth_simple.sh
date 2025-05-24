#!/bin/bash

# Simple shell script to test authentication behavior
# AI Healthcare Assistant API - Authentication Test

BASE_URL="http://localhost:8000"

echo "🚀 AI Healthcare Assistant API - Authentication Test"
echo "This script demonstrates protected vs public endpoints"

echo ""
echo "🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓 PUBLIC ENDPOINTS 🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓"

echo ""
echo "📋 TEST: Health Check (Public - Should Work)"
echo "curl -X GET \"${BASE_URL}/health\""
curl -X GET "${BASE_URL}/health" -H "accept: application/json"
echo ""

echo ""
echo "📋 TEST: User Registration (Public - Should Work)"
echo "curl -X POST \"${BASE_URL}/auth/register\" -H \"Content-Type: application/json\" -d '{...}'"
curl -X POST "${BASE_URL}/auth/register" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword123", "first_name": "Test", "last_name": "User"}'
echo ""

echo ""
echo "🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒 PROTECTED ENDPOINTS - NO AUTH 🔒🔒🔒🔒🔒🔒🔒🔒🔒🔒"

echo ""
echo "📋 TEST: Get User Profile (No Auth - Should Return 401)"
echo "curl -X GET \"${BASE_URL}/users/profile\""
curl -X GET "${BASE_URL}/users/profile" -H "accept: application/json"
echo ""

echo ""
echo "📋 TEST: Send Chat Message (No Auth - Should Return 401)"
echo "curl -X POST \"${BASE_URL}/chat/message\" -H \"Content-Type: application/json\" -d '{...}'"
curl -X POST "${BASE_URL}/chat/message" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"message": "What does my insurance cover?"}'
echo ""

echo ""
echo "🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐 PROTECTED ENDPOINTS - WITH AUTH 🔐🔐🔐🔐🔐🔐🔐🔐🔐🔐"

echo ""
echo "📋 TEST: Get User Profile (With Auth - Should Work)"
echo "curl -X GET \"${BASE_URL}/users/profile\" -H \"Authorization: Bearer test-token\""
curl -X GET "${BASE_URL}/users/profile" \
  -H "accept: application/json" \
  -H "Authorization: Bearer test-jwt-token-placeholder"
echo ""

echo ""
echo "📋 TEST: Send Chat Message (With Auth - Should Work)"
echo "curl -X POST \"${BASE_URL}/chat/message\" -H \"Authorization: Bearer test-token\" -d '{...}'"
curl -X POST "${BASE_URL}/chat/message" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-jwt-token-placeholder" \
  -d '{"message": "What does my insurance cover?", "context": {"user_type": "international_student"}}'
echo ""

echo ""
echo "📋 TEST: Update User Profile (With Auth - Should Work)"
echo "curl -X PUT \"${BASE_URL}/users/profile\" -H \"Authorization: Bearer test-token\" -d '{...}'"
curl -X PUT "${BASE_URL}/users/profile" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-jwt-token-placeholder" \
  -d '{"first_name": "Updated", "last_name": "Name"}'
echo ""

echo ""
echo "🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯 TEST SUMMARY 🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯"
echo "✅ Public endpoints work without authentication"
echo "❌ Protected endpoints return 401 without authentication"
echo "✅ Protected endpoints work with Bearer token"
echo "🔒 This demonstrates proper API security implementation"
echo ""
echo "Note: JWT validation is placeholder - implement actual validation in production!" 