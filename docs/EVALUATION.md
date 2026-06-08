# Evaluation

This file explains how the project checks whether the recommender is doing
anything useful.

## The Main Test

Each test user has one hidden liked item.

The model gets the user's older liked items, then ranks the catalog. If the
hidden item appears near the top, the model gets credit.

That is why the main metrics use `@10`: we care about the first 10 items shown
to the user.

## Metrics In Plain English

| Metric | What it means |
|---|---|
| `Recall@10` | Did the hidden liked item show up in the top 10? |
| `Precision@10` | How much of the top 10 is known to be relevant? This is small here because each user has only one hidden positive item. |
| `MAP@10` | Gives more credit when the hit appears higher in the list. |
| `NDCG@10` | Also rewards hits near the top. |
| `Catalog Coverage@10` | How much of the catalog appears across users' top-10 lists. |
| `Long-tail Share@10` | How often the model recommends less popular items. |
| `Intra-list Diversity@10` | Whether one user's list has variety instead of ten near-copies. |
| `Average Distinct Genres@10` | How many genre labels show up in a user's top-10 list. |
| `Gini Index@10` | Whether recommendations are concentrated on a small set of items. Lower is usually less concentrated. |

## How To Read The Main Numbers

Popularity is the easy baseline. It recommends famous items and often gets some
hits, but it usually covers very little of the catalog.

The two-stage ranker is stronger on the main goal:

- popularity Recall@10: `0.0399`
- two-stage Recall@10: `0.0584 +/- 0.0007`

It also spreads recommendations across more items:

- popularity Coverage@10: `2.96%`
- two-stage Coverage@10: `23.65% +/- 1.33%`

That coverage jump is the strongest discovery angle in this project.

## Seed Variance

The project runs three seeds: `11`, `42`, and `73`.

Why bother?

Because a recommender can look good by luck. Running more than one seed gives a
basic check that the result is not just one lucky training run.

## Sampled 100-Negative Test

This is a second, easier test.

For each user, the model ranks:

- one hidden liked item,
- 100 sampled negative items.

ItemKNN does best here:

- HitRate@10: `0.6154 +/- 0.0018`
- NDCG@10: `0.3466 +/- 0.0009`

Do not mix this with all-item ranking. Ranking against 100 sampled negatives is
much easier than ranking against the whole catalog.

## Cold-Start Test

Cold start means the system has weak behavior data for some items.

This project hides 894 low-interaction items from collaborative training. Then
it checks whether fallback signals can still recover some of those hidden items.

Results:

- popularity fallback NDCG@10: `0.0000`
- content fallback NDCG@10: `0.0068`
- hybrid fallback NDCG@10: `0.0299`

This does not prove a production cold-start system. It does show that content
and novelty signals help when pure popularity has no useful answer.

## Business Claim Boundary

Offline metrics do not prove:

- conversion lift,
- retention lift,
- revenue impact,
- better user satisfaction,
- live production performance.

Those need product logs and online experiments. This repo stays inside offline
benchmark evaluation.
