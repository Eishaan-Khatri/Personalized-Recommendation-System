# CV Bullet Selection Guide

This file answers one question:

**What are the three strongest CV points from this project that are actually
backed by repo outputs?**

The project is useful for Pratilipi-style roles because it is about
personalisation, recommendations, and discovery. It is not just a notebook that
prints recommendations. It has a validation split, several baselines, a
two-stage ranker, seed variance, sampled-negative testing, and a cold-start
check.

## Use These 3 Bullets

Use this version for a role that mentions Personalisation, Recommendations, and
Discovery.

- Built a two-stage recommendation pipeline over MovieLens 1M, processing
  1,000,209 ratings across 6,040 anonymous users with BPR, ALS, and ItemKNN
  top-200 candidate retrieval followed by hybrid re-ranking.
- Tuned the hybrid ranker on a validation holdout and compared popularity,
  content-based, ItemKNN, BPR matrix factorization, implicit ALS, and hybrid
  models across 3 seeds.
- Improved all-item Recall@10 over popularity from 0.0399 to
  0.0584 +/- 0.0007 and expanded Catalog Coverage@10 from 2.96% to
  23.65% +/- 1.33% with the two-stage ranker.

These are the safest three because they cover:

- system design,
- experiment discipline,
- discovery value beyond plain accuracy.

## Shorter Version

Use this if the resume has less space.

- Built a two-stage MovieLens-1M recommender using BPR, ALS, and ItemKNN
  candidate retrieval with hybrid re-ranking over 1,000,209 ratings.
- Compared popularity, content-based, ItemKNN, BPR, ALS, and hybrid models with
  validation tuning and 3-seed test reporting.
- Raised all-item Recall@10 from 0.0399 to 0.0584 and Coverage@10 from 2.96%
  to 23.65% against the popularity baseline.

## One-Line Version

Built a two-stage MovieLens-1M recommender with BPR/ALS/ItemKNN top-200
candidate retrieval and hybrid re-ranking; across 3 seeds, improved all-item
Recall@10 from 0.0399 to 0.0584 and Coverage@10 from 2.96% to 23.65%.

## Evidence Table

Use only these facts in the CV.

| Claim | Value | Evidence file |
|---|---:|---|
| Ratings processed | 1,000,209 | `outputs/metrics/dataset_summary.json` |
| Anonymous users | 6,040 | `outputs/metrics/dataset_summary.json` |
| Catalog items | 3,883 | `outputs/metrics/dataset_summary.json` |
| Positive interactions | 575,281 | `outputs/metrics/dataset_summary.json` |
| Training positives | 563,211 | `outputs/metrics/dataset_summary.json` |
| Validation users | 6,035 | `outputs/metrics/dataset_summary.json` |
| Test users | 6,035 | `outputs/metrics/dataset_summary.json` |
| Candidate retrieval depth | top-200 | `outputs/metrics/dataset_summary.json` |
| Seeds | 11, 42, 73 | `outputs/metrics/dataset_summary.json` |
| Best all-item Recall@10 model | two-stage hybrid ranker | `outputs/metrics/model_comparison.csv` |
| Two-stage Recall@10 | 0.0584 +/- 0.0007 | `outputs/metrics/model_comparison.csv` |
| Two-stage NDCG@10 | 0.0283 +/- 0.0004 | `outputs/metrics/model_comparison.csv` |
| Two-stage MAP@10 | 0.0194 +/- 0.0003 | `outputs/metrics/model_comparison.csv` |
| Two-stage Coverage@10 | 23.65% +/- 1.33% | `outputs/metrics/model_comparison.csv` |
| Popularity Recall@10 | 0.0399 | `outputs/metrics/model_comparison.csv` |
| Popularity Coverage@10 | 2.96% | `outputs/metrics/model_comparison.csv` |
| Best sampled 100-negative model | ItemKNN | `outputs/metrics/sampled_100_negative_metrics.csv` |
| Sampled 100-negative HitRate@10 | 0.6154 +/- 0.0018 | `outputs/metrics/sampled_100_negative_metrics.csv` |
| Cold-item hybrid fallback NDCG@10 | 0.0299 | `outputs/metrics/cold_start_experiment.csv` |

## Why These Bullets Work

The first bullet says the project has real recommender-system shape. It talks
about candidate retrieval and re-ranking, not just "I used ML."

The second bullet says the experiment was not lazy. There is validation tuning,
more than one baseline, and more than one random seed.

The third bullet gives the strongest measurable result. The recall lift is
useful, but the coverage jump is the better discovery story.

## What The Numbers Mean

The users are anonymous MovieLens users.

They are not Pratilipi users.

The ratings are public benchmark ratings.

They are not real production events.

The metrics are offline recommender metrics. They do not prove business impact.

## Claims To Avoid

Do not put these on the CV:

- used Pratilipi data,
- served live users,
- deployed to production,
- improved conversion,
- improved retention,
- improved revenue,
- ran an A/B test,
- achieved target Recall@10 of 0.0746,
- achieved target sampled HitRate@10 of 0.641.

Those last two target numbers were not produced by the current run. Do not use
them unless a future output CSV supports them.

## Interview Explanation

If asked where the numbers came from, say this:

> I used MovieLens 1M, a public recommender benchmark. I treated ratings of 4 or
> 5 as positive interactions. For each eligible user, I trained on older liked
> items, tuned on the second-latest liked item, and tested on the latest liked
> item. The CV numbers come from offline test metrics averaged across three
> seeds. They are not business-impact claims.

## Best Project Heading

`Personalized Recommendation System | Python, NumPy, pandas, ItemKNN, BPR, ALS, hybrid re-ranking, batch scoring`

Alternative for a Pratilipi-focused resume:

`Personalized Recommendation System | Personalisation, recommendations, discovery, candidate retrieval, hybrid ranking`
