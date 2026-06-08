# Data

The pipeline downloads MovieLens 1M from GroupLens on first run.

Raw data is not committed to the repository. The generated local folder is:

```text
data/raw/ml-1m/
```

MovieLens 1M contains approximately:

- 1,000,209 ratings,
- 6,040 users,
- 3,883 catalog movies/items,
- 3,706 movies/items that appear in the ratings file,
- genre metadata for items.

The project treats ratings of 4 or 5 as positive implicit-feedback events for
recommendation evaluation. This is a standard offline simplification and is not
equivalent to real production feedback such as reads, follows, saves, shares, or
completion depth.
