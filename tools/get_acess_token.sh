#!/usr/bin/env bash

# Load environment variables from .env if present. This allows the script to use
# configuration such as KC_BASE_URL, KC_REALM, KC_APP_CLIENT_ID and
# KC_APP_CLIENT_SECRET defined in the repository root.
if [[ -f ".env" ]]; then
  set -a
  source ".env"
  set +a
else
  echo "Error: .env file not found in $(pwd)" >&2
  exit 1
fi

USERNAME="${1:-demo_user_1}"
PASSWORD="${2:-123456}"

KC_BASE_URL='http://localhost:8080/'

TOKEN_URL="${KC_BASE_URL}realms/${KC_REALM}/protocol/openid-connect/token"

curl -X POST \
  "${TOKEN_URL}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=${KC_APP_CLIENT_ID}" \
  -d "client_secret=${KC_APP_CLIENT_SECRET}" \
  -d "username=${USERNAME}" \
  -d "password=${PASSWORD}" \
  -d "grant_type=password" \
  | jq
