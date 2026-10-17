#!/usr/bin/env python3
"""Controlla un documento d'avventura scritto con il modello di enhanced-avventure-rpg.

Uso: python3 controlla.py avventura.md

Gli errori violano il modello e vanno corretti; gli avvisi segnalano scelte da
rivedere. Esce con 1 se c'è almeno un errore.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = [
    "La vicenda in breve",
    "A colpo d'occhio",
    "Da non perdere stasera",
    "Orologio",
    "Verità del mondo",
    "Inizio forte",
    "Mappa delle scene",
    "Scene",
    "Indizi",
    "PNG",
    "Appendice",
]
OPTIONAL = ["Antefatto", "Schede", "Prima della sessione"]
SCENE_FIELDS = [
    ("**Da non perdere qui**", "Da non perdere qui"),
    ("**Cosa succede da sé**", "Cosa succede da sé"),
    ("**Se deragliano:**", "Se deragliano"),
]
PREAMBLE_WORDS = 700
SYNOPSIS_WORDS = (300, 600)
GLOBAL_REMINDERS = 5


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def section_name(title: str) -> str | None:
    for name in REQUIRED + OPTIONAL:
        if title == name or title.startswith(name + ":") or title.startswith(name + " "):
            return name
    return None


def split_sections(lines: list[str]) -> dict[str, tuple[int, int]]:
    """Map each known H2 section to its (start, end) line range."""
    heads = [(i, line[3:].strip()) for i, line in enumerate(lines) if line.startswith("## ")]
    out = {}
    for n, (start, title) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        name = section_name(title)
        if name:
            out[name] = (start, end)
    return out


def check(path: Path) -> Report:
    report = Report()
    lines = path.read_text().splitlines()
    sections = split_sections(lines)

    # Sections: present, and in the expected order.
    for i, line in enumerate(lines):
        if line.startswith("## ") and not section_name(line[3:].strip()):
            report.warn(f"riga {i + 1}: sezione fuori modello «{line[3:].strip()}»")
    missing = [name for name in REQUIRED if name not in sections]
    for name in missing:
        report.error(f"manca la sezione «## {name}»")
    present = [name for name in REQUIRED if name in sections]
    if [sections[n][0] for n in present] != sorted(sections[n][0] for n in present):
        report.error("le sezioni non seguono l'ordine del modello: " + ", ".join(
            sorted(present, key=lambda n: sections[n][0])))

    # Forbidden dashes, per scrittura-italiana.
    for i, line in enumerate(lines):
        for dash in ("—", "–"):
            if dash in line:
                report.error(f"riga {i + 1}: trattino «{dash}» vietato: {line.strip()[:70]}")

    # A bold or italic field must start its own paragraph: without a blank line
    # before it, Markdown renderers merge it into the previous line.
    in_comment = False
    for i, line in enumerate(lines):
        if "<!--" in line:
            in_comment = "-->" not in line
            continue
        if in_comment:
            in_comment = "-->" not in line
            continue
        previous = lines[i - 1].strip() if i else ""
        if re.match(r"(\*\*|_|\*[^\s*])", line) and previous and not previous.startswith("#"):
            report.error(f"riga {i + 1}: manca una riga vuota prima di «{line.strip()[:40]}»: "
                         "si attacca alla riga precedente")

    # visual:/mood: belong to the appendix only.
    appendix_start = sections.get("Appendice", (len(lines), len(lines)))[0]
    for i, line in enumerate(lines[:appendix_start]):
        if re.match(r"\s*(visual|mood):", line):
            report.error(f"riga {i + 1}: «{line.split(':')[0].strip()}:» fuori dall'appendice")

    # The synopsis opens the document, before everything else.
    if "La vicenda in breve" in sections:
        start, end = sections["La vicenda in breve"]
        first_h2 = next((i for i, l in enumerate(lines) if l.startswith("## ")), start)
        if first_h2 != start:
            report.error("«La vicenda in breve» deve essere la prima sezione del documento")
        words = len(re.sub(r"<!--.*?-->", "", "\n".join(lines[start + 1:end]), flags=re.S).split())
        low, high = SYNOPSIS_WORDS
        if not low <= words <= high:
            report.warn(f"«La vicenda in breve» ha {words} parole (tra {low} e {high})")

    # The first page, from the glance to the strong start, must fit one screen.
    if "Inizio forte" in sections and "A colpo d'occhio" in sections:
        start = sections["A colpo d'occhio"][0]
        words = len(" ".join(lines[start:sections["Inizio forte"][0]]).split())
        if words > PREAMBLE_WORDS:
            report.warn(f"da «A colpo d'occhio» a «Inizio forte» ci sono {words} parole (massimo {PREAMBLE_WORDS})")

    if "Da non perdere stasera" in sections:
        start, end = sections["Da non perdere stasera"]
        bullets = [l for l in lines[start + 1:end] if re.match(r"\s*- ", l)]
        if len(bullets) > GLOBAL_REMINDERS:
            report.error(f"«Da non perdere stasera» ha {len(bullets)} righe (massimo {GLOBAL_REMINDERS})")

    # Scenes: headings, fields, and agreement with the scene map.
    scenes: dict[str, str] = {}
    if "Scene" in sections:
        start, end = sections["Scene"]
        heads = [(i, lines[i]) for i in range(start + 1, end) if lines[i].startswith("### ")]
        for n, (i, head) in enumerate(heads):
            match = re.match(r"### (S\d+)\. \S", head)
            if not match:
                report.error(f"riga {i + 1}: titolo di scena fuori modello, atteso «### S1. Nome»: {head}")
                continue
            stop = heads[n + 1][0] if n + 1 < len(heads) else end
            body = "\n".join(lines[i:stop])
            scenes[match.group(1)] = body
            for marker, label in SCENE_FIELDS:
                if marker not in body:
                    report.error(f"{match.group(1)}: manca «{label}»")
            if not re.search(r"^\|\s*Se i PG", body, re.M):
                report.error(f"{match.group(1)}: manca la tabella «Se i PG… | Allora…»")
            if not re.search(r"^> ?\S", body, re.M):
                report.error(f"{match.group(1)}: manca il testo da leggere (blocco «>»)")
            written = re.findall(r"^- \*\*(I\d+)\.\*\* \S.{10,}", body, re.M)
            if "**Indizi qui" not in body:
                report.warn(f"{match.group(1)}: nessun campo «Indizi qui»")
            elif not written:
                report.error(f"{match.group(1)}: «Indizi qui» deve scrivere gli indizi per esteso "
                             "(«- **I1.** testo (R1)»), non solo il numero")
        if not scenes:
            report.error("nessuna scena «### S1. Nome» dentro «## Scene»")

    if "Mappa delle scene" in sections:
        start, end = sections["Mappa delle scene"]
        mapped = re.findall(r"^\|\s*(S\d+)\s*\|", "\n".join(lines[start:end]), re.M)
        for sid in sorted(set(mapped) - set(scenes)):
            report.error(f"la mappa elenca {sid}, che non ha una scena")
        for sid in sorted(set(scenes) - set(mapped)):
            report.error(f"{sid} non compare nella mappa delle scene")

    # Clues: at least three per revelation, each one placed in a scene.
    revelations = []
    if "A colpo d'occhio" in sections:
        start, end = sections["A colpo d'occhio"]
        revelations = re.findall(r"\*\*(R\d+)\.\*\*", "\n".join(lines[start:end]))
        if not revelations:
            report.error("«A colpo d'occhio» non elenca rivelazioni «**R1.** …»")
    clues: dict[str, tuple[list[str], list[str]]] = {}
    if "Indizi" in sections:
        start, end = sections["Indizi"]
        for line in lines[start:end]:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and re.fullmatch(r"I\d+", cells[0]) and len(cells) >= 4:
                clues[cells[0]] = (re.findall(r"R\d+", cells[2]), re.findall(r"S\d+", cells[3]))
        if not clues:
            report.error("la tabella «Indizi» non ha righe «| I1 | … | R1 | S1 | |»")
    for rid in revelations:
        linked = [cid for cid, (rids, _) in clues.items() if rid in rids]
        if len(linked) < 3:
            report.error(f"{rid} ha {len(linked)} indizi (minimo 3)")
        places = {sid for cid in linked for sid in clues[cid][1]}
        if linked and len(places) < 2:
            report.warn(f"{rid}: tutti gli indizi stanno in una sola scena")
    scene_text = "\n".join(scenes.values())
    for cid, (rids, sids) in clues.items():
        for rid in rids:
            if rid not in revelations:
                report.error(f"{cid} rimanda a {rid}, che non è fra le rivelazioni")
        for sid in sids:
            if sid not in scenes:
                report.error(f"{cid} sta in {sid}, che non esiste")
        if not re.search(rf"^- \*\*{cid}\.\*\* \S", scene_text, re.M):
            report.error(f"{cid} è nel tracker ma non è scritto per esteso in nessuna scena")
        for sid in sids:
            if sid in scenes and not re.search(rf"^- \*\*{cid}\.\*\* \S", scenes[sid], re.M):
                report.warn(f"{cid}: il tracker lo mette in {sid}, ma {sid} non lo scrive")

    # Appendix: a visual and a mood per scene.
    if "Appendice" in sections:
        start, end = sections["Appendice"]
        text = "\n".join(lines[start:end])
        for sid in scenes:
            block = re.search(rf"^### {sid}\. .*?(?=^### |\Z)", text, re.M | re.S)
            if not block:
                report.warn(f"{sid}: nessuna voce in appendice")
                continue
            for key in ("visual", "mood"):
                if not re.search(rf"^{key}:", block.group(0), re.M):
                    report.warn(f"{sid}: manca «{key}:» in appendice")

    return report


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    report = check(Path(sys.argv[1]))
    for message in report.errors:
        print(f"errore: {message}")
    for message in report.warnings:
        print(f"avviso: {message}")
    print(f"\n{len(report.errors)} errori, {len(report.warnings)} avvisi")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
