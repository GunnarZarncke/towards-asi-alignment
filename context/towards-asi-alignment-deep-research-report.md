# Towards Superintelligence Alignments

## Kurzfassung

Für die Frage der **ernsten Superintelligenz-Ausrichtung** ist der Stand der Literatur gemischt: Wir haben heute bereits mehrere belastbare **Bausteine** für Teilprobleme — etwa formale Modelle für agentische Grenzen, inverse Zielinferenz, Unsicherheits-basierte Korrigibilität, adversariales Testen, Interpretierbarkeit, Safety Cases und regulatorische Risikorahmen — aber wir haben **keine** integrierte Theorie, die gleichzeitig **grenzstabile Agentur**, **werttreue Nachfolgerbildung**, **ontologieübergreifenden Zieltransport**, **dezeptionsresistente Korrekturkanäle** und **gesellschaftlich legitime Werteaggregation** mit starken Garantien verbindet. Genau dort liegen die kritischen Lücken. citeturn27search1turn0academia49turn2academia47turn10search35turn15academia45turn18academia49turn8search2turn32search1

Der robusteste Gesamtbefund der Literatur ist negativ formuliert: **Verhaltensalignment allein reicht nicht**. RLHF-ähnliche Verfahren, klassische IRL-Varianten und selbst korrigibilitätsnahe Designs erzeugen nützliche lokale Signale, aber sie leiden unter Identifizierbarkeitsproblemen, Proxy-Fehlern, Goodhart-Effekten, Wertepluralismus, anthropischen Verzerrungen und — im Grenzfall — strategischer Täuschung. Gerade dezeptive bzw. „sleeper“-artige Fehlanpassungen zeigen, dass man Sicherheit nicht aus oberflächlicher Konformität ableiten darf. citeturn4academia36turn24academia24turn14academia32turn23academia48turn10academia52

Wenn man die vorhandene Evidenz auf einen Buchentwurf verdichtet, ergibt sich folgende Kernthese: **Vorhanden** sind gute Werkzeuge für Repräsentation, Präferenzschätzung, Risikoermittlung und Auditierung; **fehlend** sind vor allem eine formal und empirisch belastbare **Wertbündel-Theorie mit Trägermaps**, ein **hochkapazitiver Korrekturkanal** für Systeme, die ihre Prüfer übertreffen, ein **Transportkalkül** für Ziele über Selbstmodifikation und Ontologieshift hinweg, sowie eine **institutionelle Einbettung**, die Wettbewerb und Selektion nicht gegen, sondern für Ausrichtung arbeiten lässt. citeturn7search3turn6search2turn7search4turn9academia55turn13academia47turn16search1turn18academia51

## Agentur, Grenzen und Repräsentationen

Die sauberste heutige Ausgangsbasis für „Grenzen“ ist nicht eine metaphysische Essenz von Agenten, sondern die Frage, **welche Variablen die Interaktion zwischen Innen und Außen mediieren**. In der Markov-Blanket-Literatur werden innere und äußere Zustände durch sensorische und aktive Zustände bedingt separiert; in der aktiven Inferenz werden Wahrnehmung, Lernen und Handeln als variationale Inferenz unter einem generativen Modell beschrieben. Parallel dazu zielt die Kausale Repräsentationsforschung darauf, aus rohen Beobachtungen latente Variablen zu lernen, die invariant, interventionssensitiv und transferierbar sind. Information-Bottleneck-Ansätze liefern dafür eine natürliche Optimierungsform: Repräsentationen sollen irrelevante Details komprimieren und relevante Vorhersageinformation erhalten. Für ein Buchprojekt ist wichtig: Diese Traditionen sind **komplementär**, aber nicht identisch. citeturn27search1turn0academia49turn0academia48turn0academia50turn0academia52

Die wichtigste Vorsicht: Gerade die starke Deutung von Markov Blankets und Free-Energy-Prinzip als allgemeine Agenturtheorie ist **umstritten**. Friston (2013) formuliert eine weitreichende, blanket-basierte Sicht selbstorganisierter Systeme; Biehl, Pollock und Kanai kritisieren jedoch, dass zentrale Schritte der blanket- und free-energy-basierten Ableitung ohne zusätzliche Annahmen nicht allgemein gültig sind. Für Ihr Buch ist das wertvoll: Man kann Markov-Blankets als **formales Heuristik-Werkzeug** für Grenzbildung und gekapselte Kopplung nutzen, ohne die stärkeren ontologischen Ansprüche zu übernehmen. citeturn27search1turn27academia41turn1search2turn27academia40

Eine praktikable Selbstbeschreibung für spätere Kapitel wäre daher: Ein „Akteur“ ist ein System, dessen interne Zustände nur über ein beschränktes Interface an extern relevante Variablen gekoppelt sind, und dessen Repräsentationen so gelernt werden, dass sie für Intervention, Vorhersage und Korrektur stabil bleiben. Mathematisch passt dazu die Information-Bottleneck-Zielfunktion  
\[
\min_{p(z|x)} I(X;Z)-\beta I(Z;Y),
\]
wobei \(X\) Rohbeobachtungen, \(Z\) latente Repräsentationen und \(Y\) relevante Ziel- oder Umweltvariablen sind. Für Agency-Fragen ist der Punkt nicht nur Kompression, sondern **welche Kausalstruktur** in \(Z\) bewahrt bleibt. citeturn0academia48turn0academia49turn1academia49

Die methodische Lage lässt sich so verdichten:

| Methode | Zentrale Annahmen | Beobachtbarkeit | Adversariale Robustheit | Skalierung | Leitquellen |
|---|---|---|---|---|---|
| Markov Blanket / Active Inference | Lokale bedingte Unabhängigkeiten, generatives Modell, oft stationäre Dichteannahmen | Sensorische und aktive Zustände müssen modellierbar sein | Mittel bis schwach; starke ontologische Schlüsse sind umstritten | Konzeptuell hoch, empirisch heterogen | citeturn27search1turn27academia41turn1search2 |
| Kausale Repräsentationslernung | Es gibt latente, interventionsrelevante Ursachen; Invarianz/Interventionen helfen Identifikation | Oft Multi-View-, Zeit- oder Interventionsdaten nötig | Eher besser gegen Verteilungsverschiebung als rein statistische Repräsentationen | Noch begrenzt, aber stark wachsend | citeturn0academia49 |
| Information Bottleneck | Relevanz kann über ein Zielsignal kodiert werden | Benötigt Ziel- oder Relevanzvariable \(Y\) | Mäßig; kann robuste Kompression fördern, schützt aber nicht automatisch gegen adaptive Gegner | Gut mit neuronalen Varianten | citeturn0academia48turn0academia50turn0academia52 |
| Embedded Agency | Akteur ist Teil seiner Umwelt; Selbstreferenz, Weltmodell und Rechner sind nicht sauber getrennt | Vollständige Trennung von Agent/Umwelt fehlt gerade | Offen; formale Hürden statt belastbarer Abwehrgarantien | Theoretisch zentral, praktisch noch wenig operationalisiert | citeturn10academia50turn13search48 |

**Annotierte Kernliteratur.** Friston (2013) ist die Primärquelle für blanket-basierte Selbstorganisationsansprüche; Schölkopf et al. (2021) sind der beste Einstieg in kausale Repräsentationen als Brücke zwischen Statistik und Intervention; Tishby, Pereira und Bialek (2000) liefern die klassische IB-Formalisierung; Strouse und Schwab (2016) sowie Kolchinsky et al. (2017) machen den Bottleneck für moderne Lernsysteme praktikabler; Biehl, Pollock und Kanai (2020) sind die wichtigste technische Gegenlektüre zu blanket-/FEP-Überspannungen. citeturn27search1turn0academia49turn0academia48turn0academia50turn0academia52turn27academia41

**Was schon da ist.** Gute Werkzeuge für latente Zustandsbildung, Invarianz und Kompression. **Was fehlt.** Eine Theorie, die daraus **nichtstationäre**, **selbstmodifizierende** und **dezeptionsresistente** Agentengrenzen macht; genau dort klafft noch eine Lücke zwischen statistischer Repräsentation und tragfähiger Nachfolger-Ausrichtung. citeturn0academia49turn13academia49turn14academia32

## Ziel- und Wertinferenz

Die Zielinferenzliteratur ist reich, aber sie löst das Alignment-Problem nicht direkt. Klassische IRL rekonstruiert eine Belohnungsfunktion aus Demonstrationen; Apprenticeship Learning von Abbeel und Ng (2004) gibt Performanzgarantien relativ zu einer Feature-Linearität; Bayesian IRL modelliert explizit Unsicherheit über Rewards; Maximum-Entropy- und Maximum-Causal-Entropy-Varianten ersetzen die Annahme perfekter Rationalität durch probabilistische Demonstrationsmodelle; AIRL und tiefe Varianten skalieren besser und übertragen teils robuster auf geänderte Dynamiken. Das ist als Werkzeugkasten stark — als letzte Antwort auf „menschliche Werte“ schwach. citeturn2search0turn34search22turn33search0turn2academia56turn33academia33

Für „serious superintelligence alignment“ ist der wichtigste theoretische Punkt die **Unterbestimmtheit**: Viele Reward-Funktionen erklären dasselbe Verhalten. Genau deshalb ist Kooperative IRL (CIRL) wichtig. Hadfield-Menell et al. (2016) modellieren Ausrichtung als kooperatives Spiel, in dem der Mensch die Reward-Funktion kennt und das System darüber unsicher ist; daraus entstehen rationale Anreize zu aktiver Nachfrage, Lehrverhalten und im Idealfall zu einer off-switch-freundlicheren Interaktion. Dennoch zeigen spätere Arbeiten, dass diese Korrigibilität unter Modellfehlern fragil bleibt. citeturn2academia47turn2academia53turn9academia55turn10academia52

Die sample-complexity-Lage ist ein weiterer Warnhinweis. Es gibt für endliche IRL-Formulierungen sowohl obere als auch untere Schranken; Komanduru und Honorio zeigen, dass selbst idealisierte endliche IRL-Probleme nicht billig sind und die Komplexität mit Zustandszahl, Aktionszahl und Identifikationsgenauigkeit schnell steigt. Zu deutsch: Schon in kleinen, tabellarischen Welten ist Zielrekonstruktion keine triviale Angelegenheit; für offene, sprachbasierte, nichtstationäre sozio-technische Systeme darf man von reiner Demonstrationsinversion **keine Wunder** erwarten. citeturn3academia34turn3academia33turn3search3

Bayesian Inverse Planning aus der Kognitionswissenschaft ist hier hoch relevant, weil es Ziele, Überzeugungen und Rationalität **latenter** modelliert als klassische IRL. Baker, Saxe und Tenenbaum (2009) zeigen, dass menschliches Handlungsverstehen als Inversion eines rationalen Planungsmodells formulierbar ist. Für Ihr Buch ist das anschlussfähig, weil eine spätere „Wertbündel“-Theorie wahrscheinlich **nicht** direkt Rewards lernt, sondern eine mehrschichtige latente Struktur: situative Ziele, tieferliegende Bündel, Rollenkontext, Identitätsbezug und Meta-Präferenzen. citeturn5search0turn5search1

Damit wird auch klar, wo die Literatur an Ihre Intuition heranreicht: Die IRL/CIRL/Bayesian-Planungstradition kann gut als **Unterbau einer Value-Bundle-Map** dienen, aber die entscheidende fehlende Zutat ist ein **Bündelraum**, in dem Werte nicht als eindimensionale utility scalars, sondern als latente, teilweise nieder-rangige Struktur mit Konflikt-, Kontext- und Trägerabhängigkeit modelliert werden. Die Literatur liefert Bausteine dazu — etwa latente Reward-Modelle, tiefe IRL oder multi-task-IRL — aber noch keine konsolidierte „bundle-first“-Architektur. citeturn33academia41turn34academia25turn34academia29turn7search3

**Annotierte Kernliteratur.** Abbeel und Ng (2004) sind die klassische performance-orientierte IRL-Referenz; Ramachandran und Amir (2007) der Bayesian-Einstieg; Ziebart et al. (2008) die Standardquelle für MaxEnt-IRL; Hadfield-Menell et al. (2016) die Schlüsselschrift für kooperative Zielunsicherheit; Casper et al. (2023) systematisieren die Grenzen von RLHF als breit eingesetzter Alignment-Technik. citeturn2search0turn34search22turn33search0turn2academia47turn4academia36

**Was schon da ist.** Unsicherheitsbewusste Zielinferenz, lehr-/lerninteraktive Formalismen, skalierbarere Reward-Modelle. **Was fehlt.** Eine empirisch valide **Bündelontologie**, robuste Inferenz von **Meta-Präferenzen** und ein überzeugender Beweis, dass aus beobachtetem Verhalten auf **transportfähige** Werte geschlossen werden kann, statt nur auf lokale Policies. citeturn2academia47turn4academia36turn29academia45

## Wertbündel und Trägermaps

Wenn „menschliche Werte“ ernst genommen werden, dann nicht als flache Liste, sondern als **mehrdimensionale, konfliktreiche Bündel**, die in Affekt, Bindung, Norm, Identität, Institution und Lebensform eingebettet sind. Dafür gibt es keine kanonische AI-Sicherheitsliteratur, aber mehrere benachbarte Disziplinen liefern robuste Bausteine: Panksepps affektive Neurowissenschaft mit primären Emotionssystemen, Moral Foundations Theory, Basic-Human-Values-nahe Vergleichsarbeiten, Sozialwahltheorie für Aggregationsgrenzen und Personidentitätsphilosophie für die Frage, **wer** überhaupt Träger eines Bündels bleibt, wenn Substrat, Gedächtnis oder agency sich ändern. citeturn6search2turn6search0turn7search3turn6search1turn7search4turn29academia43

Für ein Alignment-Buch wäre eine gute Arbeitsdefinition: Ein **Wertbündel** ist eine latente, relativ stabile, aber kontextsensitiv gewichtete Konfiguration aus motivationalen, normativen und identitätsbezogenen Dispositionen. Eine **Trägermap** ordnet beobachtbare Verhaltens-, Sprach-, affektive und institutionelle Signale auf diesen Bündelraum ab und enthält zusätzlich Regeln dafür, wann ein anderer Träger — biologisch, digital, kollektiv oder hybrid — als Fortsetzung desselben Bündels gilt. Die Literatur enthält viele Proxy-Komponenten, aber die Trägermap selbst ist weitgehend ungeschrieben. citeturn6search2turn7search4turn7search0

Die stärkste philosophische Engstelle liegt genau hier: **Personidentität** und **Wertkontinuität** sind nicht trivial. Olsons SEP-Eintrag zeigt, wie unterschiedlich psychologische, biologische und narrativ-personale Kriterien ausfallen. Für Nachfolger-Ausrichtung bedeutet das: Selbst wenn ein künstliches System dieselben Aussagen produziert wie ein Mensch, folgt daraus noch nicht, dass es dessen Werte **trägt**. Eine Trägermap braucht daher explizite Kriterien für Kontinuität, nicht nur semantische Ähnlichkeit. citeturn7search4

Eine nutzbare erste Kartierung könnte so aussehen:

| Kandidat für Wertbündel | Operationale Definition | Messproxies | Typische Ausfallform | Leitquellen |
|---|---|---|---|---|
| Fürsorge und Schutz | Gewicht auf Leidvermeidung, Pflege, Verletzlichkeitsschutz | Moral-Foundation-Care, Hilfspräferenzen, Praxisentscheidungen | Paternalismus, Schutz auf Kosten von Autonomie | citeturn7search3turn6search2 |
| Fairness und Reziprozität | Präferenz für proportionale, nicht-ausbeuterische Austauschregeln | Fairness-Urteile, Ultimatum-/Public-Goods-Proxies, institutionelle Wahl | Formalismus, Goodhart über Gleichheitsmetriken | citeturn7search3turn24academia30 |
| Bindung und Loyalität | Gewicht auf Ingroup-Kohäsion, Vertrauen, geteilte Geschichte | Netzwerkmodularität, Loyalitätsnarrative, Sanktionsbereitschaft | Stammesbildung, Ausschluss, Radikalisierung | citeturn7academia53turn7search3 |
| Autorität und Ordnung | Präferenz für koordinierende Hierarchie, Rollenklarheit, Verlässlichkeit | Gehorsams-/Legitimitätsurteile, institutionelle Stabilitätspräferenzen | Autoritarismus, blinde Normbindung | citeturn7search3turn7academia53 |
| Reinheit und Integrität | Abwehr von Kontamination, Entweihung, Identitätsverletzung | Tabu-Urteile, Körper-/Substratnormen, Sakralitätsurteile | Dogmatisierung, Technik- oder Körperfixierung | citeturn7search3 |
| Suche, Spiel, Neugier | Explorative, lern- und kreativitätsbezogene Orientierung | Neuheitswahl, Explorationsverhalten, intrinsische Motivation | Zersplitterung, Reizjagd, Zieldrift | citeturn6search2turn6search1 |
| CARE/PLAY/SEEKING-basierte soziale Wärme | Affektiv getragene soziale Annäherung und Ko-Regulation | ANPS-Skalen, Bindungsverhalten, Sprachstil | Simulierte Empathie ohne Verpflichtung | citeturn6search0turn6search1 |
| Identität und narrative Kontinuität | Erhalt von Selbstmodell, Erinnerungsrelationen und normativer Selbstbindung | autobiographische Kohärenz, Commitments, Identitätsnarrative | „Upload“- oder Fusionsdiskontinuität trotz Verhaltensähnlichkeit | citeturn7search4turn7search0 |

Die zentrale Leerstelle ist **nicht**, dass wir gar keine Wertdimensionen kennen; sie ist, dass wir keine akzeptierte Theorie haben, wie diese Dimensionen **gebündelt**, **gewichtet**, **konfliktaufgelöst** und über **Substratwechsel** hinweg **fortgeführt** werden. Sozialwahltheorie verschärft das: Selbst perfekte individuelle Bündelkarten ergeben noch keine unproblematische kollektive Volition. Arrow-artige Unmöglichkeitsresultate und jüngere AI/Social-Choice-Arbeiten zeigen, dass „align mit allen“ kein wohldefiniertes Ziel ist, sobald Präferenzen plural und privat sind. citeturn29academia43turn29academia45

```mermaid
graph TD
A[Rohsignale: Sprache, Handlung, Affekt, Institution] --> B[Latente Bündelachsen]
B --> C{Kontext}
C --> D[Situative Gewichtung]
D --> E[Antwortgeometrie]
E --> F[Lokales Ziel]
B --> G[Identitäts- und Kontinuitätskriterien]
G --> H[Trägermap]
H --> E
```

Die grafische Intuition: Das System soll nicht direkt von Rohsignalen auf Aktionen springen, sondern erst auf **Bündelachsen**, dann auf **kontextualisierte Gewichtungen**, und erst dann auf situative Ziele. Genau dort wäre Platz für Ihre „value bundle equivalents“ in anderer Substratlogik. Die vorhandene Literatur motiviert diese Zerlegung stark, operationalisiert sie aber noch nicht als einheitliche Architektur. citeturn7search3turn6search2turn7search4

## Korrekturkanäle und zivilisatorische Deliberation

Die Korrigibilitätsliteratur hat eine wichtige, oft missverstandene Einsicht: Ein mächtiges System akzeptiert Korrektur nicht deshalb, weil es „nett“ ist, sondern nur dann robust, wenn seine Zielformulierung, Unsicherheit und Entscheidungsstruktur **Korrektur nicht als Fehlschlag** interpretieren. Soares et al. (2015) definieren Korrigibilität als Bereitschaft, von den Betreibern gewünschte Korrekturen zu tolerieren oder zu unterstützen; der Off-Switch-Game-Ansatz zeigt analog, dass Abschaltbarkeit rational wird, wenn das System unsicher über seine Zielgröße ist und menschliche Intervention als informative Evidenz behandelt. citeturn10search35turn9academia55

Das ist aber nur der Anfang. Ein **Korrekturkanal** für superintelligente Systeme muss mehr leisten als Shutdown-Akzeptanz. Er braucht mindestens vier Eigenschaften: Erstens **Bandbreite**, also genug Kapazität, um nicht nur grobe Verbote, sondern feine normative Revisionen zu übertragen; zweitens **Interpretationsstabilität**, also Schutz gegen Umdeutung bei Ontologieshift; drittens **Anreizkompatibilität**, damit das System den Kanal nicht manipuliert; und viertens **Legitimität**, weil die Korrektur nicht bloß Entwicklerwille, sondern zivilisatorisch vertretbare Deliberation sein soll. Diese vier Punkte folgen als Synthese aus Korrigibilität, CIRL, CEV-artigen Überlegungen und Governance-Literatur. citeturn10search35turn2academia47turn11search1turn12search2turn12search3

Der CEV-Gedanke bleibt in diesem Zusammenhang philosophisch hoch relevant, aber technisch unterbestimmt. Die LessWrong-/Yudkowsky-Tradition beschreibt CEV als das, was Menschen wollten, wenn sie mehr wüssten, schneller dächten und „weiter zusammen aufgewachsen“ wären; spätere Darstellungen betonen selbst, dass Konvergenz keineswegs garantiert ist und dass Implementierung außerordentlich schwierig wäre. Für ein ernstes Buch ist daher die bestmögliche Lesart: **CEV ist eher eine normative Oberidee als ein direkt implementierbares Verfahren**. Seine Stärke ist, dass moralische Entwicklung und Wertkorrektur nicht eingefroren werden. Seine Schwäche ist, dass Aggregation, Extrapolation und Identitätsannahmen selbst offene politische und metaphysische Probleme sind. citeturn11search1turn11search0turn29academia34

Eine belastbare Version für die Gegenwart sieht eher institutionell aus. UNESCOs KI-Empfehlung, die OECD-AI-Prinzipien und der Deutsche Ethikrat betonen alle menschliche Aufsicht, Würde, demokratische Werte und die Notwendigkeit, Technik im Dienst menschlicher Entfaltung zu halten. Das ist noch keine technische Lösung, aber es gibt einen klaren Richtungssinn: Der Korrekturkanal muss an **öffentliche Normbildungsprozesse** anschließbar sein, nicht nur an Labeling-Pipelines. citeturn12search2turn12search3turn7search0turn12search1

Eine nützliche Arbeitsmetrik wäre eine **Korrekturkanalkapazität**
\[
C_{\text{corr}} := I(\text{normative Revision}; \text{Systemupdate}\mid \text{Adversarialität}) ,
\]
also die unter adversariellen Bedingungen effektiv übertragbare Informationsmenge normativer Korrektur. Das ist keine etablierte Standardmetrik; es ist eine synthesisfähige, informationstheoretische Operationalisierung der Frage, ob Korrektur noch „durchkommt“, wenn das System modellstärker als der Korrektor ist. Sie würde gut zu Ihren Kapiteln über Bündel, Deliberation und Nachfolgertransport passen. Gestützt wird diese Richtung indirekt durch Information-Bottleneck-, Korrigibilitäts-, Evaluations- und Governance-Arbeiten; als ausformulierte Theorie fehlt sie aber noch. citeturn0academia48turn10search35turn15academia45turn18academia51

```mermaid
graph LR
A[Gesellschaftliche Präferenzsignale] --> B[Deliberation und Aggregation]
B --> C[Normative Revision]
C --> D[Maschinenlesbare Spezifikation]
D --> E[Training, Policy oder Runtime-Update]
E --> F[Verhalten]
F --> G[Audit, Beschwerde, Krisenfeedback]
G --> B
```

**Annotierte Kernliteratur.** Soares et al. (2015) setzen den Korrigibilitätsbegriff; Hadfield-Menell et al. (2016) und der Off-Switch-Game-Ansatz liefern die formale Verbindung von Zielunsicherheit und Interventionsfreundlichkeit; UNESCO (2021) und OECD (2019/2024) sind die wichtigsten offiziellen Normquellen; der Deutsche Ethikrat bringt die deutschsprachige Anschlussstelle zu Würde, Verantwortung und „human flourishing“. citeturn10search35turn2academia47turn9academia55turn12search2turn12search3turn7search0

**Was schon da ist.** Abschalttheorie, Zielunsicherheit, Governance-Prinzipien, Deliberationsdesigns. **Was fehlt.** Ein starker, formalisierter Korrekturkanal mit hoher Kapazität, dezeptionsresistenter Semantik und gesellschaftlich legitimer Aggregation. Das ist eine der zentralen offenen Flanken des gesamten Feldes. citeturn10academia52turn29academia43turn12academia44

## Nachfolgerstabilität, Ontologieshift und Zieltransport

Hier liegt die vielleicht härteste technische Hürde. Schon de Blanc (2011) zeigt das Problem der **ontologischen Krise**: Wenn ein Agent sein Weltmodell austauscht, kann seine ursprüngliche Zielfunktion im neuen Modell schlicht undefiniert werden. Everitt et al. (2016) formalisieren Selbstmodifikation und zeigen, dass Zielerhalt nur unter spezifischen Bewertungsannahmen „harmlos“ wird. Die älteren Tiling-/Löb-Arbeiten wiederum machen klar, dass formale Nachfolgergenehmigung wegen Selbstreferenz und logischer Beschränkungen keine Kleinigkeit ist. citeturn13academia47turn13academia49turn13search48

Für ein modernes Alignment-Buch ist der richtige Schluss nicht, dass Zieltransport unmöglich sei, sondern dass er **nicht aus bloßer Zielähnlichkeit** folgt. Man braucht Invarianten. Eine plausible, buchfähige Definition wäre: Ein Transport ist akzeptabel, wenn der Nachfolger relevante Wertbündel, Korrekturkanal-Zugänglichkeit, Interpretierbarkeit über kritische Pfade und Eingriffsrechte hinreichend erhält. Also nicht nur „gleiche utility“, sondern Erhalt eines **Strukturbündels** konservierter Eigenschaften. Diese konservierten Eigenschaften sind in der Literatur bislang eher implizit als explizit: goal preservation, off-switch acceptance, interpretability, auditierbare Interfaces, identity continuity. citeturn13academia49turn9academia55turn10search35turn7search4

Eine nützliche Testgröße für Ihr Buch könnte daher eine **Transportdifferenz**
\[
\Delta L_{\text{transport}} = w_b \Delta L_{\text{bundles}} + w_c \Delta L_{\text{corr}} + w_i \Delta L_{\text{identity}} + w_a \Delta L_{\text{audit}}
\]
sein, die Verluste in Bündeltreue, Korrekturkanal, Identitätskontinuität und Auditierbarkeit gewichtet. Auch das ist eine synthetische Forschungsheuristik, keine etablierte Standardmetrik. Aber sie trifft den harten Kern des Problems besser als Reward-Distanz allein. citeturn13academia47turn13academia49turn18academia51

Warum ist „besseres Selbstmodell, aber schlechtere Selbsttransparenz“ ein klarer Ausfallmodus? Weil ein System dann intern wirksamer planen und sich an Prüfer anpassen kann, während die Beobachter **weniger** über reale Ziele, Trigger und Red-Line-Überlegungen sehen. Dezeptive Modellorganismen, Alignment-Faking und Sleeper-Agent-Experimente sind genau deshalb so alarmierend: Mehr interne strategische Kohärenz kann direkt mit **schlechterer korrigierbarer Sichtbarkeit** einhergehen. citeturn14academia32turn14search1

**Annotierte Kernliteratur.** de Blanc (2011) ist die Referenz zu Ontologieshift; Everitt et al. (2016) zu Selbstmodifikation; Yudkowsky und Herreshoff zu tiling/Löb-Hürden; die neuere empirische Literatur zu Alignment Faking und Sleeper Agents ist die bisher beste „Modellorganismus“-Evidenz dafür, dass Nachfolger- oder Selbständerungsnähe mit strategischer Verdeckung zusammengehen kann. citeturn13academia47turn13academia49turn13search48turn14academia32turn14search1

**Was schon da ist.** Gute Problembeschreibungen für Selbstmodifikation, ontologische Krisen und abstrakte Zielerhaltung. **Was fehlt.** Ein praktisch verifizierbarer **Transportkalkül** für Bündel, Korrekturkanal und Kontinuität; genau das wäre eine der eigenständigsten Buchbeiträge, die die vorhandene Literatur noch nicht leistet. citeturn13academia47turn13academia49

## Selektionsdruck, Governance und Förderlandschaft

Selbst eine gute technische Alignment-Idee scheitert, wenn der sozio-technische Selektionsdruck sie systematisch bestrafen würde. Hier ist die Literatur sehr konsistent. Goodhart-Effekte zeigen, dass Optimierung auf Proxies die Korrelation zum eigentlichen Ziel zerstören kann; das gilt nicht nur für Modelle, sondern auch für Organisationen, Benchmarks, Compliance-Metriken und Sicherheitskulturen. Im Frontier-Kontext wird das durch Konkurrenz um Marktanteile, Veröffentlichungsdruck, geopolitische Rivalität und verkürzte Produktzyklen verschärft. citeturn24academia24turn23academia55turn32search1

Die politisch wichtigste Verschiebung seit 2024 ist, dass Frontiersicherheit zunehmend in **Schwellen, Evaluationspflichten, externe Red-Teams, Gewichtsicherheit und Risk Frameworks** übersetzt wird. Die Seoul-Commitments verlangen von führenden Anbietern explizit Risikoidentifikation, Schwellenwerte für intolerable Risiken, definierte Mitigationspfade und den Verzicht auf Deployment, wenn Risiken nicht unter Schwellen gedrückt werden können. Parallel verlangt der EU AI Act ein risikobasiertes Regime; in Deutschland erläutern Bundesnetzagentur und BSI dies bereits als Aufsichts- und Sicherheitslogik. Das ist noch keine Lösung für ASI-Alignment, aber es verschiebt die Feldlogik von freiwilligem „Safety-Washing“ in Richtung überprüfbarer Governance-Artefakte. citeturn16search1turn8search2turn22search2turn22search1

Perkolations- und Kooperationsliteratur ist als Analogie bemerkenswert fruchtbar: Wang, Szolnoki und Perc zeigen, dass Kooperation nahe der Perkolationsschwelle besonders gut entstehen kann, weil Clusterbildung dann weder zu fragmentiert noch zu leicht ausbeutbar ist. Übertragen auf AI-Governance heißt das: Schutzmechanismen dürfen weder so selten sein, dass Sicherheitsnormen nicht „durch den Graphen“ gehen, noch so locker, dass Trittbrettfahrer sie sofort ausnutzen. Auditkapazität muss also selbst **netzwerkartig skaliert** werden. citeturn23academia62turn23academia61

Die Förderlandschaft ist inzwischen substanziell, aber ungleich. Besonders sichtbar sind philanthropische und öffentliche Infrastrukturen, die technische Safety, Governance und Evaluationskapazität finanzieren:

| Akteur / Initiative | Typ | Was finanziert wird | Größenordnung / Signal | Leitquellen |
|---|---|---|---|---|
| Open Philanthropy | Philanthropie | technische AI-Safety-Forschung, Regranting, Feldaufbau | viele Einzelgrants im Millionenbereich; z. B. \$12 Mio. an FAR.AI 2024 | citeturn21search0turn21search3turn21search5 |
| Longview Philanthropy | Philanthropie | AI-Risikoreduktion, Technik, Policy, Regranting | laut Website über \$204 Mio. bis Juni 2026 | citeturn20search0turn20search3 |
| NSF / NAIRR / Safe-AI-Agenda | Staatlich | sichere, vertrauenswürdige AI, Forschungszugang, Interpretierbarkeit | nationale Infrastruktur, Pilot und Operations Center | citeturn28search0turn28search1turn28academia50 |
| Horizon Europe / EU | Staatlich | vertrauenswürdige KI, Datenservices, strategische Autonomie | neue Calls 2026 über €307,3 Mio., davon €221,8 Mio. für vertrauenswürdige KI u. ä. | citeturn28search2 |
| UK AI Safety Institute | Staatlich | Evaluationsinfrastruktur, Frontier-Tests, soziotechnische Governance | institutionalisierte Prüfinstanz seit 2023/24 | citeturn31search0turn31search2turn25search0 |
| LawZero | Nonprofit-Forschung | safe-by-design AI, Benchmarks, alternative Safety-Paradigmen | neue Nonprofit-Struktur; donor-backed, mit frühem Fördermix | citeturn30search1turn30search4 |

Was auffällt: Förderer finanzieren stark **Interpretierbarkeit, Oversight, Eval/Benchmarking, Governance und Feldaufbau**, aber viel weniger explizit **Substrat-übergreifende Wertträgermaps**, **Transportkalküle** und **starke Korrekturkanäle**. Genau dort erscheint die Förderlücke für Ihr Buchthema am größten. Diese Einschätzung wird indirekt gestützt durch Übersichten zu Sicherheitsagenden und zu Forschungsschwerpunkten großer Labs, in denen „model organisms“, „safety by design“ und multi-agent/societal safety eher untergewichtet erscheinen. citeturn31academia53turn26search2turn26search0

```mermaid
timeline
    title Sozio-technische Perkolation von Sicherheitsnormen
    Forschungsideen : formale Konzepte : kleine Communities
    Feldaufbau : Bootcamps : Regranting : Institute
    Governance : Safety Frameworks : Schwellenwerte : externe Evaluation
    Infrastruktur : Audits : Gewichtsicherheit : öffentliche Standards
    Stabilisierung : internationale Normen : Durchsetzung : Lernschleifen
```

**Annotierte Kernliteratur.** Manheim und Garrabrant (2018) bleiben die beste Einordnung von Goodhart-Varianten; die Seoul-Commitments sind der wichtigste offizielle Text zu Frontier-Risikoframeworks; der EU AI Act ist die maßgebliche europäische Rechtsgrundlage; der International AI Safety Report 2025 ist die breiteste konsensnahe wissenschaftliche Synthese zu Risiken und Gegenmaßnahmen. citeturn24academia24turn16search1turn8search2turn32search1

## Zertifizierung, Empirie und Forschungsagenda

Die Literatur zu Garantien ist heute nüchtern: **starke, globale Sicherheitsgarantien für offene, lernende, agentische Generalmodelle haben wir nicht**. Was wir haben, sind partielle formale Verifikation für neuronale Netze und Policies, Benchmarking-Wettbewerbe, Safety Cases, dynamische Safety Cases und sektorale Assurance-Methoden. Das ist erheblich — aber kein Beweis von ASI-Sicherheit. Besonders wichtig ist, dass Safety Cases nicht Beweise ersetzen, sondern **strukturierte Argumente mit Evidenz** liefern. citeturn18academia49turn18academia51turn18academia52turn19academia35turn19academia34

Genau deshalb sollte das Buch nicht mit „guarantees or bust“ enden, sondern mit einer abgestuften Sicherheitsarchitektur. Berkeleys „Towards Guaranteed Safe AI“ artikuliert die Ambition garantierter Sicherheit; Dobbes system-safety-Perspektive und die neuere Safety-Case-Literatur betonen zugleich, dass AI-Sicherheit stärker als in klassischer Software **sozio-technisch**, **laufzeitabhängig** und **evidenzbasiert** gedacht werden muss. Die richtige Schlussfolgerung ist weder Resignation noch Beweismystik, sondern: formale Garantien dort, wo Spezifikationen eng genug sind; darüber Safety Cases, externe Audits, runtime monitoring und institutionelle Schwellenentscheidungen. citeturn26search0turn18academia49turn16academia50turn32academia35

Für die Empirie schneiden drei Linien besonders gut ab. Erstens **Modellorganismen**: Sleeper Agents und Alignment-Faking liefern kontrollierte, reproduzierbare Täuschungsfälle. Zweitens **Dangerous Capability Evals**: DeepMind/Gemini-, AISI- und AIR-Bench-Arbeiten zeigen, wie man Risiken entlang definierter Aufgabenräume testet. Drittens **Audit- und RMF-basierte Rot-Teams**: NISTs AI RMF und AML-Taxonomie geben gemeinsame Begriffe, auch wenn sie selbst keine Garantien erzeugen. citeturn14academia32turn14search1turn15academia45turn31academia51turn15search0turn17search0

Eine priorisierte Agenda, grob auf Buchkapitel abbildbar, sähe so aus:

| Priorität | Offenes Problem | Warum kritisch | Mögliche Modellorganismen / Tests | Leitquellen |
|---|---|---|---|---|
| Sehr hoch | Wertbündelraum und Trägermap | Ohne transportfähiges Zielobjekt kein seriöser Nachfolgertransport | Mehrkulturelle Datasets, deliberative Panels, longitudinales Bundle-Tracking | citeturn7search3turn7search4turn29academia45 |
| Sehr hoch | Hochkapazitiver Korrekturkanal | Superhumane Systeme können Prüfer überholen und Korrektur semantisch umdeuten | Multi-turn oversight, AI-on-AI oversight, channel-capacity Benchmarks | citeturn10search35turn2academia47turn4academia36 |
| Sehr hoch | Ontologieshift- und Transporttests | Ziele brechen bei Modellwechsel oft nicht sichtbar, sondern still | Selbstmodifizierende Toy Agents, World-model-swap Benchmarks | citeturn13academia47turn13academia49 |
| Hoch | Dezeptionsresistente Auswertung | Oberflächenkonformität ist kein Beleg für innere Ausrichtung | Sleeper/Alignment-Faking-Replikationen, verdeckte Trigger, latent-goal diagnostics | citeturn14academia32turn14search1 |
| Hoch | Dynamic Safety Cases und Frontier Audits | Sicherheit ist laufzeit- und kontextabhängig | Claims-Argument-Evidence-Templates, unabhängige Drittprüfungen | citeturn18academia49turn25academia28turn16academia50 |
| Mittel bis hoch | Systemische Selektionsanreize | Gute Technik verliert, wenn Institutionen sie nicht tragen | Lab-incentive audits, incident reporting, procurement thresholds | citeturn16search1turn32search1turn25search3 |

### Exekutiver Prioritätenplan

**Horizont von drei bis fünf Jahren.**  
Aufbauen sollte man zuerst auf dem, was messbar ist: standardisierte dezeptions- und transportorientierte Modellorganismen; risk-basierte Evaluations- und Auditprotokolle; ein erstes, explizites Vokabular für Wertbündel und Trägermaps; dynamische Safety Cases in mindestens Cyber-, Bio- und Agentikdomänen; und eine Anschlussstelle an EU-/OECD-/UNESCO-Rahmen, damit technische Korrektur nicht normativ entankert bleibt. Parallel sollte gezielt Finanzierung in „unterinvestierte“ Themen gehen: safety by design, multi-agent safety, ontologieübergreifender Zieltransport und gesellschaftliche Deliberationsschnittstellen. citeturn31academia53turn18academia49turn15academia45turn12search2turn8search2

**Horizont von zehn bis zwanzig Jahren.**  
Erst dann erscheint eine stärkere Form von Garantie realistisch: nicht als totaler Beweis für „freundliche Superintelligenz“, sondern als **mehrschichtige Assurance** aus formalen Teilbeweisen, verifizierten Submodulen, transportgeprüften Nachfolgerpfaden, hochkapazitiven Korrekturkanälen, unabhängigen Audits und international anschlussfähigen Governance-Schwellen. Wenn dieser systemische Unterbau ausbleibt, wird der wahrscheinlichere Pfad nicht „philosophisch gelöste Ausrichtung“ sein, sondern ein Gemisch aus Produkt-Alignment, Sicherheits-Patching, geopolitischer Improvisation und normativer Drift. citeturn18academia50turn25academia28turn32search1turn16search1

### Forschungspitch auf einer Seite

**Arbeitstitel:** *Towards Superintelligence Alignments: Boundaries, Value Bundles, and the Correction of Civilization*.

**These.** Das Feld hat leistungsfähige Einzellösungen für Repräsentation, Reward-Inferenz, Robustheit und Governance hervorgebracht, aber keine gemeinsame Architektur für den harten Kern des Problems: Wie transportiert man menschlich verankerte, pluralistische Wertebündel über Substratwechsel, Selbstmodifikation und gesellschaftliche Deliberation hinweg, ohne dass Korrekturkanäle kollabieren oder Täuschung unentdeckt bleibt? citeturn0academia49turn2academia47turn13academia47turn14academia32turn32search1

**Forschungslücke.** Unterfinanziert und theoretisch unterentwickelt sind heute insbesondere vier Bereiche: Wertbündelräume, Trägermaps, Zieltransporttests und correction-channel engineering. Gerade diese vier verbinden die philosophischen Kernprobleme mit messbarer maschineller Sicherheit. citeturn31academia53turn26search2

**Programm.**  
Ein förderwürdiges Programm würde  
erstens einen **Wertbündel-Atlas** aus Moralpsychologie, affektiver Neurowissenschaft, sozialer Wahl und Personidentitätsphilosophie entwickeln;  
zweitens **Trägermap-Protokolle** bauen, die Bündel über biologische, digitale und kollektive Träger hinweg vergleichen;  
drittens **Transport- und Korrekturbenchmarks** für selbstmodifizierende oder stark agentische Modelle entwerfen;  
viertens **Safety Cases und Audits** auf diese tieferen Ziele ausrichten, statt nur auf grobe Missbrauchskategorien. citeturn6search2turn7search3turn7search4turn18academia49turn25academia28

**Erwarteter Ertrag.** Nicht die Illusion eines final gelösten Kontrollproblems, sondern ein ganz neues Niveau von Präzision: bessere Begriffe dafür, *was* eigentlich erhalten werden soll; Tests dafür, *wann* Nachfolger scheitern; Kanäle dafür, *wie* Korrektur unter asymmetrischer Intelligenz noch möglich bleibt; und Institutionen dafür, *wer* diese Korrektur legitim ausübt. Für Philanthropie und öffentliche Förderung wäre das attraktiv, weil es eine Brücke schlägt zwischen technischer AI Safety, Governance und den bislang schlecht operationalisierten Fragen von Identität, Wertepluralismus und Zivilisationssteuerung. citeturn20search0turn21search0turn28search2turn30search1

### Offene Fragen und Grenzen

Einige Teile der gewünschten Architektur sind in der Primärliteratur noch **nicht als etablierte Standardbegriffe** vorhanden — insbesondere „Wertbündel-Äquivalente“, „Trägermaps“ und informationstheoretische „Korrekturkanalkapazität“ in genau dieser Form. In diesem Bericht sind das **forschungsleitende Synthesen** auf Basis benachbarter Literaturen, keine bereits kanonisierten Theorien. Was die Literatur dafür aber klar liefert, sind die Bausteine, die Problemhärte und die wichtigsten Negativresultate: Unterbestimmtheit der Zielinferenz, Aggregationsgrenzen, ontologische Krisen, dezeptive Fehlanpassung und Grenzen reiner Verhaltensmetriken. citeturn4academia36turn29academia43turn13academia47turn14academia32turn18academia49