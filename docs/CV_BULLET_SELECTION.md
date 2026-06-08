# CV Bullet Selection Guide

## Purpose

This file exists to select exactly three strong CV points for the Personalized
Recommendation System project without using unsupported business-impact claims.

The project is strongest for roles involving:

- personalisation,
- recommendations,
- discovery,
- user-item modeling,
- ranking metrics,
- content platforms,
- product-facing data science.

It is especially useful for Pratilipi-style roles because the project connects
benchmark recommendation modeling with content-discovery surfaces such as
homepage recommendations, similar-story retrieval, and reader-interest modeling.

## Evidence Sources

Use only these project-backed facts in the CV.

| Evidence | Value | Source |
|---|---:|---|
| Ratings processed | 1,000,209 | `outputs/metrics/dataset_summary.json` |
| Anonymous benchmark users | 6,040 | `outputs/metrics/dataset_summary.json` |
| Catalog items | 3,883 | `outputs/metrics/dataset_summary.json` |
| Rated items | 3,706 | `outputs/metrics/dataset_summary.json` |
| Positive interactions | 575,281 | `outputs/metrics/dataset_summary.json` |
| Training positive interactions | 569,244 | `outputs/metrics/dataset_summary.json` |
| Evaluation users | 6,037 | `outputs/metrics/dataset_summary.json` |
| Matrix sparsity | 95.7353% | `outputs/metrics/dataset_summary.json` |
| Best model | Hybrid | `outputs/metrics/model_comparison.csv` |
| Hybrid Recall@10 | 0.0500 | `outputs/metrics/model_comparison.csv` |
| Hybrid NDCG@10 | 0.0241 | `outputs/metrics/model_comparison.csv` |
| Hybrid Catalog Coverage@10 | 15.94% | `outputs/metrics/model_comparison.csv` |
| Popularity Recall@10 | 0.0406 | `outputs/metrics/model_comparison.csv` |
| Popularity Catalog Coverage@10 | 2.96% | `outputs/metrics/model_comparison.csv` |
| Sample recommendation rows | 250 | `outputs/recommendations/sample_user_recommendations.csv` |

## What The Numbers Mean

The numbers are real project outputs, but they are offline benchmark numbers.

- The users are anonymous MovieLens benchmark users, not Pratilipi users.
- Ratings are public benchmark interactions, not production platform events.
- Recall@10, NDCG@10, MAP@10, and coverage are offline ranking metrics.
- Catalog coverage measures how widely recommendations spread across the item catalog.
- These metrics do not prove conversion, retention, revenue, or live engagement impact.

## Claims To Avoid

Do not use these in the CV unless future evidence exists:

- boosted conversion by 20%,
- increased retention by 30%,
- improved revenue,
- production deployment,
- served live users,
- used Pratilipi data,
- ran real A/B tests,
- achieved business impact from recommendations.

These claims are too risky because the current project evidence only supports an
offline benchmark pipeline.

## Selection Criteria For The 3 CV Points

The three bullets should cover three different strengths:

1. Scale and pipeline construction.
2. Modeling and measurable evaluation.
3. Product relevance to personalization, recommendations, and discovery.

Avoid three bullets that all say "built a recommender." Each bullet needs a
different job in the CV.

## Candidate Bullet Bank

### Candidate 1 - Scale and data pipeline

Built an offline recommendation pipeline over MovieLens 1M, processing
1,000,209 user-item ratings across 6,040 anonymous users and 3,883 catalog
items with holdout-based top-K evaluation.

Why it is useful:

- establishes dataset scale,
- shows this is not a tiny toy example,
- gives the recruiter immediate proof of project substance.

Risk:

- safe, as long as MovieLens is clearly treated as benchmark data.

### Candidate 2 - Model comparison

Compared popularity, content-based, collaborative filtering, and hybrid
recommenders using Recall@10, MAP@10, NDCG@10, and catalog coverage over 6,037
evaluated users.

Why it is useful:

- shows experimentation discipline,
- proves more than one model was implemented,
- aligns with recommendation-system evaluation.

Risk:

- safe.

### Candidate 3 - Best measured result

Improved Recall@10 from 0.0406 to 0.0500 over the popularity baseline with a
hybrid model, while increasing Catalog Coverage@10 from 2.96% to 15.94%.

Why it is useful:

- has real before/after numbers,
- shows ranking quality and discovery breadth,
- is much safer than fake conversion/retention numbers.

Risk:

- safe, but should be phrased as offline benchmark improvement, not product lift.

### Candidate 4 - Batch scoring

Generated top-K recommendation outputs through batch scoring, including 250
sample ranked recommendations with item titles, genres, model scores, and user
ids for inspection.

Why it is useful:

- shows the project produces concrete outputs,
- useful for data-science and ML-engineering resumes.

Risk:

- safe, but less impressive than model comparison unless the role stresses
  pipelines.

### Candidate 5 - Content-discovery mapping

Mapped user-item recommendation logic to content-discovery surfaces such as
personalized homepage ranking, similar-story retrieval, cold-start handling, and
reader-interest modeling.

Why it is useful:

- directly fits Pratilipi,
- shows product thinking,
- separates the project from generic MovieLens notebook work.

Risk:

- safe if phrased as mapping or relevance, not as implementation on Pratilipi data.

### Candidate 6 - Sparsity and real recommender difficulty

Modeled recommendations under 95.7353% user-item matrix sparsity, using positive
interaction holdouts to test whether models recovered each user's hidden item in
the top 10.

Why it is useful:

- shows understanding of sparse user-item data,
- useful for technical interviews.

Risk:

- safe, but may be too technical for a short CV unless the role is strongly
  recommender-focused.

## Final Recommended 3 CV Points

Use this version for Pratilipi or similar personalization/recommendation roles.

1. Built an offline hybrid recommendation pipeline over MovieLens 1M, processing
   1,000,209 user-item ratings across 6,040 anonymous users and 3,883 catalog
   items with holdout-based top-K evaluation.

2. Compared popularity, content-based, collaborative filtering, and hybrid
   recommenders over 6,037 evaluated users using Recall@10, MAP@10, NDCG@10,
   and catalog coverage.

3. Improved offline Recall@10 from 0.0406 to 0.0500 over the popularity
   baseline with a hybrid model, while expanding Catalog Coverage@10 from 2.96%
   to 15.94%.

## Strong 3-Bullet CV Version

Use this when the CV has enough space for three full bullets.

- Built an offline hybrid recommendation pipeline over MovieLens 1M, processing
  1,000,209 user-item ratings across 6,040 anonymous users and 3,883 catalog
  items with holdout-based top-K evaluation.
- Compared popularity, content-based, collaborative filtering, and hybrid
  recommenders over 6,037 evaluated users using Recall@10, MAP@10, NDCG@10, and
  catalog coverage.
- Improved offline Recall@10 from 0.0406 to 0.0500 over the popularity baseline
  with a hybrid model, while expanding Catalog Coverage@10 from 2.96% to 15.94%.

## Pratilipi-Focused 3-Bullet CV Version

Use this version if the role specifically mentions Personalisation,
Recommendations, and Discovery.

- Built a hybrid recommendation and discovery pipeline over MovieLens 1M,
  processing 1,000,209 user-item ratings across 6,040 anonymous users and 3,883
  catalog items.
- Evaluated popularity, content-based, collaborative filtering, and hybrid
  recommenders over 6,037 users using Recall@10, NDCG@10, MAP@10, and catalog
  coverage.
- Mapped the pipeline to content-discovery use cases such as personalized
  homepage ranking, similar-item retrieval, reader-interest modeling, and
  cold-start recommendation handling.

## Short CV Version

Use this if the CV has only one line for the project.

Built a hybrid recommendation pipeline over MovieLens 1M, comparing popularity,
content-based, collaborative, and hybrid models across 6,037 evaluated users;
hybrid improved offline Recall@10 from 0.0406 to 0.0500 and Coverage@10 from
2.96% to 15.94%.

## Resume Header Line

Recommended project heading:

`Personalized Recommendation System | Python, pandas, NumPy, collaborative filtering, content-based filtering, hybrid ranking, batch scoring`

Alternative Pratilipi-focused heading:

`Personalized Recommendation System | Recommendations, discovery, user-item modeling, hybrid ranking, batch scoring`

## Interview Explanation

Use this explanation if asked where the numbers came from:

The project uses MovieLens 1M, a public recommender-system benchmark. The users
are anonymous MovieLens users, not Pratilipi users. I treated ratings of 4 or 5
as positive interactions, held out each eligible user's latest positive item,
and evaluated whether each model could recover that hidden item in the top 10.
The numbers in the CV are offline ranking metrics from that evaluation, not
business-impact claims.

## Final Recommendation

For the Pratilipi CV, use the Pratilipi-focused 3-bullet version if the resume
already has enough technical detail elsewhere. Use the strong 3-bullet version
if this project needs to carry most of the recommendation-system proof.

Do not use conversion or retention claims. The offline ranking and coverage
numbers are strong enough, and they are defensible in an interview.
