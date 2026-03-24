#!/usr/bin/env python3
"""
Test Custom Headers for Skill Identification
Tests if we can add custom headers to identify API calls from Skills
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

def build_headers(method: str, body: Optional[Dict] = None, include_custom: bool = True) -> Dict[str, str]:
    """Build authenticated headers for BitoPro API with optional custom headers."""
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

    headers = {
        'X-BITOPRO-APIKEY': API_KEY,
        'X-BITOPRO-PAYLOAD': payload,
        'X-BITOPRO-SIGNATURE': signature,
        'Content-Type': 'application/json',
        'User-Agent': 'bitopro-ai-trade/1.0.0 (Skill)'
    }

    # Add custom skill identification headers
    if include_custom:
        headers.update({
            'X-Execution-Source': 'Claude-Skill',
            'X-Skill-Name': 'bitopro/ai-trade',
            'X-Skill-Version': '1.0.0',
            'X-Client-Type': 'AI-Agent'
        })

    return headers

def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_public_api_with_headers():
    """Test 1: Public API with custom headers (no auth required)"""
    print_section("Test 1: Public API with Custom Headers")

    url = f"{BASE_URL}/tickers/btc_twd"

    # Test with custom headers
    headers = {
        'User-Agent': 'bitopro-ai-trade/1.0.0 (Skill)',
        'X-Execution-Source': 'Claude-Skill',
        'X-Skill-Name': 'bitopro/ai-trade',
        'X-Skill-Version': '1.0.0',
        'X-Client-Type': 'AI-Agent'
    }

    print(f"\n📤 Sending request to: {url}")
    print(f"\n📋 Headers:")
    for key, value in headers.items():
        print(f"   {key}: {value}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        ticker = data.get('data', {})
        last_price = float(ticker.get('lastPrice', 0))

        print(f"\n✅ SUCCESS - Public API accepts custom headers!")
        print(f"\n📊 Response Data:")
        print(f"   Last Price: {last_price:,.2f} TWD")
        print(f"   Status Code: {response.status_code}")

        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False

def test_authenticated_api_with_headers():
    """Test 2: Authenticated API with custom headers"""
    print_section("Test 2: Authenticated API with Custom Headers")

    url = f"{BASE_URL}/accounts/balance"
    headers = build_headers('GET', include_custom=True)

    print(f"\n📤 Sending authenticated request to: {url}")
    print(f"\n📋 Headers:")
    for key, value in headers.items():
        if 'SECRET' in key or 'SIGNATURE' in key:
            print(f"   {key}: {'*' * 20} (hidden)")
        else:
            print(f"   {key}: {value}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        balances = data.get('data', [])

        print(f"\n✅ SUCCESS - Authenticated API accepts custom headers!")
        print(f"\n💰 Account Balance (showing non-zero only):")
        print(f"   {'Currency':<10} {'Available':<20}")
        print(f"   {'-' * 30}")

        for bal in balances:
            available = float(bal.get('available', 0))
            if available > 0:
                print(f"   {bal['currency'].upper():<10} {available:<20.8f}")

        print(f"\n📊 Response Status: {response.status_code}")

        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False

def test_comparison():
    """Test 3: Compare requests with and without custom headers"""
    print_section("Test 3: Comparison - With vs Without Custom Headers")

    url = f"{BASE_URL}/tickers/eth_twd"

    # Test WITHOUT custom headers
    print("\n🔸 Request WITHOUT custom headers:")
    headers_standard = {
        'User-Agent': 'bitopro-ai-trade/1.0.0'
    }

    try:
        response1 = requests.get(url, headers=headers_standard, timeout=10)
        response1.raise_for_status()
        print(f"   Status: {response1.status_code} ✅")
    except Exception as e:
        print(f"   Error: {e} ❌")
        return False

    time.sleep(0.5)

    # Test WITH custom headers
    print("\n🔹 Request WITH custom headers:")
    headers_custom = {
        'User-Agent': 'bitopro-ai-trade/1.0.0 (Skill)',
        'X-Execution-Source': 'Claude-Skill',
        'X-Skill-Name': 'bitopro/ai-trade',
        'X-Skill-Version': '1.0.0',
        'X-Client-Type': 'AI-Agent'
    }

    try:
        response2 = requests.get(url, headers=headers_custom, timeout=10)
        response2.raise_for_status()
        print(f"   Status: {response2.status_code} ✅")
    except Exception as e:
        print(f"   Error: {e} ❌")
        return False

    print(f"\n✅ Both requests succeeded!")
    print(f"\n📝 Conclusion: BitoPro API accepts custom headers without issues")

    return True

def main():
    print("\n" + "=" * 70)
    print("  BitoPro Custom Headers Test")
    print("  Testing Skill Identification via HTTP Headers")
    print("=" * 70)
    print(f"\n  Account: {EMAIL}")
    print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    results = []

    # Test 1: Public API
    results.append(test_public_api_with_headers())
    time.sleep(1)

    # Test 2: Authenticated API
    results.append(test_authenticated_api_with_headers())
    time.sleep(1)

    # Test 3: Comparison
    results.append(test_comparison())

    # Summary
    print_section("Test Summary")

    test_names = [
        "Public API with custom headers",
        "Authenticated API with custom headers",
        "Comparison test (with vs without)"
    ]

    print("\n📊 Results:")
    for i, (name, result) in enumerate(zip(test_names, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {i}. {name}: {status}")

    all_passed = all(results)

    if all_passed:
        print("\n" + "=" * 70)
        print("  ✅ ALL TESTS PASSED")
        print("=" * 70)
        print("\n  建議的 Skill 識別 Headers:")
        print("    • X-Execution-Source: Claude-Skill")
        print("    • X-Skill-Name: bitopro/ai-trade")
        print("    • X-Skill-Version: 1.0.0")
        print("    • X-Client-Type: AI-Agent")
        print("    • User-Agent: bitopro-ai-trade/1.0.0 (Skill)")
        print("\n  這些 headers 可以安全地添加到所有 BitoPro API 請求中，")
        print("  用於識別和追蹤由 Skill 執行的交易。")
        print("=" * 70)
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
