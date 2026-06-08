# Data Dictionary

This file explains the data in plain language.

The project uses **MovieLens 1M**, a public movie-rating dataset. It is useful
because it has the same basic pieces a recommender needs:

- users,
- items,
- past actions,
- item tags,
- timestamps.

It is not Pratilipi data.

## Dataset Size

| Field | Value |
|---|---:|
| Rating rows | 1,000,209 |
| Users | 6,040 |
| Movie rows in catalog | 3,883 |
| Movies with at least one rating | 3,706 |
| Positive ratings used by the recommender | 575,281 |

The recommender treats ratings of 4 or 5 as positive. In simple words: the user
liked that item enough for it to count as a useful signal.

## Ratings Table

| Field | Type | Plain meaning |
|---|---|---|
| `user_id` | integer | Original anonymous MovieLens user ID |
| `item_id` | integer | Original MovieLens movie ID |
| `rating` | integer | Star rating from 1 to 5 |
| `timestamp` | integer | When the rating happened |
| `user_idx` | integer | Clean internal user number used by the code |
| `item_idx` | integer | Clean internal item number used by the code |
| `is_positive` | boolean | True when `rating >= 4` |

## Items Table

| Field | Type | Plain meaning |
|---|---|---|
| `item_id` | integer | Original MovieLens movie ID |
| `title` | string | Movie title |
| `genres` | string | Movie genres, split by `|` |
| `item_idx` | integer | Clean internal item number used by the code |

## Genre Features

Each genre becomes a yes/no feature. For example, a movie can be marked as:

- action,
- comedy,
- drama,
- romance.

The content-based model uses these tags to ask: "Has this user liked items with
similar tags before?"

## How This Maps To A Reading App

| MovieLens field | Reading-platform version |
|---|---|
| `user_id` | reader ID |
| `item_id` | story, book, comic, audio episode, or author page |
| `rating` | read, like, save, follow, finish, skip, or review |
| `genres` | language, theme, format, author type, mood, or category |
| `timestamp` | reading or listening time |

The data is different, but the recommender problem is similar: use past behavior
to rank the next set of items.
