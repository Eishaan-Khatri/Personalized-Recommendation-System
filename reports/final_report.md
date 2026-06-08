# Final Report

## Dataset Summary

| Metric | Value |
|---|---:|
| Ratings | 1,000,209 |
| Users | 6,040 |
| Catalog items | 3,883 |
| Rated items | 3,706 |
| Positive interactions | 575,281 |
| Training positives | 563,211 |
| Validation users | 6,035 |
| Evaluation users | 6,035 |
| User-item matrix sparsity | 95.7353% |
| Seeds | 11, 42, 73 |
| Candidate retrieval depth | 200 |
| Sampled negatives | 100 |

## Split Design

For every user with at least three positive interactions:

- train uses all positive interactions except the latest two,
- validation uses the second-latest positive item,
- test uses the latest positive item.

Ranker weights are selected on validation. Final numbers below are test-set
means and standard deviations across seeds.

## All-Item Model Comparison

| model | recall_at_10_mean | recall_at_10_std | ndcg_at_10_mean | ndcg_at_10_std | map_at_10_mean | catalog_coverage_at_10_mean | long_tail_share_at_10_mean | gini_index_at_10_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| two_stage_hybrid_ranker | 0.0584 | 0.0007 | 0.0283 | 0.0004 | 0.0194 | 0.2365 | 0.0132 | 0.9778 |
| hybrid_score_blend | 0.0583 | 0.0006 | 0.0283 | 0.0004 | 0.0193 | 0.2316 | 0.0137 | 0.9779 |
| itemknn | 0.0580 | 0.0000 | 0.0287 | 0.0000 | 0.0199 | 0.0901 | 0.0009 | 0.9872 |
| popularity | 0.0399 | 0.0000 | 0.0188 | 0.0000 | 0.0126 | 0.0296 | 0.0000 | 0.9949 |
| bpr_matrix_factorization | 0.0389 | 0.0014 | 0.0177 | 0.0007 | 0.0115 | 0.2028 | 0.0129 | 0.9917 |
| content_based | 0.0149 | 0.0000 | 0.0066 | 0.0000 | 0.0042 | 0.7247 | 0.7412 | 0.8531 |
| implicit_als | 0.0021 | 0.0006 | 0.0009 | 0.0002 | 0.0005 | 0.1945 | 0.9998 | 0.9694 |

## Best Offline Model

The best all-item model by mean Recall@10, then mean NDCG@10, is
`two_stage_hybrid_ranker`.

## Sampled 100-Negative Evaluation

| model | seeds | evaluated_users | sampled_negatives | hit_rate_at_10_mean | hit_rate_at_10_std | map_at_10_mean | map_at_10_std | ndcg_at_10_mean | ndcg_at_10_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| itemknn | 3 | 6035 | 100 | 0.6154 | 0.0018 | 0.2642 | 0.0005 | 0.3466 | 0.0009 |
| two_stage_hybrid_ranker | 3 | 6035 | 100 | 0.5230 | 0.0108 | 0.2408 | 0.0010 | 0.3073 | 0.0032 |
| popularity | 3 | 6035 | 100 | 0.4924 | 0.0020 | 0.2027 | 0.0011 | 0.2703 | 0.0010 |
| bpr_matrix_factorization | 3 | 6035 | 100 | 0.4767 | 0.0012 | 0.1944 | 0.0017 | 0.2602 | 0.0012 |
| hybrid_score_blend | 3 | 6035 | 100 | 0.4663 | 0.0022 | 0.2266 | 0.0022 | 0.2832 | 0.0021 |
| content_based | 3 | 6035 | 100 | 0.2846 | 0.0006 | 0.1430 | 0.0009 | 0.1757 | 0.0007 |
| implicit_als | 3 | 6035 | 100 | 0.2139 | 0.0700 | 0.0542 | 0.0182 | 0.0905 | 0.0301 |

This is an easier diagnostic task than all-item ranking because each user has
one held-out positive item plus 100 sampled negatives. It should not be mixed
with all-item Recall@10 or NDCG@10.

## Cold-Start Experiment

| model | evaluated_users | precision_at_10 | recall_at_10 | map_at_10 | ndcg_at_10 | catalog_coverage_at_10 | unique_recommended_items | avg_distinct_genres_at_10 | long_tail_share_at_10 | intra_list_diversity_at_10 | gini_index_at_10 | cold_items_hidden_from_collaborative_training | cold_item_popularity_cutoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cold_popularity_fallback | 131 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0149 | 58 | 9.6794 | 0.0000 | 0.6766 | 0.9951 | 894 | 12 |
| cold_content_fallback | 131 | 0.0023 | 0.0229 | 0.0025 | 0.0068 | 0.1471 | 571 | 3.5649 | 0.7565 | 0.0827 | 0.9204 | 894 | 12 |
| cold_hybrid_fallback | 131 | 0.0076 | 0.0763 | 0.0161 | 0.0299 | 0.1136 | 441 | 3.2519 | 0.9947 | 0.1019 | 0.9468 | 894 | 12 |

The cold-start experiment hides low-interaction items from collaborative
training, then compares fallback behavior. A percentage lift over popularity is
not reported when popularity scores zero.

## Interpretation

The popularity baseline is a useful lower bound because it measures how much
recommendation quality can be achieved without personalization. ItemKNN and BPR
capture behavior similarity. Content-based scoring adds metadata awareness and
helps cold-start cases. The two-stage ranker retrieves candidates with behavior
models, then re-ranks with collaborative, content, popularity, and novelty
signals.

## Product Mapping

For a platform like Pratilipi, the same structure maps to reader-story
recommendations:

- users become readers or listeners,
- items become stories, authors, comics, or audio content,
- genres become language, theme, format, and category features,
- batch top-K scoring becomes personalized homepage or feed refresh,
- offline metrics become pre-launch checks before online experimentation.

## Claim Boundary

The reported numbers are offline benchmark metrics. They do not claim conversion,
retention, revenue, or production impact.
