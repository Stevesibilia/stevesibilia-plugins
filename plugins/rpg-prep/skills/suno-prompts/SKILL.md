---
name: suno-prompts
description: Generate ready-to-paste Suno AI prompts for tabletop RPG session music — ambience loops, scene themes, combat tracks, tavern songs, ritual chants, boss music. Use this skill whenever the user wants music, a soundtrack, ambience, background audio, or "audio hints" for their RPG session, asks for "suno prompts", wants a music cue for a scene from an adventure document, or says things like "musica per la scena del faro", "combat track for the finale", "something to play during the ritual". Also trigger when processing an adventure file with "mood:" fields, or when the user wants a consistent sonic identity for a whole campaign.
---

# Suno Prompts for RPG Session Music

Turn scene moods into effective Suno prompts the user pastes into Suno (Custom Mode). Prompts are **always in English** — the model performs best on English. Explanations follow the conversation language. Exception: sung lyrics may be Italian if the user wants a diegetic song their table understands (a tavern ballad, a ritual chant).

For full tag syntax read `references/suno-syntax.md`. Current flagship model: **v5.5**.

## What RPG music needs (and pop doesn't)

Session music is background: it must loop emotionally, avoid vocal distraction, and not demand attention. Defaults for this skill, unless the user asks otherwise:

- **Instrumental** — recommend the Instrumental toggle + no vocal descriptors + "vocals" in the Exclude field. Sung words in the players' language pull focus from the GM's voice.
- **Flat-ish dynamic arc** — ambience shouldn't build to a drop. Use style words like "slowly evolving", "sustained", "hypnotic". Combat and boss tracks are the exception: they want an arc.
- **4–7 style descriptors** — fewer defaults to generic; more compete. Suno leans upbeat by default, so dark/ambient briefs need emphatic mood words ("bleak", "oppressive", "hollow") to counteract it.

## Prompt construction

Style field structure:

```
[genre/palette], [tempo feel], [key instruments], [production texture], [mood words]
```

Lyrics field (even for instrumentals) carries structural meta tags controlling the arrangement:

```
[Intro: distant, sparse]
[Instrumental]
[Build: layered strings]
[Outro: fade out]
[End]
```

Always close with `[End]` — prevents trailing garbage audio. Parameterized tags (`[Verse: sparse, reverb-heavy]`) give per-section control.

Slider advice to include with each prompt: **Weirdness low-to-center** (conventional scores stay coherent), **Style Influence high** (descriptors honored strictly).

## Cue types

| Cue | Length feel | Skeleton |
|---|---|---|
| Exploration/ambience | long loop | slow tempo, evolving pads or sparse ensemble, no percussion or soft pulse |
| Tension/investigation | loop | low drones, irregular textures, muted dissonance, held breath feel |
| Combat | 2–3 min arc | driving percussion, ostinato strings/synths, high energy, `[Build]`/`[Climax]` tags |
| Boss/finale | arc | combat + choir or signature motif + `[Crescendo]`, biggest orchestration |
| Social (tavern, court, feast) | loop | period/diegetic instruments, mid energy, can be a real song with lyrics |
| Ritual/supernatural | loop | chant, bells, reversed textures, unresolved harmony |
| Aftermath/emotional | short | solo instrument, wide reverb, slow |

## Campaign sonic identity

Same principle as visual style: one palette per campaign, then vary energy per scene. Presets (adapt, then keep stable):

| Campaign / genre | Sonic palette |
|---|---|
| 7th Sea — swashbuckling | orchestral adventure, strings and brass, sea shanty colors (fiddle, concertina), bold and romantic |
| Broken Compass — pulp | big-band-tinged adventure score, brassy stabs, jungle percussion, 1930s serial energy |
| Call of Cthulhu — 1920s horror | dark ambient with period ghosts: detuned piano, distant gramophone jazz, low strings, creeping dread |
| Symbaroum — dark forest | Nordic dark folk: bowed nyckelharpa, frame drums, low female vocalise (wordless), ancient and cold |
| Vileborn — gothic grimdark | gothic orchestral, church organ and choir, funeral bells, oppressive and majestic |

Keep one recognizable element (an instrument or texture) in every cue of the campaign — that's the sonic thread players learn unconsciously.

## Input modes

**Direct request** — the user names a scene or moment ("musica per il funerale del PNG"). Base case: pick the cue type from the table above, apply the campaign palette, build the prompt.

**Structured adventure doc** — a file from the `enhanced-avventure-rpg` skill, whose «Appendice: immagini e musica» lists a `mood:` line under each scene heading (`### S3. Nome`). Harvest each scene's `mood:` field as pre-digested raw material.

**Existing/external adventure** — published module, old notes, any adventure text without `mood:` fields. Derive the mood yourself: for each scene, read its function (investigation? ambush? revelation? aftermath?) and emotional register from the prose, map it to a cue type, and state the mood you inferred in one line so the GM can correct it cheaply.

Per scene/cue, produce:

1. **Style prompt** (code block)
2. **Lyrics-field block** with meta tags (code block)
3. One line: when to start/stop the cue at the table

## Output format

````markdown
**Scena 3 — Il faro spento** (start when they see the open door; loop until the lantern room)

Style:
```
dark ambient, very slow, low cello drones and detuned piano, distant thunder
and rain texture, hollow reverb, creeping dread, bleak and unresolved
```

Lyrics field:
```
[Intro: rain and wind only]
[Instrumental]
[Sparse: single piano notes, long silences]
[Low drone swell]
[Outro: fade out]
[End]
```

Instrumental: ON · Weirdness: low · Style Influence: strong · Exclude: vocals
````

## Iteration

Map complaints to levers: too busy → cut instruments to two, add "sparse, minimal"; too cheerful → double the dark mood words (Suno's upbeat bias needs overcorrection); ignores structure → move key descriptors into the first 20 words and raise Style Influence; ends abruptly → `[Outro: fade out]` + `[End]`. For longer pieces, generate the core loop first, then use Extend with new section tags — continuity survives extension better than one long generation.
