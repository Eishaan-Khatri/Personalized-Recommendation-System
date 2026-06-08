# CV Bullet Selection Guide

## Purpose

This file selects strong CV points for the Personalized Recommendation System
project using only metrics that exist in the repository outputs.

The project is strongest for:

- personalisation,
- recommendations,
- discovery,
- user-item modeling,
- candidate generation,
- hybrid ranking,
- cold-start handling,
- evaluation discipline.

It is especially useful for Pratilipi-style roles because the project connects a
public recommender benchmark with content-discovery surfaces such as homepage
ranking, similar-item retrieval, reader-interest modeling, and cold-start
fallbacks.

## Evidence Sources

Use only these project-backed facts in the CV.

| Evidence | Value | Source |
|---|---:|---|
| Ratings processed | 1,000,209 | `outputs/metrics/dataset_summary.json` |
| Anonymous benchmark users | 6,040 | `outputs/metrics/dataset_summary.json` |
| Catalog items | 3,883 | `outputs/metrics/dataset_summary.json` |
| Rated items | 3,706 | `outputs/metrics/dataset_summary.json` |
| Positive interactions | 575,281 | `outputs/metrics/dataset_summary.json` |
| Training positive interactions | 563,211 | `outputs/metrics/dataset_summary.json` |
| Validation users | 6,035 | `outputs/metrics/dataset_summary.json` |
| Test/evaluation users | 6,035 | `outputs/metrics/dataset_summary.json` |
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
| Sampled 100-negative NDCG@10 | 0.3466 +/- 0.0009 | `outputs/metrics/sampled_100_negative_metrics.csv` |
| Cold-item hybrid fallback Recall@10 | 0.0763 | `outputs/metrics/cold_start_experiment.csv` |
| Cold-item hybrid fallback NDCG@10 | 0.0299 | `outputs/metrics/cold_start_experiment.csv` |
| Sample recommendation rows | 250 | `outputs/recommendations/sample_user_recommendations.csv` |

## What The Numbers Mean

The numbers are real project outputs, but they are offline benchmark numbers.

- The users are anonymous MovieLens benchmark users, not Pratilipi users.
- Ratings are public benchmark interactions, not production platform events.
- The project uses a train/validation/test split based on each eligible user's
  latest positive interactions.
- Ranker weights are selected on validation and final metrics are reported on
  the test holdout.
- Recall@10, NDCG@10, MAP@10, coverage, long-tail share, diversity, Gini, and
  sampled-negative metrics are offline recommender metrics.
- These metrics do not prove conversion, retention, revenue, or live engagement
  impact.

## Claims To Avoid

Do not use these in the CV unless future evidence exists:

- boosted conversion by 20%,
- increased retention by 30%,
- improved revenue,
- production deployment,
- served live users,
- used Pratilipi data,
- ran real A/B tests,
- achieved business impact from recommendations,
- achieved target Recall@10 of 0.0746,
- achieved target sampled HitRate@10 of 0.641.

The last two target-style numbers were not produced by the current run. The
current safe numbers are the CSV-backed values above.

## Selection Criteria For The 3 CV Points

The three bullets should cover three different strengths:

1. Scale and two-stage system design.
2. Validation, model comparison, and seed variance.
3. Discovery/cold-start relevance beyond plain accuracy.

Avoid three bullets that all say "built a recommender." Each bullet needs a
different job in the CV.

## Candidate Bullet Bank

### Candidate 1 - Two-stage architecture

Built a two-stage recommendation pipeline over MovieLens 1M, processing
1,000,209 ratings across 6,040 anonymous users with BPR/ALS/ItemKNN top-200
candidate generation followed by hybrid re-ranking.

Why it is useful:

- directly addresses recommender-system architecture,
- sounds more senior than a single notebook model,
- maps well to discovery/feed ranking systems.

Risk:

- safe.

### Candidate 2 - Validation and model comparison

Tuned hybrid ranker weights on a validation holdout and compared popularity,
content-based, ItemKNN, BPR matrix factorization, implicit ALS, and hybrid
rankers across 3 seeds.

Why it is useful:

- fixes the previous missing validation split,
- shows experimentation discipline,
- avoids over-relying on one lucky run.

Risk:

- safe.

### Candidate 3 - Best all-item result

Achieved the best all-item Recall@10 with a two-stage hybrid ranker
(0.0584 +/- 0.0007), with NDCG@10 of 0.0283 +/- 0.0004 and MAP@10 of
0.0194 +/- 0.0003 across 6,035 test users.

Why it is useful:

- gives real test-set numbers,
- includes seed variance,
- shows that the ranker won on Recall@10.

Risk:

- safe, but do not say it won every metric. ItemKNN has slightly higher
  NDCG@10 in the current run.

### Candidate 4 - Coverage/discovery improvement

Expanded Catalog Coverage@10 from 2.96% for popularity to 23.65% +/- 1.33% with
the two-stage hybrid ranker, improving discovery breadth while preserving higher
Recall@10 than the popularity baseline.

Why it is useful:

- this is the strongest discovery/product angle,
- directly addresses the weakness of popularity-only recommendations,
- better Pratilipi fit than just saying "accuracy."

Risk:

- safe.

### Candidate 5 - Sampled-negative diagnostic

Reported sampled 100-negative evaluation separately, where ItemKNN achieved
0.6154 +/- 0.0018 HitRate@10 and 0.3466 +/- 0.0009 NDCG@10.

Why it is useful:

- shows recommender evaluation maturity,
- demonstrates the difference between all-item and sampled-negative tasks.

Risk:

- safe only if clearly described as sampled-negative. Do not mix this with
  all-item Recall@10.

### Candidate 6 - Cold-start fallback

Simulated low-interaction cold items by hiding 894 items from collaborative
training; hybrid content/novelty fallback reached 0.0763 Recall@10 and 0.0299
NDCG@10 on 131 cold-item test users.

Why it is useful:

- directly addresses cold-start, which most student projects ignore,
- useful for content platforms with new stories/authors/items.

Risk:

- safe, but the sample is smaller than the main test set. Keep it as fallback
  analysis, not the main project headline.

## Final Recommended 3 CV Points

Use this version for Pratilipi or similar personalization/recommendation roles.

1. Built a two-stage recommendation pipeline over MovieLens 1M, processing
   1,000,209 ratings across 6,040 anonymous users with BPR/ALS/ItemKNN top-200
   candidate generation followed by hybrid re-ranking.

2. Tuned hybrid ranker weights on a validation holdout and compared popularity,
   content-based, ItemKNN, BPR matrix factorization, implicit ALS, and hybrid
   rankers across 3 seeds.

3. Improved all-item Recall@10 over popularity from 0.0399 to 0.0584 +/- 0.0007
   and expanded Catalog Coverage@10 from 2.96% to 23.65% +/- 1.33% with the
   two-stage hybrid ranker.

## Strong 3-Bullet CV Version

Use this when the CV has enough space for three full bullets.

- Built a two-stage recommendation pipeline over MovieLens 1M, processing
  1,000,209 ratings across 6,040 anonymous users with BPR/ALS/ItemKNN top-200
  candidate generation followed by hybrid re-ranking.
- Tuned hybrid ranker weights on a validation holdout and compared popularity,
  content-based, ItemKNN, BPR matrix factorization, implicit ALS, and hybrid
  rankers across 3 seeds.
- Improved all-item Recall@10 over popularity from 0.0399 to 0.0584 +/- 0.0007
  and expanded Catalog Coverage@10 from 2.96% to 23.65% +/- 1.33% with the
  two-stage hybrid ranker.

## Pratilipi-Focused 3-Bullet CV Version

Use this version if the role specifically mentions Personalisation,
Recommendations, and Discovery.

- Built a two-stage recommendation and discovery pipeline over MovieLens 1M,
  using BPR/ALS/ItemKNN candidate retrieval and hybrid re-ranking across
  1,000,209 user-item ratings.
- Tuned ranker weights on validation and evaluated popularity, content-based,
  ItemKNN, BPR, ALS, and hybrid models across 3 seeds on 6,035 test users.
- Expanded Catalog Coverage@10 from 2.96% to 23.65% +/- 1.33% and added a
  cold-item fallback experiment for low-interaction catalog items.

## One-Line CV Version

Use this if the CV has only one line for the project.

Built a two-stage MovieLens-1M recommender using BPR/ALS/ItemKNN top-200
candidate retrieval and hybrid re-ranking; across 3 seeds, improved all-item
Recall@10 from 0.0399 to 0.0584 and Coverage@10 from 2.96% to 23.65%.

## Resume Header Line

Recommended project heading:

`Personalized Recommendation System | Python, NumPy, pandas, ItemKNN, BPR, ALS, hybrid re-ranking, batch scoring`

Alternative Pratilipi-focused heading:

`Personalized Recommendation System | Recommendations, discovery, user-item modeling, candidate generation, hybrid ranking`

## Interview Explanation

Use this explanation if asked where the numbers came from:

The project uses MovieLens 1M, a public recommender-system benchmark. The users
are anonymous MovieLens users, not Pratilipi users. I treated ratings of 4 or 5
as positive interactions, used the second-latest positive item for validation,
and used the latest positive item for final test evaluation. The ranker weights
were selected on validation. The CV numbers are offline test metrics averaged
over three seeds, not business-impact claims.

## Final Recommendation

For the Pratilipi CV, use the Pratilipi-focused 3-bullet version if the resume
already has enough technical detail elsewhere. Use the strong 3-bullet version
if this project needs to carry most of the recommender-system proof.

Do not use conversion or retention claims. The validation split, two-stage
architecture, coverage improvement, seed variance, sampled-negative check, and
cold-start analysis are now the defensible proof.
