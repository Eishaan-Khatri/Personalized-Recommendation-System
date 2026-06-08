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

## Planned Outputs

The pipeline writes measured artifacts to:

- `outputs/metrics/model_comparison.csv`
- `outputs/metrics/catalog_coverage.csv`
- `outputs/recommendations/sample_user_recommendations.csv`
- `reports/final_report.md`

The README will be updated with final measured numbers after the pipeline is run.

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
