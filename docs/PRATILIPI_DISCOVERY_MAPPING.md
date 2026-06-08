# Pratilipi Discovery Mapping

This project is not a Pratilipi clone.

It is a public-data recommender project that uses the same basic building
blocks a reading platform would care about: users, items, behavior, item
metadata, ranking, and catalog coverage.

## Simple Fictional Example

Fictional example, not a real Pratilipi user:

> Aarav mostly reads Hindi crime stories. He sometimes tries short romance
> stories, but he skips long fantasy series. A useful homepage should not show
> him only the most popular story on the platform. It should mix strong matches,
> a few fresh items, and maybe a new author close to his taste.

That is what this project is trying to model in benchmark form.

## Translation Table

| Recommender term | Pratilipi-style version |
|---|---|
| user | reader or listener |
| item | story, book, comic, audio episode, podcast, or author page |
| rating | read, save, like, finish, follow, review, skip, or share |
| genre | language, theme, format, topic, mood, or category |
| candidate generation | finding a smaller set of possible stories from a large catalog |
| ranking | ordering homepage, feed, search, or similar-story results |
| batch scoring | refreshing recommendation lists every few hours or every day |
| cold start | new reader, new story, new author, or new language/category |

## Where This Would Show Up In A Product

A similar system shape could support:

- homepage recommendations,
- similar-story rows,
- author discovery,
- category pages,
- trending plus personal taste,
- continue-reading suggestions,
- new-story cold-start fallback.

## Signals A Real Platform Would Need

User behavior:

- opens,
- reading time,
- completion,
- saves,
- follows,
- shares,
- reviews,
- skips,
- hides,
- session order.

Item data:

- language,
- genre,
- author,
- format,
- length,
- tags,
- publish date,
- freshness,
- popularity,
- text or content embedding.

Context:

- device,
- time of day,
- entry page,
- recent history,
- preferred language,
- new or returning user.

## What This Repo Covers

This repo covers the offline version:

1. Turn past behavior into training data.
2. Use item metadata.
3. Pull top-200 candidate items.
4. Re-rank candidates with several signals.
5. Check recall, ranking quality, coverage, diversity, and cold-start fallback.
6. Write the results to CSV files.

## Interview Talking Point

The honest way to say it:

> I rebuilt the project on MovieLens 1M, then shaped it like a content discovery
> system. It compares popularity, content, ItemKNN, BPR, ALS, and a two-stage
> hybrid ranker. The strongest angle is not just recall; it is that the hybrid
> ranker improves recall over popularity while recommending from a much wider
> part of the catalog.

Do not say it used Pratilipi data or proved business impact. It did not.
