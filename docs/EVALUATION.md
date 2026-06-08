# Evaluation

## Offline Ranking Task

Each eligible user contributes one held-out positive item. Models score all
candidate items not already seen in the user's training history. The goal is to
rank the held-out item in the top-K list.

## Metrics

| Metric | Meaning |
|---|---|
| `Precision@10` | Fraction of top-10 recommendations that match the held-out item |
| `Recall@10` | Fraction of held-out items recovered in top 10 |
| `MAP@10` | Mean average precision at 10; rewards higher rank positions |
| `NDCG@10` | Discounted gain; rewards hits near the top |
| `Catalog Coverage@10` | Fraction of all items that appear in at least one top-10 list |

With one held-out positive item per user, `Recall@10` is the clearest main
metric. `Precision@10` will be numerically smaller because only one relevant
item is known per user.

## Interpretation Rules

- Popularity can perform well but usually has low catalog coverage.
- Content-based scoring can improve cold-start interpretability but may miss
  behavior patterns.
- Collaborative filtering can capture behavior similarity but may recommend
  narrow or popular clusters.
- Hybrid models are preferred when they improve ranking quality without
  collapsing coverage.

## Business Metric Boundary

Offline metrics do not prove conversion, retention, or revenue impact. Those
claims require online A/B testing and product telemetry.
