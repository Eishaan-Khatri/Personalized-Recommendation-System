# Limitations

## Data

The project uses MovieLens 1M, not private platform data. Movie ratings are a
useful benchmark for recommender systems but do not fully represent story
reading behavior.

## Feedback

Ratings are explicit feedback. Real content platforms rely heavily on implicit
signals such as reads, dwell time, completion, follows, saves, skips, and session
continuity.

## Offline Evaluation

Offline ranking metrics do not prove business impact. Conversion, retention, and
engagement improvements require online controlled experiments.

## Model Scope

The implemented models are intentionally explainable and lightweight:

- popularity baseline,
- content-based scoring,
- ItemKNN,
- BPR matrix factorization,
- implicit ALS,
- two-stage hybrid re-ranking,
- validation tuning,
- sampled-negative evaluation,
- cold-start fallback analysis.

Deep sequence models, graph neural recommenders, approximate nearest-neighbor
serving, and real-time feature pipelines are natural future extensions but are
not required for the core proof.

## Metric Caveats

All-item Recall@10 and sampled-negative HitRate@10 are not comparable. The
sampled-negative task is easier because each user has one positive and only 100
sampled negatives. The README reports both but keeps them separate.

Cold-start percentage lift is not reported when the popularity fallback has a
zero score. In that case, absolute Recall@10 and NDCG@10 are the defensible
numbers.

## Responsible Claiming

Safe claims:

- benchmark dataset scale,
- validation/test split design,
- mean and standard deviation across repeated seeds,
- measured offline ranking metrics,
- sampled-negative diagnostic metrics,
- cold-start fallback metrics,
- generated recommendation outputs,
- implemented model families,
- documented product mapping.

Unsafe claims without additional evidence:

- real conversion lift,
- real retention lift,
- production deployment,
- private Pratilipi data usage,
- live user impact,
- causal A/B test results.
