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
- implicit-feedback collaborative filtering,
- hybrid scoring.

Deep sequence models, graph neural recommenders, approximate nearest-neighbor
serving, and real-time feature pipelines are natural future extensions but are
not required for the core proof.

## Responsible Claiming

Safe claims:

- benchmark dataset scale,
- measured offline ranking metrics,
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
