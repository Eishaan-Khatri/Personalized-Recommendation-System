# Personalized Recommendation System

Two-stage recommendation and discovery pipeline using ItemKNN, BPR matrix
factorization, implicit ALS, content features, hybrid re-ranking, validation
tuning, seed variance, cold-start analysis, and batch recommendation generation.

## Problem

Content platforms need to match each reader with relevant items from a large
catalog. A useful recommender should not only surface popular content; it should
model user-item behavior, item attributes, cold-start constraints, and discovery
quality.

This project builds an offline recommendation pipeline over the MovieLens 1M
benchmark dataset and maps the same design to content-discovery products such as
Pratilipi, where users discover stories, authors, genres, languages, and formats.

## What The Project Demonstrates

- user-item interaction modeling over a 1M+ interaction benchmark,
- popularity, content-based, ItemKNN, BPR, ALS, and hybrid recommendation approaches,
- validation tuning before final test reporting,
- 3-seed repeated runs with mean and standard deviation,
- holdout evaluation with ranking metrics such as Precision@K, Recall@K,
  MAP@K, and NDCG@K,
- discovery metrics including catalog coverage, long-tail share, intra-list
  diversity, average genre diversity, and Gini concentration,
- sampled 100-negative recommender evaluation,
- low-interaction cold-item fallback analysis,
- batch top-K recommendation generation,
- product reasoning for personalization, recommendations, and discovery.

## Measured Results

The full pipeline was run on MovieLens 1M with a validation/test split:

- train: all except each eligible user's last two positive interactions,
- validation: second-latest positive interaction,
- test: latest positive interaction.

Final numbers below are test-set means across 3 seeds.

| Metric | Value |
|---|---:|
| Ratings processed | 1,000,209 |
| Users | 6,040 |
| Catalog items | 3,883 |
| Rated items | 3,706 |
| Positive interactions | 575,281 |
| Training positive interactions | 563,211 |
| Validation users | 6,035 |
| Evaluation users | 6,035 |
| User-item matrix sparsity | 95.7353% |
| Candidate retrieval depth | top-200 |
| Seeds | 11, 42, 73 |
| Best all-item model | Two-stage hybrid ranker |
| Recall@10 mean +/- std | 0.0584 +/- 0.0007 |
| NDCG@10 mean +/- std | 0.0283 +/- 0.0004 |
| MAP@10 mean +/- std | 0.0194 +/- 0.0003 |
| Catalog Coverage@10 mean +/- std | 23.65% +/- 1.33% |
| Sampled 100-negative best HitRate@10 | 0.6154 +/- 0.0018 |
| Cold-item hybrid fallback NDCG@10 | 0.0299 |

The two-stage hybrid ranker improved all-item Recall@10 over the popularity
baseline from 0.0399 to 0.0584 and expanded Catalog Coverage@10 from 2.96% to
23.65%. The sampled 100-negative evaluation is reported separately because it is
an easier candidate-set task and should not be mixed with all-item metrics.

## Generated Outputs

The pipeline writes measured artifacts to:

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

## Repository Map

| Path | Purpose |
|---|---|
| `src/` | Reusable data, modeling, evaluation, and batch scoring modules |
| `docs/` | Data dictionary, methodology, evaluation notes, and Pratilipi mapping |
| `notebooks/` | Notebook entry points for exploration and explanation |
| `outputs/` | Generated metrics and sample recommendations |
| `reports/` | Final project report |

## Methods

The project is built around seven recommender variants:

1. Popularity baseline.
2. Content-based user profile scoring from item metadata.
3. Collaborative ItemKNN.
4. BPR matrix factorization.
5. Implicit ALS.
6. Hybrid all-item score blend.
7. Two-stage hybrid ranker: retrieve top-200 candidates with BPR, ALS, and
   ItemKNN; re-rank with collaborative, content, popularity, and novelty signals.

## Model Comparison

| Model | Recall@10 | NDCG@10 | MAP@10 | Coverage@10 | Long-tail@10 |
|---|---:|---:|---:|---:|---:|
| Two-stage hybrid ranker | 0.0584 +/- 0.0007 | 0.0283 +/- 0.0004 | 0.0194 +/- 0.0003 | 0.2365 +/- 0.0133 | 0.0132 +/- 0.0018 |
| Hybrid score blend | 0.0583 +/- 0.0006 | 0.0283 +/- 0.0004 | 0.0193 +/- 0.0003 | 0.2316 +/- 0.0123 | 0.0137 +/- 0.0018 |
| ItemKNN | 0.0580 +/- 0.0000 | 0.0287 +/- 0.0000 | 0.0199 +/- 0.0000 | 0.0901 +/- 0.0000 | 0.0009 +/- 0.0000 |
| Popularity | 0.0399 +/- 0.0000 | 0.0188 +/- 0.0000 | 0.0126 +/- 0.0000 | 0.0296 +/- 0.0000 | 0.0000 +/- 0.0000 |
| BPR matrix factorization | 0.0389 +/- 0.0014 | 0.0177 +/- 0.0007 | 0.0115 +/- 0.0006 | 0.2028 +/- 0.0233 | 0.0129 +/- 0.0023 |
| Content-based | 0.0149 +/- 0.0000 | 0.0066 +/- 0.0000 | 0.0042 +/- 0.0000 | 0.7247 +/- 0.0000 | 0.7412 +/- 0.0000 |
| Implicit ALS | 0.0021 +/- 0.0006 | 0.0009 +/- 0.0002 | 0.0005 +/- 0.0001 | 0.1945 +/- 0.0234 | 0.9998 +/- 0.0002 |

## Cold-Start And Sampled-Negative Checks

| Experiment | Best result | Interpretation |
|---|---:|---|
| Sampled 100-negative HitRate@10 | 0.6154 +/- 0.0018 | ItemKNN was strongest when each user had one positive plus 100 sampled negatives. |
| Sampled 100-negative NDCG@10 | 0.3466 +/- 0.0009 | Sampled-negative metrics are easier than all-item ranking and are reported separately. |
| Cold-item hybrid fallback Recall@10 | 0.0763 | Hybrid content/novelty fallback recovered hidden low-interaction items better than popularity. |
| Cold-item hybrid fallback NDCG@10 | 0.0299 | Popularity fallback scored 0.0000 NDCG@10 after cold items were hidden. |

## Pratilipi Relevance

The project is shaped for personalisation, recommendations, and discovery work:

- reader behavior maps to user-item interactions,
- stories map to catalog items,
- genres/languages/themes map to item metadata,
- candidate generation maps to large-catalog retrieval,
- ranking maps to homepage/feed ordering,
- batch scoring maps to periodic recommendation refresh.

See `docs/PRATILIPI_DISCOVERY_MAPPING.md` for the detailed product mapping.

## Limitations

This is an offline benchmark project. It does not use private Pratilipi data,
does not claim production deployment, and does not claim conversion or retention
lift. Business metrics require real online experiments and product telemetry.

## Safe Resume Claim

Built a hybrid recommendation pipeline over a 1M+ interaction benchmark dataset,
using ItemKNN, BPR/ALS candidate generation, validation-tuned hybrid re-ranking,
3-seed offline evaluation, sampled-negative checks, and cold-item fallback
analysis over 6,035 evaluated users.

## Quick Start

Install the lightweight dependencies:

```bash
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python -m src.run_pipeline
```

The first run downloads MovieLens 1M into `data/raw/`.
