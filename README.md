# Monday 23 November 2026 — The World in One Picture

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/udgraphiccs/news-image-20261123/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/udgraphiccs/news-image-20261123/reward.svg)](https://make.fun/c/news-image-20261123)

A make.fun entry for [news-image-20261123](https://make.fun/c/news-image-20261123):
one 1024×1024 image summing up the world news of Monday 23 November 2026.

## The six stories

1. **COP31 ends with no deal** — Climate talks in Antalya close with no pact as the UN chief warns there is "no ambiguity in the science".
2. **Tankers struck in Hormuz** — At least two oil tankers are hit by projectiles in the Strait of Hormuz as Iran–US tensions flare.
3. **Magnitude 6.7 quake hits Peru** — A powerful earthquake strikes the Andes region of central Peru.
4. **Factory fire in Java** — Three dead and dozens missing after a blaze tears through a candy factory in Banten, Indonesia.
5. **Drone hits Kyiv region** — At least 14 people are missing after a Russian drone strikes a building, Zelenskyy says.
6. **Trump: China's nuclear arsenal growing** — Warning comes a day after his meeting with Xi Jinping and Vladimir Putin.

Plus a footer ticker: Modi meets Nepal's PM, the EU proposes a Big Tech tax, and Hong Kong polls return 723 members.

## How the image is made

`draw.py` draws the front page with Pillow (masthead, lead story, four-story
grid, bottom story, footer ticker) and writes `entry.png`. `main.ts` copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Both runs write identical bytes.

## License

MIT — see [LICENSE](LICENSE).
