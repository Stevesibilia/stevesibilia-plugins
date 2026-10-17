# Installing the plugins

Nine skills: `campagna-rpg`, `enhanced-avventure-rpg`, `impagina-avventura`, `revisione-avventura`, `cronaca-di-sessione`, `scrittura-italiana`, `midjourney-prompts`, `suno-prompts`, `suno-prompt-creator`.

The repository is public at <https://github.com/Stevesibilia/stevesibilia-plugins> and is a Claude plugin marketplace named `stevesibilia`. `.claude-plugin/marketplace.json` lists two plugins:

- `essentials`: general-purpose skills, today `scrittura-italiana`.
- `rpg-prep`: the eight RPG skills. It depends on `essentials`, because every RPG skill applies `scrittura-italiana`. A plugin installed on your Claude account is available in chat, in Cowork and in Claude Code.

## 1. Claude.ai, desktop and mobile apps

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Add marketplace** and enter `Stevesibilia/stevesibilia-plugins` (or `https://github.com/Stevesibilia/stevesibilia-plugins`).
3. Install the `essentials` and `rpg-prep` plugins.
4. On the marketplace, turn on **Sync automatically**, or select **Check for updates** after each change.

The [plugin guide](https://claude.com/docs/cowork/guide/plugins.md) supports marketplaces on github.com, gitlab.com and bitbucket.org; self-hosted instances are refused unless an organisation configures them.

If you previously uploaded these skills as zips, remove those copies, or every skill will exist twice.

## 2. Claude Code

```
/plugin marketplace add Stevesibilia/stevesibilia-plugins
/plugin install rpg-prep@stevesibilia
```

Claude Code installs `essentials` too, as a dependency of `rpg-prep`. Install `essentials@stevesibilia` alone to get the general-purpose skills without the RPG ones.

Update after a change:

```
/plugin marketplace update stevesibilia
```

From a local clone instead, for editing:

```
/plugin marketplace add /path/to/stevesibilia-plugins
```

## Upgrading from the `rpg-prep` marketplace name

Until version 0.6.0 the repository was `Stevesibilia/rpg-prep` and the marketplace was named `rpg-prep`, so the plugin was `rpg-prep@rpg-prep`. GitHub redirects the old repository URL. The rename changes every plugin ID. Remove the old marketplace and add the repository again:

```
/plugin marketplace remove rpg-prep
/plugin marketplace add Stevesibilia/stevesibilia-plugins
/plugin install rpg-prep@stevesibilia
```

On claude.ai, remove the marketplace under **Customize → Plugins**, add it again, and install both plugins.

## 3. Fallback: zip upload on claude.ai

Every tag builds one zip per skill, across both plugins, and attaches them to the [release](https://github.com/Stevesibilia/stevesibilia-plugins/releases), built by `.github/workflows/release.yml`. On claude.ai: **Settings → Capabilities → Skills → Upload skill**, one zip per skill. Re-upload after each release.

To build the zips locally:

```bash
mkdir -p dist
for d in plugins/*/skills/*/; do
  s="$(basename "$d")"
  (cd "$(dirname "$d")" && zip -qr "$OLDPWD/dist/$s.zip" "$s")
done
```

## Using the skills

Skills trigger when the request matches their description. A typical flow:

```
> Progetta la campagna: Venezia 1923, le isole della laguna si svuotano
  → campagna-rpg writes the Joplin note «Campagna: La Laguna Muta»

> Prepara l'avventura di sabato per Symbaroum: il villaggio ai margini
  del Davokar è stato abbandonato in una notte
  → enhanced-avventure-rpg produces the full Italian adventure doc

> Rivedi l'avventura: regge?
  → revisione-avventura reports the problems in the chat, then brainstorms fixes

> Dammi le immagini per tutte le scene
  → midjourney-prompts reads the visual: fields, emits MJ prompts

> E le musiche
  → suno-prompts reads the mood: fields, emits Suno prompts
```

You can also name a skill explicitly: «usa revisione-avventura su questa avventura».

## Keeping everything in sync

This repository is the single source of truth.

1. Edit `plugins/<plugin>/skills/<name>/`.
2. Push to `main`. A marketplace with sync turned on picks the change up; in Claude Code, run `/plugin marketplace update stevesibilia`.
3. Tag a release only if you still use the zip fallback.
