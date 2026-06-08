# Methodology

## Objective

Generate personalized top-K item recommendations using user behavior and item
attributes, then evaluate recommendation quality with offline ranking metrics.

## Interaction Framing

Ratings of 4 or 5 are treated as positive implicit interactions. For each user
with enough positive history, the most recent positive interaction is held out
as the test item. Remaining positive interactions are used for training.

This creates a practical next-item recommendation task:

> Given the user's previous positive interactions, can the system rank the held
> out item in the top-K recommendations?

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

### Collaborative Filtering

Uses implicit-feedback matrix factorization trained with Bayesian Personalized
Ranking style updates. Each step compares a positive user-item interaction
against a sampled negative item.

Purpose:

- learns user and item embeddings from interaction behavior,
- captures taste similarity not visible in raw metadata,
- provides a scalable candidate scoring mechanism for batch recommendation.

### Hybrid Scoring

Combines collaborative scores, content scores, and popularity scores.

Purpose:

- balances personalization with cold-start and popularity information,
- produces a more product-realistic ranking signal,
- reduces dependence on a single model family.

## Evaluation

The project reports:

- Precision@10,
- Recall@10,
- MAP@10,
- NDCG@10,
- catalog coverage,
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
