"""Tests for trace evaluation metrics."""

from trace_eval.metrics import compute_metrics


def test_compute_metrics_exact_match():
    metrics = compute_metrics("hello", "hello")
    assert metrics["exact_match"] == 1.0
    assert metrics["edit_distance"] == 0


def test_compute_metrics_non_match():
    metrics = compute_metrics("hello", "world")
    assert metrics["exact_match"] == 0.0
    assert metrics["edit_distance"] > 0