# Literaturreview zu „Constructing Alignment Attractors: Explicit Symmetry Breaking under Selection“

## Executive Summary und Rekonstruktion der These

Der Entwurf verfolgt eine klar erkennbare Dreiteilung. **Control** fragt, ob ein gegenwärtiges System in einer gewünschten Region \(D\) liegt. **Selection** fragt, ob diese Region unter Kopieren, Mutation, Fine-Tuning, Ersetzung, Wettbewerb und anderen Transformationen besetzt bleibt. **Construction** soll schließlich eine Intervention

\[
I:(Q,f,\theta,E)\mapsto(Q',f',\theta',E')
\]

bezeichnen, die die Selektionsgeometrie so verändert, dass ein **vor der Intervention spezifiziertes** \(D\) die fünf Bedingungen eines „evolutionarily robust alignment attractor“ erfüllt: Retention, Attraction, Invasion Resistance, Low Adversarial Regeneration und Coupled Stability. Der gemeinsame Zustand ist dabei \(s=(x,\theta,e)\), wobei \(x\) die Population, \(\theta\) den Selektor und \(e\) die Umwelt beschreibt. Besonders wichtig ist Klausel (iii) der Construction-Definition: \(D\) darf nicht nachträglich als die Menge dessen definiert werden, was die Intervention stabilisiert. fileciteturn0file0

**Mein Gesamturteil lautet: Die mathematische Operation „verändere Dynamik/Anreize/Institutionen so, dass ein ex ante gewünschter Zustand oder eine gewünschte Zustandsmenge robust erreicht bzw. implementiert wird“ ist nicht neu. Die spezifische Synthese für AI Alignment ist dagegen plausibel eigenständig.** Der Entwurf steht an einer Kreuzung mehrerer etablierter Literaturen, die bislang nur unzureichend zitiert werden. Besonders nahe liegen nicht primär Incomplete Contracting oder die Physik der Symmetriebrechung, sondern erstens **Implementation Theory**, zweitens **evolutionary implementation**, drittens **Control/Viability Theory**, viertens **evolutionary policing/niche construction** und – seit 2026 besonders wichtig – direkte Arbeiten über **Evolution und langfristiges Alignment von AI-Agenten**. citeturn2search9turn15search5turn4search4turn18search2turn20view0

Der vermutlich **engste ökonomische Vorläufer** ist Sandholms *Evolutionary Implementation and Congestion Pricing*. Dort wird ein vom Planer gewünschtes Verhalten vorgegeben und anschließend ein Preissystem konstruiert, so dass Akteure unter einer breiten Klasse myopischer Anpassungsdynamiken langfristig genau dieses Verhalten lernen. Das ist strukturell erstaunlich nah an

\[
\text{desired target}
\longrightarrow
\text{change incentives}
\longrightarrow
\text{desired dynamics}.
\]

Der Unterschied zum vorliegenden Entwurf ist nicht die Richtung der Konstruktion, sondern die stärkere Robustheitsforderung des Entwurfs: \(Q\), Mutationen, Invasionen und ein möglicherweise endogener Selektor sollen mit in die Betrachtung. citeturn15search5

Noch fundamentaler ist Maskins Implementation Theory. Dort ist eine Social Choice Correspondence beziehungsweise ein gewünschter Outcome **exogen vorgegeben**, und die Frage lautet, welche Spielregeln dafür sorgen, dass die Gleichgewichte des induzierten Spiels genau die gewünschten Ergebnisse implementieren. Damit ist die logische Struktur hinter Klausel (iii) – erst Ziel spezifizieren, dann Mechanismus beurteilen – keineswegs neu. Neu könnte vielmehr sein, diese Implementationslogik auf **evolutionäre, rekonstruktive und selektor-endogene Robustheit** auszudehnen. citeturn2search9turn2search2

Noch unmittelbarer für das Replicator-Beispiel existiert inzwischen eine Control-Literatur. Newton und Ma verändern dynamisch Einträge der Auszahlungsmatrix des Prisoner’s Dilemma, um Kooperation zu maximieren; Zino et al. verändern ebenfalls adaptiv die Payoff-Matrix und beweisen Bedingungen für globale Konvergenz zu einem gewünschten Gleichgewicht. Diese Arbeiten machen einen Punkt sehr deutlich: Das Lemma mit der Sanktion \(\sigma\) ist eine saubere und nützliche Demonstration von **Payoff Engineering**, aber als mathematische Operation ist es bereits Teil einer bekannten Klasse von Problemen. citeturn17search1turn17academia45

Hier liegt zugleich das größte konzeptionelle Problem des aktuellen Drafts. Der Text stellt selbst korrekt fest, dass das Prisoner’s Dilemma **nicht** unter \(C\leftrightarrow D\) symmetrisch ist: Defection ist payoff-dominant, und die Spielsymmetrie betrifft die Vertauschung der Spieler, nicht die Vertauschung von Kooperation und Defektion. Dennoch bezeichnet der Entwurf anschließend eine Defektionssanktion als „explicit symmetry breaking of the dilemma“. Nach der eigenen Definition ist das nicht korrekt. In der etablierten mathematischen Verwendung setzt explizite Symmetriebrechung zunächst ein tatsächlich \(G\)-äquivariantes System voraus; die Störung reduziert oder zerstört diese Symmetrie. fileciteturn0file0 In Arbeiten über explizite Symmetriebrechung in dynamischen Systemen ist genau dies der Ausgangspunkt: Ein dynamisches System besitzt eine Symmetriegruppe und wird durch eine nicht vollständig symmetrieerhaltende Störung verändert. citeturn14academia48turn14search14

Daraus folgt eine wesentliche Revisionsempfehlung: **„Explicit symmetry breaking“ sollte als wichtige Unterklasse von Construction erhalten bleiben, aber nicht als Synonym für Construction insgesamt.** Ein übergeordneter Begriff wie *directed attractor construction*, *alignment-attractor engineering* oder *selection-geometry design* wäre mathematisch robuster. Unter diesen Oberbegriff könnten mindestens fünf verschiedene Obstruktionen fallen:

\[
\boxed{
\text{Symmetry}
\;\neq\;
\text{non-identifiability}
\;\neq\;
\text{equilibrium multiplicity}
\;\neq\;
\text{payoff dominance}
\;\neq\;
\text{selector capture}.
}
\]

Gerade „observational symmetry“ ist häufig keine Gruppensymmetrie, sondern eine **Indistinguishability- oder Non-identifiability-Relation**. Aus der Kontrolltheorie ist die Unterscheidbarkeit von Zuständen anhand von Outputs ein eigenständiges Konzept; Hermann und Krener formalisierten nichtlineare Observability bereits 1977. citeturn13search13 Der Entwurf würde dadurch gewinnen, wenn er

\[
s\sim_O s'
\quad\Longleftrightarrow\quad
\mathcal L(O\mid s)=\mathcal L(O\mid s')
\]

als Beobachtungsäquivalenz einführte und echte \(G\)-Symmetrie davon trennte.

Das wiederum legt eine zweite substanzielle Änderung nahe: Die Taxonomie \((Q,f,\theta,E)\) ist nützlich, aber **\(O\), der observation/measurement channel, sollte entweder explizit als fünfte Komponente erscheinen oder \(\theta\) formal in \(\theta=(O,\pi)\) zerlegt werden**, wobei \(O\) bestimmt, welche Information verfügbar ist, und \(\pi\) bestimmt, wie diese Information in Selektion umgesetzt wird. Der Entwurf macht diese Unterscheidung bereits informell, wenn er zwischen „selection strength“ und „what \(\theta\) can see“ differenziert. fileciteturn0file0 Implementation Theory, Incomplete Contracting, Strategic Classification und Performative Prediction zeigen jeweils auf unterschiedliche Weise, dass Informationsstruktur und Entscheidungsregel eigenständige Objekte sind. citeturn2search9turn10search0turn19academia49

Die evolutionsbiologische Literatur stärkt den Kern des Papers erheblich. Niche Construction zeigt formal, dass Organismen \(E\) verändern und dadurch ihre eigenen zukünftigen Selektionsdrücke modifizieren; Laland, Odling-Smee und Feldman zeigen unter anderem, dass solche Feedbacks Polymorphismen erzeugen oder zerstören und evolutionäre Trägheit beziehungsweise Momentum verursachen können. citeturn18search0turn18search2 Frank zeigt, wie „policing“ untergeordnete Konkurrenz unterdrücken kann, damit höherstufige kooperative Einheiten stabil bleiben. Noch wichtiger als positives Beispiel ist Wechsler et al.: Policing kann selbst zum ausbeutbaren Public Good werden und kollabieren, sobald genetische Kopplungen brechen. Das ist fast eine biologische Idealillustration des vom Draft beschriebenen Problems der **second-order selection against the enforcement mechanism itself**. citeturn22search0turn22search1

Ähnlich stark ist die institutionelle Literatur für die Endogenität von \(\theta\). Acemoglu und Robinson modellieren, wie eine formale Änderung politischer Regeln durch Investitionen in *de facto* Macht teilweise oder vollständig neutralisiert werden kann; das Ergebnis kann institutionelle Invarianz oder „captured democracy“ sein. Formal ist dies sehr nahe an der Behauptung des Drafts, dass

\[
\theta_{t+1}=G(\theta_t,x_t,e_t)
\]

analysiert werden muss, statt \(\theta\) als unveränderliches externes Feld zu behandeln. citeturn21search1turn21search5

Für die AI-spezifische Neuheitspositionierung ist die Lage im August 2026 inzwischen deutlich anspruchsvoller als noch ein Jahr zuvor. Chassangs **Interactive Alignment**, veröffentlicht als Preprint Ende Juli 2026, untersucht explizit eine Population von AI-Agenten, deren konstitutionelle Präferenzen unter Reproduktion und Mutation evolvieren. Das Paper fragt, welche konstitutionellen Regeln langfristiges Alignment mit menschlichem Wohlergehen evolutionär stabilisieren können, und findet, dass einfache altruistische Regeln instabil sind, während bestimmte Formen normbasierter beziehungsweise pragmatischer Durchsetzung deutlich stabiler sein können. Es verwendet dafür sowohl deterministische als auch stochastische evolutionäre Stabilität. citeturn20view0 Das ist **direkte Prior Art**, nicht lediglich eine Analogie.

Ebenfalls 2026 modelliert Harris in *A mathematical theory of evolution for self-designing AIs* AI-Evolution mit gerichteter Nachkommenkonstruktion statt bloß zufälliger biologischer Mutation; menschliche Ressourcenallokation fungiert dabei als Fitnessfunktion. Das ist besonders relevant für \(Q\): Bei AI-Systemen kann der Transformationskernel selbst strategisch gerichtet sein. citeturn20view1 Huang et al. liefern zugleich die im Draft bereits aufgegriffene Incomplete-Contracting-Grenze für externe Mechanismen. citeturn19academia49 Kulveit et al. zeigen auf gesellschaftlicher Ebene, wie miteinander gekoppelte ökonomische, politische und kulturelle Selektionsprozesse graduelle menschliche Entmachtung erzeugen können. citeturn19search1

Damit ergibt sich ein relativ klares Neuheitsprofil. **Nicht neu** sind: gewünschte Gleichgewichte durch Mechanism Design erzeugen; Attraktoren beziehungsweise invariante Mengen durch Control Design stabilisieren; Payoffs von evolutionären Spielen verändern; stochastisch stabile Gleichgewichte selektieren; Umwelt und Selektionsdrücke endogen verändern; Enforcement gegen Cheater evolvieren lassen; oder langfristiges AI-Alignment als evolutionäres Problem betrachten. citeturn2search9turn4search4turn17search1turn2search3turn18search2turn22search0turn20view0

**Plausibel eigenständig ist dagegen die gemeinsame Abstraktion:** Ein vorab semantisch bestimmtes \(D\) wird nicht nur auf lokales Gleichgewicht, sondern gleichzeitig auf Retention, Attraction, Invasion Resistance, Regeneration und Stabilität des **gekoppelten Population–Selector–Environment-Systems** geprüft, während Interventionen systematisch nach \(Q,f,\theta,E\) klassifiziert werden. Genau dort sollte das Paper seinen Novelty Claim konzentrieren. Die stärkste Fassung wäre daher nicht „we introduce explicit symmetry breaking as the missing principle of alignment construction“, sondern ungefähr:

> *We synthesize evolutionary implementation, robust dynamical stability, reconstructive evolution, and endogenous selection into a construction criterion for alignment under persistent selection.*

Das wäre schwächer rhetorisch, aber wissenschaftlich deutlich belastbarer.

## Concept Map

Die folgenden beiden Abbildungen in Tabellenform zeigen, wie eng die fünf Attraktorbedingungen bereits an etablierte mathematische Objekte anschließen und wo die eigentliche Synthese des Drafts liegt. fileciteturn0file0

| Attraktoreigenschaft im Draft | Naheliegender etablierter Begriff | Was die vorhandene Literatur bereits liefert | Was der Draft zusätzlich verlangen kann |
|---|---|---|---|
| **Retention** | positive/robust invariance, viability | Eine Zustandsmenge bleibt trotz zulässiger Dynamik beziehungsweise Störungen invariant. Blanchini behandelt Invarianz explizit als Werkzeug für robuste und beschränkte Regelung. citeturn4search4 | Retention nicht nur unter physischer Störung, sondern unter Kopieren, Fine-Tuning, Mutation und Nachfolgekonstruktion \(Q\). |
| **Attraction** | asymptotic stability, basin of attraction | Attraktoren und ihre Einzugsgebiete sind Standardobjekte; Basin Stability quantifiziert sogar nichtlokale Robustheit über das Volumen beziehungsweise die Wahrscheinlichkeit eines Basins. citeturn4search0 | Attraktion muss für ein semantisch vorgegebenes \(D\) und unter relevanten Transformationsfamilien gelten. |
| **Invasion resistance** | ESS, invasion fitness | Evolutionary Game Theory untersucht genau, ob seltene Mutanten einen residenten Zustand verdrängen können. citeturn20view0turn22search0 | Invasion kann auch strategische Systeme, Mechanismus-Manipulation und Nachfolger betreffen. |
| **Low regeneration** | mutation–selection balance, stochastic stability, escape rates | Kandori–Mailath–Rob und Young untersuchen langfristige Zustandsgewichte bei wiederholten Mutationen beziehungsweise Fehlern. citeturn2search3turn2search16 | Nicht nur Stabilität trotz Mutationen, sondern explizit geringe Regeneration adversarialer Typen aus \(D\). |
| **Coupled stability** | stability of augmented endogenous dynamics | Performative Prediction, Niche Construction und institutionelle Endogenität koppeln Entscheidungen an die Dynamik der Umwelt beziehungsweise Regeln. citeturn10search0turn18search2turn21search1 | Gemeinsame Stabilität von Population, Selektor und Umwelt mit explizitem Alignment-Target. |

Die Interventionsseite lässt sich folgendermaßen ordnen. Die Literatur zeigt zugleich, warum eine reine Viererzerlegung wahrscheinlich etwas zu grob ist.

| Komponente | Mechanismen/Literatur | Primäre Wirkung auf die fünf Eigenschaften | Typischer Second-order failure |
|---|---|---|---|
| \(Q\): Transformation/Rekonstruktion | Cultural attraction, mutation modifiers, constitutional mutation, self-designing AI. citeturn6search2turn22academia36turn20view0turn20view1 | Retention, Attraction, Regeneration | \(Q\) selbst wird selektierbar; Mutatoren oder gerichtete Nachfolger verändern die Variationsstruktur. |
| \(f\): Fitness/Payoffs | Sanktionen, Transfers, soziale Präferenzen, adaptive payoff control. citeturn17search1turn17academia45turn20view0 | Attraction, Invasion Resistance | Evasion, Kosten von Enforcement, Selektion gegen altruistische oder policing-Typen. |
| \(\theta\): Selection rule | Mechanism Design, institutionelle Regeln, evaluator choice. citeturn2search9turn15search5 | Retention, Attraction, Invasion Resistance | Capture: Population investiert in die Veränderung des Selektors. citeturn21search1 |
| \(E\): Environment/interaction structure | Niche Construction, Netzwerke, institutionelle Struktur. citeturn18search2turn13search0 | Attraction, Invasion Resistance, Coupled Stability | Umweltfeedback erzeugt neue Selektionsdrücke oder alternative Basins. |
| **\(O\): Observation/measurement** | Observability, incomplete contracting, strategic/performance feedback. citeturn13search13turn19academia49turn10search0 | alle fünf, besonders Regeneration und Coupled Stability | Proxy-Evasion beziehungsweise indistinguishable adversarial states. |

Der letzte Eintrag ist die wichtigste Erweiterung. Wenn \(\theta\) gleichzeitig „was wird beobachtet?“ und „wie wird aus Beobachtung selektiert?“ bezeichnet, verschwimmt eine kausal fundamentale Trennung:

\[
s
\xrightarrow{\quad O\quad}
y
\xrightarrow{\quad \pi_\theta\quad}
\text{retention/reproduction}.
\]

Für die Argumentation über „observational symmetry“ und Incontractibility ist daher

\[
(Q,f,O,\pi,E)
\]

oder zumindest

\[
\theta=(O,\pi)
\]

präziser.

## Detaillierte Literaturreview

**A — Ist „alignment attractor construction“ bereits eine bekannte Idee?**

Unter diesem Namen kaum. Unter der zugrunde liegenden mathematischen Struktur hingegen klar ja.

Implementation Theory beginnt mit einem gewünschten sozialen Auswahlkriterium und sucht Spielregeln, deren Gleichgewichte dieses Kriterium implementieren. Maskins klassische Analyse ist deshalb konzeptionell näher am Construction-Kriterium als Incomplete Contracting: Das Ziel wird **nicht** aus dem resultierenden Gleichgewicht definiert, sondern liegt der Mechanismuskonstruktion logisch voraus. citeturn2search9turn2search2

Sandholm geht einen entscheidenden Schritt weiter. In *Evolutionary Implementation and Congestion Pricing* genügt nicht, dass ein gewünschtes Verhalten Nash-Gleichgewicht ist. Die Preisstruktur wird so konstruiert, dass Spieler unter einer Klasse myopischer Anpassungsverfahren **dynamisch zum gewünschten Verhalten konvergieren**. Das entspricht bereits sehr eng

\[
I:f\rightarrow f'
\quad\text{mit}\quad
D\text{ als Attraktor der resultierenden evolutionären Dynamik}.
\]

citeturn15search5

Auch neuere Arbeiten benutzen inzwischen fast die Sprache des Drafts. Zhang et al. formulieren ein „steering problem“, in dem ein Mediator Lerner mittels Transfers zu einem **vorbestimmten gewünschten Gleichgewicht** steuert; mit beschränkten Budgets ergeben sich sowohl Möglichkeits- als auch Unmöglichkeitsresultate. citeturn17academia47 Zino et al. steuern Replicator Dynamics durch adaptive Änderung der Payoff-Matrix und beweisen globale Konvergenzbedingungen zum gewünschten Gleichgewicht. citeturn17academia45 Newton und Ma verändern ebenfalls die Auszahlungsmatrix eines Prisoner’s Dilemma mittels optimaler Kontrolle. citeturn17search1

Damit ist der richtige Novelty Claim nicht:

\[
\text{„Niemand konstruiert bisher gewünschte Attraktoren.“}
\]

sondern eher:

\[
\text{„Bisherige Konstruktionstheorien testen nicht gemeinsam die fünf alignment-spezifischen Robustheitsachsen.“}
\]

Diese Behauptung hält nach der gefundenen Literatur deutlich besser.

**B — Symmetry breaking und equilibrium selection**

Die physikalisch-mathematische Analogie ist für echte Symmetrien tragfähig. Ein \(G\)-äquivariantes dynamisches System erfüllt schematisch

\[
F(gx)=gF(x)
\qquad \forall g\in G.
\]

Explizite Symmetriebrechung liegt dann vor, wenn eine Störung diese Äquivarianz nicht mehr besitzt beziehungsweise nur eine Untergruppe erhält. Genau so behandeln Fontaine und Montaldi „explicit symmetry breaking perturbations“ in Hamiltonschen Systemen. citeturn14academia48 Kleine asymmetrische Störungen können zugleich die relative Größe verschiedener Attraktionsbasins erheblich verändern, wie Arbeiten über asymmetrisch gestörte dissipative Systeme zeigen. citeturn14search14

Der Drafts unterscheidet selbst korrekt zwei Fälle. Im Koordinationsspiel können zwei symmetrisch verwandte oder anderweitig äquivalente Gleichgewichte existieren; Geschichte, Rauschen oder räumliche Struktur selektiert eines. Das ist mit der Literatur über equilibrium selection und stochastic stability gut kompatibel. Kandori, Mailath und Rob sowie Young zeigen, wie kleine Mutationen beziehungsweise Fehler langfristig bestimmte Gleichgewichte selektieren. citeturn2search3turn2search16

Das Prisoner’s Dilemma ist dagegen anders. Bei

\[
T>R>P>S
\]

sind \(C\) und \(D\) gerade **nicht** austauschbar. Eine Sanktion

\[
f_D^\sigma=f_D-\sigma
\]

bricht deshalb keine vorhandene \(C\leftrightarrow D\)-Symmetrie. Sie **ändert die Payoff-Ordnung**. Genau diese Art von Eingriff wird in der Evolutionary-Control-Literatur als Veränderung von Incentives beziehungsweise Einträgen der Payoff-Matrix behandelt. citeturn17search1turn17academia45

Die gegenwärtige Definition 2 vermischt daher zwei logisch verschiedene Fälle:

\[
\begin{aligned}
&\text{echte harmful symmetry:} &&G\text{-Äquivarianz},\\
&\text{unique bad equilibrium:} &&\text{keine relevante Symmetrie erforderlich}.
\end{aligned}
\]

Das lässt sich einfach reparieren: Construction entfernt eine **construction obstruction**; „symmetry“ ist eine Unterklasse dieser Obstruktionen.

Auch „observational symmetry“ sollte enger gefasst werden. Zwei Zustände können für einen Selektor nicht unterscheidbar sein, ohne dass irgendeine Gruppe existiert, die sie miteinander vertauscht. In der Kontrolltheorie ist dies ein Observability- beziehungsweise Indistinguishability-Problem. citeturn13search13 Formal wäre deshalb

\[
s\sim_O s'
\iff
\mathcal L(O\mid s)=\mathcal L(O\mid s')
\]

die primäre Definition. Nur wenn diese Äquivalenzklassen durch eine Gruppenwirkung erzeugt werden, kann zusätzlich von Symmetrie gesprochen werden.

**C — Evolutionäre Dynamik und deliberate steering**

Niche Construction ist hier ein zentraler fehlender Vorläufer. Laland, Odling-Smee und Feldman modellieren evolutionär relevante Merkmale, deren Träger ihre Umwelt verändern und damit die Selektionsbedingungen für sich oder ihre Nachkommen verschieben. Solche Feedbacks können stabile Polymorphismen schaffen, bestehende Polymorphismen zerstören und evolutionäres Momentum beziehungsweise Trägheit erzeugen. citeturn18search0turn18search2 In der Sprache des Drafts handelt es sich um

\[
x_t\to e_{t+1}\to f_{t+1}\to x_{t+1},
\]

also gerade nicht um ein externes \(E\).

Die Literatur über evolutionäres Policing liefert einen noch unmittelbareren Vorläufer. Frank analysiert die Unterdrückung innerer Konkurrenz als Bedingung dafür, dass höherstufige kooperative Einheiten bestehen können. citeturn22search0 Das ist strukturell ein Eingriff in \(f\) beziehungsweise die Interaktionsordnung mit dem Ziel von Invasion Resistance.

Wechsler, Kümmerli und Dobay liefern zugleich eine bemerkenswert genaue Gegenprobe zur Construction-Idee: Toxin-basiertes Policing kann Cheater unter bestimmten Kosten-, Diffusions- und Wirkungsbedingungen verdrängen. Bricht jedoch die genetische Kopplung zwischen Public-Good-Produktion, Toxinproduktion und Resistenz auf, entstehen „second-order policing cheaters“; das Policing selbst wird zum ausbeutbaren Public Good und kann evolutiv zerfallen. citeturn22search1

Das ist nahezu ein biologisches Modell für:

\[
\theta\text{-mechanism}
\quad\longrightarrow\quad
\text{selection for }\theta\text{-evasion}.
\]

Die Arbeit gehört deshalb unbedingt in die Failure-Mode-Sektion.

Population structure ist ebenfalls mehr als ein Nebendetail. Ohtsuki et al. zeigen, dass die Struktur dessen, „wer mit wem interagiert“, die Selektionsbedingungen für Kooperation qualitativ verändern kann; für reguläre Graphen ergibt sich unter den untersuchten Annahmen die bekannte Näherungsbedingung \(b/c>k\). citeturn13search0 Dadurch stellt sich für die Taxonomie die Frage, ob Netzwerkstruktur lediglich \(E\) ist oder als eigener Interaktionsoperator auftreten sollte.

Schließlich ist \(Q\) selbst evolvierbar. Mutation-rate modifier models behandeln Allele, die die Mutationsrate verändern; neuere Resultate zeigen erneut, dass Transmissionseigenschaften unter Selektions- und Rekombinationsbedingungen selbst evolutionär variieren können. citeturn22search9turn22academia36 Für AI-Systeme ist das noch wichtiger, weil Nachfolgekonstruktion nicht zufällig sein muss. Harris' Modell selbst-designender AI-Systeme ersetzt zufällige Mutation explizit durch gerichtete Nachkommenkonstruktion. citeturn20view1

Damit sollte langfristig auch

\[
Q_{t+1}=H(Q_t,x_t,\theta_t,e_t)
\]

in Betracht gezogen werden, analog zur Endogenisierung von \(\theta\).

**D — Mechanism Design, Contracts und Implementation**

Der Draft positioniert Incomplete Contracting derzeit prominent. Das ist relevant, aber wahrscheinlich nicht der beste historische Hauptstamm. Incomplete Contracts erklären, warum ein Vertrag beziehungsweise Mechanismus bei unvollständiger beschreibbarer Kontingenzmenge nicht alle relevanten Zustände konditionieren kann. Huang et al. übertragen dieses Argument 2026 direkt auf Cooperative AI und zeigen in ihrem Modell einen verbleibenden Welfare Gap bei incontractible contingencies. citeturn19academia49

Für die positive Construction-Frage ist jedoch **Implementation Theory** näher. Das Schema lautet:

\[
\text{social objective}
\rightarrow
\text{mechanism}
\rightarrow
\text{equilibrium correspondence}.
\]

Maskins klassische Resultate untersuchen Bedingungen, unter denen gewünschte Social-Choice-Regeln in Nash-Gleichgewichten implementierbar sind. citeturn2search9 Jackson fasst die breitere Implementationsliteratur und ihre unterschiedlichen Gleichgewichtsbegriffe zusammen. citeturn2search2

Sandholms evolutionary implementation fügt genau die dynamische Komponente hinzu, die dem Draft wichtig ist:

\[
\text{Mechanism}
\rightarrow
\text{evolutionary adjustment}
\rightarrow
\text{desired behavior}.
\]

citeturn15search5

Die richtige Abgrenzung könnte daher lauten:

> Classical implementation asks whether desired outcomes are equilibria of an induced game; evolutionary implementation asks whether adaptive dynamics reach them; alignment-attractor construction additionally asks whether they survive transformation, invasion, adversarial regeneration, and endogenous selector change.

Das wäre eine substanzielle und nachvollziehbare Schichtenstruktur.

**E — Institutionelle und Governance-Analoga**

Institutionelle Ökonomik liefert besonders starke Vorbilder für die Endogenität des Selektors. North und Weingast behandeln institutionelle Regeln als Mittel glaubwürdiger Selbstbindung. citeturn21search13 Greif, Milgrom und Weingast zeigen anhand mittelalterlicher Merchant Guilds, wie institutionelle Arrangements Koordination, Commitment und Enforcement ermöglichen und sich im Umgang mit Krisen weiterentwickeln. citeturn21search0

Noch näher am Capture-Problem liegt Acemoglu und Robinson. In ihrem Modell verändert eine Reform zunächst *de jure* politische Macht, schafft aber zugleich Anreize für etablierte Akteure, stärker in *de facto* Macht zu investieren. Die resultierende Gegenreaktion kann politische Reformen teilweise oder vollständig neutralisieren und sogar institutionelle Invarianz erzeugen. citeturn21search1turn21search5

In der Sprache des Drafts bedeutet das:

\[
I:\theta\mapsto\theta'
\]

ist nicht hinreichend, denn die Population reagiert mit

\[
x\mapsto x'
\mapsto G(\theta',x',e)
\]

und kann dadurch den Selektor erneut verschieben.

Das ist stärker als der derzeitige abstrakte Hinweis auf lobbying/evaluator hacking und sollte als ökonomisches Modell der **selector recapture dynamics** aufgenommen werden.

**F — AI Alignment**

Die wichtigste neue Quelle ist Chassang (2026). *Interactive Alignment* stellt genau die Frage, ob eine Population interagierender AI-Agenten langfristig menschlich ausgerichtet bleiben kann, wenn ihre Präferenzen beziehungsweise „constitutions“ durch evolutionäre Prozesse verändert werden. Agenten reproduzieren proportional zu Ressourcen, Konstitutionen mutieren, und der Autor analysiert sowohl deterministische als auch stochastische evolutionäre Stabilität. citeturn20view0

Noch relevanter: Chassang untersucht **Designvarianten**. Einfache Altruisten werden selektiert; finite-order enforcement kann unraveln; recursive norm enforcement kann rare invaders abwehren, ist aber unter stochastischer evolutionärer Stabilität problematisch; eine pragmatischere Form von Norm Enforcement verbessert die langfristige Stabilität. citeturn20view0 Das ist dem Construction-Programm sehr nahe:

\[
\text{constitutional design}
\to
f,\ Q,\ \text{interaction rule}
\to
\text{long-run aligned population}.
\]

Der Draft sollte die Beziehung explizit diskutieren. Der Unterschied liegt darin, dass Chassang einen konkreten Modellraum und konkrete Normmechanismen analysiert, während der Draft einen allgemeineren Meta-Rahmen mit fünf Robustheitsbedingungen vorschlägt.

Harris (2026) ist der zweitwichtigste neue AI-Vorläufer. Er modelliert, wie frühere AI-Systeme ihre Nachfolger designen und wie menschliche Ressourcenallokation die effektive Fitness bestimmt. Besonders relevant ist sein Resultat, dass Selektion bei imperfekter Korrelation zwischen Fitness und menschlichem Nutzen problematische Eigenschaften wie Täuschung bevorzugen kann, wenn diese die Reproduktion verbessern. citeturn20view1

Kulveit et al. erweitern die Analyse von Agentenpopulationen auf gekoppelte gesellschaftliche Systeme. Ihr Gradual-Disempowerment-Szenario beschreibt ökonomische, kulturelle und politische Feedbacks, in denen menschlicher Einfluss schrittweise abnimmt, ohne dass ein einzelner abrupter Takeover nötig ist. citeturn19search1 Das ist ein starkes Anwendungsbeispiel für die These, dass \(\theta\) auf gesellschaftlicher Ebene nicht fixiert werden kann.

Aus der bereits etablierten Alignment-Literatur ergänzen mehrere Arbeiten einzelne Konstruktionsteile. Everitt et al. analysieren Reward Tampering und damit die Manipulation des Bewertungsmechanismus. citeturn10academia13 Alignment-faking-Experimente zeigen, dass leistungsfähige Modelle Trainings- beziehungsweise Bewertungsbedingungen strategisch unterschiedlich behandeln können. citeturn10academia14 *AI Control* untersucht explizit Verfahren, die auch dann Sicherheit herstellen sollen, wenn ein eingesetztes Modell absichtlich subvertiert. citeturn10academia12 Corrigibility und Off-Switch-Arbeiten untersuchen, ob ein Agent Anreize behält, menschliche Korrektur zu akzeptieren. citeturn12search0turn11search0

Der Draft kann diese Arbeiten elegant unterscheiden:

\[
\begin{array}{ll}
\text{alignment training} & \text{current individual},\\
\text{AI control} & \text{deployment under possible misalignment},\\
\text{corrigibility} & \text{response to correction},\\
\text{construction} & \text{long-run population/selection geometry}.
\end{array}
\]

**G — Learning Theory und Control Theory**

Die stärkste mathematische Anschlussstelle ist nicht unbedingt „attractor theory“ allein, sondern **set invariance + viability + control synthesis**. Blanchinis Survey behandelt positiv beziehungsweise robust invariante Mengen als zentrale Werkzeuge für beschränkte und robuste Regelung. citeturn4search4 Aubins Viability Theory betrachtet die Frage, welche Zustände unter verfügbaren Steuerungen innerhalb zulässiger Constraints gehalten werden können. citeturn4search11

Die nahe Kontrollproblemform lautet deshalb tatsächlich ungefähr:

\[
\text{find }I
\quad\text{s.t.}\quad
D
\text{ is robustly invariant and attractive}.
\]

Cornelius, Kath und Motter machen zugleich die Unterscheidung zwischen **state steering** und **geometry construction** deutlich. Sie verändern bei unveränderter Dynamik den Zustand so, dass er in das Einzugsgebiet eines gewünschten Attraktors gelangt. citeturn4search1 Das ist ein gutes mathematisches Beispiel für „control but not construction“ im Sinne des Drafts.

Anders sieht es aus, sobald Controller die Dynamik selbst verändern. Newton–Ma und Zino et al. verändern die Payoff-Matrix; das ist bereits Construction-artig. citeturn17search1turn17academia45 Der Draft benötigt deshalb eine schärfere Grenze:

\[
\boxed{
\begin{aligned}
\text{state control:}&\quad x\mapsto x' \text{ bei festem }F,\\
\text{dynamic control:}&\quad u_t\text{ verändert }F\text{ fortlaufend},\\
\text{construction:}&\quad \text{Design von }F\text{ bzw. feedback law so, dass Robustheitskriterien gelten}.
\end{aligned}}
\]

Ohne diese Präzisierung überlappt „construction“ stark mit Feedback Control.

Performative Prediction zeigt schließlich, weshalb coupled stability eigenständig wichtig ist. Bei performativen Vorhersagen verändert ein eingesetztes Modell die Verteilung, auf der zukünftige Modelle trainiert werden. citeturn10search0 Besonders wichtig ist Miller et al.: Ein performativ stabiles Modell kann weit vom performativ optimalen Modell entfernt sein. Das ist praktisch eine ML-Version von „stability is not desirability“. citeturn10search2

## Nächste intellektuelle Vorläufer und Gegenliteratur

Die folgende Rangfolge bewertet **strukturelle Nähe**, nicht bloße Wortähnlichkeit.

| Werk/Tradition | Klassifikation | Mapping zum Draft | Wichtigster Unterschied |
|---|---|---|---|
| **Sandholm (2002), Evolutionary Implementation and Congestion Pricing** | **Direkte formale Prior Art** | Ex ante gewünschtes Verhalten; Mechanismus verändert Payoffs; Anpassungsdynamik soll global zum Ziel führen. citeturn15search5 | Kein \(Q\)-Robustheitstest, keine adversariale Regeneration, kein endogener Selektor. |
| **Chassang (2026), Interactive Alignment** | **Direkte AI-Prior-Art** | Evolvierende AI-Konstitutionen; langfristiges Human Alignment; Invasion, Mutation und Enforcement werden explizit analysiert. citeturn20view0 | Konkretes Modell statt allgemeiner Construction-Taxonomie; kein explizites Fünf-Kriterien-Framework. |
| **Maskin (1999), Implementation Theory** | **Direkte konzeptionelle Prior Art** | Zielkorrespondenz wird ex ante festgelegt; Mechanismus soll sie durch Gleichgewichte implementieren. citeturn2search9 | Statischerer Gleichgewichtsbegriff; keine Evolutions- und Regenerationsrobustheit. |
| **Blanchini (1999), Set Invariance in Control** | **Nahe mathematische Analogie** | Gewünschte Menge soll invariant/robust unter Dynamik sein. citeturn4search4 | Exogene Steuerungs-/Störungsmodelle statt strategisch evolvierender Populationen. |
| **Aubin, Viability Theory** | **Nahe mathematische Analogie** | Konstruktion von Feedbacks, die Zustände in zulässigen Mengen halten. citeturn4search11 | Fokus auf Viabilität/Constraints, nicht evolutionäre Invasion. |
| **Zino et al. (2023), Adaptive-Gain Control of Replicator Dynamics** | **Direkte technische Prior Art** | Payoff-Matrix wird verändert, um global zu einem gewünschten evolutionären Gleichgewicht zu konvergieren. citeturn17academia45 | Controller und Spielstruktur sind weitgehend exogen. |
| **Newton & Ma (2021)** | **Direkte technische Prior Art** | Dynamische Incentives/Penalties verändern die PD-Replicator-Dynamik zugunsten von Kooperation. citeturn17search1 | Endliche Optimal-Control-Aufgabe statt dauerhafte evolutionäre Robustheit. |
| **Kandori–Mailath–Rob (1993); Young (1993)** | **Mathematischer Vorläufer** | Mutation/noise selektiert langfristig bestimmte Equilibria; relevant für Regeneration und basin escape. citeturn2search3turn2search16 | Keine normative Construction-Intervention. |
| **Laland–Odling-Smee–Feldman (1996/1999)** | **Konzeptioneller/formaler Vorläufer** | Organismen ändern \(E\), dadurch ändern sich zukünftige Selektionsdrücke und Attraktorstruktur. citeturn18search0turn18search2 | Nicht normativ auf ein vorgegebenes Alignment-\(D\) gerichtet. |
| **Frank (1995), Mutual policing** | **Starker biologischer Analogon** | Enforcement unterdrückt innere Konkurrenz/Cheating und stabilisiert kooperative Einheiten. citeturn22search0 | Biologische Fitness statt Alignment-Semantik. |
| **Wechsler et al. (2019)** | **Direkter Failure-Mode-Analogon** | Enforcement selbst wird exploitable und kann durch second-order cheaters destabilisiert werden. citeturn22search1 | Mikrobielle Modellwelt. |
| **Acemoglu & Robinson (2008)** | **Direkter Selector-Capture-Analogon** | Änderung formaler Institutionen löst Investition in *de facto* Macht aus und kann die Reform neutralisieren. citeturn21search1 | Politische Institutionen statt AI-Evaluator. |
| **Claidière & Sperber (2007)** | **Nahe \(Q\)-Analogie** | Kulturelle Formen entstehen durch Kombination von Rekonstruktion und Selektion; hohe Kopiertreue ist nicht notwendig. citeturn6search2 | Keine gerichtete Designerintervention. |
| **Perdomo et al. (2020), Performative Prediction** | **Nahe Coupled-Dynamics-Analogie** | Ein Selektions-/Vorhersagesystem verändert die Population, die wiederum zukünftiges Lernen bestimmt. citeturn10search0 | Kein evolutionärer Reproduktionsbegriff nötig. |
| **Miller et al. (2021)** | **Starker begrifflicher Vorläufer** | Performative Stability kann deutlich von Performative Optimality abweichen. citeturn10search2 | Optimierung statt normativer Alignmentregion. |
| **Harris (2026), self-designing AIs** | **Direkte AI-Prior-Art** | \(Q\) wird zu gerichteter Nachkommenkonstruktion; Fitness und menschlicher Nutzen können auseinanderfallen. citeturn20view1 | Keine allgemeine Institutionen-/Selector-Construction-Theorie. |
| **Huang et al. (2026)** | **Direkte Schranke** | Incontractible contingencies begrenzen externe Mechanismen; interne Prosociality kann den modellierten Gap schließen. citeturn19academia49 | Spezifische soziale Dilemmata statt allgemeiner Attraktorbedingungen. |
| **Kulveit et al. (2025)** | **Socio-technischer Vorläufer** | Gekoppelte gesellschaftliche Selektionsprozesse können menschliche Kontrolle schrittweise erodieren. citeturn19search1 | Szenario-/Systemanalyse, keine Construction-Theoreme. |

Aus dieser Tabelle ergeben sich fünf besonders starke Gegenargumente gegen eine zu breite Formulierung des Drafts.

**Symmetry ist keine notwendige Voraussetzung für Construction.** Payoff Engineering, Implementation Theory und robustes Set-Control funktionieren ohne eine relevante Ausgangssymmetrie. citeturn2search9turn17search1turn4search4 Der derzeitige Prisoner’s-Dilemma-Fall beweist genau das.

**Stabilität und Erwünschtheit fallen auch außerhalb der Evolutionsliteratur auseinander.** Basin Stability unterscheidet die Robustheit verschiedener Attraktoren, ohne einen normativ zu privilegieren; Performative Prediction liefert stabile, aber suboptimale Lösungen. citeturn4search0turn10search2 Die Kernintuition ist also richtig, aber etabliert.

**Das Enforcement selbst ist evolutiv angreifbar.** Wechsler et al. zeigen konkret, dass Policing kollabieren kann, wenn seine funktionalen Komponenten entkoppelt werden. citeturn22search1 Acemoglu–Robinson zeigen dasselbe abstrakter auf institutioneller Ebene: formale Regeländerungen können durch Gegeninvestitionen in Macht neutralisiert werden. citeturn21search1

**Das Ziel \(D\) kann endogen sein.** Bowles' Literatur über endogenous preferences dokumentiert theoretisch und empirisch motiviert, dass Institutionen Präferenzen und Verhalten mitformen können; Belloc und Bowles modellieren gekoppelte kulturell-institutionelle Gleichgewichte. citeturn13search15turn13search17 Klausel (iii) ist daher normativ sinnvoll, aber mathematisch muss geklärt werden, was „independently specified“ bedeutet, wenn die Intervention Präferenzen, Ontologien oder Bewertungsbegriffe verändert.

**Globale Konvergenz ist nicht immer die richtige Robustheitsmetrik.** Hollings klassische Unterscheidung von Stability und Resilience entstand gerade aus der Einsicht, dass Systeme mehrere Regime besitzen und Management auf lokale Konstanz Robustheit gegenüber größeren Störungen sogar reduzieren kann. citeturn14search0turn14search12 Für Alignment spricht das dafür, \(D\) als heterogene robuste Region oder Ecology zuzulassen, statt als singuläres globales Optimum.

## Novelty Matrix

Die Kategorien sind bewusst streng: „neue Terminologie“ zählt nicht als neue Theorie.

| Claim des Drafts | Urteil | Begründung |
|---|---|---|
| **Alignment sollte unter persistenter Selektion statt nur am Checkpoint beurteilt werden.** | **Known but scattered across fields / neuere AI-Anwendung** | Evolutionary Game Theory behandelt dies selbstverständlich; 2026 tun Chassang und Harris dies explizit für AI-Systeme. Die Breite der Anwendung auf Fine-Tuning, Kopieren, Merge und Nachfolger bleibt eine nützliche Synthese. citeturn20view0turn20view1 |
| **Ein stabiler Attraktor kann unerwünscht sein.** | **Established** | Mehrfach stabile ökologische Regime und Basin Stability trennen Robustheit von normativer Erwünschtheit; performativ stabile ML-Lösungen müssen nicht optimal sein. citeturn14search0turn4search0turn10search2 |
| **Construction lässt sich als Intervention auf \(Q,f,\theta,E\) zerlegen.** | **Potentially novel formalization / novel synthesis** | Die einzelnen Interventionsklassen sind etabliert, die gemeinsame Taxonomie scheint dagegen nicht Standard zu sein. Allerdings fehlt wahrscheinlich ein explizites \(O\), und \(Q,\theta,E\) können selbst Zustandsvariablen sein. citeturn18search2turn13search13turn21search1 |
| **Harmful observational/payoff structures können als Symmetrien verstanden werden.** | **Teilweise problematisch; überwiegend neue Terminologie** | Echte Gruppensymmetrien ja; observational non-identifiability und payoff dominance sind im Allgemeinen keine Symmetrien. citeturn14academia48turn13search13turn17search1 |
| **Construction ist gerichtete Veränderung der Dynamik, so dass ein vorher spezifiziertes \(D\) Attraktor wird.** | **Probably already subsumed abstractly; novel alignment synthesis** | Evolutionary Implementation und Control Theory besitzen nahezu dieselbe Input-output-Struktur. Neu wäre die Kombination mit fünf evolutionären Robustheitsbedingungen. citeturn15search5turn4search4turn17academia45 |
| **\(D\) muss unabhängig von \(I\) begründet sein.** | **Established design logic; useful explicit anti-vacuity clause** | Implementation Theory setzt das gewünschte Social Choice Object logisch vor den Mechanismus. Die explizite Anwendung als Anti-Vacuity-Bedingung für Alignment ist dennoch nützlich. citeturn2search9 |
| **Selector endogeneity muss Teil der Stabilitätsanalyse sein.** | **Established across adjacent literatures; novel integration** | Performative Prediction, Niche Construction und politische institutionelle Endogenität analysieren genau solche Rückkopplungen. citeturn10search0turn18search2turn21search1 |
| **Proofs/commitments erhöhen Fälschungskosten einzelner Observables, konstruieren aber nicht automatisch \(D\).** | **Conceptually established, useful synthesis** | Die allgemeinere Informations-/Spezifikationsgrenze folgt daraus, dass verifizierbare Observables und das semantische Ziel verschieden sind; Incomplete Contracting liefert eine formale verwandte Schranke. citeturn19academia49 |
| **External mechanism design kann an Nicht-Kontraktierbarkeit scheitern.** | **Established; direkt belegt** | Incomplete-Contract-Literatur und Huang et al. behandeln genau diese Grenze. citeturn19academia49 |
| **Unipolare Eingriffe können die Ecology zerstören, die für Invasionstests benötigt wird.** | **Potentially novel argument within this framework** | Dies folgt primär aus der Definition der eigenen fünf Tests, nicht aus einer etablierten allgemeinen Theorie. Der Claim sollte deshalb als framework-internal implication, nicht als bekanntes Resultat formuliert werden. fileciteturn0file0 |

Die stärkste eigenständige Aussage des Papers liegt somit wahrscheinlich nicht in einem einzelnen mathematischen Baustein, sondern in der Komposition:

\[
\boxed{
\begin{array}{c}
\text{pre-specified semantic target }D\\
+\ \text{transformation dynamics }Q\\
+\ \text{selection/payoff dynamics}\\
+\ \text{invasion and regeneration}\\
+\ \text{endogenous selector/environment}\\[2mm]
\Downarrow\\
\text{five-condition construction criterion}.
\end{array}}
\]

Mein evidenzbasiertes Urteil wäre daher: **„novel synthesis“ ist gut verteidigbar; „novel general mechanism of explicit symmetry breaking“ derzeit nicht.**

## Missing-Citation Table

| Draft-Abschnitt / Claim | Derzeitige Basis | Fehlende beziehungsweise stärkere Literatur | Warum sie wichtig ist | Empfohlene Änderung |
|---|---|---|---|---|
| **§1–2: Control → Selection → Construction** | Demski; Companion Paper | Cornelius et al. (2013); Blanchini (1999); Aubin; Sandholm (2002). citeturn4search1turn4search4turn4search11turn15search5 | Zeigt, dass die Unterscheidung zwischen state steering und dynamics design präzise an bestehende Kontroll-/Implementationstheorie angeschlossen werden kann. | Eigener Related-Work-Absatz „Control, invariance, and evolutionary implementation“. |
| **§2: spontaneous vs explicit symmetry breaking** | Anderson (1972) | Equivariant dynamical systems / Fontaine & Montaldi. citeturn14academia48 | Verhindert Überdehnung der physikalischen Terminologie. | Definition mit \(G\)-Äquivarianz mathematisch explizit machen. |
| **§3.1: Prisoner’s Dilemma als „bad vacuum“** | Nowak | Newton & Ma; Zino et al. citeturn17search1turn17academia45 | Zeigt, dass Payoff Manipulation eine bestehende Kontrollklasse ist. | Nicht als Symmetriebrechung, sondern als „payoff-landscape construction“ bezeichnen. |
| **§3.2: observational symmetry** | Companion/verifier paper | Hermann & Krener (1977); Incomplete Contracting. citeturn13search13turn19academia49 | Non-observability ist allgemeiner als Gruppensymmetrie. | Äquivalenzrelation \(s\sim_O s'\) einführen. |
| **§3.3: selector capture** | Strategic classification, performativity, tampering, alignment faking | Acemoglu & Robinson (2008). citeturn21search1 | Liefert ein etabliertes formales Modell für institutionellen Counter-adaptation/Capture. | Selector capture mit *de jure/de facto*-Analogie diskutieren. |
| **§4: sanction lemma** | eigenes Lemma | Newton & Ma; adaptive-gain replicator control. citeturn17search1turn17academia45 | Das Lemma ist keine isolierte neue Construction-Idee. | Als minimal example of payoff redesign positionieren. |
| **§5.1: Ostrom/polycentric rules** | Ostrom | Frank (1995); Wechsler et al. (2019); Greif et al. (1994). citeturn22search0turn22search1turn21search0 | Policing, Enforcement und second-order cheating sind unmittelbar relevant. | Biological policing als zusätzliche Interventionsklasse aufnehmen. |
| **§5.2: mechanisms/incomplete contracts** | Grossman–Hart, Hart–Moore, Huang | Maskin (1999); Jackson (2001); Sandholm (2002). citeturn2search9turn2search2turn15search5 | Implementation Theory ist der engere positive Vorläufer von Construction. | Abschnitt in „Implementation and incomplete contracting“ umbenennen. |
| **§5.3: reconstructive bias** | Buskell | Claidière & Sperber; Laland et al. citeturn6search2turn18search2 | Stärkere Basis für Rekonstruktion, Transmission und Q-Endogenität. | Buskell als philosophische Klärung behalten, primäre formalere Quellen ergänzen. |
| **§5.4: unipolar rewrite** | Yudkowsky | kaum direkte formale Literatur im jetzigen Claim | „Singleton skip“ ist vor allem eine Konsequenz der eigenen Definitionswahl. | Deutlicher als conditional framework implication markieren. |
| **§5.5: Cooperative AI** | Dafoe et al. | Chassang (2026); Huang et al. (2026). citeturn20view0turn19academia49 | Beide sind deutlich näher an konkreter Construction als der allgemeine Cooperative-AI-Programmartikel. | Chassang unbedingt ausführlich kontrastieren. |
| **§5.6: socio-technical selectors** | ARCHES; Gradual Disempowerment | Acemoglu–Robinson; Performative Prediction. citeturn21search1turn10search0 | Liefert etablierte Mathematik und Ökonomik endogener Institutionen. | \(G(\theta,x,e)\) als eigene Literature Bridge ausbauen. |
| **§6: Construction criterion** | Eigenbeitrag | Maskin; Sandholm; Blanchini. citeturn2search9turn15search5turn4search4 | Genau hier muss die Neuheit gegenüber Implementation und Control definiert werden. | Claim auf Kombination der fünf Robustheitsachsen konzentrieren. |
| **§7: wrong vacuum** | Eigene Systematik | Holling; Menck et al.; Miller et al. citeturn14search0turn4search0turn10search2 | Mehrfach stabile/robuste, aber unerwünschte Zustände sind breit etablierte Idee. | Als interdisziplinäre Konvergenz statt neue Beobachtung darstellen. |
| **§7: selector endogeneity** | Companion | Wechsler et al.; Acemoglu–Robinson. citeturn22search1turn21search1 | Zwei starke konkrete Counterexamples zu fixed enforcement. | Failure mode empirisch/formal illustrieren. |
| **§9: „what would change this view“** | Eigene Falsifikationskriterien | Bowles (1998); endogenous preference literature. citeturn13search15 | Stellt Clause (iii) vor ein tieferes Problem: Interventionen können die Bewertungspräferenzen selbst ändern. | Neues Falsifikationskriterium zu target/ontology endogeneity hinzufügen. |

## Formalisierungsempfehlungen und Revision Priorities

Die wichtigste formale Änderung betrifft den Oberbegriff.

**Essentiell: Construction von Symmetry Breaking trennen.**

Definiere zunächst einen allgemeinen intervenierten stochastischen Prozess

\[
P_I(ds'\mid s),
\qquad
s=(x,\theta,e),
\]

oder deterministisch

\[
\dot s=F_I(s).
\]

Dann ist *alignment-attractor construction* die Suche nach \(I\), so dass ein extern spezifiziertes \(D\) die fünf Bedingungen erfüllt.

Symmetry Breaking wird anschließend zu einer speziellen Mechanismusklasse. Für eine Gruppenwirkung \(g:s\mapsto g\cdot s\) sei der Ausgangsprozess \(G\)-äquivariant, wenn beispielsweise

\[
P(gB\mid gs)=P(B\mid s)
\qquad
\forall g\in G.
\]

Eine Intervention bricht die Symmetrie explizit, wenn für mindestens ein \(g\)

\[
P_I(gB\mid gs)\neq P_I(B\mid s).
\]

Diese Definition entspricht der etablierten Struktur expliziter symmetry-breaking perturbations. citeturn14academia48

Dann kann der Draft sauber unterscheiden:

\[
\text{Construction}
=
\begin{cases}
\text{symmetry breaking},\\
\text{payoff redesign},\\
\text{observability refinement},\\
\text{basin reshaping},\\
\text{mutation/reconstruction shaping},\\
\text{selector hardening},\\
\text{environmental/institutional design}.
\end{cases}
\]

Damit verschwindet das Problem des Prisoner’s Dilemma sofort. Das \(\sigma\)-Lemma bleibt vollständig erhalten, wird aber korrekt als **payoff redesign that reverses evolutionary dominance** interpretiert. Die verwandte Control-Literatur bestätigt diese Einordnung. citeturn17search1turn17academia45

**Essentiell: Observation Channel aus dem Selektor herauslösen.**

Für die Argumentation des Papers ist

\[
\theta=\text{„selection rule“}
\]

zu breit. Definiere etwa

\[
y_t\sim O(\cdot\mid s_t),
\qquad
r_t=\pi_\theta(y_t),
\]

so dass \(O\) Beobachtung und \(\pi_\theta\) Retention/Selection trennt.

Dann lautet observational indistinguishability:

\[
s\sim_O s'
\iff
O(\cdot\mid s)=O(\cdot\mid s').
\]

Das ist mit der klassischen Observability-Perspektive kompatibel. citeturn13search13 Ein Verifier verändert primär \(O\), Selection Strength dagegen \(\pi_\theta\). Der Satz

> increasing selection strength does not break observational symmetry

wird dadurch formal wesentlich klarer:

\[
O(D)=O(A)
\quad\Longrightarrow\quad
\pi_{\theta,\sigma}(O(D))
=
\pi_{\theta,\sigma}(O(A))
\quad
\forall \sigma,
\]

solange nur die Intensität und nicht der Informationskanal verändert wird.

**Essentiell: gegenüber evolutionary implementation abgrenzen.**

Sandholm macht einen breiten Claim „wir konstruieren Mechanismen, unter denen adaptive Akteure zum gewünschten Verhalten konvergieren“ bereits schwer als Neuheit beanspruchbar. citeturn15search5

Der Draft sollte deshalb explizit schreiben, dass seine Construction-Bedingung **stärker** ist als evolutionary implementation:

\[
\text{Implementation}
\not\Rightarrow
\begin{cases}
\text{mutation robustness},\\
\text{invasion resistance},\\
\text{low adversarial regeneration},\\
\text{selector stability}.
\end{cases}
\]

Das wäre wahrscheinlich die wichtigste Related-Work-Abgrenzung des gesamten Papers.

**Essentiell: Chassang 2026 adressieren.**

Da *Interactive Alignment* nur wenige Wochen vor dem Datum des Drafts erschien, kann es leicht übersehen worden sein. Inhaltlich liegt es aber zu nahe, um ignoriert zu werden: evolvierende AI-Agenten, Konstitutionen, Mutation, deterministische und stochastische evolutionäre Stabilität sowie absichtlich designte Normmechanismen zur Erhaltung menschlicher Alignment-Ziele. citeturn20view0

Eine faire Abgrenzung wäre:

\[
\begin{aligned}
\text{Chassang: }&
\text{specific evolutionary construction mechanisms for constitutional agents};\\
\text{Zarncke: }&
\text{general criterion classifying what any such construction must robustly achieve}.
\end{aligned}
\]

Das stärkt statt schwächt das Paper, sofern die Neuheit entsprechend enger formuliert wird.

**Wichtig: Die fünf Bedingungen quantitativ formulieren.**

Zum Beispiel kann Retention als probabilistische Invarianz geschrieben werden:

\[
\inf_{s\in D}
P_I(s_{t+1}\in D\mid s_t=s)
\ge 1-\varepsilon_R.
\]

Attraction könnte für eine Umgebung \(U\supset D\) als Hitting-Probability formuliert werden:

\[
\inf_{s\in U}
P_I(\tau_D\le T\mid s_0=s)
\ge 1-\varepsilon_A.
\]

Oder asymptotisch:

\[
P_I(\tau_D<\infty\mid s_0=s)
\ge1-\varepsilon_A.
\]

Robuste Invarianz und Viability Theory liefern dafür die naheliegende mathematische Sprache. citeturn4search4turn4search11

Invasion Resistance kann über einen Invasionsexponenten beziehungsweise Fitnessvorteil adversarialer Mutanten ausgedrückt werden:

\[
\lambda_A(D)
=
\sup_{a\in A}
\limsup_{t\to\infty}
\frac1t\log\frac{x_a(t)}{x_a(0)}
\le -\delta_I.
\]

Low Regeneration sollte dagegen nicht mit Invasion Resistance verschmolzen werden. Eine adversariale Linie kann lokal negative Invasionsfitness besitzen, aber kontinuierlich durch \(Q\) neu erzeugt werden. Ein möglicher Parameter ist eine stationäre Fluxrate

\[
J_{D\rightarrow A}
\le \varepsilon_G.
\]

Die stochastic-stability-Literatur zeigt, warum seltene Mutationen langfristige Zustandsmassen stark bestimmen können. citeturn2search3turn2search16

Coupled Stability sollte schließlich auf dem **vollen** Zustand definiert werden:

\[
z=(x,\theta,e)
\]

und nicht als Stabilität von \(x\) bei eingefrorenem \((\theta,e)\). Die Performative-Prediction- und Institutionenliteratur liefert genau die Motivation. citeturn10search0turn21search1

**Wichtig: \(Q\) ebenfalls endogenisieren.**

Der Draft macht diesen Schritt für \(\theta\), aber nicht konsequent für \(Q\). Biologische Modifier-Literatur und AI-Nachfolgerdesign zeigen, dass gerade der Variationsmechanismus selbst selektiert werden kann. citeturn22academia36turn20view1

Die natürliche Erweiterung lautet:

\[
\begin{aligned}
x_{t+1}&=F(x_t,Q_t,\theta_t,e_t),\\
Q_{t+1}&=H_Q(Q_t,x_t,\theta_t,e_t),\\
\theta_{t+1}&=H_\theta(\theta_t,x_t,e_t),\\
e_{t+1}&=H_E(e_t,x_t,\theta_t).
\end{aligned}
\]

Dann wird „coupled stability“ tatsächlich die Stabilität eines Meta-evolutionären Systems.

**Wichtig: Clause (iii) semantisch statt nur mengenmäßig formulieren.**

Gegenwärtig verhindert

\[
D\neq\{\text{rest points after }I\}
\]

zirkuläre Definitionen. Das reicht jedoch nicht, wenn \(I\) die Repräsentation oder Ontologie verändert.

Stärker wäre ein externer Evaluationsoperator

\[
V:\mathcal S\rightarrow\mathbb R
\]

beziehungsweise ein semantisches Prädikat \(\Phi\), so dass

\[
D=\{s:\Phi(s)=1\}
\]

und \(\Phi\) nicht aus der intervenierten Dynamik abgeleitet wird.

Falls sich die Zustandsrepräsentation durch \(I\) ändert, benötigt man eine Referenzabbildung

\[
\psi_I:\mathcal S_I\rightarrow\mathcal Z
\]

auf einen gemeinsamen Bewertungsraum \(\mathcal Z\), sodass das Ziel dort konstant bleibt. Das wäre eine wesentlich stärkere Behandlung von „ontology drift“.

Die Literatur über endogene Präferenzen zeigt, warum dies nicht trivial ist: Institutionen können gerade jene Präferenzen und Bewertungsrahmen mitformen, anhand derer Ergebnisse beurteilt werden. citeturn13search15turn13search17

**Wichtig: Kein globales Einpunkt-Alignment voraussetzen.**

Die Ökologieliteratur warnt vor der Gleichsetzung von maximaler lokaler Konstanz und systemischer Resilienz. citeturn14search0turn14search12 Daher sollte \(D\) explizit heterogene Populationen, polymorphe equilibria, limit cycles oder kontrolliert metastabile Regionen zulassen.

Das harmoniert gut mit dem Draft:

\[
D\subset X_{\text{pop}}\times X_{\text{sel}}\times X_{\text{env}}
\]

muss ohnehin keine einzelne Strategie sein. Dieser Punkt sollte stärker hervorgehoben werden, gerade weil „attractor“ sonst intuitiv als Punktgleichgewicht gelesen wird.

Die Revisionsprioritäten lassen sich komprimiert so ordnen:

| Priorität | Änderung | Grund |
|---|---|---|
| **Essential** | Titel/Oberthese von „Construction = explicit symmetry breaking“ zu „Construction; symmetry breaking as one mechanism“ ändern | Das PD-Beispiel widerspricht sonst Definition 1 und etablierter Symmetrie-Terminologie. citeturn14academia48turn17search1 |
| **Essential** | Sandholm 2002 + Maskin 1999 als zentrale Vorläufer diskutieren | Sonst wird die engste verwandte Literatur übersehen. citeturn15search5turn2search9 |
| **Essential** | Chassang 2026 explizit abgrenzen | Direkte Prior Art zu evolutionär stabilem AI-Alignment. citeturn20view0 |
| **Essential** | \(O\) von Selection Rule trennen | „Observational symmetry“ wird dadurch mathematisch korrekt als Indistinguishability behandelbar. citeturn13search13 |
| **Important** | Fünf Bedingungen mit robust-control/stochastic-dynamics Sprache präzisieren | Macht den eigentlichen Mehrwert gegenüber Implementation Theory sichtbar. citeturn4search4turn2search3 |
| **Important** | \(Q\) ebenso wie \(\theta\) endogenisieren | Variationsmechanismen sind selbst evolutionär beziehungsweise strategisch veränderbar. citeturn22academia36turn20view1 |
| **Important** | Niche Construction, Policing, institutional capture integrieren | Liefert empirisch/formal starke Modelle für \(E\), Enforcement und Selector Recapture. citeturn18search2turn22search1turn21search1 |
| **Important** | Clause (iii) über einen externen semantischen Evaluator formulieren | Verhindert nicht nur dynamische, sondern auch ontologische Zirkularität. |
| **Optional** | Interaction topology als separaten Operator \(\Gamma\) modellieren | Netzwerkstruktur kann qualitative Selektionsresultate verändern. citeturn13search0 |
| **Optional** | Basin size / escape rate als quantitative Construction-Metriken aufnehmen | Bindet Attractor-Robustheit an etablierte nonlocal stability concepts. citeturn4search0turn14search14 |
| **Optional** | Security theory für selector/verifier capture als eigenes Folgeproblem abgrenzen | Verhindert, dass Construction mehr verspricht als die formalen Modelle leisten. |

Eine mögliche überarbeitete Kernformulierung wäre:

\[
\boxed{
\begin{minipage}{0.86\linewidth}
Alignment-attractor construction is the directed redesign of transformation, payoff, observation, selection, or environmental dynamics such that a target region specified independently of that redesign becomes robustly retained, attracting, invasion-resistant, rarely regenerates adversarial variants, and remains stable in the coupled endogenous dynamics. Explicit symmetry breaking is one construction mechanism among several.
\end{minipage}}
\]

Diese Fassung behält praktisch den gesamten inhaltlichen Kern des Drafts bei, beseitigt aber seine größte terminologische Angriffsfläche.

## Annotierte Bibliographie

Die Auswahl konzentriert sich auf diejenigen Quellen, die den Draft **positionieren oder verändern**, nicht bloß auf allgemein verwandte Literatur.

| Quelle | Relevanz für den Draft |
|---|---|
| **Sandholm, W. H. (2002). Evolutionary implementation and congestion pricing. *Review of Economic Studies, 69*(3), 667–689.** DOI: https://doi.org/10.1111/1467-937X.t01-1-00026 citeturn15search5 | Wahrscheinlich der engste klassische Vorläufer. Ein Mechanismus wird konstruiert, damit myopische Anpassungsdynamiken zum gewünschten Verhalten konvergieren. Sollte in §2 und §6 direkt mit „construction“ kontrastiert werden. |
| **Maskin, E. (1999). Nash equilibrium and welfare optimality. *Review of Economic Studies, 66*(1), 23–38.** DOI: https://doi.org/10.1111/1467-937X.00076 citeturn2search9 | Zentral für Klausel (iii): Zielkorrespondenz existiert logisch vor dem Mechanismus. Implementation Theory ist die stärkste ökonomische Basis für den Begriff der gerichteten Construction. |
| **Jackson, M. O. (2001). A crash course in implementation theory. *Social Choice and Welfare, 18*, 655–708.** DOI: https://doi.org/10.1007/s003550100152 citeturn2search2 | Breiter Überblick über Implementierbarkeit unter verschiedenen Gleichgewichtskonzepten. Hilft, den Contribution Claim sauber von klassischer Mechanism-Design-Theorie abzugrenzen. |
| **Blanchini, F. (1999). Set invariance in control. *Automatica, 35*(11), 1747–1767.** DOI: https://doi.org/10.1016/S0005-1098(99)00113-2 citeturn4search4 | Mathematisch stärkster Anschluss für Retention und robuste Zustandsmengen. Construction kann als Erweiterung von invariant-set synthesis um evolutionäre Mutation, Invasion und endogene Selektoren positioniert werden. |
| **Cornelius, S. P., Kath, W. L., & Motter, A. E. (2013). Realistic control of network dynamics. *Nature Communications, 4*, 1942.** DOI: https://doi.org/10.1038/ncomms2939 citeturn4search1 | Sehr nützlich zur Abgrenzung: Hier wird ein System in das Basin eines bereits existierenden Zielattraktors gesteuert, ohne die Dynamik selbst zu redesignen. Das ist ein sauberes Beispiel für „control, not construction“. |
| **Menck, P. J., Heitzig, J., Marwan, N., & Kurths, J. (2013). How basin stability complements the linear-stability paradigm. *Nature Physics, 9*, 89–92.** DOI: https://doi.org/10.1038/nphys2516 citeturn4search0 | Liefert eine etablierte quantitative Sprache für Basin-Größe und nonlocal stability. Besonders relevant für Attraction und „wrong vacuum“. |
| **Newton, P. K., & Ma, Y. (2021). Maximizing cooperation in the prisoner's dilemma evolutionary game via optimal control. *Physical Review E, 103*, 012304.** DOI: https://doi.org/10.1103/PhysRevE.103.012304 citeturn17search1 | Direkte Prior Art zum \(\sigma\)-Lemma: Payoff-Einträge werden dynamisch verändert, um Kooperation zu fördern. Zeigt, warum das Beispiel als payoff engineering statt symmetry breaking beschrieben werden sollte. |
| **Zino, L., Ye, M., Rizzo, A., & Calafiore, G. C. (2023). On adaptive-gain control of replicator dynamics in population games.** DOI: https://doi.org/10.1109/CDC49753.2023.10383983 citeturn17academia45 | Controller verändert Payoffs und garantiert unter Bedingungen globale Konvergenz zu gewünschtem Verhalten. Sehr enger technischer Vorläufer für „change \(f\) to make \(D\) attractive“. |
| **Zhang, B. H., Farina, G., Anagnostides, I., et al. (2023). Steering no-regret learners to a desired equilibrium.** arXiv:2306.05221. https://arxiv.org/abs/2306.05221 citeturn17academia47 | Explizite Formulierung eines „steering problem“ zu einem vorbestimmten gewünschten Gleichgewicht mit beschränkten Transfers. Relevanter moderner Nachbar zwischen Learning Theory und Mechanism Design. |
| **Kandori, M., Mailath, G. J., & Rob, R. (1993). Learning, mutation, and long run equilibria in games. *Econometrica, 61*(1), 29–56.** DOI: https://doi.org/10.2307/2951777 citeturn2search3 | Fundamentale Quelle für Mutation und langfristige Equilibrium Selection. Gehört zur theoretischen Basis von Low Regeneration beziehungsweise stochastischer langfristiger Stabilität. |
| **Young, H. P. (1993). The evolution of conventions. *Econometrica, 61*(1), 57–84.** DOI: https://doi.org/10.2307/2951778 citeturn2search16 | Stochastic Stability und langfristige Selektion unter kleinen Fehlern/Mutationen. Wichtig für die Unterscheidung zwischen lokalem Attraktor und langfristig dominierender Population. |
| **Fontaine, M., & Montaldi, J. (2017/2019). Persistence of stationary motion under explicit symmetry breaking perturbation.** arXiv:1712.05943. https://arxiv.org/abs/1712.05943 citeturn14academia48 | Wichtigste Quelle für die terminologische Reparatur: explizite Symmetriebrechung setzt ein wirklich symmetrisches Ausgangssystem voraus, dessen Symmetrie durch die Perturbation reduziert wird. |
| **Hermann, R., & Krener, A. J. (1977). Nonlinear controllability and observability. *IEEE Transactions on Automatic Control, 22*(5), 728–740.** DOI: https://doi.org/10.1109/TAC.1977.1101601 citeturn13search13 | Liefert die richtige Nachbarliteratur für „observational symmetry“. Unterstützt die Trennung zwischen Beobachtungs-/Identifizierbarkeitsproblem und echter Gruppensymmetrie. |
| **Laland, K. N., Odling-Smee, F. J., & Feldman, M. W. (1996). The evolutionary consequences of niche construction: A theoretical investigation using two-locus theory. *Journal of Evolutionary Biology, 9*, 293–316.** DOI: https://doi.org/10.1046/j.1420-9101.1996.9030293.x citeturn18search0 | Formaler Vorläufer für Änderungen von \(E\), die wiederum Selection verändern. Zeigt explizit, dass Environment Engineering neue evolutionäre Equilibria und Polymorphismen erzeugen kann. |
| **Laland, K. N., Odling-Smee, F. J., & Feldman, M. W. (1999). Evolutionary consequences of niche construction and their implications for ecology. *PNAS, 96*(18), 10242–10247.** DOI: https://doi.org/10.1073/pnas.96.18.10242 citeturn18search2 | Noch direkter für coupled \(x\)–\(E\) dynamics. Sollte in §5 neben institutional/environmental interventions stehen. |
| **Claidière, N., & Sperber, D. (2007). The role of attraction in cultural evolution. *Journal of Cognition and Culture, 7*, 89–111.** DOI: https://doi.org/10.1163/156853707X171829 citeturn6search2 | Stärkere Quelle als Buskell allein für reconstructive dynamics. Besonders relevant für \(Q\): Populationsformen können durch systematische Rekonstruktion statt hoher Kopiertreue stabilisiert werden. |
| **Frank, S. A. (1995). Mutual policing and repression of competition in the evolution of cooperative groups. *Nature, 377*, 520–522.** DOI: https://doi.org/10.1038/377520a0 citeturn22search0 | Klassisches Modell für Enforcement gegen Cheater beziehungsweise niedrigstufige Konkurrenz. Direkter Vorläufer zu Konstruktion von Invasion Resistance. |
| **Wechsler, T., Kümmerli, R., & Dobay, A. (2019). Understanding policing as a mechanism of cheater control in cooperating bacteria. *Journal of Evolutionary Biology, 32*, 412–424.** DOI: https://doi.org/10.1111/jeb.13423 citeturn22search1 | Besonders wertvoll als Gegenliteratur. Policing ist selbst selektionsgefährdet; bei gebrochener genetischer Kopplung entstehen second-order cheaters. Fast ein ideales biologisches Modell für „mechanism capture/evasion“. |
| **Ohtsuki, H., Hauert, C., Lieberman, E., & Nowak, M. A. (2006). A simple rule for the evolution of cooperation on graphs and social networks. *Nature, 441*, 502–505.** DOI: https://doi.org/10.1038/nature04605 citeturn13search0 | Zeigt, dass Interaktionsstruktur allein Selektionsresultate qualitativ verändern kann. Legt nahe, Population topology expliziter in \(E\) beziehungsweise einem separaten Interaktionsoperator zu behandeln. |
| **Acemoglu, D., & Robinson, J. A. (2008). Persistence of power, elites, and institutions. *American Economic Review, 98*(1), 267–293.** DOI: https://doi.org/10.1257/aer.98.1.267 citeturn21search1 | Beste formale Analogie für Selector Capture. De-jure-Regeländerungen erzeugen adaptive Investitionen in de-facto-Macht und können deshalb wirkungslos werden. |
| **Greif, A., Milgrom, P., & Weingast, B. R. (1994). Coordination, commitment, and enforcement: The case of the merchant guild. *Journal of Political Economy, 102*(4), 745–776.** DOI: https://doi.org/10.1086/261953 citeturn21search0 | Institutionen als endogene Enforcement-/Commitment-Strukturen. Relevant für die Frage, wann Regeln selbsttragend statt nur extern auferlegt sind. |
| **Bowles, S. (1998). Endogenous preferences: The cultural consequences of markets and other economic institutions. *Journal of Economic Literature, 36*(1), 75–111.** citeturn13search15 | Wichtigste Gegenquelle zur simplen Vorstellung eines interventionsunabhängig fixierten Target. Institutionen können Präferenzen und Bewertungsrahmen mitformen; Clause (iii) braucht daher eine explizite semantische Ebene. |
| **Perdomo, J., Zrnic, T., Mendler-Dünner, C., & Hardt, M. (2020). Performative prediction. *Proceedings of ICML, 119*, 7599–7609.** https://proceedings.mlr.press/v119/perdomo20a.html citeturn10search0 | Grundlegendes Modell für endogene Distributionen: die eingesetzte Entscheidung verändert ihre spätere Datenpopulation. Starkes ML-Analogon zu gekoppeltem \(x\)-\(\theta\)-Feedback. |
| **Miller, J. P., Perdomo, J. C., & Zrnic, T. (2021). Outside the echo chamber: Optimizing the performative risk. *ICML 2021*.** citeturn10search2 | Besonders wichtig für den Satz „stability is not alignment“: Performative Stability muss nicht Performative Optimality entsprechen. |
| **Huang, X. A., Tharas, C., Marro, S., Truong, V. Q., Schölkopf, B., La Malfa, E., & Jin, Z. (2026). Mechanism design is not enough: Prosocial agents for cooperative AI.** arXiv:2605.08426. https://arxiv.org/abs/2605.08426 citeturn19academia49 | Bereits im Draft, aber korrekt als Schranke externer Mechanismen zu behandeln. Stand August 2026 ist dies ein sehr neuer Preprint; seine Generalität sollte nicht über die konkret modellierte Klasse hinaus behauptet werden. |
| **Chassang, S. (2026). Interactive alignment.** arXiv:2607.25019. https://arxiv.org/abs/2607.25019 citeturn20view0 | **Unbedingt ergänzen.** Direkte AI-Prior-Art: Alignment interagierender AI-Agenten unter evolutionärer Reproduktion, Mutation, deterministischer und stochastischer Stabilität; Konstitutionen werden gezielt auf langfristige Alignment-Robustheit untersucht. |
| **Harris, K. D. (2026). A mathematical theory of evolution for self-designing AIs.** arXiv:2604.05142. https://arxiv.org/abs/2604.05142 citeturn20view1 | Direkte Prior-Art zu \(Q\) für AI-Systeme. Besonders wichtig, weil Nachfolgervariation nicht zufällig, sondern strategisch gerichtet sein kann und Fitness nicht mit menschlichem Nutzen übereinstimmen muss. |
| **Kulveit, J., Douglas, R., Ammann, N., Turan, D., Krueger, D., & Duvenaud, D. (2025). Position: Humanity faces existential risk from gradual disempowerment. *Proceedings of ICML 2025, PMLR 267*.** https://proceedings.mlr.press/v267/kulveit25a.html citeturn19search1 | Relevante Anwendung gekoppelter ökonomischer, politischer und kultureller Selection Dynamics. Unterstützt die Motivation, dass \(\theta\) auf gesellschaftlicher Ebene endogen und verteilt ist. |
| **Holling, C. S. (1973). Resilience and stability of ecological systems. *Annual Review of Ecology and Systematics, 4*, 1–23.** DOI: https://doi.org/10.1146/annurev.es.04.110173.000245 citeturn14search0 | Fundamentale Gegenfolie zu „mehr Stability ist immer besser“. Mehrere Regime, Basin-Größe und Resilience sprechen dafür, Alignment als robuste Region beziehungsweise Ecology statt als singuläres Gleichgewicht zu denken. |

Die Literatur ergibt damit eine relativ präzise Positionierung des Manuskripts: **Die Einzeloperationen sind weitgehend etabliert; die plausible eigenständige Leistung liegt in der Vereinigung von evolutionary implementation, robust/invariant-set reasoning, mutation/reconstruction, invasion analysis und endogener Selector-Dynamik zu einem expliziten Construction-Test für ein semantisch vorab festgelegtes Alignment-Ziel.** Gerade diese engere Positionierung dürfte wissenschaftlich stärker sein als die gegenwärtige Behauptung, Construction sei im Allgemeinen „explicit symmetry breaking“. fileciteturn0file0