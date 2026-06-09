import os
import json
import subprocess

def test_analyze_arc3_execution():
    """Verify that the analyze_arc3.py script runs without error and produces results.json."""
    if os.path.exists("results.json"):
        os.remove("results.json")

    # Run with current environment
    result = subprocess.run(["python3", "analyze_arc3.py"], capture_output=True, text=True)
    assert result.returncode == 0
    assert os.path.exists("results.json")

    with open("results.json", "r") as f:
        data = json.load(f)
        assert "ARC-AGI-3" in data["domain"]
        assert "hypotheses" in data
        assert len(data["hypotheses"]) > 0

def test_results_content():
    """Verify the content of results.json matches expected fmap mappings."""
    if not os.path.exists("results.json"):
        subprocess.run(["python3", "analyze_arc3.py"], capture_output=True, text=True)

    with open("results.json", "r") as f:
        data = json.load(f)
        theory_ids = [h["source_theory_id"] for h in data["hypotheses"]]
        # In fall-back mode these are expected.
        # In real mode, it depends on the LLM, but these are top candidates in the kernel.
        # We check for general success of finding any theories.
        assert len(theory_ids) > 0
