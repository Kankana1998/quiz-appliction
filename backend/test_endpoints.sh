#!/bin/bash
# Quick test script for API endpoints

BASE_URL="http://localhost:5001"

echo "Testing API endpoints..."
echo ""

# Test health check
echo "1. Health Check:"
curl -s "$BASE_URL/api/health" | python3 -m json.tool
echo -e "\n"

# Test get quizzes (public)
echo "2. Get All Quizzes:"
curl -s "$BASE_URL/api/quizzes" | python3 -m json.tool
echo -e "\n"

# Test login
echo "3. Login (if admin exists):"
curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | python3 -m json.tool
echo -e "\n"

echo "Done!"

