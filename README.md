[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/norv33/news-image-23-nov/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/norv33/news-image-23-nov/reward.svg)](https://make.fun/c/news-image-20261123)

# The World — 23 November 2026

A single image that sums up Monday 23 November 2026 in world news: a warm
"morning broadsheet" poster — crimson masthead, ivory paper — with the day's
six most consequential stories, an also-today strip, and the date in large
gold type.

Entry for the make.fun bounty
[Sum up 23 November's world news in one image](https://make.fun/c/news-image-20261123).

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png — run it twice and compare sha256: identical.
```

To redraw the image from scratch (needs Python 3 + Pillow):

```
python3 draw.py   # writes entry.png (1024x1024, < 1 MiB)
```

## The six stories

1. **COP31 collapses with no deal** — UN climate talks end in failure,
   the first collapse since Copenhagen in 2009, after the EU and others
   reject a final text that never mentions fossil fuels.
   (BBC News; Reuters; AP)
2. **Drone hits home; 14 missing** — a Russian drone flattens a home near
   Kyiv; a 7-year-old boy is pulled alive from the rubble.
   (BBC News)
3. **Factory fire: 24 body bags** — police remove 24 body bags from the
   burnt candy factory in Banten as the search for missing workers resumes.
   (BBC News; Reuters)
4. **Blast on Russian ship in port** — an explosion rocks a Russian ship at
   Benghazi; officials blame a suspected drone attack.
   (BBC News)
5. **Killer-robot talks go on — no ban** — states agree to keep talking on
   lethal autonomous weapons, but promise no binding ban.
   (AP; AFP)
6. **Minister quits in AI exam scandal** — South Korea's education minister
   resigns over an AI exam-cheating scandal.
   (AFP; AP)

Also today: Democrats take a 258-seat House majority; Nepal's PM meets Modi
in New Delhi; India post a record 720/9 in the Wellington Test.

## Design

A "morning broadsheet" poster: "THE WORLD" in huge cream serif type on a
crimson masthead, the date "MONDAY, 23 NOVEMBER 2026" in large gold type,
then one wide lead panel for the COP31 collapse and four story cards in two
columns — each with a hand-drawn pictogram (globe and thermometer, house and
drone, factory and flame, ship and starburst, robot head, exam paper and
chip), a coloured region tag, a headline and one fact line — followed by a
slim sixth-story row, an "ALSO TODAY" strip and a sources footer. This design
is original to this entry and deliberately different from the 22 November
entry (dark-teal evening atlas with gold), the 20 November entry (white
wire-desk poster, 2×3 grid) and the earlier broadsheet entries.

## How it works

`entry.png` (1024×1024, drawn with Python PIL and Liberation fonts by
`draw.py`) is the image. `main.ts` (Node 22, stdlib only) validates it first —
the first 8 bytes must match the PNG signature, the file must be at most 1 MiB,
and the IHDR dimensions at most 1024×1024 — then writes it atomically to
`$MAKEFUN_OUTPUT_DIR` (or `/output`) as `entry.png`: the bytes go to a
temporary file in the output directory, then rename over `entry.png`, so a
failed run never leaves a truncated image behind.

Running it twice produces byte-identical output.

Every story above happened, or was first reported, on 23 November 2026.
