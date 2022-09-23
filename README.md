# RSS feeder
This is my simple rss feeder to watch what is new n industry/my topics.

Build with no rich features, but using a rich console printing and feedparser package.


## How To

### Feeds
Update `RSS_feeds.json`

### Run

```sh
poetry install
poetry run python src/rss_feeder/app.py
```

After loading use arrows (left, right) to change topic.
`Esc`/`ctrl+c` for exit.

### Try to do stuff profiling-like

```sh
poetry run python src/profiler/profiler.py
poetry run snakeviz needs_profiling.prof
```
