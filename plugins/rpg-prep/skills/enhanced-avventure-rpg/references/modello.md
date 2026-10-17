# Modello del documento

Segui quest'ordine di sezioni. I titoli di livello 2 (`##`) sono fissi: lo script di controllo li cerca per nome. «La vicenda in breve» apre sempre il documento; «Antefatto» è facoltativa. I commenti fra `<!-- -->` spiegano la regola e non vanno nel documento.

Identificativi:

- **S1, S2…** per le scene, nel titolo `### S1. Nome`;
- **R1, R2…** per le rivelazioni;
- **I1, I2…** per gli indizi.

Il master li trova con una ricerca (Ctrl+F) in Joplin, in un editor o su carta. Non servono collegamenti.

**Righe vuote.** Ogni campo in grassetto è un paragrafo a sé: una riga vuota prima e dopo. Senza riga vuota, Joplin e ogni visualizzatore Markdown attaccano il campo alla riga precedente. Il modello qui sotto le mostra tutte; non toglierle.

```markdown
# [Titolo]

**Sistema:** … · **Formato:** one-shot / episodio · **Durata:** 4 ore · **Giocatori:** …

**Ambientazione:** luogo, data, arco di tempo della sessione

**Tempi:** S1 30' · S2-S4 2 ore · S5 1 ora · margine 30'

**Campagna:** [nome] · **Arco:** A2. [nome] · **Fronti:** F1 a F1.2 · **Fili:** T3, T5 <!-- solo per un episodio di campagna -->

## La vicenda in breve

<!-- Sempre presente, sempre in testa. È il canovaccio per il master, da leggere prima di giocare:
     chi apre il documento deve capire la storia intera senza leggere le scene.
     Prosa, non elenchi; 300-600 parole; cinque blocchi con l'etichetta in grassetto.
     Adatta le etichette al tempo dell'avventura («Stanotte» o «La giornata», «la serata» o «la giornata»).
     Può dire cosa fanno i PNG e l'antagonista; per i PG descrive la situazione e le
     possibilità, mai le loro scelte. -->

**Il passato.** [Cosa è successo prima della sessione, chi l'ha causato, quali oggetti, luoghi e segreti sono in gioco, e in che modo i PG ne sono già toccati.]

**Stanotte.** [La situazione all'inizio della sessione: cosa vuole l'antagonista, cosa farà se nessuno interviene, quali forze ha in campo, perché proprio ora.]

**Come si gioca la serata.** [La forma della sessione, luogo per luogo, nell'ordine probabile: dove si comincia, cosa si scopre dove, dove sta il climax.]

**Come può finire.** [Gli esiti possibili e cosa li provoca, compreso ciò che accade se i PG non intervengono.]

**Cosa tiene insieme la serata.** [Il legame di ogni PG con la storia (segreti, legami, colpe) e la domanda di fondo.]

## Antefatto

<!-- Facoltativa. Solo se i PG hanno un incarico o un motivo per essere lì che va spiegato
     al master: chi li manda, perché proprio loro, cosa sanno partendo, il viaggio.
     Elenco puntato, al massimo 5 voci. Il testo da leggere ai giocatori sull'incarico
     va in «Inizio forte», prima dell'evento in corso. -->

- **Chi li manda.** …
- **Perché loro.** …
- **Cosa sanno.** …

## A colpo d'occhio

| Dove | Quando | Antagonista | PNG chiave | In gioco stasera |
| ---- | ------ | ----------- | ---------- | ---------------- |
| …    | …      | …           | …          | …                |

**Domanda drammatica:** [una domanda aperta sulle scelte dei PG]

**In una frase:** [la situazione, per il master]

**Rivelazioni**

- **R1.** [conclusione che i PG possono raggiungere] (I1, I2, I3)
- **R2.** …

## Da non perdere stasera

<!-- Al massimo 5 righe. Solo ciò che attraversa tutta la sessione:
     il ritmo dell'orologio, una minaccia che segue i PG, un seme per il futuro,
     il principio di una risorsa del sistema. Ciò che riguarda una scena sola va nella scena. -->

- [ ] …

## Orologio

<!-- 4-6 passi. Ognuno: quando o cosa lo fa scattare, cosa cambia, il segnale che i PG percepiscono.
     L'ultimo passo è ciò che accade se nessuno interviene. -->

- [ ] **1. [Nome] ([quando]).** Cosa cambia. _Segnale:_ cosa si percepisce.
- [ ] **2. …**
- [ ] **Se nessuno interviene.** Cosa accade, e quale occasione resta ai PG.

## Verità del mondo

<!-- Solo per il master. Al massimo 8 voci di una o due righe: ciò che è vero,
     da consultare quando i giocatori chiedono. Niente storia che non cambia le scelte al tavolo. -->

- **[Cosa].** …

## Inizio forte

> [Testo da leggere o parafrasare. Solo ciò che i PG vedono, sentono, odorano.
> Nessuna rivelazione, nessuna emozione attribuita ai PG. Finisce su qualcosa che chiede una reazione.]

**Sotto la superficie:** [cosa sa il master di ciò che i PG stanno percependo]

**Cosa possono percepire subito:** …

## Mappa delle scene

<!-- Una riga per scena, compreso il climax. Indica l'ordine solo dove è obbligato. -->

| #   | Scena | Luogo | In gioco | PNG | Indizi |
| --- | ----- | ----- | -------- | --- | ------ |
| S1  | …     | …     | …        | …   | I1, I4 |

Ordine: S1 apre, S5 chiude; S2, S3 e S4 in qualunque ordine. S4 è facoltativa.

## Scene

### S1. [Nome evocativo]

**Luogo e momento:** …

**In gioco:** …

**Da non perdere qui**

- [ ] [indizio da seminare, momento meccanico, segreto di un PG che la scena tocca]

> [Testo da leggere quando la scena comincia: 2-4 frasi, solo ciò che si percepisce,
> nessuna rivelazione, nessuna emozione dei PG. Finisce su qualcosa che chiede una reazione.]

**Cosa succede da sé**

- …

**Chi c'è**

- **[PNG]**, vuole …; dice: «…» → Schede: [Nome]

**Indizi qui**

<!-- Ogni indizio scritto per esteso, con le rivelazioni a cui porta. Mai solo il numero. -->

- **I1.** [cosa si trova o si sente, e come] (R1)
- **I4.** … (R1, R2)

**Prove e regole:** [termini e difficoltà del sistema, o «[da manuale]»]

| Se i PG…           | Allora…       |
| ------------------ | ------------- |
| [scelta possibile] | [conseguenza] |

**Se deragliano:** [la pressione che resta e li raggiunge comunque]

### S5. [Climax]

<!-- Il climax ha gli stessi campi di ogni scena, compreso il testo da leggere, più questi due. -->

**Regole della situazione**

- **[Condizione].** Cosa accade.

**Cosa decide la notte:** …

## Indizi

<!-- Il tracker: tutti gli indizi, raggruppati per rivelazione, con una casella da spuntare.
     Almeno tre indizi per rivelazione, in almeno due scene diverse.
     Il testo deve coincidere con quello scritto nelle scene. -->

| ID  | Indizio | Rivelazione | Dove | ✓   |
| --- | ------- | ----------- | ---- | --- |
| I1  | …       | R1          | S1   |     |

## PNG

| PNG | Ruolo | Vuole | Teme | Segno distintivo | Frase | Dove |
| --- | ----- | ----- | ---- | ---------------- | ----- | ---- |
| …   | …     | …     | …    | …                | «…»   | S2   |

**Nomi di riserva:** …

## Schede

<!-- Statistiche delle minacce, pregenerati, schede complete dei PNG importanti.
     Una sottosezione per voce, nell'ordine in cui entrano in gioco, con i campi in elenco.
     Se le schede sono già in GDR Archive o in un manuale, qui basta il riassunto
     che serve al tavolo e il riferimento. -->

### [Nome]

- **Tipo:** …
- **Volontà:** …
- **Condotta:** …
- **Talenti:** …

## Prima della sessione

<!-- Ciò che serve prima di sedersi, non durante: materiali da stampare o preparare,
     deragliamenti previsti con la loro risposta, varianti della casa, limiti del tavolo. -->

**Da preparare:** …

**Deragliamenti previsti**

- **[Scelta non prevista].** [Conseguenza, non muro.] (vedi S3)

## Appendice: immagini e musica

<!-- Non serve al tavolo. Le chiavi restano in inglese per midjourney-prompts e per le skill di Suno.
     Stessi titoli delle scene. -->

### S1. [Nome]

visual: [English: concrete subjects, light, era, palette; no PC actions]

mood: [English: emotional register, energy, instrumentation]
```
