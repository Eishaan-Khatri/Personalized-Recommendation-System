# Personalized Recommendation System

This project is a small recommendation lab built around one simple question:

**If a user liked some items before, can we guess what they may like next?**

That is the same basic problem behind movie apps, shopping feeds, music apps,
and reading platforms. Pratilipi has its own version of it: readers need stories
worth opening, and the platform has to choose from a very large catalog.

This repo does not use Pratilipi data. It uses the public MovieLens 1M dataset,
then builds the kind of pipeline a content app would need: candidate retrieval,
ranking, cold-start fallback, batch scoring, and clear offline metrics.

## The Problem

Popularity is easy. Recommend the same famous items to everyone and the system
will look decent for a while.

But that gets boring fast.

A better recommender has to ask more useful questions:

- What has this user liked before?
- Which items are similar because of behavior, not just tags?
- Can new or less popular items still get a chance?
- Are we recommending from the whole catalog, or only from the same tiny group
  of popular items?
- Did the model get better on a real test split, or did it just memorize the
  past?

This project answers those questions with a reproducible benchmark.

## A Simple Example

Fictional example, not a real user:

> Riya reads mystery and romance stories late at night. She sometimes tries
> comedy, but rarely finishes it. A good recommender should not only show her
> the most popular story on the app. It should find stories close to her taste,
> leave room for a fresh author, and avoid repeating the same kind of item every
> time.

MovieLens has movies instead of stories, but the shape of the problem is close:
users, items, past behavior, item tags, and a ranked list of suggestions.

## What I Built

The pipeline compares several recommenders instead of trusting one model:

1. **Popularity baseline**: recommends items many users liked.
2. **Content-based model**: uses item genres.
3. **ItemKNN**: finds items liked by similar users.
4. **BPR matrix factorization**: learns user and item embeddings.
5. **Implicit ALS**: adds a second embedding-style baseline.
6. **Hybrid score blend**: mixes behavior, content, popularity, and novelty.
7. **Two-stage hybrid ranker**: pulls top-200 candidates first, then re-ranks
   them with several signals.

The two-stage setup matters because real recommendation systems usually do not
rank every item from scratch. They first collect a smaller pool of likely items,
then spend more care ordering that pool.

## Data Used

| Item | Value |
|---|---:|
| Dataset | MovieLens 1M |
| Ratings processed | 1,000,209 |
| Anonymous users | 6,040 |
| Catalog items | 3,883 |
| Rated items | 3,706 |
| Positive interactions | 575,281 |
| Training positive interactions | 563,211 |
| Validation users | 6,035 |
| Test users | 6,035 |
| Candidate retrieval depth | top-200 |
| Seeds | 11, 42, 73 |

Ratings of 4 or 5 are treated as positive interactions.

## How The Test Works

For each user with enough positive history:

- training gets the older liked items,
- validation gets the second-latest liked item,
- test gets the latest liked item.

The model tunes on validation, then reports final numbers on test.

That matters. Without validation, it is too easy to tune directly on the final
answer sheet.

## Main Results

These numbers come from `outputs/metrics/model_comparison.csv`.

| Model | Recall@10 | NDCG@10 | MAP@10 | Coverage@10 | Long-tail@10 |
|---|---:|---:|---:|---:|---:|
| Two-stage hybrid ranker | 0.0584 +/- 0.0007 | 0.0283 +/- 0.0004 | 0.0194 +/- 0.0003 | 0.2365 +/- 0.0133 | 0.0132 +/- 0.0018 |
| Hybrid score blend | 0.0583 +/- 0.0006 | 0.0283 +/- 0.0004 | 0.0193 +/- 0.0003 | 0.2316 +/- 0.0123 | 0.0137 +/- 0.0018 |
| ItemKNN | 0.0580 +/- 0.0000 | 0.0287 +/- 0.0000 | 0.0199 +/- 0.0000 | 0.0901 +/- 0.0000 | 0.0009 +/- 0.0000 |
| Popularity | 0.0399 +/- 0.0000 | 0.0188 +/- 0.0000 | 0.0126 +/- 0.0000 | 0.0296 +/- 0.0000 | 0.0000 +/- 0.0000 |
| BPR matrix factorization | 0.0389 +/- 0.0014 | 0.0177 +/- 0.0007 | 0.0115 +/- 0.0006 | 0.2028 +/- 0.0233 | 0.0129 +/- 0.0023 |
| Content-based | 0.0149 +/- 0.0000 | 0.0066 +/- 0.0000 | 0.0042 +/- 0.0000 | 0.7247 +/- 0.0000 | 0.7412 +/- 0.0000 |
| Implicit ALS | 0.0021 +/- 0.0006 | 0.0009 +/- 0.0002 | 0.0005 +/- 0.0001 | 0.1945 +/- 0.0234 | 0.9998 +/- 0.0002 |

The cleanest result:

- popularity Recall@10: **0.0399**
- two-stage Recall@10: **0.0584 +/- 0.0007**
- popularity Coverage@10: **2.96%**
- two-stage Coverage@10: **23.65% +/- 1.33%**

So the hybrid ranker did two useful things at once: it found more held-out liked
items, and it recommended from a wider part of the catalog.

## Extra Checks

The repo also includes two checks that many small recommender projects skip.

| Check | Result | Why it matters |
|---|---:|---|
| Sampled 100-negative HitRate@10 | 0.6154 +/- 0.0018 | Easier diagnostic task; ItemKNN was best here. |
| Sampled 100-negative NDCG@10 | 0.3466 +/- 0.0009 | Kept separate from all-item ranking. |
| Cold-item hybrid fallback Recall@10 | 0.0763 | Tests low-interaction items hidden from collaborative training. |
| Cold-item hybrid fallback NDCG@10 | 0.0299 | Popularity fallback scored 0.0000 in this cold-item setup. |

## Output Files

The numbers are not hand-written. They are stored in:

- `outputs/metrics/model_comparison.csv`
- `outputs/metrics/seed_metrics.csv`
- `outputs/metrics/hyperparameter_search.csv`
- `outputs/metrics/selected_ranker_weights.csv`
- `outputs/metrics/catalog_coverage.csv`
- `outputs/metrics/sampled_100_negative_metrics.csv`
- `outputs/metrics/sampled_100_negative_seed_metrics.csv`
- `outputs/metrics/cold_start_experiment.csv`
- `outputs/metrics/dataset_summary.json`
- `outputs/recommendations/sample_user_recommendations.csv`
- `reports/final_report.md`

## Why This Fits Pratilipi-Style Work

For Pratilipi, replace:

- MovieLens users with readers,
- movies with stories, comics, books, or audio episodes,
- genres with language, theme, format, author, and category,
- ratings with reads, saves, follows, completion, skips, and reviews.

The same system shape still holds: learn from behavior, use item metadata, pull
candidate items, rank them, and check if the list is both relevant and broad
enough.

## What I Am Not Claiming

This project does **not** claim:

- Pratilipi private data,
- live users,
- production deployment,
- conversion lift,
- retention lift,
- revenue impact,
- A/B test results.

Those claims would need real product logs and online experiments. This repo is
an offline recommender benchmark with honest numbers.

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python -m src.run_pipeline
```

The first run downloads MovieLens 1M into `data/raw/`.
