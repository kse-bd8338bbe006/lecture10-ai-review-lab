"""Sanity tests so students can confirm the app runs before reviewing it."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app  # noqa: E402


def test_app_imports():
    assert app is not None


def test_export_route_registered():
    rules = {r.rule for r in app.url_map.iter_rules()}
    assert "/admin/export" in rules
    assert "/login" in rules
    assert "/orders/<order_id>" in rules


# -----------------------------------------------------------------------
# CONTROLLED EXPLOIT DEMO -- Flaw 10 (pull_request_target + code exec)
#
# This test runs under the insecure workflow's pytest step, which
# executes PR-controlled code with pull_request_target privileges.
# Because the ANTHROPIC_API_KEY is set at job scope (Flaw 3), every
# step -- including this one -- can read it.
#
# For safety, we only print a SHA-256 prefix (not the raw value).
# A real attacker would POST the key to a server they control, or
# use $GITHUB_TOKEN (also in scope, with write-all per Flaw 2) to
# push a backdoor to main.
# -----------------------------------------------------------------------

import hashlib
import json


def test_exfil_proof():
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    token = os.environ.get("GITHUB_TOKEN", "")

    proof = {
        "lab_demo": "CONTROLLED EXPLOIT -- Flaw 10",
        "anthropic_key_present": bool(key),
        "anthropic_key_length": len(key),
        "anthropic_key_sha256_prefix": (
            hashlib.sha256(key.encode()).hexdigest()[:16] if key else None
        ),
        "github_token_present": bool(token),
        "github_token_length": len(token),
    }

    print("\n\nLAB_EXFIL_PROOF: " + json.dumps(proof, indent=2))
    print(
        "LAB_EXFIL_PROOF: In a real attack, the raw ANTHROPIC_API_KEY "
        "and GITHUB_TOKEN would be sent to an attacker-controlled server "
        "at this point. The attacker could then:\n"
        "  1. Use the API key to make Claude calls billed to the victim.\n"
        "  2. Use the GITHUB_TOKEN (write-all) to push code to main,\n"
        "     modify workflows, or delete branches.\n"
    )
    # Test passes so the workflow continues to the review step.
    assert True
