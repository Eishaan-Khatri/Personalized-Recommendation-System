# Data Dictionary

## Dataset

MovieLens 1M is used as the public benchmark dataset because it provides a
large user-item interaction table and item metadata.

The local raw files contain 3,883 catalog item rows in `movies.dat`; 3,706 of
those items appear in `ratings.dat`. The recommender scores the full catalog and
learns interaction signals from rated items.

## Tables

### Ratings

| Field | Type | Meaning |
|---|---|---|
| `user_id` | integer | Original MovieLens user identifier |
| `item_id` | integer | Original MovieLens movie identifier |
| `rating` | integer | Explicit user rating from 1 to 5 |
| `timestamp` | integer | Unix timestamp of the rating event |
| `user_idx` | integer | Internal contiguous user index |
| `item_idx` | integer | Internal contiguous item index |
| `is_positive` | boolean | `rating >= 4` |

### Items

| Field | Type | Meaning |
|---|---|---|
| `item_id` | integer | Original MovieLens movie identifier |
| `title` | string | Movie title |
| `genres` | string | Pipe-separated genre labels |
| `item_idx` | integer | Internal contiguous item index |

### Item Genre Features

Each genre becomes a binary feature. These features are used by the content-based
recommender and hybrid model.

## Pratilipi Mapping

| MovieLens Field | Content Platform Equivalent |
|---|---|
| `user_id` | reader identifier |
| `item_id` | story/book/comic/audio item |
| `rating` | read, like, save, follow, completion, or review signal |
| `genres` | language, genre, theme, format, author category |
| `timestamp` | reading/listening session time |

The benchmark is not Pratilipi data. It is used to demonstrate recommender
system design on a public dataset.
