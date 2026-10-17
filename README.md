# stevesibilia-plugins

Claude plugins by Stefano Sibilia. The repository is the `stevesibilia` plugin marketplace and ships two plugins:

- `rpg-prep`: a pre-session toolkit for tabletop RPG game masters, eight skills.
- `essentials`: general-purpose skills for any task. Today it holds `scrittura-italiana`, which every RPG skill applies, so `rpg-prep` declares `essentials` as a dependency.

Nine skills:

| Skill                    | What it does                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `enhanced-avventure-rpg` | Session prep as situations, never PC scripts, in an Italian document built to be looked up at the table: a synopsis to read before the session, at-a-glance block, clock, self-contained scenes, clue tracker (three clues per revelation), stat blocks, and `visual:`/`mood:` in an appendix. Ships `scripts/controlla.py` to check the output                    |
| `impagina-avventura`     | Lays out an `enhanced-avventure-rpg` adventure as an A4 PDF for the table: cover, synopsis, one page per scene with edge tabs, threat boxes with wound and affliction checkboxes, clue and NPC tables, stat blocks. A rule-based script (`scripts/impagina.py`, WeasyPrint) does the work and never rewrites the text                                              |
| `revisione-avventura`    | Adversarial review of an adventure or a campaign: logic and causality, clue paths and scene reachability, the golden rule, pacing, and four simulated tables (methodical, impatient, lateral, uninterested). Verifies each finding, reports in the chat with severity and root cause, then brainstorms fixes one question at a time. Does not rewrite the document |
| `campagna-rpg`           | Campaign and arc story design, the layer above a session: premise, world truths, fronts with clocks, factions, PC hooks, arcs as functions, possible endings, thread tracker. Writes a Joplin note «Campagna: <nome>» that `enhanced-avventure-rpg` reads. Ships `scripts/controlla.py`                                                                            |
| `cronaca-di-sessione`    | Turns a session recap into an in-world chronicle in the style of medieval travel accounts, with a chronicler fitted to the milieu                                                                                                                                                                                                                                  |
| `scrittura-italiana`     | In `essentials`. Italian writing rules applied by every other skill: no em or en dash, Italian punctuation and quotes                                                                                                                                                                                                                                              |
| `suno-prompt-creator`    | General-purpose Suno prompts: songs, themes, jingles, lyrics with structure tags                                                                                                                                                                                                                                                                                   |
| `midjourney-prompts`     | Scene/NPC → ready-to-paste Midjourney prompts (v8.1/v7 aware), campaign style consistency                                                                                                                                                                                                                                                                          |
| `suno-prompts`           | Scene mood → ready-to-paste Suno prompts (v5.5), session cue types, campaign sonic identity                                                                                                                                                                                                                                                                        |

The skills chain: `campagna-rpg` plans the campaign in a Joplin note; `enhanced-avventure-rpg` reads that note to prepare each session and emits `visual:` and `mood:` fields per scene; `midjourney-prompts` and `suno-prompts` consume them; `impagina-avventura` turns the adventure into a PDF to print.

## Install

The repository is a Claude plugin marketplace. On claude.ai, the desktop app or Cowork: **Customize → Plugins → Add marketplace**, enter `Stevesibilia/stevesibilia-plugins`, install `essentials` and `rpg-prep`, turn on **Sync automatically**. In Claude Code:

```
/plugin marketplace add Stevesibilia/stevesibilia-plugins
/plugin install rpg-prep@stevesibilia
```

Claude Code installs `essentials` with `rpg-prep`, because `rpg-prep` depends on it.

[INSTALL.md](INSTALL.md) has the details and a zip fallback for claude.ai.

## Layout

```
.claude-plugin/marketplace.json    marketplace manifest
plugins/rpg-prep/
  .claude-plugin/plugin.json       plugin manifest, depends on essentials
  skills/*/SKILL.md                the seven RPG skills (+ references/, scripts/)
plugins/essentials/
  .claude-plugin/plugin.json       plugin manifest
  skills/*/SKILL.md                general-purpose skills (scrittura-italiana)
archive/skills/                    superseded skills, kept for reference
docs/similar-skills.md             similar skills found online, and what was borrowed
evals/                             eval prompts and expected outputs
dist/                              zips built by CI on each tag (fallback for claude.ai)
```
