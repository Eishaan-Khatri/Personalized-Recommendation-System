# Methodology

This project tries to answer a practical question:

**Can we use a user's past likes to rank the next items they may like?**

The code uses MovieLens 1M, but the setup is close to what a reading platform
would do with readers and stories.

## What Counts As A Like

MovieLens ratings go from 1 to 5.

I treated ratings of **4 or 5** as positive interactions. That means the user
liked the item enough for it to train or test the recommender.

## Train, Validation, And Test Split

For each user with enough positive history:

- old liked items go into training,
- the second-latest liked item goes into validation,
- the latest liked item goes into test.

This is a next-item style task.

Simple fictional example:

> A user liked 20 movies over time. The model sees the first 18. It uses movie
> 19 to tune the ranker. Then it has to rank movie 20 near the top.

That is stricter than randomly hiding an item, because time order matters.

## Models Compared

### Popularity

This recommends what many users liked.

It is a useful baseline because every recommender should beat "show everyone the
same famous items." It also shows how narrow the catalog becomes when popularity
does all the work.

### Content-Based

This looks at item tags, such as genres.

If a user liked many drama and thriller movies, this model gives higher scores
to other drama and thriller movies. On a reading app, the same idea could use
language, theme, author, format, or story tags.

### ItemKNN

This asks: "Which items are liked by similar users?"

If many users liked item A and item B together, then item B becomes a good
candidate for someone who liked item A.

### BPR Matrix Factorization

BPR learns user and item embeddings from behavior.

The training loop compares a liked item against a not-seen item and tries to
score the liked item higher. This is useful when raw tags are not enough to
describe taste.

### Implicit ALS

ALS is another embedding-style model. I added it so the project does not depend
on only one collaborative filtering method.

### Hybrid Score Blend

This combines several scores:

- behavior score,
- content score,
- popularity score,
- novelty score.

The goal is not to worship one model. The goal is to build a ranked list that is
useful and not too narrow.

### Two-Stage Hybrid Ranker

This is the main system.

Stage 1 pulls a smaller pool of candidates. It uses BPR, ALS, and ItemKNN to
collect up to 200 possible items.

Stage 2 re-ranks that pool with:

- BPR score,
- ALS score,
- ItemKNN score,
- content score,
- popularity score,
- novelty / long-tail score.

This shape is closer to real recommendation systems. First get a good shortlist.
Then spend more care sorting it.

## Validation Tuning

The hybrid weights are tuned on validation, not on the final test set.

The latest run selected this weight mix for all three seeds:

| Signal | Weight |
|---|---:|
| BPR | 0.20 |
| ALS | 0.20 |
| ItemKNN | 0.15 |
| Content | 0.25 |
| Popularity | 0.05 |
| Novelty | 0.15 |

The selected setup is saved in:

`outputs/metrics/selected_ranker_weights.csv`

## What Gets Measured

The pipeline reports:

- Recall@10,
- NDCG@10,
- MAP@10,
- catalog coverage,
- long-tail share,
- genre diversity,
- recommendation concentration,
- sampled 100-negative metrics,
- cold-item fallback metrics,
- mean and standard deviation across 3 seeds.

## Product View

Offline metrics are not the whole story.

For a real app, the next checks would include:

- click-through rate,
- start-reading rate,
- completion depth,
- saves and follows,
- repeat sessions,
- creator coverage,
- user complaints, hides, or skips.

This repo stops at offline benchmark proof. It does not claim live product
impact.
