#!/usr/bin/env python3
"""Impagina un'avventura scritta con il modello di enhanced-avventure-rpg in un PDF A4.

Uso: python3 impagina.py avventura.md uscita.pdf

Nessun LLM: la nota viene divisa secondo il modello (sezioni ##, scene ### S1. Nome,
campi in grassetto, blocchi citazione, tabelle) e montata su un modello HTML fisso,
poi WeasyPrint produce il PDF.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from weasyprint import HTML

QUI = Path(__file__).resolve().parent
MD = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table")

GRADI = {"Ordinaria": (3, 1), "Straordinaria": (6, 2), "Leggendaria": (9, 3)}
CAMPI_SCENA = [
    "Luogo e momento", "In gioco", "Da non perdere qui", "Cosa succede da sé", "Chi c'è",
    "Indizi qui", "Prove e regole", "Se deragliano", "Regole della situazione",
    "Cosa decide la notte",
]
CHIAVI_NON_TALENTO = {"Tipo", "Aspetto", "Volontà", "Condotta", "Cosa dice", "Al rito", "Chi è",
                      "Vuole", "Teme", "Cosa dice sempre", "Cosa dice solo a chi le tiene la mano",
                      "Cosa tace", "Al passo 5", "Chi sono", "Come compaiono", "Cosa vogliono",
                      "Se un PG viene cucito"}


def slug(testo: str) -> str:
    testo = testo.lower()
    testo = re.sub(r"[àáâ]", "a", testo)
    testo = re.sub(r"[èéê]", "e", testo)
    testo = re.sub(r"[ìí]", "i", testo)
    testo = re.sub(r"[òó]", "o", testo)
    testo = re.sub(r"[ùú]", "u", testo)
    return re.sub(r"[^a-z0-9]+", "-", testo).strip("-")


def md(testo: str) -> str:
    """Markdown in HTML, con le caselle «- [ ]» trasformate in caselle da spuntare."""
    testo = re.sub(r"^(\s*)- \[[ xX]\] ", r'\1- <span class="box"></span> ', testo, flags=re.M)
    out = MD.render(testo)
    out = out.replace('<li><span class="box"></span>', '<li class="task"><span class="box"></span>')
    out = re.sub(r"<ul>(\s*<li class=\"task\">)", r'<ul class="tasks">\1', out)
    return out


def sezioni(testo: str) -> tuple[str, str, dict[str, str]]:
    righe = testo.splitlines()
    titolo = ""
    if righe and righe[0].startswith("# "):
        titolo = righe[0][2:].strip()
        righe = righe[1:]
    testa, corpo, nome = [], {}, None
    for riga in righe:
        if riga.startswith("## "):
            nome = riga[3:].strip()
            corpo[nome] = []
            continue
        (corpo[nome] if nome else testa).append(riga)
    return titolo, "\n".join(testa), {k: "\n".join(v).strip() for k, v in corpo.items()}


def sottosezioni(testo: str, livello: str = "### ") -> list[tuple[str, str]]:
    parti, nome, buf = [], None, []
    for riga in testo.splitlines():
        if riga.startswith(livello):
            if nome is not None:
                parti.append((nome, "\n".join(buf).strip()))
            nome, buf = riga[len(livello):].strip(), []
        elif nome is not None:
            buf.append(riga)
    if nome is not None:
        parti.append((nome, "\n".join(buf).strip()))
    return parti


def campi_scena(testo: str) -> dict[str, str]:
    """Divide una scena nei suoi campi. Il blocco citazione va in «Leggi», le tabelle in «Reazioni»."""
    campi: dict[str, list[str]] = {"_": []}
    corrente = corrente_prima = "_"
    for riga in testo.splitlines():
        m = re.match(r"^\*\*([^*]+?):?\*\*:?\s*(.*)$", riga)
        if m and m.group(1).strip().rstrip(":") in CAMPI_SCENA:
            corrente = m.group(1).strip().rstrip(":")
            campi[corrente] = [m.group(2)] if m.group(2) else []
            continue
        if riga.startswith(">"):
            blocco = "Leggi" if ("Leggi" not in campi or corrente == "_leggi") else "Documenti"
            if blocco == "Leggi":
                corrente_prima = corrente if corrente != "_leggi" else corrente_prima
                corrente = "_leggi"
            elif corrente != "_doc":
                campi.setdefault("Documenti", []).append("\n<!-- documento -->\n")
                corrente_prima = corrente
                corrente = "_doc"
            campi.setdefault(blocco, []).append(riga[1:].strip())
            continue
        if corrente in ("_leggi", "_doc"):
            if not riga.strip():
                continue
            corrente = corrente_prima
        if riga.startswith("|"):
            campi.setdefault("Reazioni", []).append(riga)
            continue
        campi.setdefault(corrente, []).append(riga)
    return {k: "\n".join(v).strip() for k, v in campi.items()}


def schede(testo: str) -> dict[str, dict]:
    out = {}
    for nome, corpo in sottosezioni(testo):
        voci = re.findall(r"^- \*\*([^*]+?):?\*\*:?\s*(.*)$", corpo, re.M)
        tipo = next((v for k, v in voci if k.rstrip(":") == "Tipo"), "")
        riga_talenti = next((v for k, v in voci if k.rstrip(":") == "Talenti"), None)
        if riga_talenti:
            talenti = [(re.sub(r"\s*\(.*$", "", t).strip(), (re.search(r"\((.*)\)", t) or [None, ""])[1])
                       for t in riga_talenti.split(" · ")]
        else:
            talenti = [(k.rstrip(":"), v) for k, v in voci if k.rstrip(":") not in CHIAVI_NON_TALENTO]
        out[nome] = {"tipo": tipo, "talenti": talenti, "id": "scheda-" + slug(nome)}
    return out


def trova_scheda(nome: str, tutte: dict[str, dict]) -> tuple[str, dict] | None:
    """Nome esatto, oppure la scheda il cui titolo comincia con il nome («Tenente Donato, il Primo…»)."""
    nome = nome.strip()
    if nome in tutte:
        return nome, tutte[nome]
    for k, v in tutte.items():
        if k.startswith(nome + ",") or k.startswith(nome + " "):
            return k, v
    return None


def riquadro_minaccia(nome: str, scheda: dict) -> str:
    grado = next((g for g in GRADI if g in scheda["tipo"]), None)
    if not grado:
        return ""
    ferite, afflizioni = GRADI[grado]
    caselle_f = '<span class="gruppo"></span>'.join(['<span class="box"></span>' * 3] * (ferite // 3))
    caselle_a = '<span class="box"></span>' * afflizioni
    branco = " · branco" if "branco" in scheda["tipo"] else ""
    if len(scheda["talenti"]) > 2:
        nomi = " · ".join(re.sub(r"\s*\(.*?\)", "", k) for k, _ in scheda["talenti"])
        talenti = f"<p><b>Talenti:</b> {html.escape(nomi)}</p>"
    else:
        talenti = "".join(
            f'<p>{md_inline(f"**{k}**: {breve(v)}" if v else f"**{k}**")}</p>' for k, v in scheda["talenti"]
        )
    return (
        f'<div class="minaccia"><div class="m-nome">{html.escape(nome)}</div>'
        f'<div class="m-grado">Minaccia {grado}{branco}</div>'
        f'<div class="m-caselle"><span class="m-etic">Ferite</span><span class="m-fila">{caselle_f}</span></div>'
        f'<div class="m-caselle"><span class="m-etic">Afflizioni</span><span class="m-fila">{caselle_a}</span></div>{talenti}'
        f'<div class="m-rimando"><a href="#{scheda["id"]}">scheda completa</a></div></div>'
    )


def breve(testo: str) -> str:
    """Prima frase, per la scheda breve nella colonna laterale."""
    m = re.match(r"(.+?[.!?])(\s|$)", testo)
    return m.group(1) if m else testo


def md_inline(testo: str) -> str:
    return MD.renderInline(testo)


def collega_schede(htmltesto: str, tutte: dict[str, dict]) -> str:
    def sost(m: re.Match) -> str:
        nome = m.group(1).strip()
        trovata = trova_scheda(nome, tutte)
        if not trovata:
            return m.group(0)
        s = trovata[1]
        return f'→ <a class="rif" href="#{s["id"]}">{html.escape(nome)}</a>'
    return re.sub(r"→ Schede: ([^<.;,]+)", sost, htmltesto)


def linguetta(attiva: str, voci: list[str]) -> str:
    elementi = "".join(
        f'<div class="t{" on" if v == attiva else ""}{" lunga" if len(v) > 3 else ""}">{html.escape(v)}</div>'
        for v in voci
    )
    return f'<div class="linguetta">{elementi}</div>'


def scena_html(titolo: str, corpo: str, tutte: dict[str, dict], voci: list[str]) -> str:
    m = re.match(r"(S\d+)\.\s*(.+)", titolo)
    sid, nome = (m.group(1), m.group(2)) if m else ("", titolo)
    c = campi_scena(corpo)

    laterale = []
    if c.get("Da non perdere qui"):
        laterale.append(f'<div class="riquadro"><h4>Da non perdere qui</h4>{md(c["Da non perdere qui"])}</div>')
    if c.get("Chi c'è"):
        chi = collega_schede(md(c["Chi c'è"]), tutte)
        trovate = [trova_scheda(n, tutte) for n in re.findall(r"→ Schede: ([^\n.;,»]+)", c["Chi c'è"])]
        visti, minacce = set(), ""
        for t in trovate:
            if t and t[0] not in visti:
                visti.add(t[0])
                minacce += riquadro_minaccia(t[0].split(",")[0], t[1])
        laterale.append(f'<div class="chi"><h4>Chi c\'è</h4>{chi}</div>{minacce}')

    principale = []
    if c.get("Leggi"):
        principale.append(f'<div class="leggi"><div class="etichetta">Da leggere</div>{md(c["Leggi"])}</div>')
    for campo in ("Cosa succede da sé", "Indizi qui"):
        if c.get(campo):
            principale.append(f"<h3>{campo}</h3>{collega_schede(md(c[campo]), tutte)}")
    for doc in [d for d in c.get("Documenti", "").split("<!-- documento -->") if d.strip()]:
        principale.append(f'<div class="documento"><div class="etichetta">Documento da consegnare</div>{md(doc)}</div>')
    if c.get("Prove e regole"):
        principale.append(f'<div class="prova"><b>Prove e regole.</b> {md_inline(c["Prove e regole"])}</div>')

    if c.get("Reazioni"):
        principale.append(f'<div class="reazioni">{md(c["Reazioni"])}</div>')
    if c.get("Se deragliano"):
        principale.append(f'<p class="deraglia"><b>Se deragliano.</b> {md_inline(c["Se deragliano"])}</p>')

    sotto = []
    if c.get("Regole della situazione"):
        sotto.append(f'<h3>Regole della situazione</h3>{md(c["Regole della situazione"])}')
    if c.get("Cosa decide la notte"):
        sotto.append(f'<h3>Cosa decide la notte</h3>{md(c["Cosa decide la notte"])}')

    luogo = md_inline(c.get("Luogo e momento", ""))
    ingioco = md_inline(c.get("In gioco", ""))
    return f"""
<section class="scena" id="{slug(titolo)}">
  {linguetta(sid, voci)}
  <div class="piede" data-testo="{html.escape(titolo)}"></div>
  <header class="testata-scena"><div class="num">{sid}</div>
    <div><h2>{html.escape(nome)}</h2><div class="luogo">{luogo}</div></div></header>
  <p class="ingioco"><span class="etichetta">In gioco</span> {ingioco}</p>
  <aside class="laterale">{''.join(laterale)}</aside>
  <div class="principale">{''.join(principale)}</div>
  <div class="sotto">{''.join(sotto)}</div>
</section>"""


def costruisci(testo: str) -> str:
    titolo, testa, sez = sezioni(testo)
    tutte = schede(sez.get("Schede", ""))
    scene = sottosezioni(sez.get("Scene", ""))
    ids = [re.match(r"(S\d+)", n).group(1) for n, _ in scene if re.match(r"S\d+", n)]
    voci = ["Notte", *ids, "Schede"]

    parti = []
    titolo_principale, _, sottotitolo = titolo.partition(":")
    titolo_principale = re.sub(r"\s*\(.*?\)\s*", " ", titolo_principale).strip()
    m = re.search(r"\((.*?)\)", titolo)
    sottotitolo = m.group(1) if m else sottotitolo.strip()

    # Apertura: la vicenda e l'antefatto
    parti.append(f"""
<section class="apertura">
  {linguetta("Notte", voci)}
  <div class="piede" data-testo="La notte"></div>
  <header class="frontespizio"><div class="sopra">{md_inline(testa.strip().splitlines()[0] if testa.strip() else '')}</div>
    <h1>{html.escape(titolo_principale)}</h1><div class="sottotitolo">{html.escape(sottotitolo)}</div></header>
  <div class="meta">{md("\n".join(testa.strip().splitlines()[1:]))}</div>
  {f'<h2 class="sez">La vicenda in breve</h2>{md(sez["La vicenda in breve"])}' if "La vicenda in breve" in sez else ''}
  {f'<h2 class="sez">Antefatto</h2>{md(sez["Antefatto"])}' if "Antefatto" in sez else ''}
</section>""")

    # La notte: colpo d'occhio, promemoria, orologio, verità
    occhio = sez.get("A colpo d'occhio", "")
    riv = occhio.split("**Rivelazioni**", 1)
    occhio_testa, rivelazioni = riv[0], (riv[1] if len(riv) > 1 else "")
    parti.append(f"""
<section class="notte{'' if 'La vicenda in breve' in sez or 'Antefatto' in sez else ' segue'}">
  <h2 class="sez">A colpo d'occhio</h2>
  {md(occhio_testa)}
  <aside class="laterale">
    <div class="riquadro"><h4>Da non perdere stasera</h4>{md(sez.get("Da non perdere stasera", ""))}</div>
    <div class="riquadro"><h4>Rivelazioni</h4>{md(rivelazioni)}</div>
  </aside>
  <div class="principale">
    <h2 class="sez">Orologio</h2>{md(sez.get("Orologio", ""))}
    <h2 class="sez">Verità del mondo</h2>{md(sez.get("Verità del mondo", ""))}
  </div>
</section>""")

    parti.append(f"""
<section class="inizio">
  <h2 class="sez">Inizio forte</h2>
  {re.sub(r"<blockquote>", '<blockquote class="leggi">', md(sez.get("Inizio forte", "")))}
  <h2 class="sez">Mappa delle scene</h2>{md(sez.get("Mappa delle scene", ""))}
</section>""")

    if "Regole della notte" in sez:
        parti.append(f"""
<section class="regole"><h2 class="sez">Regole della notte</h2>
  <div class="due-colonne">{md(sez["Regole della notte"])}</div></section>""")

    for nome, corpo in scene:
        parti.append(scena_html(nome, corpo, tutte, voci))

    # Riferimenti: indizi, PNG, schede, preparazione
    blocchi_schede = []
    for nome, corpo in sottosezioni(sez.get("Schede", "")):
        if nome == "Pregenerati":
            intro, *_ = corpo.split("####", 1)
            cartellini = "".join(
                f'<div class="pregenerato"><h3>{html.escape(n)}</h3>{md(c)}</div>'
                for n, c in sottosezioni(corpo, "#### ")
            )
            blocchi_schede.append(
                f'<div class="pregenerati" id="scheda-pregenerati"><h2 class="sez">Pregenerati</h2>{md(intro)}{cartellini}</div>'
            )
        else:
            blocchi_schede.append(
                f'<div class="scheda" id="scheda-{slug(nome)}"><h3>{html.escape(nome)}</h3>{md(corpo)}</div>'
            )
    parti.append(f"""
<section class="riferimenti">
  {linguetta("Schede", voci)}
  <div class="piede" data-testo="Schede e riferimenti"></div>
  <h2 class="sez">Indizi</h2><div class="tabella-piccola">{md(sez.get("Indizi", ""))}</div>
  <h2 class="sez">PNG</h2><div class="tabella-piccola">{md(sez.get("PNG", ""))}</div>
  <h2 class="sez">Schede</h2>{''.join(blocchi_schede)}
  {f'<h2 class="sez prima">Prima della sessione</h2>{md(sez["Prima della sessione"])}' if "Prima della sessione" in sez else ''}
</section>""")

    css = (QUI / "stile.css").read_text().replace("FONTS/", (QUI / "fonts").as_uri() + "/")
    css = css.replace("TITOLO", titolo_principale.replace('"', "'"))
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>{html.escape(titolo)}</title><style>{css}</style></head><body>{''.join(parti)}</body></html>"""


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip())
        return 2
    sorgente, uscita = Path(sys.argv[1]), Path(sys.argv[2])
    pagina = costruisci(sorgente.read_text())
    uscita.with_suffix(".html").write_text(pagina)
    HTML(string=pagina, base_url=str(QUI)).write_pdf(uscita)
    print(f"PDF scritto: {uscita}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
