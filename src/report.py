"""Report generation."""

from __future__ import annotations

import pandas as pd


def _markdown_table(frame: pd.DataFrame) -> str:
    """Render a small DataFrame as a Markdown table without extra dependencies."""
    columns = list(frame.columns)
    rows = []
    for _, row in frame.iterrows():
        values = []
        for column in columns:
            value = row[column]
            if isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        rows.append(values)

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(values) + " |" for values in rows]
    return "\n".join([header, separator, *body])


def build_final_report(
    metrics: pd.DataFrame,
    dataset_summary: dict[str, int | float],
    best_model: str,
    top_k: int,
) -> str:
    """Create the Markdown final report."""
    metric_table = _markdown_table(metrics)
    return f"""# Final Report

## Dataset Summary

| Metric | Value |
|---|---:|
| Ratings | {dataset_summary["ratings"]:,} |
| Users | {dataset_summary["users"]:,} |
| Items | {dataset_summary["items"]:,} |
| Positive interactions | {dataset_summary["positive_interactions"]:,} |
| Training positives | {dataset_summary["train_positive_interactions"]:,} |
| Evaluation users | {dataset_summary["evaluation_users"]:,} |
| User-item matrix sparsity | {dataset_summary["sparsity_percent"]:.4f}% |

## Model Comparison

{metric_table}

## Best Offline Model

The best model by Recall@{top_k}, then NDCG@{top_k}, is `{best_model}`.

## Interpretation

The popularity baseline is a useful lower bound because it measures how much
recommendation quality can be achieved without personalization. Content-based
scoring adds metadata awareness. Collaborative filtering learns behavior-based
similarity. The hybrid model blends these signals, which is closer to how a
content-discovery product would combine behavioral, item, and popularity signals.

## Product Mapping

For a platform like Pratilipi, the same structure maps to reader-story
recommendations:

- users become readers or listeners,
- items become stories, authors, comics, or audio content,
- genres become language, theme, format, and category features,
- batch top-K scoring becomes personalized homepage or feed refresh,
- offline metrics become pre-launch checks before online experimentation.

## Claim Boundary

The reported numbers are offline benchmark metrics. They do not claim conversion,
retention, revenue, or production impact.
"""
