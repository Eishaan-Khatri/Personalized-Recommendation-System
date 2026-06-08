# Pratilipi Discovery Mapping

This project is designed to be readable for roles focused on personalisation,
recommendations, and discovery.

## Domain Translation

| Recommender Concept | Pratilipi-Style Equivalent |
|---|---|
| user | reader or listener |
| item | story, book, comic, audio episode, podcast, author page |
| rating | read, like, save, follow, complete, review, share |
| genre | language, theme, category, format, mood, topic |
| candidate generation | finding possible stories from a large catalog |
| ranking | ordering homepage/feed/search/similar-story results |
| batch scoring | daily or hourly refresh of recommendation lists |
| cold start | new reader, new story, new author, new language/category |

## Discovery Surfaces

The same pipeline can support:

- personalized homepage recommendations,
- similar-story recommendations,
- author and creator discovery,
- genre/category recommendations,
- trending plus personalized blending,
- continue-reading and next-item surfaces,
- cold-start recommendations for new users or new content.

## Signals A Real Platform Would Use

### User Behavior

- story opens,
- reading time,
- completion rate,
- saves,
- follows,
- shares,
- ratings/reviews,
- skips,
- hides,
- session sequence.

### Item Attributes

- language,
- genre,
- author,
- format,
- length,
- tags,
- publish date,
- popularity,
- freshness,
- content embedding.

### Context

- device,
- session time,
- entry surface,
- recent history,
- user language preference,
- new vs returning user.

## Why The Project Is Relevant

The project demonstrates the core structure behind discovery systems:

1. Learn from user-item behavior.
2. Represent item metadata.
3. Retrieve plausible candidates.
4. Rank candidates with multiple signals.
5. Generate recommendation lists at scale.
6. Evaluate ranking quality and coverage.

## Interview-Ready Talking Point

The project is not a Pratilipi clone. It is a public-data recommender benchmark
implemented in a way that maps to Pratilipi's discovery problem: matching readers
with relevant content using behavior, item attributes, and ranking-friendly
signals.
