---
name: midjourney-prompts
description: Generate ready-to-paste Midjourney prompts for tabletop RPG visuals — scene illustrations, NPC portraits, locations, handouts, maps, item art. Use this skill whenever the user wants an image, illustration, artwork, portrait, or visual for their RPG session, asks for "midjourney prompts", wants art for a scene or NPC from an adventure document, or says things like "give me visuals for scene 3", "un'immagine per questo PNG", "art for the lighthouse". Also trigger when processing an adventure file with "visual:" fields, or when the user wants a consistent art style across a whole campaign's images.
---

# Midjourney Prompts for RPG Visuals

Turn scene descriptions, NPCs, and locations into effective Midjourney prompts the user pastes into Midjourney. Prompts are **always in English** regardless of conversation language — the model performs best on English. Everything else (your explanations, option labels) follows the conversation language.

For full parameter syntax and values, read `references/mj-parameters.md`. Current default model is **v8.1**; `--oref` (character reference) and `--q` require `--v 7` — switch versions when the job needs them.

## Prompt construction

Write prompts as natural visual descriptions, not keyword soup. Order matters — Midjourney weighs early words heaviest:

```
[subject] [subject details], [context/setting], [lighting], [style/medium], [mood] --ar … --v …
```

Rules that materially change output quality:

- **Concrete beats abstract.** "Rembrandt lighting, soft fill from the left" outperforms "dramatic lighting". "Rust-eaten iron lantern" beats "old lantern".
- **No junk tokens.** Never include "8k, masterpiece, highly detailed, stunning, beautiful" — on v7/v8 these actively degrade results.
- **One idea per prompt.** A scene with three focal points produces mush. If the user's `visual:` field packs a crowd, an interior, and a storm, offer 2–3 prompts, one per shot.
- **Think like a cinematographer.** Specify shot type (wide establishing / medium / close portrait), camera angle, and light source. This is the single highest-leverage habit.
- **Exclude with `--no`,** not with negations in prose ("no people" in prose puts people in the image; `--no people` removes them).

## Input modes

**Direct description** — the user describes a scene, NPC, or location in chat. This is the base case; build the prompt from their words, asking at most one clarifying question (and only if the answer changes composition, e.g. "portrait or full scene?").

**Structured adventure doc** — a file from the `enhanced-avventure-rpg` skill, whose «Appendice: immagini e musica» lists a `visual:` line under each scene heading (`### S3. Nome`). Harvest each scene's `visual:` field and the NPCs' `Segno distintivo` lines; those are pre-digested raw material.

**Existing/external adventure** — any other adventure text: published module excerpts, old campaign notes, a PDF paste. No `visual:` fields exist, so extract them yourself: for each scene or location, identify subject, era/setting, light source, weather, palette from the prose, then build the prompt as usual. Where the text is silent (lighting, time of day), choose what serves the scene's function and say so — the GM can override in one word.

For each visual produced, output:

1. The prompt (code block, ready to paste)
2. One line: what shot this is and where it's usable at the table (opener splash, handout, portrait to show on phone)

Batch mode: if asked for "all the visuals", go scene by scene, one prompt each, plus one portrait per named NPC.

## Campaign style consistency

Images across a campaign should feel like one artist made them. Achieve this with a **style block**: a fixed tail appended to every prompt of that campaign. Genre presets (adapt freely, then keep stable):

| Campaign / genre | Style block |
|---|---|
| 7th Sea — swashbuckling | `dramatic oil painting, golden age of piracy, warm candlelight and sea spray, rich baroque color, painterly brushwork --ar 16:9` |
| Broken Compass — pulp adventure | `1930s pulp magazine cover art, saturated adventure palette, dynamic diagonal composition, screen-printed texture --ar 2:3` |
| Call of Cthulhu — 1920s horror | `1920s period photograph aesthetic, desaturated sepia and slate, deep shadows, cosmic horror atmosphere, subtle wrongness --ar 3:2 --exp 10` |
| Symbaroum — dark forest fantasy | `dark atmospheric fantasy painting, ancient forest gloom, muted greens and ochre, fog, in the style of grim Nordic concept art --ar 16:9` |
| Vileborn — gothic grimdark | `gothic dark fantasy illustration, oppressive chiaroscuro, blackened silver and dried-blood red, ornate decay --ar 16:9` |

Stronger consistency: once the user has one image they love, reuse it as `--sref <url>` in every subsequent prompt (add `--sw 200–400` for a tighter grip). Offer this as soon as they report a keeper.

## Recurring characters

For an NPC who must look the same across images: generate the definitive portrait first, then use `--oref <url> --ow 200 --v 7` for every later appearance (v7 only). Mention the 2× GPU cost once.

## Output format

For each requested visual:

````markdown
**Scena 3 — Il faro spento** (wide establishing shot, session opener)
```
abandoned stone lighthouse on jagged cliffs at night, storm clouds gathering,
cold moonlight breaking through the shattered lantern room, waves exploding
on rocks below, 1920s Italian coastline, desaturated blues and slate grey,
1920s period photograph aesthetic, deep shadows, cosmic horror atmosphere,
subtle wrongness --ar 3:2 --exp 10
```
````

Aspect ratio guidance: `16:9` scene/screen display, `2:3` portraits and posters, `3:2` handouts/photographs, `1:1` tokens and item icons.

## Iteration

When the user reports "too X / not enough Y", adjust the specific lever, don't rewrite blind: composition problems → shot type and `--ar`; style drift → strengthen style block or add `--sref`; too literal/boring → raise `--exp` (10–25) or `--chaos` (10–20); AI-slick look → add `--raw`. Explain which lever you pulled so the user learns the mapping.
