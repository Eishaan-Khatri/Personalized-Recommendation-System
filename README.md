# Personalized Recommendation System

Hybrid recommendation and discovery pipeline using collaborative filtering,
content-based signals, ranking metrics, and batch recommendation generation.

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
- popularity, collaborative, content-based, and hybrid recommendation approaches,
- holdout evaluation with ranking metrics such as Precision@K, Recall@K,
  MAP@K, and NDCG@K,
- batch top-K recommendation generation,
- product reasoning for personalization, recommendations, and discovery.

## Measured Results

The full pipeline was run on MovieLens 1M with one held-out positive item per
eligible user.

| Metric | Value |
|---|---:|
| Ratings processed | 1,000,209 |
| Users | 6,040 |
| Items | 3,883 |
| Positive interactions | 575,281 |
| Training positive interactions | 569,244 |
| Evaluation users | 6,037 |
| User-item matrix sparsity | 95.7353% |
| Best offline model | Hybrid |
| Best Recall@10 | 0.0500 |
| Best NDCG@10 | 0.0241 |
| Best Catalog Coverage@10 | 15.94% |

The hybrid model improved Recall@10 over the popularity baseline by 23.3%
relative and expanded Catalog Coverage@10 from 2.96% to 15.94%.

## Generated Outputs

The pipeline writes measured artifacts to:

- `outputs/metrics/model_comparison.csv`
- `outputs/metrics/catalog_coverage.csv`
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

The project is built around five recommender variants:

1. Popularity baseline.
2. Content-based user profile scoring from item metadata.
3. Collaborative filtering with implicit-feedback matrix factorization.
4. Hybrid score combining collaborative, content, and popularity signals.
5. Batch top-K recommendation generation over the item catalog.

## Model Comparison

| Model | Precision@10 | Recall@10 | MAP@10 | NDCG@10 | Coverage@10 |
|---|---:|---:|---:|---:|---:|
| Hybrid | 0.0050 | 0.0500 | 0.0164 | 0.0241 | 0.1594 |
| Popularity | 0.0041 | 0.0406 | 0.0130 | 0.0193 | 0.0296 |
| Collaborative filtering | 0.0038 | 0.0384 | 0.0114 | 0.0177 | 0.1537 |
| Content-based | 0.0016 | 0.0156 | 0.0048 | 0.0073 | 0.7126 |

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
combining collaborative filtering, content-based metadata signals, implicit user
embeddings, ranking-oriented offline evaluation, and top-K batch recommendation
generation for 6,037 evaluated users.

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
