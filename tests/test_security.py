Python
import json
import os
import pytest
from jsonschema import validate, ValidationError

def test_security_schema_exists():
    assert os.path.exists("schemas/security_event_schema.json"), "security_event_schema.json is missing"

def test_valid_security_event():
    schema_path = "schemas/security_event_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    valid_event = {
        "event_id": "a2c4e680-1357-4b9d-8f2e-0a1b2c3d4e5f",
        "timestamp": "2026-10-22T14:35:00Z",
        "severity_level": "SEV-1",
        "threat_type": "CRYPTOGRAPHIC_HASH_MISMATCH",
        "source_endpoint": "node-cluster-a-01",
        "evidence_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }

    # Must validate cleanly without exception
    validate(instance=valid_event, schema=schema)

def test_invalid_severity_level_fails():
    schema_path = "schemas/security_event_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    invalid_event = {
        "event_id": "a2c4e680-1357-4b9d-8f2e-0a1b2c3d4e5f",
        "timestamp": "2026-10-22T14:35:00Z",
        "severity_level": "SEV-0",  # Invalid level (not in enum)
        "threat_type": "UNAUTHORIZED_STATE_DRIFT",
        "source_endpoint": "node-cluster-a-01",
        "evidence_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }

    with pytest.raises(ValidationError):
        validate(instance=invalid_event, schema=schema)
File Name: scripts/verify_security.py
Python
#!/usr/bin/env python3
"""
Division 005 — Security & Threat Intelligence Integrity Verification Script
BEAST System 3.0
"""

import os
import sys
import json

REQUIRED_FILES = [
    "DIVISION_005_SECURITY_INTELLIGENCE.md",
    "schemas/security_event_schema.json",
    "src/sentinel_engine.py",
    "tests/test_security.py"
]

def verify_structure():
    print("[-] Verifying Division 005 file layout...")
    missing = [f for f in REQUIRED_FILES if not os.path.exists(f)]
    if missing:
        print(f"[!] ERROR: Missing required security component files: {missing}")
        sys.exit(1)
    print("[+] All required Division 005 components present.")

def verify_schema():
    print("[-] Validating security_event_schema.json...")
    schema_path = "schemas/security_event_schema.json"
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            json.load(f)
        print("[+] security_event_schema.json contains valid JSON.")
    except Exception as e:
        print(f"[!] ERROR: security_event_schema.json validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=== BEAST System 3.0: Division 005 Verification ===")
    verify_structure()
    verify_schema()
    print("[*] Division 005 integrity verification completed successfully.")
    sys.exit(0)
File Name: .github/workflows/validate.yml
YAML
name: Division 005 Security & Threat Intelligence CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install jsonschema pytest

    - name: Verify Security Structure
      run: python3 scripts/verify_security.py

    - name: Execute Security Sentinel Tests
      run: pytest tests/
📂 Division 005 Inventory Summary
