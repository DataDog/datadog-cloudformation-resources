#!/usr/bin/env python3
"""End-to-end integration tests for monitor Assets (runbooks).

Exercises the same Datadog API flows the CFN handler uses when Assets are set
on create, update, and read. Cleans up created monitors on exit.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests

CONFIG_PATH = Path.home() / ".cfn-cli" / "typeConfiguration.json"
NOTEBOOK_ID = "15414666"
BASE_URL = "https://api.datadoghq.com/api/v1"
TEST_PREFIX = "CFN Assets Integration Test"


def load_headers() -> dict[str, str]:
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    creds = cfg["DatadogCredentials"]
    return {
        "DD-API-KEY": creds["ApiKey"],
        "DD-APPLICATION-KEY": creds["ApplicationKey"],
        "Content-Type": "application/json",
    }


def create_monitor(payload: dict) -> int:
    resp = requests.post(f"{BASE_URL}/monitor", headers=load_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["id"]


def get_monitor(monitor_id: int) -> dict:
    resp = requests.get(
        f"{BASE_URL}/monitor/{monitor_id}",
        headers=load_headers(),
        params={"with_assets": "true"},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def update_monitor(monitor_id: int, payload: dict) -> dict:
    resp = requests.put(f"{BASE_URL}/monitor/{monitor_id}", headers=load_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def delete_monitor(monitor_id: int) -> None:
    resp = requests.delete(f"{BASE_URL}/monitor/{monitor_id}", headers=load_headers(), timeout=60)
    resp.raise_for_status()


def assert_assets(monitor: dict, expected: list[dict], label: str) -> None:
    assets = monitor.get("assets") or []
    if len(assets) != len(expected):
        raise AssertionError(f"{label}: expected {len(expected)} assets, got {len(assets)}: {assets}")

    for i, exp in enumerate(expected):
        got = assets[i]
        for key in ("category", "name", "url"):
            if got.get(key) != exp[key]:
                raise AssertionError(f"{label}: asset[{i}].{key} expected {exp[key]!r}, got {got.get(key)!r}")
        if "resource_type" in exp and got.get("resource_type") != exp["resource_type"]:
            raise AssertionError(
                f"{label}: asset[{i}].resource_type expected {exp['resource_type']!r}, got {got.get('resource_type')!r}"
            )
        if "resource_key" in exp and got.get("resource_key") != exp["resource_key"]:
            raise AssertionError(
                f"{label}: asset[{i}].resource_key expected {exp['resource_key']!r}, got {got.get('resource_key')!r}"
            )
    print(f"PASS: {label}")


def base_monitor(name: str) -> dict:
    return {
        "type": "query alert",
        "query": "avg(last_5m):avg:system.cpu.user{*} > 100",
        "name": f"{TEST_PREFIX} - {name}",
        "message": "Integration test monitor for Assets",
        "options": {"thresholds": {"critical": 100}},
    }


def run_tests() -> None:
    created: list[int] = []
    passed = 0
    try:
        # 1. External runbook URL on create
        payload = base_monitor("External Runbook")
        payload["assets"] = [
            {
                "category": "runbook",
                "name": "External Runbook",
                "url": "https://example.com/runbooks/cpu-troubleshooting",
            }
        ]
        mid = create_monitor(payload)
        created.append(mid)
        time.sleep(2)
        monitor = get_monitor(mid)
        assert_assets(
            monitor,
            [{"category": "runbook", "name": "External Runbook", "url": "https://example.com/runbooks/cpu-troubleshooting"}],
            "create external runbook",
        )
        passed += 1

        # 2. Notebook runbook on create
        payload = base_monitor("Notebook Runbook")
        payload["assets"] = [
            {
                "category": "runbook",
                "name": "Datadog Notebook Runbook",
                "url": f"/notebook/{NOTEBOOK_ID}/cpu-troubleshooting",
                "resource_type": "notebook",
                "resource_key": NOTEBOOK_ID,
            }
        ]
        mid = create_monitor(payload)
        created.append(mid)
        time.sleep(2)
        monitor = get_monitor(mid)
        assert_assets(
            monitor,
            [
                {
                    "category": "runbook",
                    "name": "Datadog Notebook Runbook",
                    "url": f"/notebook/{NOTEBOOK_ID}/cpu-troubleshooting",
                    "resource_type": "notebook",
                    "resource_key": NOTEBOOK_ID,
                }
            ],
            "create notebook runbook",
        )
        passed += 1

        # 3. Update: replace single asset with two assets
        payload = base_monitor("Asset Updates")
        payload["assets"] = [
            {
                "category": "runbook",
                "name": "Initial Runbook",
                "url": "https://example.com/runbooks/initial",
            }
        ]
        mid = create_monitor(payload)
        created.append(mid)
        time.sleep(2)

        update_payload = base_monitor("Asset Updates")
        update_payload["assets"] = [
            {
                "category": "runbook",
                "name": "External Runbook v2",
                "url": "https://example.com/runbooks/load-troubleshooting",
            },
            {
                "category": "runbook",
                "name": "Notebook Runbook v2",
                "url": f"/notebook/{NOTEBOOK_ID}/load-runbook",
                "resource_type": "notebook",
                "resource_key": NOTEBOOK_ID,
            },
        ]
        update_monitor(mid, update_payload)
        time.sleep(2)
        monitor = get_monitor(mid)
        assert_assets(
            monitor,
            [
                {
                    "category": "runbook",
                    "name": "External Runbook v2",
                    "url": "https://example.com/runbooks/load-troubleshooting",
                },
                {
                    "category": "runbook",
                    "name": "Notebook Runbook v2",
                    "url": f"/notebook/{NOTEBOOK_ID}/load-runbook",
                    "resource_type": "notebook",
                    "resource_key": NOTEBOOK_ID,
                },
            ],
            "update add multiple runbooks",
        )
        passed += 1

        # 4. Update: remove all assets
        update_payload = base_monitor("Asset Updates")
        update_payload["assets"] = []
        update_monitor(mid, update_payload)
        time.sleep(2)
        monitor = get_monitor(mid)
        assets = monitor.get("assets") or []
        if assets:
            raise AssertionError(f"remove assets: expected empty assets, got {assets}")
        print("PASS: update remove all runbooks")
        passed += 1

    finally:
        for mid in created:
            try:
                delete_monitor(mid)
                print(f"Cleaned up monitor {mid}")
            except requests.HTTPError as exc:
                print(f"WARN: failed to delete monitor {mid}: {exc}", file=sys.stderr)

    print(f"\nAll integration tests passed ({passed}/4)")


if __name__ == "__main__":
    try:
        run_tests()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
