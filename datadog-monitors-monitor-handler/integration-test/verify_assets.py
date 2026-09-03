#!/usr/bin/env python3
"""Verify monitor assets via Datadog API after CFN stack deployment."""
import json
import os
import sys
from pathlib import Path

import requests

CONFIG_PATH = Path.home() / ".cfn-cli" / "typeConfiguration.json"


def load_credentials():
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    creds = cfg["DatadogCredentials"]
    return creds["ApiKey"], creds["ApplicationKey"]


def get_monitor(monitor_id: int):
    api_key, app_key = load_credentials()
    resp = requests.get(
        f"https://api.datadoghq.com/api/v1/monitor/{monitor_id}",
        params={"with_assets": "true"},
        headers={
            "DD-API-KEY": api_key,
            "DD-APPLICATION-KEY": app_key,
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def verify_assets(monitor_id: int, expected_count: int | None = None):
    monitor = get_monitor(monitor_id)
    assets = monitor.get("assets") or []
    print(f"Monitor {monitor_id}: {monitor.get('name')}")
    print(f"  assets count: {len(assets)}")
    for i, asset in enumerate(assets):
        print(f"  [{i}] category={asset.get('category')} name={asset.get('name')}")
        print(f"      url={asset.get('url')}")
        if asset.get("resource_type"):
            print(f"      resource_type={asset.get('resource_type')} resource_key={asset.get('resource_key')}")
    if expected_count is not None and len(assets) != expected_count:
        print(f"FAIL: expected {expected_count} assets, got {len(assets)}")
        return False
    if not assets:
        print("FAIL: no assets on monitor")
        return False
    print("PASS")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <monitor_id> [expected_count]")
        sys.exit(1)
    mid = int(sys.argv[1])
    exp = int(sys.argv[2]) if len(sys.argv) > 2 else None
    ok = verify_assets(mid, exp)
    sys.exit(0 if ok else 1)
