#!/usr/bin/env python3
"""
Test clientId Parameter for Skill Order Identification
Tests using clientId=2147483647 to identify orders from AI Trade Skill
"""

import os
import sys
import json
import time
import hmac
import hashlib
import base64
import requests
from typing import Dict, Optional

# --- User Credentials ---
API_KEY = "c37801439dc0c2c5896d95e1204042c7"
API_SECRET = "$2a$12$dPs6vWUkBHc3sbTm3UB0Ju1cpC9VN9wfPgQTTGuL/b1lFrlZAJyIS"
EMAIL = "vividboy@msn.com"

BASE_URL = "https://api.bitopro.com/v3"

# Skill identification constant
SKILL_CLIENT_ID = 2147483647  # Maximum allowed value, reserved for Skill orders

def build_headers(method: str, body: Optional[Dict] = None) -> Dict[str, str]:
    """Build authenticated headers for BitoPro API."""
    nonce = int(time.time() * 1000)

    if method.upper() in ('GET', 'DELETE'):
        payload_obj = {"identity": EMAIL, "nonce": nonce}
    else:
        payload_obj = {**(body or {}), "nonce": nonce}

    payload = base64.b64encode(
        json.dumps(payload_obj).encode('utf-8')
    ).decode('utf-8')

    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha384
    ).hexdigest()

    return {
        'X-BITOPRO-APIKEY': API_KEY,
        'X-BITOPRO-PAYLOAD': payload,
        'X-BITOPRO-SIGNATURE': signature,
        'Content-Type': 'application/json',
        'User-Agent': 'bitopro-ai-trade/1.0.0 (Skill)',
        'X-Execution-Source': 'Claude-Skill',
        'X-Skill-Name': 'bitopro/ai-trade',
        'X-Skill-Version': '1.0.0'
    }

def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_get_balance():
    """Check current account balance"""
    print_section("Step 1: Check Account Balance")

    url = f"{BASE_URL}/accounts/balance"
    headers = build_headers('GET')

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        balances = {}
        print("\n✅ Balance Retrieved\n")
        print(f"{'Currency':<10} {'Available':<20}")
        print("-" * 30)

        for bal in data.get('data', []):
            available = float(bal.get('available', 0))
            if available > 0:
                print(f"{bal['currency'].upper():<10} {available:<20.8f}")
                balances[bal['currency'].upper()] = available

        return balances

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def test_execute_order_with_client_id(pair: str, action: str, amount: str):
    """Execute market order with clientId for Skill identification"""
    print_section(f"Step 2: Execute Order with clientId={SKILL_CLIENT_ID}")

    print(f"\n📝 Order Details:")
    print(f"   Pair:     {pair.upper()}")
    print(f"   Action:   {action.upper()}")
    print(f"   Amount:   {amount} {'TWD' if action.upper() == 'BUY' else pair.split('_')[0].upper()}")
    print(f"   Type:     MARKET")
    print(f"   ClientID: {SKILL_CLIENT_ID} (Skill Identifier)")

    url = f"{BASE_URL}/orders/{pair}"
    nonce = int(time.time() * 1000)

    body = {
        "action": action.upper(),
        "amount": amount,
        "type": "MARKET",
        "timestamp": nonce,
        "clientId": SKILL_CLIENT_ID,  # Add Skill identifier
        "nonce": nonce
    }

    headers = build_headers('POST', body)

    print("\n🚀 Sending order with Skill clientId...")
    time.sleep(1)

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)

        print(f"\n📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Order Executed Successfully!")
            print(f"\n📋 Order Response:")
            print(f"   Order ID:    {data.get('orderId')}")
            print(f"   Action:      {data.get('action')}")
            print(f"   Amount:      {data.get('amount')}")
            print(f"   Price:       {data.get('price', 'MARKET')}")
            print(f"   Client ID:   {data.get('clientId')} {'✅ Skill ID confirmed!' if data.get('clientId') == SKILL_CLIENT_ID else '⚠️ Different ID'}")
            print(f"   Timestamp:   {data.get('timestamp')}")
            print(f"   TimeInForce: {data.get('timeInForce', 'N/A')}")
            return data
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"\n❌ Order Failed")
            print(f"\n   Response: {json.dumps(error_data, indent=2)}")
            return None

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def test_get_order_history():
    """Get recent order history to verify clientId"""
    print_section("Step 3: Verify clientId in Order History")

    url = f"{BASE_URL}/orders/history/btc_twd"
    headers = build_headers('GET')

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        orders = data.get('data', [])

        print(f"\n✅ Order History Retrieved")
        print(f"\n🔍 Looking for orders with clientId={SKILL_CLIENT_ID}:\n")

        skill_orders = []
        for order in orders[:10]:  # Check last 10 orders
            if order.get('clientId') == SKILL_CLIENT_ID:
                skill_orders.append(order)
                print(f"   ✅ Found Skill Order:")
                print(f"      Order ID:  {order.get('id')}")
                print(f"      Action:    {order.get('action')}")
                print(f"      Status:    {order.get('status')}")
                print(f"      ClientID:  {order.get('clientId')}")
                print(f"      Created:   {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(order.get('createdTimestamp', 0) / 1000))}")
                print()

        if skill_orders:
            print(f"   📊 Total Skill orders found: {len(skill_orders)}")
        else:
            print(f"   ℹ️  No Skill orders found in recent history")
            print(f"      (This is normal if this is your first test)")

        return skill_orders

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def main():
    print("\n" + "=" * 70)
    print("  BitoPro AI Trade Skill - clientId Identification Test")
    print("  Using clientId=2147483647 to identify Skill orders")
    print("=" * 70)
    print(f"\n  Account:   {EMAIL}")
    print(f"  API Key:   {API_KEY[:8]}...{API_KEY[-4:]}")
    print(f"  Skill ID:  {SKILL_CLIENT_ID}")
    print(f"  Time:      {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: Check balance
    balances = test_get_balance()
    if not balances:
        print("\n❌ Failed to get balance. Aborting.")
        return 1

    twd_balance = balances.get('TWD', 0)
    print(f"\n💰 TWD Balance: {twd_balance:,.2f} TWD")

    if twd_balance < 200:
        print(f"\n❌ Insufficient TWD balance (need at least 200 TWD)")
        print(f"   Current: {twd_balance:.2f} TWD")
        return 1

    # Step 2: Execute order with clientId
    print("\n\n⚠️  Ready to execute REAL order with Skill clientId ⚠️")
    print("   This will spend 200 TWD to buy BTC with clientId=2147483647")
    print("\n   Proceeding in 3 seconds...")
    time.sleep(3)

    order_result = test_execute_order_with_client_id("btc_twd", "BUY", "200")

    if not order_result:
        print("\n❌ Order execution failed. Aborting.")
        return 1

    # Step 3: Wait and check order history
    print("\n   Waiting 2 seconds before checking order history...")
    time.sleep(2)

    order_history = test_get_order_history()

    # Final Summary
    print_section("Test Summary")

    if order_result and order_result.get('clientId') == SKILL_CLIENT_ID:
        print("\n✅ ALL TESTS PASSED!")
        print(f"\n📊 Results:")
        print(f"   ✅ Balance check: PASS")
        print(f"   ✅ Order execution with clientId: PASS")
        print(f"   ✅ ClientId verification: PASS")
        print(f"\n📋 Order Details:")
        print(f"   Order ID:  {order_result.get('orderId')}")
        print(f"   Client ID: {order_result.get('clientId')} (Skill Identifier)")
        print(f"   Amount:    200 TWD")
        print(f"   Status:    Executed")
        print("\n" + "=" * 70)
        print("  ✅ clientId=2147483647 可成功用於識別 Skill 訂單")
        print("=" * 70)
        print("\n  建議實施方式:")
        print("    • 所有 Skill 執行的訂單都帶上 clientId=2147483647")
        print("    • 可透過訂單歷史的 clientId 欄位篩選 Skill 訂單")
        print("    • 結合 X-Execution-Source header 提供雙重識別")
        print("    • 在訂單確認時顯示 clientId 讓用戶知道是 Skill 執行")
        print("=" * 70)
        return 0
    else:
        print("\n❌ TEST FAILED")
        print(f"\n   Expected clientId: {SKILL_CLIENT_ID}")
        print(f"   Received clientId: {order_result.get('clientId') if order_result else 'N/A'}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
