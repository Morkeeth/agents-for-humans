"""GitHub Actions CI — judge-demo workflow must exist and call the kill-bar."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "judge-demo.yml"


def test_ci_workflow_exists():
    assert WORKFLOW.is_file(), "missing .github/workflows/judge-demo.yml"


def test_ci_workflow_runs_judge_demo():
    text = WORKFLOW.read_text()
    assert "judge-demo.sh" in text
    assert "stranger-pass.sh" in text
    assert "cold-clone-verify.sh" in text
    assert "ubuntu-latest" in text
