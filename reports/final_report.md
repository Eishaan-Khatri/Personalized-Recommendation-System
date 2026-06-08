# Final Report

## Dataset Summary

| Metric | Value |
|---|---:|
| Ratings | 1,000,209 |
| Users | 6,040 |
| Items | 3,883 |
| Positive interactions | 575,281 |
| Training positives | 569,244 |
| Evaluation users | 6,037 |
| User-item matrix sparsity | 95.7353% |

## Model Comparison

| model | evaluated_users | precision_at_10 | recall_at_10 | map_at_10 | ndcg_at_10 | catalog_coverage_at_10 | unique_recommended_items | avg_distinct_genres_at_10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hybrid | 6037 | 0.0050 | 0.0500 | 0.0164 | 0.0241 | 0.1594 | 619 | 8.6598 |
| popularity | 6037 | 0.0041 | 0.0406 | 0.0130 | 0.0193 | 0.0296 | 115 | 9.5556 |
| collaborative_filtering | 6037 | 0.0038 | 0.0384 | 0.0114 | 0.0177 | 0.1537 | 597 | 9.8029 |
| content_based | 6037 | 0.0016 | 0.0156 | 0.0048 | 0.0073 | 0.7126 | 2767 | 3.7592 |

## Best Offline Model

The best model by Recall@10, then NDCG@10, is `hybrid`.

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
