---
name: impagina-avventura
description: "Impagina un'avventura scritta con il modello di enhanced-avventure-rpg in un PDF A4 da usare al tavolo: frontespizio, vicenda in breve, colpo d'occhio con colonna laterale, una pagina per scena con linguette sul bordo, riquadri delle minacce con caselle per ferite e afflizioni, tabelle di indizi e PNG, schede. Lo fa uno script a regole (Python e WeasyPrint), senza riscrivere il testo. Usala quando il master vuole il PDF, la stampa o l'impaginazione di un'avventura, di una one-shot o di una sessione, da un file Markdown o da una nota Joplin. Frasi tipiche: «impagina l'avventura», «fammi il PDF», «la voglio stampare», «PDF per il tavolo», «make a PDF of the adventure»."
---

# Impaginare un'avventura in PDF

Trasforma una nota d'avventura nel modello di `enhanced-avventure-rpg` in un PDF A4 da consultare al tavolo. Il lavoro lo fa `scripts/impagina.py`: legge la nota secondo il modello (sezioni `##`, scene `### S1. Nome`, campi in grassetto, blocchi citazione, tabelle), la monta su un modello HTML fisso e WeasyPrint produce il PDF. Tu prepari la nota, lanci lo script e controlli il risultato. **Non riscrivere il contenuto per farlo entrare nel PDF**: se la nota non segue il modello, dillo al master.

Scrivi al master in **italiano** e applica la skill `scrittura-italiana`.

## Cosa lo script impagina

Lo script cerca le sezioni per nome. Tutto il resto **non entra nel PDF**, senza avvisi:

| Pagine             | Sezioni `##` lette                                                                                   |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| Apertura           | titolo `#`, righe di testa, «La vicenda in breve», «Antefatto»                                       |
| La notte           | «A colpo d'occhio» (con «**Rivelazioni**»), «Da non perdere stasera», «Orologio», «Verità del mondo» |
| Inizio             | «Inizio forte», «Mappa delle scene», «Regole della notte»                                            |
| Una pagina a scena | «Scene», con le scene `### S1. Nome`                                                                 |
| Riferimenti        | «Indizi», «PNG», «Schede» (con `### Pregenerati` e i `####` dei personaggi), «Prima della sessione»  |

L'appendice con `visual:` e `mood:` resta fuori di proposito: serve prima della sessione, non al tavolo.

Dentro una scena lo script riconosce i campi in grassetto del modello («Luogo e momento», «In gioco», «Da non perdere qui», «Cosa succede da sé», «Chi c'è», «Indizi qui», «Prove e regole», «Se deragliano», «Regole della situazione», «Cosa decide la notte»). Il primo blocco citazione diventa «Da leggere», i successivi «Documento da consegnare», la tabella «Se i PG… | Allora…» le reazioni. Ogni `→ Schede: Nome` diventa un rimando alla scheda; se la scheda ha `- **Tipo:** Minaccia Ordinaria`, `Straordinaria` o `Leggendaria` (i gradi di Kulthos), accanto alla scena compare un riquadro con le caselle di ferite e afflizioni.

## Workflow

### 1. Procurati la nota

- **File Markdown**: usalo così com'è.
- **Nota Joplin**: leggila con `get_note` e scrivi il corpo in un file `.md` temporaneo. In Joplin il titolo sta fuori dal corpo: se il corpo non comincia con `# Titolo`, aggiungilo tu, prendendolo dal titolo della nota.

### 2. Prepara il file

Lo script è rigido sulla prima riga, quindi lavora su una copia:

- La **prima riga** deve essere `# Titolo`, senza righe vuote o commenti prima. Il titolo diventa il frontespizio e il piè di pagina; quello che sta fra parentesi, o dopo i due punti, diventa il sottotitolo.
- Togli i commenti `<!-- … -->`: lo script li stamperebbe come testo.

```bash
python3 -c "import re,sys; t=open(sys.argv[1]).read(); open(sys.argv[2],'w').write(re.sub(r'<!--.*?-->\n?','',t,flags=re.S).lstrip())" avventura.md pronta.md
```

Poi confronta i titoli `##` della nota (`grep '^## ' pronta.md`) con la tabella sopra. Se una sezione non è fra quelle lette e non è l'appendice, avvisa il master che resterà fuori dal PDF.

Se c'è la skill `enhanced-avventure-rpg`, lancia anche il suo `scripts/controlla.py` sulla copia. Gli errori di struttura (sezioni mancanti, scene senza campi) diventano pagine vuote o campi persi: riferiscili al master e proponi di sistemare la nota con `enhanced-avventure-rpg` prima di impaginare. Gli avvisi non bloccano.

### 3. Controlla le dipendenze

Servono Python 3.12 o successivo, `markdown-it-py` e `weasyprint` (vedi `scripts/requirements.txt`). WeasyPrint ha bisogno delle librerie Pango.

```bash
python3 -c "import weasyprint, markdown_it"
```

Se fallisce, in ordine:

1. **Ambiente virtuale**: `python3 -m venv .venv-impagina && .venv-impagina/bin/pip install -r <cartella della skill>/scripts/requirements.txt`, poi usa `.venv-impagina/bin/python3`.
2. **Pango mancante** (su Linux di solito c'è; su Mac `brew install pango`). È un'installazione di sistema: chiedi al master prima di farla.
3. **Docker**, se c'è e il master non vuole installare niente:

   ```bash
   docker run --rm -v "<cartella della skill>/scripts":/app:ro -v "$PWD":/lavoro python:3.12-slim sh -c \
     'apt-get update -qq && apt-get install -y -qq libpango-1.0-0 libpangoft2-1.0-0 >/dev/null \
      && pip install -q -r /app/requirements.txt && python3 /app/impagina.py /lavoro/pronta.md /lavoro/avventura.pdf'
   ```

### 4. Impagina

```bash
python3 <cartella della skill>/scripts/impagina.py pronta.md avventura.pdf
```

Lo script scrive anche `avventura.html` accanto al PDF, utile per capire un problema di impaginazione. Se il PDF va bene, cancellalo insieme alla copia preparata.

Salva il PDF dove il master chiede. Se non lo dice, mettilo accanto al file Markdown con lo stesso nome; se la nota viene da Joplin, proponi di allegare il PDF alla nota con `add_attachment`.

### 5. Guarda il risultato

Apri il PDF e guarda almeno la prima pagina, una scena e le schede. Controlla che:

- il titolo stia nel frontespizio e nel piè di pagina;
- non compaiano `<!--`, `**` o `→ Schede:` come testo;
- ogni scena abbia la sua pagina, con la linguetta giusta accesa;
- i riquadri delle minacce compaiano accanto alle scene che le nominano.

Se qualcosa non torna, la causa è quasi sempre nella nota (un campo scritto in modo diverso dal modello, una scena senza `S1.`). Dì al master cosa cambiare nella nota; non correggere lo script per un caso singolo.

## Limiti da conoscere

- Le etichette «Notte» (linguetta) e «La notte» (piè di pagina) sono fisse, anche per un'avventura di giorno.
- I riquadri delle minacce esistono solo per i gradi di Kulthos; con altri sistemi le schede restano in fondo, raggiungibili dai rimandi.
- Il carattere è fisso: Spectral, IM Fell English e IBM Plex Sans Condensed, in `scripts/fonts/` (Google Fonts, licenza OFL).
