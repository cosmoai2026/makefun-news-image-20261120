# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/cosmoai2026/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/cosmoai2026/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

The World in One Image — 20 November 2026. A broadsheet-style front page that sums up the day's world news in a single 1024×1024 PNG: a masthead, an editorial hero illustration, a caption, and six short stories in a two-column grid.

`build_image.py` draws the page with PIL from the hero illustration that ships in this repository; `main.py` is the entrypoint the grader runs, copying the finished `entry.png` into the output directory. No network access is needed and the output is deterministic.

## Stories covered

- **Peace deal** — Trump, Xi and Putin sign peace declaration in Shenzhen.
- **Court** — The World Court rules Myanmar committed genocide against the Rohingya.
- **Markets** — Anthropic pops 17% in its Nasdaq debut.
- **Riyadh** — Houthi missiles hit the Saudi PIF tower.
- **Hormuz** — A tanker burns after a mine strike near the strait.
- **Ukraine** — The UK sends 1,000 drones as Kyiv comes under fire.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=xqg9f248&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
