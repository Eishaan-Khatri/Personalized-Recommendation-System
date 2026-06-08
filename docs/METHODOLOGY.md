# Methodology

## Objective

Generate personalized top-K item recommendations using user behavior and item
attributes, then evaluate recommendation quality with offline ranking metrics,
seed variance, validation tuning, sampled-negative checks, and cold-start
fallback analysis.

## Interaction Framing

Ratings of 4 or 5 are treated as positive implicit interactions.

For each user with at least three positive interactions:

- all except the latest two positives are used for training,
- the second-latest positive item is used for validation,
- the latest positive item is used for final test evaluation.

This creates a practical next-item recommendation task:

> Given the user's previous positive interactions, can the system recover hidden
> future positive items in the top-K recommendations?

## Models

### Popularity Baseline

Ranks items by positive interaction count in the training set.

Purpose:

- basic sanity check,
- measures how far personalized models improve beyond popularity,
- exposes popularity bias.

### Content-Based Recommender

Builds a user profile from the average genre vector of the user's training
items, then scores candidate items by cosine similarity.

Purpose:

- handles sparse user histories better than pure collaborative filtering,
- demonstrates use of item metadata,
- maps naturally to story genre, language, theme, and format signals.

### ItemKNN

Builds item-item collaborative similarity from co-interaction patterns and
scores candidates by similarity to each user's history.

Purpose:

- strong collaborative baseline,
- interpretable "users who liked similar items" behavior,
- useful for sampled-negative evaluation.

### BPR Matrix Factorization

Uses implicit-feedback matrix factorization trained with Bayesian Personalized
Ranking style updates. Each step compares a positive user-item interaction
against a sampled negative item.

Purpose:

- learns user and item embeddings from interaction behavior,
- captures taste similarity not visible in raw metadata,
- provides a scalable candidate scoring mechanism for batch recommendation.

### Implicit ALS

Uses alternating least-squares style positive-feedback factor updates.

Purpose:

- adds a second matrix-factorization family,
- checks whether the final result depends on one collaborative model,
- gives a contrasting baseline for BPR and ItemKNN.

### Two-Stage Hybrid Ranker

Stage 1 retrieves top-200 candidates from BPR, ALS, and ItemKNN. Stage 2
re-ranks the union using:

- BPR score,
- ALS score,
- ItemKNN score,
- content score,
- popularity score,
- novelty / long-tail signal.

Purpose:

- separates candidate generation from ranking,
- mirrors real content-discovery system architecture,
- balances personalization with metadata, popularity, and novelty information,
- reduces dependence on a single model family.

## Validation Tuning

The ranker weight grid is tuned on the validation holdout. The final test set is
not used for weight selection.

The selected validation configuration in the latest run is `content_safety` for
all three seeds:

- BPR: 0.20,
- ALS: 0.20,
- ItemKNN: 0.15,
- content: 0.25,
- popularity: 0.05,
- novelty: 0.15.

## Evaluation

The project reports:

- Precision@10,
- Recall@10,
- MAP@10,
- NDCG@10,
- catalog coverage,
- long-tail share,
- intra-list diversity,
- average genre diversity,
- Gini recommendation concentration,
- sampled 100-negative HitRate@10 and NDCG@10,
- cold-item fallback results,
- mean and standard deviation across three seeds,
- sample top-K recommendation output.

## Product Lens

Offline metrics are necessary but incomplete. A production content-discovery
system would also monitor:

- click-through rate,
- read/listen start rate,
- completion depth,
- saves/follows,
- repeat sessions,
- creator/content coverage,
- retention,
- complaint or hide signals.
