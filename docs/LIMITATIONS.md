# Limitations

This file is here so the project does not sound bigger than it is.

The work is useful. It is not production proof.

## The Data Is Public Movie Data

The project uses MovieLens 1M.

That means:

- the users are anonymous MovieLens users,
- the items are movies,
- the actions are star ratings.

It is not Pratilipi data. It is not private app data. It does not contain real
reader sessions, story opens, follows, saves, or completion depth.

## Ratings Are Cleaner Than Real Behavior

A 5-star rating is easy to read: the user liked the movie.

Real product signals are messier. A reader may open a story, leave after 20
seconds, come back later, save it, skip it, or follow the author. Those actions
are richer, but also harder to model cleanly.

This project keeps the first version honest by using a public dataset.

## Offline Metrics Are Not Business Metrics

Recall@10 and NDCG@10 are useful checks.

They do not prove that users would:

- read more,
- stay longer,
- spend money,
- return tomorrow,
- follow more authors.

Those claims need online testing.

## The Models Are Deliberately Lightweight

The repo uses models that are easy to inspect:

- popularity,
- content-based scoring,
- ItemKNN,
- BPR matrix factorization,
- implicit ALS,
- hybrid re-ranking.

It does not include:

- deep sequence recommenders,
- graph neural networks,
- real-time feature stores,
- approximate nearest-neighbor serving,
- online A/B testing.

Those would be good next steps, but they are not needed to show the core
recommendation workflow.

## Sampled Metrics Need Care

The sampled 100-negative test is useful, but easier than the all-item test.

It ranks one hidden liked item against 100 sampled negative items. The all-item
test ranks against the full catalog.

So these two numbers should not be compared directly.

## Cold-Start Lift Needs Care

In the cold-start experiment, popularity fallback gets zero NDCG@10.

Because of that, I do not report a percentage lift over popularity. A percentage
lift from zero would be misleading. The safer numbers are the absolute Recall@10
and NDCG@10 values.

## Safe Claims

Safe:

- built a two-stage recommender,
- used MovieLens 1M,
- compared multiple baselines,
- tuned on validation,
- reported 3-seed test results,
- added sampled-negative and cold-start checks,
- generated batch recommendation outputs.

Not safe:

- used Pratilipi data,
- served live users,
- improved retention,
- improved conversion,
- improved revenue,
- ran an A/B test,
- deployed a production recommender.
