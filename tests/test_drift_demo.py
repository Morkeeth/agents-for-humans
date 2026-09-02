"""drift-demo — live embarrassing case for doc drift."""
from magnet.drift_demo import run_drift_demo


def test_drift_demo_catches_fake_repo_and_passes_real():
    out = run_drift_demo()
    assert "fake repo" in out
    assert "[FAIL]" in out
    assert "exit code: 1" in out
    assert "this repo" in out
    assert "exit code: 0" in out
    assert "repro      magnet drift-demo" in out
