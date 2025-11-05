"""
Simple metric functions for trace evaluation.

This module defines a few basic scoring functions used by the evaluation
harness. The goal is to illustrate how one could compute scores such as
exact match and edit distance. You can expand this module with more
sophisticated metrics like semantic similarity or safety filters.
"""

from typing import Dict


def levenshtein(a: str, b: str) -> int:
    """Compute the Levenshtein distance between two strings."""
    if not a:
        return len(b)
    if not b:
        return len(a)
    if a[0] == b[0]:
        return levenshtein(a[1:], b[1:])
    return 1 + min(
        levenshtein(a[1:], b),    # deletion
        levenshtein(a, b[1:]),    # insertion
        levenshtein(a[1:], b[1:]) # substitution
    )


def compute_metrics(expected: str, actual: str) -> Dict[str, float]:
    """Compute a set of metrics comparing expected and actual outputs."""
    metrics: Dict[str, float] = {}
    if not expected:
        metrics["exact_match"] = 0.0
        metrics["edit_distance"] = len(actual)
    else:
        metrics["exact_match"] = 1.0 if expected.strip() == actual.strip() else 0.0
        metrics["edit_distance"] = float(levenshtein(expected, actual))
    return metrics