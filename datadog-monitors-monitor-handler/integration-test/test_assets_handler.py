#!/usr/bin/env python3
"""Handler-level integration tests for monitor Assets via the CFN resource handler."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Handler deps live in the packaged build directory.
BUILD_DIR = Path(__file__).resolve().parents[1] / "build"
sys.path.insert(0, str(BUILD_DIR))

from cloudformation_cli_python_lib import Action  # noqa: E402
from datadog_monitors_monitor.handlers import create_handler, delete_handler, read_handler, update_handler  # noqa: E402
from datadog_monitors_monitor.models import ResourceHandlerRequest, ResourceModel, TypeConfigurationModel  # noqa: E402

CONFIG_PATH = Path.home() / ".cfn-cli" / "typeConfiguration.json"
NOTEBOOK_ID = "15414666"


def load_type_configuration() -> TypeConfigurationModel:
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    return TypeConfigurationModel._deserialize(cfg)


def make_request(action: Action, model: ResourceModel, previous: ResourceModel | None = None):
    return ResourceHandlerRequest(
        clientRequestToken="test-token",
        desiredResourceState=model,
        previousResourceState=previous,
        desiredResourceTags=None,
        previousResourceTags=None,
        systemTags=None,
        previousSystemTags=None,
        typeConfiguration=load_type_configuration(),
        awsAccountId="876496569223",
        region="us-east-1",
        awsPartition="aws",
        logicalResourceIdentifier="TestMonitor",
        stackId="arn:aws:cloudformation:us-east-1:876496569223:stack/test/00000000-0000-0000-0000-000000000001",
        nextToken=None,
    )


def assert_success(event, label: str):
    if event.status.name != "SUCCESS":
        raise AssertionError(f"{label}: expected SUCCESS, got {event.status.name}: {event.message}")
    if event.resourceModel is None:
        raise AssertionError(f"{label}: missing resourceModel in response")
    print(f"PASS: {label}")


def run_tests() -> None:
    monitor_id = None
    try:
        # 1. Create with external runbook
        model = ResourceModel._deserialize(
            {
                "Type": "query alert",
                "Query": "avg(last_5m):avg:system.cpu.user{*} > 100",
                "Name": "CFN Handler Integration - External Runbook",
                "Message": "handler integration test",
                "Options": {"Thresholds": {"Critical": 100}},
                "Assets": [
                    {
                        "Category": "runbook",
                        "Name": "External Runbook",
                        "Url": "https://example.com/runbooks/cpu-troubleshooting",
                    }
                ],
            }
        )
        create_event = create_handler(None, make_request(Action.CREATE, model), {})
        assert_success(create_event, "handler create external runbook")
        monitor_id = create_event.resourceModel.Id

        # 2. Read returns assets (requires with_assets=True in read_handler)
        read_event = read_handler(None, make_request(Action.READ, create_event.resourceModel), {})
        assert_success(read_event, "handler read external runbook")
        assets = read_event.resourceModel.Assets or []
        if len(assets) != 1 or assets[0].Url != "https://example.com/runbooks/cpu-troubleshooting":
            raise AssertionError(f"read assets mismatch: {assets}")

        # 3. Update to notebook + external runbooks
        previous = read_event.resourceModel
        updated = ResourceModel._deserialize(
            {
                "Type": previous.Type,
                "Query": previous.Query,
                "Name": previous.Name,
                "Message": previous.Message,
                "Options": {"Thresholds": {"Critical": 100}},
                "Id": previous.Id,
                "Assets": [
                    {
                        "Category": "runbook",
                        "Name": "Notebook Runbook",
                        "Url": f"/notebook/{NOTEBOOK_ID}/runbook",
                        "ResourceType": "notebook",
                        "ResourceKey": NOTEBOOK_ID,
                    }
                ],
            }
        )
        update_event = update_handler(None, make_request(Action.UPDATE, updated, previous), {})
        assert_success(update_event, "handler update notebook runbook")
        assets = update_event.resourceModel.Assets or []
        if len(assets) != 1 or assets[0].ResourceType != "notebook":
            raise AssertionError(f"update assets mismatch: {assets}")

        # 4. Update remove assets
        previous = update_event.resourceModel
        cleared = ResourceModel._deserialize(
            {
                "Type": previous.Type,
                "Query": previous.Query,
                "Name": previous.Name,
                "Message": previous.Message,
                "Options": {"Thresholds": {"Critical": 100}},
                "Id": previous.Id,
                "Assets": [],
            }
        )
        clear_event = update_handler(None, make_request(Action.UPDATE, cleared, previous), {})
        assert_success(clear_event, "handler update remove assets")
        assets = clear_event.resourceModel.Assets or []
        if assets:
            raise AssertionError(f"expected no assets after clear, got {assets}")

        print("\nAll handler integration tests passed (4/4)")

    finally:
        if monitor_id is not None:
            delete_model = ResourceModel._deserialize(
                {
                    "Id": monitor_id,
                    "Type": "query alert",
                    "Query": "avg(last_5m):avg:system.cpu.user{*} > 100",
                }
            )
            delete_handler(None, make_request(Action.DELETE, delete_model), {})
            print(f"Cleaned up monitor {monitor_id}")


if __name__ == "__main__":
    try:
        run_tests()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
