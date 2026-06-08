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
    sampled_metrics: pd.DataFrame | None = None,
    cold_start_metrics: pd.DataFrame | None = None,
) -> str:
    """Create the Markdown final report."""
    columns = [
        "model",
        f"recall_at_{top_k}_mean",
        f"recall_at_{top_k}_std",
        f"ndcg_at_{top_k}_mean",
        f"ndcg_at_{top_k}_std",
        f"map_at_{top_k}_mean",
        f"catalog_coverage_at_{top_k}_mean",
        f"long_tail_share_at_{top_k}_mean",
        f"gini_index_at_{top_k}_mean",
    ]
    metric_table = _markdown_table(metrics[columns])
    sampled_table = _markdown_table(sampled_metrics) if sampled_metrics is not None else "Not generated."
    cold_start_table = (
        _markdown_table(cold_start_metrics) if cold_start_metrics is not None else "Not generated."
    )
    return f"""# Final Report

## Dataset Summary

| Metric | Value |
|---|---:|
| Ratings | {dataset_summary["ratings"]:,} |
| Users | {dataset_summary["users"]:,} |
| Catalog items | {dataset_summary["items"]:,} |
| Rated items | {dataset_summary["rated_items"]:,} |
| Positive interactions | {dataset_summary["positive_interactions"]:,} |
| Training positives | {dataset_summary["train_positive_interactions"]:,} |
| Validation users | {dataset_summary["validation_users"]:,} |
| Evaluation users | {dataset_summary["evaluation_users"]:,} |
| User-item matrix sparsity | {dataset_summary["sparsity_percent"]:.4f}% |
| Seeds | {", ".join(str(seed) for seed in dataset_summary["seeds"])} |
| Candidate retrieval depth | {dataset_summary["candidate_k"]:,} |
| Sampled negatives | {dataset_summary["sampled_negatives"]:,} |

## Split Design

For every user with at least three positive interactions:

- train uses all positive interactions except the latest two,
- validation uses the second-latest positive item,
- test uses the latest positive item.

Ranker weights are selected on validation. Final numbers below are test-set
means and standard deviations across seeds.

## All-Item Model Comparison

{metric_table}

## Best Offline Model

The best all-item model by mean Recall@{top_k}, then mean NDCG@{top_k}, is
`{best_model}`.

## Sampled 100-Negative Evaluation

{sampled_table}

This is an easier diagnostic task than all-item ranking because each user has
one held-out positive item plus 100 sampled negatives. It should not be mixed
with all-item Recall@{top_k} or NDCG@{top_k}.

## Cold-Start Experiment

{cold_start_table}

The cold-start experiment hides low-interaction items from collaborative
training, then compares fallback behavior. A percentage lift over popularity is
not reported when popularity scores zero.

## Interpretation

The popularity baseline is a useful lower bound because it measures how much
recommendation quality can be achieved without personalization. ItemKNN and BPR
capture behavior similarity. Content-based scoring adds metadata awareness and
helps cold-start cases. The two-stage ranker retrieves candidates with behavior
models, then re-ranks with collaborative, content, popularity, and novelty
signals.

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
