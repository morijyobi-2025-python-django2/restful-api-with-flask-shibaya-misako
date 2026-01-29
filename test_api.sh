#!/bin/bash

# Flask版 Syllabus API テストスクリプト
# Usage: ./test_api.sh

set -e

# カラー設定
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Flask版のURL
BASE_URL="http://localhost:5000/api/syllabi"

PASSED=0
FAILED=0

echo "=============================================================="
echo " Flask版 Syllabus API テスト開始"
echo "=============================================================="
echo "BASE_URL: $BASE_URL"
echo ""

check_status() {
    local expected=$1
    local actual=$2
    local name=$3

    if [ "$expected" = "$actual" ]; then
        echo -e "${GREEN}✓${NC} $name (status=$actual)"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $name (expected=$expected, actual=$actual)"
        ((FAILED++))
    fi
}

echo "=============================================================="
echo "1. GET /api/syllabi - 一覧取得"
echo "=============================================================="

RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL")
BODY=$(echo "$RESPONSE" | sed '$d')
STATUS=$(echo "$RESPONSE" | tail -n 1)

check_status "200" "$STATUS" "GET /api/syllabi"

echo "$BODY" | python3 -m json.tool 2>/dev/null | head -20
echo ""

echo "=============================================================="
echo "2. POST /api/syllabi - 新規作成"
echo "=============================================================="

PAYLOAD='{
  "subject_name": "テスト科目",
  "academic_year": 2025,
  "semester": "前期",
  "instructor": "テスト教員",
  "eligible_departments": ["情報工学科"],
  "class_schedule": [
    {"order": 1, "class_hours": 2, "content": "導入"},
    {"order": 2, "class_hours": 2, "content": "基礎"}
  ]
}'

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

BODY=$(echo "$RESPONSE" | sed '$d')
STATUS=$(echo "$RESPONSE" | tail -n 1)

check_status "201" "$STATUS" "POST /api/syllabi"

echo "$BODY" | python3 -m json.tool 2>/dev/null | head -20

CREATED_ID=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "作成されたID: $CREATED_ID"
echo ""

echo "=============================================================="
echo "3. GET /api/syllabi/{id} - 詳細取得"
echo "=============================================================="

RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL/$CREATED_ID")
BODY=$(echo "$RESPONSE" | sed '$d')
STATUS=$(echo "$RESPONSE" | tail -n 1)

check_status "200" "$STATUS" "GET /api/syllabi/$CREATED_ID"

echo "$BODY" | python3 -m json.tool 2>/dev/null | head -20
echo ""

echo "=============================================================="
echo "4. PUT /api/syllabi/{id} - 全更新"
echo "=============================================================="

PAYLOAD='{
  "subject_name": "更新後の科目",
  "academic_year": 2026,
  "semester": "後期",
  "instructor": "更新教員"
}'

RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/$CREATED_ID" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

BODY=$(echo "$RESPONSE" | sed '$d')
STATUS=$(echo "$RESPONSE" | tail -n 1)

check_status "200" "$STATUS" "PUT /api/syllabi/$CREATED_ID"

echo "$BODY" | python3 -m json.tool 2>/dev/null | head -20
echo ""

echo "=============================================================="
echo "5. PATCH /api/syllabi/{id} - 部分更新"
echo "=============================================================="

PAYLOAD='{
  "subject_name": "部分更新後の科目"
}'

RESPONSE=$(curl -s -w "\n%{http_code}" -X PATCH "$BASE_URL/$CREATED_ID" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

BODY=$(echo "$RESPONSE" | sed '$d')
STATUS=$(echo "$RESPONSE" | tail -n 1)

check_status "200" "$STATUS" "PATCH /api/syllabi/$CREATED_ID"

echo "$BODY" | python3 -m json.tool 2>/dev/null | head -20
echo ""

echo "=============================================================="
echo "6. DELETE /api/syllabi/{id} - 削除"
echo "=============================================================="

RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/$CREATED_ID")
STATUS=$(echo "$RESPONSE" | tail -n 1)

check_status "204" "$STATUS" "DELETE /api/syllabi/$CREATED_ID"
echo ""

echo "=============================================================="
echo "7. GET /api/syllabi/{id} - 削除確認 (404 expected)"
echo "=============================================================="

RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL/$CREATED_ID")
STATUS=$(echo "$RESPONSE" | tail -n 1)

check_status "404" "$STATUS" "GET /api/syllabi/$CREATED_ID after delete"
echo ""

echo "=============================================================="
echo "テスト結果"
echo "=============================================================="

TOTAL=$((PASSED + FAILED))
echo "合計: $TOTAL"
echo -e "${GREEN}成功: $PASSED${NC}"
echo -e "${RED}失敗: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ 全て成功${NC}"
else
    echo -e "${RED}✗ 失敗あり${NC}"
fi