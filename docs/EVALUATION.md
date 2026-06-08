# Evaluation

## Offline Ranking Task

Each eligible user contributes two held-out positive items:

- validation item: second-latest positive interaction,
- test item: latest positive interaction.

Models score all catalog items not already seen in the user's training history.
The goal is to rank the held-out item in the top-K list.

## Metrics

| Metric | Meaning |
|---|---|
| `Precision@10` | Fraction of top-10 recommendations that match the held-out item |
| `Recall@10` | Fraction of held-out items recovered in top 10 |
| `MAP@10` | Mean average precision at 10; rewards higher rank positions |
| `NDCG@10` | Discounted gain; rewards hits near the top |
| `Catalog Coverage@10` | Fraction of all items that appear in at least one top-10 list |
| `Long-tail Share@10` | Fraction of recommendations from outside the top popularity head |
| `Intra-list Diversity@10` | Average genre dissimilarity inside each recommendation list |
| `Average Distinct Genres@10` | Number of genres represented in each recommendation list |
| `Gini Index@10` | Recommendation concentration; lower is more evenly distributed |

With one held-out positive item per user, `Recall@10` is the clearest main
metric. `Precision@10` will be numerically smaller because only one relevant
item is known per user.

## Interpretation Rules

- Popularity can perform well but usually has low catalog coverage.
- Content-based scoring can improve cold-start interpretability but may miss
  behavior patterns.
- ItemKNN is a strong collaborative baseline for user-item histories.
- BPR and ALS check embedding-based collaborative behavior.
- Hybrid rankers are preferred when they improve ranking quality without
  collapsing coverage.

## Validation And Seed Variance

The ranker is tuned on validation and reported on test. The main model table
reports mean and standard deviation across seeds 11, 42, and 73.

## Sampled-Negative Evaluation

The project also reports a sampled 100-negative task. For each user, the heldout
positive item is ranked against 100 sampled negatives. This is easier than
all-item ranking and should be interpreted as a diagnostic metric, not a
replacement for all-item Recall@10.

## Cold-Start Evaluation

The cold-start experiment hides low-interaction items from collaborative
training, then evaluates fallback scores on users whose test item is one of
those hidden low-interaction items.

The compared fallback strategies are:

- popularity fallback,
- content fallback,
- hybrid content/novelty fallback.

## Business Metric Boundary

Offline metrics do not prove conversion, retention, or revenue impact. Those
claims require online A/B testing and product telemetry.
