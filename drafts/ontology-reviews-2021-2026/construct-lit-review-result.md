# Konstruierbare Teile sozio-technischer Kontrollsysteme für fortgeschrittene KI

Stand: August 2026.

Der zentrale Befund ist enger, aber belastbarer, als die üblichen „Governance“- oder „Alignment-by-design“-Formulierungen suggerieren. **Wir können bereits mehrere Teile eines Kontrollsystems konstruieren**, sofern die gewünschte Eigenschaft \(D\) auf einer Schnittstelle liegt, die hinreichend beobachtbar, vertraglich beschreibbar, technisch kontrollierbar und institutionell durchsetzbar ist. Wir können etwa festlegen, wer einen Schlüssel benutzen darf, welche Binärdatei bootet, wer ein Produkt legal verkaufen darf, welche Nash-Gleichgewichte ein Mechanismus besitzt oder welche C-Implementierung eine formale Spezifikation verfeinert. Was wir nicht allgemein können, ist aus denselben Werkzeugen ableiten, dass ein semantisch reiches Ziel wie „verhält sich in allen relevanten zukünftigen Situationen gut“ erreicht wurde.

Die entscheidende Trennlinie ist daher nicht „technisch versus sozial“, sondern:

\[
\boxed{\text{Konstruktion wird stark, wenn }D\text{ an eine kontrollierbare, unterscheidbare Grenze gekoppelt werden kann.}}
\]

Wenn dagegen erwünschte und unerwünschte Zustände an dieser Grenze gleich aussehen, kann weder ein Vertrag noch ein Token-Vote, ein TEE, ein zk-Beweis, ein stärkerer Selektor oder ein formal verifizierter Compiler die fehlende Unterscheidung erzeugen.

## Executive summary

- **[proved / historical] Payoffs, Zulassung und Auswahl \(f,\theta,E,H\) sind konstruierbar.** Steuern, Kautionen, Lizenzpflichten, Versicherungsnachweise, Procurement-Regeln oder Zulassungen können eine Aktion tatsächlich von einem Gate abhängig machen. FAA-Airworthiness-Zertifikate autorisieren den Flugbetrieb; bestimmte US-Luftfahrtunternehmen müssen Versicherungsnachweise hinterlegen; neue Arzneimittel benötigen einen FDA-Marktzugangspfad. Das funktioniert, wenn ein kontrollierbarer Engpass existiert, die sanktionierende Instanz Jurisdiktion besitzt und Umgehung hinreichend teuer ist. citeturn21search2turn21search26turn21search19

- **[historical] Unabhängige Korrektoren \(C\) können organisatorisch konstruiert werden.** Der Energy Reorganization Act von 1974 trennte die amerikanische Atomförderung von der unabhängigen Regulierung: Die AEC verschwand, die NRC erhielt Lizenzierungs- und Regulierungsaufgaben, während Förderung/Forschung anderswo lagen. Nach Enron wurden mit Sarbanes–Oxley und dem PCAOB ebenfalls Interessenkonflikte des Auditorenmodells institutionell angegriffen. Das konstruiert Mandatstrennung; es beweist nicht dauerhaft fehlende Capture. citeturn0search1turn0search28turn0search5

- **[standard / historical] Stopps, Vetos, Schwellen und Verzögerungen \(H\) sind besonders gut konstruierbar, wenn die geschützte Ressource technisch unter dem Handle liegt.** Threshold-Kryptographie kann \(k\)-von-\(n\)-Zustimmung für Schlüsseloperationen erzwingen; ein Timelock kann eine Mindestwartezeit vor einer privilegierten Transaktion erzwingen; Maker implementierte einen Emergency-Shutdown-Mechanismus. Das funktioniert nicht, wenn ein alternativer Pfad am Handle vorbeiführt oder die Reaktionszeit länger als der Schadenshorizont ist. citeturn24search9turn24search0turn10search4

- **[standard / historical] Vererbungshebel \(L\) sind teilweise konstruierbar.** Copyleft kann rechtliche Pflichten an Distribution modifizierter Software koppeln. GPLv3 §6 verlangt bei bestimmten „User Products“ zusätzlich Installationsinformationen und reagiert damit gerade auf die Klasse von „tivoization“-Fällen, in denen Quellcode verfügbar bleibt, das Gerät aber modifizierte Software kryptographisch ablehnt. Netzwerkdienste zeigen umgekehrt, dass ein Distribution-Trigger nicht automatisch jede Nutzung einer Ableitung erfasst. citeturn6search15turn6search16turn6search6turn6search9

- **[proved] Spiele und Mechanismen \(f,\theta\) können unter formalisierten Voraussetzungen konstruiert werden.** Maskin zeigt konstruktiv: Bei mindestens drei Akteuren sind Monotonizität plus No-Veto-Power hinreichend für Nash-Implementierung einer Social-Choice Rule. Sandholm geht einen für diese Frage noch wichtigeren Schritt und konstruiert unter Konkavitäts- und Dynamikannahmen Preisschemata, unter denen effiziente Zustände global attraktiv werden. Das ist echte Konstruktion im hier verlangten Sinn, aber relativ zu einer festgelegten Zustands-, Payoff- und Dynamikklasse. citeturn18search1turn20view1

- **[proved] Es existieren harte Grenzen dieser Konstruktion.** Gibbard–Satterthwaite schränkt nichtmanipulierbare allgemeine Abstimmungsregeln drastisch ein; Myerson–Satterthwaite zeigt im bilateralen Handel eine Inkompatibilität von ex-post Effizienz, Incentive Compatibility und Individual Rationality ohne geeignete externe Subventionierung; Huang et al. zeigen 2026 in ihrem Modell, dass bei „incontractible cells“ ein positiver Wohlfahrtsabstand für jedes zulässige Mechanismusdesign verbleibt. citeturn18search0turn20view0turn3view0

- **[proved / standard] Records \(R\) und Verifier \(V\) sind stark konstruierbar, aber nur propositionsrelativ.** seL4 beweist maschinengeprüft Refinement von Implementierung zu Spezifikation; CompCert beweist semantische Erhaltung durch den Compiler; Attestation kann eine gemessene Software-/Hardwarekonfiguration an eine Vendor-Vertrauenskette binden; Zero-Knowledge-Beweise können die Gültigkeit einer definierten Aussage beziehungsweise Berechnung nachweisen. Keines davon erzeugt aus einer unvollständigen Spezifikation eine vollständige. citeturn14search8turn14search29turn12search2turn24search2

- **[empirical / agenda] KI-spezifische Trainings- und Deploymentprotokolle können bereits engere Teile \(Q,f,\theta,H\) bauen, nicht die allgemeine semantische Zielregion.** Constitutional AI/RLAIF verändert Training und Reward-Signal und zeigt empirische Verhaltensänderungen; AI Control baut in einem konkreten Coding-Testbed Filter-/Monitoring-Protokolle, die die Backdoor-Rate gegenüber Baselines reduzieren. Guaranteed/Safeguarded AI dagegen ist gegenwärtig eine Architekturagenda aus Weltmodell, Spezifikation und Verifier, nicht der Nachweis eines allgemeinen End-to-End-Builders. citeturn15search6turn15search23turn15search0turn15search21

Der robuste gemeinsame Nenner lautet damit: **Wir können Regeln an Grenzen bauen; wir können nicht durch das Benennen einer Grenze die Semantik hinter ihr konstruieren.**

## Negatives

**Geschriebene Verträge. — [proved / standard]** Ein Vertrag konstruiert Verhalten nur, soweit relevante Zustände, Handlungen oder Beweise *contractible* sind. Die Incomplete-Contracts-Literatur behandelt gerade den Fall, dass nicht alle zukünftigen Kontingenzen sinnvoll vorab vertraglich beschrieben und durchgesetzt werden können; Eigentums- und Residualrechte verteilen dann Entscheidungsmacht über die Lücken. citeturn2search0turn2search2 Huang et al. verschärfen dies für einen expliziten Mechanismusraum: Die Spezifikationssprache erzeugt eine Partition \(\mathcal P\) des Zustandsraums \(\Omega\). Liegen in derselben beobachtbaren Zelle Zustände, die unterschiedliche erstbeste Aktionen verlangen, und kann kein zulässiger Mechanismus diese Zustände auseinanderhalten, bleibt unter ihrer „strict incontractibility“-Annahme

\[
\Delta(M)>0 \qquad \forall M
\]

und sogar ein strikt positiver unterer Wohlfahrtsabstand über alle zulässigen Mechanismen. Das ist **[proved]**, allerdings nur innerhalb dieses Modells; es wäre für KI idle, wenn die relevante Sprache tatsächlich alle sicherheitsrelevanten Unterschiede ausdrücken könnte oder zusätzliche Outcomes/Transfers die Zellen separierten. citeturn3view0turn3view3

**Coin voting. — [proved + empirical]** Ein Token-Vote konstruiert sehr zuverlässig die Eigenschaft „Stimmgewicht folgt dieser Token-/Delegationsregel“. Er konstruiert nicht automatisch „fair“, „nicht gefangen“, „gemeinwohlorientiert“ oder „wahrheitsgemäß“. Gibbards Resultat zeigt bereits im abstrakteren Social-Choice-Fall, wie restriktiv universelle Strategy-Proofness ist. Neuere DAO-Datensätze finden zusätzlich wiederkehrende Konzentration von Stimmrechten und einen Zusammenhang zwischen Delegations-/Stakingstrukturen und Machtkonzentration. Optimism begründete seine Citizens’ House explizit als Gegengewicht zu reinem Token-Voting. citeturn18search0turn11search4turn11search7turn22search3 Ein Token-Vote ist deshalb ein konstruierter **Selector \(\theta\)**, keine konstruierte Sozialwohlfunktion.

**TEEs, Ledgers und Beweise. — [standard / empirical]** Ein Ledger kann Transaktionsreihenfolge und Zustandsübergänge gegen bestimmte Fälschungen absichern; Attestation kann zeigen, welche gemessene Konfiguration unter einer Zertifikatskette lief; ein zk-Beweis kann zeigen, dass eine formale Relation erfüllt ist. Das jeweilige \(D\) lautet dann etwa „dieser State Transition entspricht diesem Programm“ oder „dieser Measurement-Wert wurde von einer akzeptierten Vertrauenskette attestiert“. Es lautet nicht „die ausgeführte Handlung war gesellschaftlich erwünscht“. AMD-SEV-SNP-Verifikation bindet beispielsweise an AMD-Zertifikatsketten; TDX hat entsprechende Attestation-Infrastruktur. Reale SGX-, TDX- und SEV-Sicherheitslücken zeigen außerdem, dass die Hardware- und Firmwareannahmen selbst angreifbar bleiben. citeturn12search2turn12search3turn13search0turn13search2turn13search23

**Auf eine Katastrophe warten. — [proved by model conditions, not a universal impossibility]** Selektion durch Scheitern ist nur dann ein brauchbarer Konstrukteur, wenn schlechte Varianten wiederholt ausprobiert, zuverlässig erkannt und entfernt werden können, bevor das System irreversibel verloren ist. Sandholms positives Resultat ist hier aufschlussreich: Konvergenz entsteht nicht durch „mehr Wettbewerb“ allein, sondern durch eine spezifische Payoff-Transformation und eine Klasse payoff-monotoner Anpassungsdynamiken; ohne Potentialstruktur müssen die ursprünglichen Dynamiken gerade nicht konvergieren. citeturn19view1turn20view1 Ein einmaliger globaler oder irreversibler KI-Fehler liefert dagegen möglicherweise Information, aber keinen zweiten Selektionsschritt. „Katastrophe als Feedback“ ist unter diesen Bedingungen keine Konstruktion.

**Einen indiscriminaten Selector verstärken. — [proved in the stated model]** Kann der Selektor erwünschte Zustände und unerwünschte Lookalikes nicht unterscheiden, erhöht stärkerer Selektionsdruck nur den Druck auf die beobachtbare Äquivalenzklasse. Huang et al. formulieren genau einen solchen Fall: Wenn First-Best und eine Defektionshandlung denselben verifizierbaren Record erzeugen, fehlt dem Mechanismus die Evidenz zur unterschiedlichen Behandlung. citeturn3view3 Das ist die präzisere Fassung des häufig unscharf verwendeten „Goodhart“-Arguments: Das Problem ist nicht „zu viel Optimierung“, sondern fehlende Identifizierbarkeit relativ zu \((R,V,f,\theta)\).

## Master table

„Idle for AI“ bedeutet hier nicht „falsch“, sondern: Die Konstruktion bleibt formal oder historisch richtig, greift aber nicht auf das KI-Problem durch, wenn die genannte Voraussetzung ausfällt.

| Source | Part | Acts on | Strength | Idle for AI if… | Bucket |
|---|---|---:|---|---|---:|
| Cox, Arnold & Villamayor-Tomás zu Ostrom citeturn0search21turn0search24 | robuste CPR-Regeln / Genesis | f, E, S, C | **empirical** | Ressourcen- und Nutzergrenzen unklar sind; Monitoring/Legitimität fehlen; Geschwindigkeit lokale Anpassung überholt | **3** |
| AEC → NRC/ERDA-Split citeturn0search1turn0search28 | unabhängiger Corrector | C, θ, E, H | **historical** | Regulator keinen Engpass kontrolliert, abhängig finanziert ist oder Promotion de facto zurückkehrt | **1** |
| Enron/Andersen → SOX/PCAOB citeturn0search5 | externe Aufsicht / Interessenkonflikt-Trennung | C, θ, E | **historical** | Prüfer/promoter weiterhin ökonomisch identisch sind oder Aufsicht nur Berichte erzeugt | **1** |
| Acemoglu & Robinson, *Persistence of Power* citeturn21search0turn21search4 | Grenze de-jure-Reform | S, C, E | **proved** | de-facto Macht nicht endogen reagiert – dann ist das Negativ weniger relevant | **4** |
| GPLv3 §6 / Tivoization-Reaktion citeturn6search15turn6search6 | Vererbungshebel + Nutzer-Handle | Q, L, H, E | **standard / historical** | Kopie außerhalb des Lizenztriggers liegt, Durchsetzung fehlt oder Gewichte nicht als erfasste Ableitung gelten | **1** |
| FAA Airworthiness + Carrier Insurance citeturn21search2turn21search26 | Betriebs-/Versicherungsgate | θ, E, H, f | **historical** | Betrieb illegal/offshore leicht möglich ist oder Zertifikat nicht an tatsächlichen Betrieb gebunden bleibt | **1** |
| FDA NDA-Marktzugang citeturn21search19turn21search3 | Verkaufsselector | θ, E, H | **historical** | Modellkopien ohne regulierten Vertriebskanal verbreitet werden können | **1** |
| Gibbard 1973 citeturn18search0 | Grenze strategy-proof voting | θ, S | **proved** | Präferenzdomäne stark eingeschränkt oder ≤2 relevante Outcomes bestehen | **4** |
| Maskin 1999 citeturn18search1turn18search13 | Nash-Implementierung | f, θ, V | **proved** | Zustands-/Präferenzmodell falsch ist, <3 Agenten, Monotonizität/No-veto fehlen oder Nash kein plausibles Verhaltensmodell ist | **1** |
| Myerson–Satterthwaite 1983 citeturn20view0 | Trade-off IC/IR/Effizienz | f, θ | **proved** | Informations- oder Subventionsannahmen entfallen | **4** |
| Sandholm 2005 citeturn19view1turn20view1 | dynamisch konvergierende Payoffs | f, θ | **proved** | Konkavität, Separierbarkeit oder payoff-monotone Anpassung scheitern | **1** |
| Grossman–Hart 1986 citeturn2search0 | Residualrechte bei unvollständigen Verträgen | f, L, S | **proved / standard** | alle relevanten Kontingenzen tatsächlich vollständig vertraglich spezifizierbar sind | **4** |
| Huang et al. 2026 citeturn2search3turn3view0 | Incontractibility-Grenze | f, θ, V, R | **proved** | Sprache/Beweise relevante Zustände separieren oder der zulässige Mechanismusraum erweitert wird | **4** |
| The DAO / SEC Report citeturn9view1turn7search1 | Governance-Fail + Fork | R, S | **historical** | — der Fall zeigt gerade die Differenz zwischen Code-Ausführung und D | **4** |
| Maker Emergency Shutdown citeturn10search0turn10search4 | bindender Notstopp | H, f, θ, R | **historical** | relevante Assets/Aktionen außerhalb der Settlement-Logik liegen oder Governance zu langsam ist | **1** |
| Optimism bicamerale Governance citeturn22search1turn22search3 | Gegen-Veto zu Token House | θ, H, S | **historical; agenda für capture-resistance** | Houses korreliert/captured sind oder Veto nicht bindend ausgeführt wird | **1** für Mechanik; **5** für Fairnessclaim |
| Arbitrum AIP-1 → AIP-1.1 citeturn22search16turn22search4 | Fail + Budget-/Vesting-Handle | θ, H, S, R | **historical** | Foundation Ressourcen außerhalb DAO-kontrollierter Streams halten kann | **4→1** |
| DAO-Machtkonzentration, 48–100 DAOs citeturn11search4turn11search7 | Grenze tokenbasierter Selector | θ, S | **empirical** | Identitäts-/Delegationsmechanismen diese Konzentration tatsächlich verhindern | **4** |
| NIST Threshold Cryptography citeturn24search9 | Schwellenzustimmung | H, R | **standard** | Schwellenkoalition kolludiert oder alternative privilegierte Pfade bestehen | **1** |
| OpenZeppelin Timelock citeturn24search0 | verbindliche Verzögerung | H, E | **standard** | Schadenszeit < Delay/Reaktionszeit oder Aktion umgeht Timelock | **1** |
| Remote attestation: SEV-SNP/TDX citeturn12search2turn12search3 | Nachweis gemessener Konfiguration | R, V | **standard** | Vendor root, Firmware, Measurement oder Hardwaremodell kompromittiert ist | **2** |
| Foreshadow / neuere TEE-Advisories citeturn13search0turn13search2turn13search23 | Grenze des TEE-Modells | E, R, V | **empirical** | Angriffsklasse aus dem Threat Model ausgeschlossen und Hardware gepatcht ist | **4** |
| seL4 citeturn14search8turn14search20 | Implementierung erfüllt formale Kernel-Spec | V, E | **proved** | Spezifikation nicht D erfasst oder Trusted Base/Hardwareannahmen falsch sind | **1** |
| CompCert citeturn14search1turn14search29 | Compiler-Semantik-Erhaltung | V, Q | **proved** | Quellprogramm/Semantik bereits falsch spezifiziert ist | **1** |
| DO-178C/DO-333; Common Criteria citeturn14search22turn14search7turn14search19 | Assurance-/Certification-Regime | R, V, θ | **standard** | Zertifikat nicht an ein Gate gekoppelt ist oder geprüfte Claims D nicht abdecken | **2/3** |
| Guaranteed/Safeguarded AI citeturn15search0turn15search21 | Weltmodell + Spec + Verifier | V, E, H | **agenda** | reale Welt außerhalb Modellabdeckung liegt oder kein end-to-end zertifizierter Controller entsteht | **5** |
| Constitutional AI/RLAIF citeturn15search6turn15search2 | Trainingsintervention | Q, f, θ | **empirical** | „D“ als vollständige Einhaltung der Constitution statt als gemessene Verhaltenseffekte verstanden wird | **1** für Proxy; **5** für starken Claim |
| AI Control, Greenblatt et al. citeturn15search23turn15search7 | Deploymentfilter gegen Backdoors | θ, H, R | **empirical** | Angreifer außerhalb des getesteten Threat Models liegt oder Monitoring nicht skaliert | **1** im Testbed |
| Frontier-Licensing, Anderljung et al. citeturn17search1 | vorgeschlagenes Entwicklungs-/Deploymentgate | θ, H, C | **agenda** | regulatorischer Engpass nicht kontrolliert wird oder Copies/Compute ausweichen | **3/5** |
| Mandatory frontier-AI insurance, Trout/Stetler citeturn23academia35turn23search18 | vorgeschlagenes Kapital-/Deploymentgate | f, θ, C, H | **agenda** | Tail risk nicht versicherbar/preisbar ist oder Versicherung nicht obligatorisch ist | **3/5** |
| BIS advanced-compute controls citeturn16search6turn16search2 | realer Compute-/Export-Selector | θ, E, H, R | **historical** | Compute substituierbar, geschmuggelt, lokal hergestellt oder außerhalb Jurisdiktion verfügbar ist | **1** |

Zwei Begriffsfallen sind dabei besonders wichtig. **[standard]** Ein *contract* im Mechanism Design ist eine zustands-/nachrichtenabhängige Allokations- und Transferregel; ein juristischer Vertrag ist ein durch Gerichte und Rechtsnormen ergänztes Instrument; ein *smart contract* ist ausführbarer Code. Ebenso ist *verification* in seL4/CompCert eine mathematische Relation zu einer formalen Spezifikation, während Common-Criteria- oder DO-178C-*verification* Teil eines Assurance-/Zertifizierungsprozesses sein kann. Gleiches englisches Wort, anderes Objekt. citeturn14search29turn14search22turn14search19

## Institutions cluster

**Genesis und lokale Regelbildung — [empirical].** Ostroms Designprinzipien sind besser als empirisch gestützte Randbedingungen für institutionelle Robustheit zu lesen denn als Rezept. Cox, Arnold und Villamayor-Tomás überprüften 91 einschlägige Studien und fanden breite Unterstützung für einen großen Teil der Prinzipien, zugleich aber theoretische und Operationalisierungsprobleme. citeturn0search21turn0search24 Für „Constructibility“ ist das wichtig: robuste Institutionen entstehen eher, wenn Ressourcengrenzen und Teilnehmerkreis bestimmbar sind, Nutzer an Regeländerungen beteiligt sind, Monitoring vorhanden ist und Konflikte/schrittweise Sanktionen institutionell verfügbar sind. Das ist **[empirical]**, keine Garantie dafür, dass dieselbe Form bei hochgradig kopierbarer und millisekundenschneller KI funktioniert.

Der allgemeinere konstitutionelle Punkt aus Buchanan-, Exit/Voice-, Principal-Agent- und Capture-Literaturen ist nützlich, aber nicht als Builder-Theorem: Man muss nicht nur Regeln für das kontrollierte Objekt betrachten, sondern auch Regeln für die Auswahl, Finanzierung und Ersetzbarkeit des Kontrolleurs. Die für diese Review belastbarere Konstruktionsevidenz liefern deshalb konkrete Gate- und Mandatfälle, nicht das Wort „Governance“.

**Dual mandate — [historical].** Der AEC/NRC-Fall ist ein echtes Bauprojekt. Vorher waren Förderung/Entwicklung und Sicherheitsregulierung im selben institutionellen Komplex angesiedelt; der Energy Reorganization Act von 1974 schaffte die AEC ab und verteilte Funktionen unter anderem auf die NRC und ERDA. Die NRC erhielt regulatorische und Lizenzierungsaufgaben. citeturn0search1turn0search28 Das konstruierte \(C\): Die Personengruppe, die einen Reaktor fördern sollte, war organisatorisch nicht mehr identisch mit der Instanz, die ihn zulassen sollte.

Das ist allerdings keine **proved** Unabhängigkeit. Eine getrennte Behörde kann über Personalrotation, Information, Budget oder Politik weiter endogenisiert werden. Acemoglu und Robinsons Modell liefert dafür eine formale Warnung: Eine Änderung von *de jure* Macht kann Investitionen in *de facto* Macht auslösen, welche die formale Reform teilweise oder vollständig neutralisieren. citeturn21search4 Für KI wäre ein „unabhängiger AI regulator“ daher erst dann ein konstruierter \(C\), wenn Mandat, Entscheidungskompetenz, Finanzierung und tatsächlicher Gate-Zugriff getrennt sind; ein eigener Briefkopf genügt nicht.

**Auditoren und unabhängige Correctors — [historical].** Der Arthur-Andersen/Enron-Fall illustriert dieselbe Struktur aus einer anderen Branche. PCAOB-Dokumente halten den Konflikt zwischen Auditfunktion und profitablen Beratungs-/Transaktionsbeziehungen fest; Sarbanes–Oxley reagierte mit einer neuen externen Aufsichtsstruktur und Unabhängigkeitsregeln. citeturn0search5 Auch hier lautet das konstruierte \(D\) nicht „Audits sind wahr“, sondern enger: bestimmte Prüfungsfunktionen werden einer separaten, gesetzlich autorisierten Aufsicht unterworfen und bestimmte Interessenkonflikte verboten.

**Inheritance und tivoization — [standard / historical].** Copyleft zeigt, dass \(L\) real sein kann, sofern das Recht einen erkennbaren Transformations-/Distributionsvorgang erfasst. Der interessante negative Fall ist tivoization: Ein Hersteller kann Nutzer mit dem Quelltext versorgen und dennoch über Signaturschlüssel verhindern, dass deren modifizierter Code auf dem gekauften Gerät läuft. GPLv3 reagiert nicht mit einer „besseren Absichtserklärung“, sondern mit einem zusätzlichen, operationalisierbaren Lieferobjekt: „Installation Information“ für bestimmte User Products. citeturn6search15turn6search6

Der Fall zeigt zugleich die Grenze. **[standard]** Ein Lizenztrigger bindet nur das, was unter seine juristisch definierten Handlungen fällt. Ein Dienst, der modifizierte Software serverseitig ausführt, ist nicht dasselbe wie Distribution an einen Nutzer; die AGPL erweitert deshalb gerade den Trigger in Richtung Netzwerkinteraktion. citeturn6search9 Für Modellgewichte wären ähnliche Fragen unvermeidbar: Ist Fine-Tuning eine Ableitung? Distillation? API-only serving? Rekonstruktion aus Outputs? Ein \(L\), der diese Transformationen nicht unterscheidet, ist kein vererbter Sicherheitsmechanismus.

**Decay versus refresh — [proved + historical].** „Reform wurde einmal verabschiedet“ ist keine dauerhaft konstruierte Eigenschaft, wenn der politische Selektor selbst endogen ist; Acemoglu–Robinson liefern dafür das formale Gegenmodell. citeturn21search0 Institutionen mit fortlaufender Revalidierung zeigen die Gegenstrategie: Lloyd’s Register formuliert Regeln nicht nur für Konstruktion, sondern auch für lifetime maintenance; FAA-Airworthiness bleibt an fortdauernde Übereinstimmung mit Type Design, sicheren Zustand und regelkonforme Wartung gebunden. citeturn21search1turn21search18 Das ist ein echter struktureller Unterschied zwischen „einmal zertifiziert“ und einem fortbestehenden Gate.

Ich würde deshalb zwei der vorgeschlagenen historischen Analogien **nicht** als load-bearing Evidenz verwenden. Die Kette „Glass–Steagall repeal \(\rightarrow\) Finanzkrise 2008“ ist für diese konkrete Konstruktionsfrage zu kausal überladen; ebenso ist „Marian reforms \(\rightarrow\) private militärische Macht \(\rightarrow\) Fall der Republik“ zu grob, um daraus ein Builder-Theorem abzuleiten. Als Analogien mögen beide anregend sein; in der Klassifikation hier wären sie Bucket **5**, nicht Beweise.

**Insurance und licensing gates — [historical].** Die stärkste Form ist nicht „ein Versicherer veröffentlicht einen Risk Score“, sondern

\[
\text{legal deployment} \Rightarrow \text{coverage},
\]

wobei der Versicherer eigenes Kapital verliert, wenn seine Risikoselektion schlecht ist. US-Air-Carrier müssen in relevanten Kategorien Versicherungsnachweise hinterlegen; der FAA-Betrieb hängt zugleich an Airworthiness-Anforderungen. citeturn21search2turn21search26 Ähnlich erlaubt ein FDA-Zulassungsregime nicht bloß eine Bewertung eines neuen Arzneimittels, sondern kontrolliert einen Marktzugangspfad. citeturn21search19 Der konstruktive Teil ist \(\theta/H\), nicht die epistemische Behauptung, die Behörde oder Versicherung könne alle Schäden vorhersehen.

## Mechanism-design cluster

Mechanism Design liefert die formal saubersten positiven **und** negativen Ergebnisse dieser gesamten Review, gerade weil es die gewünschte Region \(D\), den zulässigen Mechanismus \(I\) und die Lösungskonzeption explizit macht. Gleichzeitig sind seine Aussagen besonders leicht zu überdehnen.

**Nash implementation — [proved].** Maskins Objekt ist eine Social Choice Rule \(F\), die für jeden Präferenzzustand eine Menge gewünschter Outcomes festlegt. Vollständige Nash-Implementierung verlangt grob

\[
\operatorname{Outcome}\!\left(NE(M,\omega)\right)=F(\omega)
\]

für jeden modellierten Zustand \(\omega\). Das bedeutet nicht, dass ein einziges Gleichgewicht existiert; es bedeutet, dass alle Nash-Gleichgewichtsoutcomes in der gewünschten Menge liegen und die gewünschten Outcomes als Gleichgewichte erreichbar sind. Für mindestens drei Personen sind Monotonizität und No-Veto-Power hinreichend; Maskins Beweis ist konstruktiv. citeturn18search1turn18search5

Das ist echte Konstruktion des Teils \(f/\theta\). Für KI wird das Resultat **idle**, wenn „Typen“ oder relevante Zustände nicht in der Modellmenge liegen, wenn Akteure Koalitionen bilden, die das Nash-Konzept nicht modelliert, wenn Kommunikation/Verträge nicht die vorgesehenen Nachrichtenräume tragen oder wenn die tatsächliche Dynamik das gewünschte Gleichgewicht nicht erreicht. „Nash-implementierbar“ bedeutet insbesondere nicht „wird durch Lernen sicher dorthin konvergieren“.

**Dynamische Implementierung — [proved].** Genau deshalb ist Sandholms Resultat besonders relevant. Der Planer beobachtet Aggregate, nicht individuelle Typen, und verändert Aktionspayoffs durch ein Preisschema. Unter einer konkaven totalen common-payoff-Funktion und einer breiten Klasse „admissible“ payoff-monotoner Anpassungsdynamiken wird die Menge effizienter Bevölkerungszustände ein globaler Attraktor. Die Intervention verändert also \(f\), und danach existiert ein mathematischer Konvergenzcheck. citeturn19view1turn20view1

Das ist fast ein Musterbeispiel für die vorgegebene Definition von Konstruktion. Es zeigt zugleich, warum „mehr Selection Pressure“ nicht dasselbe ist: Sandholm muss die **Geometrie der Payoffs** so verändern, dass ein Potential entsteht; ohne diese Struktur können die ursprünglichen evolutionären Dynamiken nicht konvergieren. citeturn19view1 Für KI wäre das Resultat stark, wenn man \(F\), Aggregate und relevante Aktionen tatsächlich beobachtbar machen könnte. Genau diese Voraussetzung ist meist die offene Frage.

**Strategy-proofness — [proved].** Gibbards Manipulationsresultat schließt die Hoffnung aus, auf einer unbeschränkten Präferenzdomäne einfach einen reichhaltigen, deterministischen, nichtdiktatorischen Wahlmechanismus zu wählen, für den strategisches Misreporting grundsätzlich verschwindet. citeturn18search0 Der „Revelation Principle“-Gedanke sollte davon getrennt werden: Direkte wahrheitsgemäße Mechanismen können häufig ohne Verlust an erreichbaren Gleichgewichtsoutcomes betrachtet werden, aber daraus folgt weder, dass Wahrheit das einzige Gleichgewicht ist, noch dass die zugrunde liegenden Typen semantisch vollständig erfasst wurden.

**Budget-, Teilnahme- und Effizienzgrenzen — [proved].** Myerson und Satterthwaite untersuchen den minimalen Fall eines Verkäufers, eines Käufers und eines unteilbaren Gutes mit privater Information. Sie zeigen, dass in ihrer privaten Informationsumgebung ex-post effiziente Allokation im Allgemeinen nicht zugleich mit Bayesian Incentive Compatibility und Individual Rationality ohne den relevanten Finanzierungsspielraum erreicht werden kann. citeturn20view0 Deshalb ist „VCG benutzen“ keine universelle Antwort auf KI-Governance: Transfers, Budget, Participation Constraints, Information und Verifizierbarkeit sind Teil des Problems, nicht kostenlose Primitive.

**Incomplete contracting — [proved / standard].** Grossman–Hart verschieben bei nicht vollständig vertraglich spezifizierbaren Kontingenzen die Aufmerksamkeit auf Eigentums- und Residualkontrollrechte. citeturn2search0 Das ist gerade kein Beweis, dass „ein besserer Vertrag“ alle Lücken schließt. Für fortgeschrittene KI wäre ein Vertrag, der „handle unforeseen harmful cases appropriately“ enthält, semantisch keine Konstruktion, solange eine Gerichtsbarkeit, ein menschlicher Corrector oder eine andere Institution die Lücke nicht ex post konkretisiert.

**Incontractible cells — [proved].** Huang et al. liefern die am direktesten passende moderne Negativform. Ein Mechanismus darf nur auf die Zelle der vorgegebenen Spezifikationspartition reagieren. Eine Zelle ist incontractible, wenn kein einzelnes Aktionsprofil über die ganze Zelle first-best ist; unter ihrer strengeren Incontractibility-Bedingung gibt es positive Masse von Zuständen, in denen für jeden zulässigen Mechanismus die gewünschten First-Best-Aktionen nicht als relevante Nash-Outcomes implementiert werden können. Daraus folgt ein strikt positiver Welfare Gap. citeturn3view0

Das ist kein Theorem „Alignment ist unmöglich“. Es besagt etwas präziseres und nützlicheres:

\[
\text{fehlende Sprache} + \text{verhaltensrelevante Aliasing-Zellen}
\;\not\Rightarrow\;
\text{durch cleverere Incentives reparierbar}.
\]

Der Fail-Test ist klar: Findet man zwei relevante Zustände mit derselben verifizierbaren Evidenz, aber notwendigerweise verschiedenen gewünschten Aktionen, ist der Mechanismus relativ zu dieser Sprache nicht konstruktiv vollständig. citeturn3view3

**Robust mechanism design — [proved / standard].** Die Wilson-/Bergemann–Morris-Linie reagiert auf eine weitere fragile Voraussetzung klassischer Mechanismen: sehr starke Common-Knowledge-Annahmen über Typen und Informationsstrukturen. Robustere Mechanismen verlangen weniger davon, typischerweise zum Preis einer kleineren implementierbaren Menge oder schwächerer Performance. citeturn4search15turn4search21 Für KI ist diese Literatur deshalb eher eine Warnung gegen die Annahme „wir kennen das Agentenmodell“ als ein universeller Builder.

## DAO/crypto cluster

Die DAO-Literatur ist besonders nützlich, weil sie \(R\), \(H\), \(\theta\) und \(S\) physisch beziehungsweise kryptographisch auseinanderzieht. Ein Smart Contract kann eine enge Regel extrem zuverlässig bauen; die soziale Ordnung, die Menschen mit dieser Regel verbinden, kann trotzdem eine andere sein.

| Fall | Vorab intendiertes \(D\) | Tatsächliche Maschine | Social-layer \(S\)? | Ostrom-artiges Monitoring / graduated sanctions? | Urteil |
|---|---|---|---|---|---|
| **The DAO, 2016** | Tokenholder kontrollieren einen gemeinschaftlichen Investment-/Treasury-Prozess | Solidity-Verträge und Ethereum-State-Transition; ein rekursiver/reentrancy-artiger Exploit leitete rund 3,6 Mio. ETH in einen „child DAO“ um | **Ja.** Ethereum änderte durch Hard Fork den Zustand; eine Minderheit blieb auf Ethereum Classic | Code/Chain überwachten Transaktionen; kein wirksames abgestuftes Sanktionssystem gegen die ausgenutzte Verhaltensklasse | **[historical] Fail von D; R funktionierte** citeturn9view1turn7search1 |
| **MakerDAO** | DAI-System innerhalb definierter Collateral-/Settlement-Regeln stabilisieren; letzter Notstopp verfügbar | Vaults, Preis-/Liquidationslogik und ein explizites Emergency-Shutdown-System | Governance ist soziale Eingabe, aber der Shutdown selbst ist ein gebautes on-chain \(H\), kein nachträglicher Chain-Fork | Starke maschinelle Positionsüberwachung; Liquidation ist eine finanzielle Sanktion, aber keine Ostrom’sche gestufte Sanktion von Gouverneuren | **[historical] echter H/f-Baustein** citeturn10search0turn10search4 |
| **Optimism** | Ökonomische Tokeninteressen und langfristige menschliche Interessen durch zwei Houses balancieren | Token House: OP-Holder/Delegates; Citizens’ House: personengebundene Citizenship; im 2023-Design Vetorechte und teils manuelle Foundation-Ausführung | **Ja.** Insbesondere frühe Upgrade-Ausführung war explizit durch die Foundation vermittelt | Delegates, öffentliche Governance und KPIs bieten Monitoring; kein allgemeines abgestuftes Sanktionssystem; Veto ist eher diskreter H | **[historical] Houses existieren; [agenda] Capture-Resistance** citeturn22search1turn22search3turn22search9 |
| **Arbitrum, AIP-1** | DAO soll Treasury und Chain-Governance kontrollieren | AIP-1 sah 750 Mio. ARB für ein Foundation Administrative Budget Wallet vor; in der Governance-Debatte wurde sichtbar, dass Teile der betreffenden Übertragung/Disposition vor vollständiger Ratifikation erfolgt waren | **Ja.** Foundation, Forum und nachfolgende Governance waren für die Korrektur wesentlich | AIP-1.1 ergänzte Budgettransparenz, Vesting und DAO-kontrollierbarere Mittelströme; Stoppen eines Streams ist ein echter H, aber kein vollständiges graduated-sanctions-System | **[historical] Fail-and-patch** citeturn22search16turn22search0turn22search4 |

**The DAO — [historical].** Der Fall ist die sauberste Widerlegung von „code is law“ als vollständiger Governance-Konstruktion. Der Smart Contract besaß eine exakte ausführbare Semantik; diese Semantik war nicht identisch mit dem menschlich intendierten Eigentums-/Governance-D. Der spätere Fork war ein Eingriff von \(S\), nicht ein vorher konstruiertes on-chain \(D\). Der SEC-Bericht dokumentiert sowohl den Abfluss als auch die Hard-Fork-Reaktion. citeturn9view1

**Maker — [historical].** Maker zeigt die positivere Seite: Eine enge Notfall-Eigenschaft kann gebaut werden. „Bei Aktivierung soll das Protokoll in einen definierten Settlementpfad übergehen“ ist wesentlich contractibler als „Maker Governance soll immer klug handeln“. Emergency Shutdown ist deshalb ein reales \(H\). citeturn10search4 Es ist dennoch nur so umfassend wie die Assets, Oracles, Governance Keys und Abhängigkeiten, die unter der definierten Maschine liegen.

**Optimism — [historical + agenda].** Das Two-House-Design ist eine bewusste Änderung des Selectors: Tokenvermögen allein soll nicht über jede Kategorie entscheiden; die Citizens’ House verwendet ein reputations-/identitätsbasiertes One-Person-One-Vote-Modell, und das veröffentlichte Design sah Vetorechte gegenüber bestimmten Token-House-Entscheidungen vor. citeturn22search1turn22search3 Das **konstruiert** die bicamerale Zuständigkeits- und Vetoregel. Es konstruiert nicht den Claim „capture-resistant“. Ein klarer Fail wäre eine systematische gemeinsame Capture beider Häuser oder ein Veto, das operativ ignoriert werden kann.

**Arbitrum — [historical].** AIP-1 ist fast ein Lehrbuchfall dafür, dass eine formale DAO-Kompetenz und de-facto Verfügung auseinanderfallen können. Der anschließende AIP-1.1-Prozess ergänzte Lockup/Vesting, Budgetinformationen und stärkere DAO-Kontrolle über den Mittelstrom. citeturn22search4turn22search10 Das ist interessanter als ein abstrakter „decentralize more“-Slogan: Ein schlecht definierter Ressourcenzugriff wurde in einen überprüfbareren Handle übersetzt.

**Über viele DAOs — [empirical].** Die neuere empirische Literatur dämpft die Behauptung, Token-Governance löse Capture grundsätzlich. Studien mit großen DAO-Samples finden substanzielle Unterschiede in Partizipation und Dezentralisierung; eine 2026er Analyse aktiver Ethereum-DAOs kommt insbesondere zu dem Ergebnis, dass Staking-, Registration- und Delegationsmechanismen, obwohl sie Sicherheit und Teilnahme verbessern sollen, systematisch mit konzentrierterem Stimmgewicht zusammenhängen können. citeturn11search4turn11search7

Die allgemeine Konstruktionseinsicht aus DAOs lautet deshalb:

\[
R \neq \theta \neq H \neq S \neq D.
\]

Ein unverfälschtes Abstimmungsprotokoll ist ein besseres \(R\). Ein Timelock ist ein \(H\). Ein Token-Snapshot definiert \(\theta\). Ein Hard Fork ist \(S\). Keine dieser Aussagen sagt ohne zusätzliche Argumente, dass die gesellschaftliche Zielregion \(D\) erreicht wurde.

## Hardware, proof, and spec-relative builders

**Threshold signatures — [standard].** Threshold-Kryptographie verteilt einen geheimen Schlüssel so, dass eine kryptographische Operation erst bei einer spezifizierten Schwelle zustande kommt. NIST beschreibt das ausdrücklich als Verteilung von Vertrauen und Vermeidung eines einzelnen kritischen Operators. citeturn24search9 Das konstruiert ein sehr starkes \(D\): „Keine gültige Signatur unter diesem Schlüssel ohne die erforderliche Schwelle.“ Es konstruiert nicht „die Unterzeichner entscheiden richtig“. Fail: Schwellenkoalition kompromittiert oder relevante Aktion besitzt einen zweiten Schlüssel/Pfad.

**Timelocks — [standard].** Ein Timelock kann erzwingen, dass privilegierte Governanceaktionen zwischen Queueing und Execution mindestens \(\tau\) warten. OpenZeppelins Controller hält dafür typischerweise selbst die betroffenen Ownership-/Access-Control-Rechte. citeturn24search0turn24search10 Das ist echtes \(H\). Seine Wirksamkeit erfordert

\[
\tau_{\text{delay}}
>
\tau_{\text{detect}}+\tau_{\text{decide}}+\tau_{\text{intervene}}.
\]

Bei einem autonomen System, das irreversiblen Schaden in Sekunden erzeugen kann, ist ein 48-Stunden-Timelock formal korrekt und praktisch idle.

**Remote attestation und TEEs — [standard].** Attestation kann kryptographisch nachweisen, dass ein Report mit einem bestimmten Measurement beziehungsweise einer bestimmten TEE-Konfiguration zusammenhängt. Bei SEV-SNP validiert der Verifier eine Zertifikatskette bis zu AMD; Intel TDX stellt vergleichbare Attestation-Evidence bereit. citeturn12search2turn12search3 Damit kann ein Gate etwa lauten:

\[
\text{API key released}
\iff
\text{valid attestation}(m=m^\*).
\]

Das ist Konstruktion von \(R\), eventuell gekoppelt mit \(H\), wenn das Secret tatsächlich nur an \(m^\*\) freigegeben wird. Es ist **nicht** der Beweis „Programm \(m^\*\) wird semantisch sicher handeln“.

Die Trust Boundary ist real. **[empirical]** Foreshadow demonstrierte einen praktischen mikroarchitektonischen Angriff auf SGX-Sicherheitsziele; AMD und Intel veröffentlichten auch 2025/26 Sicherheitsadvisories für neuere Confidential-Computing-Technik. citeturn13search0turn13search2turn13search23 Ein TEE verlagert Vertrauen; es eliminiert nicht Hardware-, Firmware-, Side-Channel-, Availability- oder Vendor-Risiko.

**Tivoization — [historical / standard].** Dieselbe Technik kann einen Handle auch absichtlich **entfernen**. Wenn Secure-Boot-/Signaturpolitik ausschließlich Herstellerbins akzeptiert, kann der Hersteller die Eigenschaft „nur autorisierte Images laufen“ tatsächlich konstruieren, während der Nutzer den Handle „installiere meine modifizierte Version“ verliert. GPLv3s Installation-Information-Klausel ist gerade eine rechtliche Gegenkonstruktion für einen Teil dieser Situation. citeturn6search15turn6search6 Ein Sicherheitsmechanismus und ein Corrigibility-Mechanismus können also dieselbe technische Primitive mit umgekehrtem Vorzeichen verwenden.

**Zero-knowledge proofs — [standard].** Ein ZK-System kann einen Verifier von der Wahrheit einer formalisierten Aussage überzeugen, ohne den zugrunde liegenden Witness vollständig offenzulegen. Ethereum verwendet Validity Proofs beispielsweise zur Prüfung von Zustandsübergängen; zk-SNARK-Verifier liefern letztlich ein Ja/Nein relativ zu Circuit/Relation und kryptographischen Annahmen. citeturn24search2turn24search8turn24search22 Das konstruiert \(V/R\): „dieser Trace erfüllt \(P\)“. Es konstruiert nicht „\(P\) war die richtige Eigenschaft“. Auch Availability folgt nicht aus Integritätsbeweisen. citeturn24search12

**seL4 — [proved].** Das ursprüngliche seL4-Projekt lieferte eine maschinengeprüfte funktionale Korrektheitskette von einer abstrakten Kernel-Spezifikation bis zur C-Implementierung; die ursprüngliche Arbeit machte explizite Annahmen unter anderem über Hardware, Bootcode und damals außerhalb des Kernbeweises liegende Komponenten. citeturn14search8turn14search36 Das ist ein sehr starkes \(V\): Implementierung und stated spec werden gekoppelt. Es sagt nicht, dass die abstrakte Spezifikation die gesellschaftlich gewünschte Kernelpolitik enthält.

**CompCert — [proved].** CompCert formuliert die Garantie noch klarer: Wenn der Compiler aus Source \(S\) Code \(C\) erzeugt, dann entspricht das beobachtbare Verhalten des erzeugten Codes den durch die Source-Semantik erlaubten Verhaltensweisen in der bewiesenen Refinementrelation. citeturn14search29turn14search1 Compiler-Fehler als Transformationsrisiko \(Q\) werden damit drastisch reduziert. Ein bösartiges oder falsch spezifiziertes Sourceprogramm wird dadurch nicht gut.

**DO-178C, DO-333 und Common Criteria — [standard].** Diese werden häufig mit formaler Konstruktion vermischt. Die FAA erkennt DO-178C als Software-Development-Assurance-Rahmen an; DO-333 ergänzt ihn für Formal Methods. citeturn14search22turn14search2 Common Criteria ist ebenfalls ein Evaluations-/Certification-Regime für definierte Security Functions und Assurance Claims. citeturn14search7turn14search19 Allein sind sie daher hauptsächlich \(R/V\)- und institutionelle Assurance-Systeme. Erst wenn „kein gültiges Zertifikat \(\Rightarrow\) kein Marktzugang“ gesetzlich oder vertraglich durchgesetzt wird, wird das Zertifizierungssystem selbst zu \(\theta/H\).

**Guaranteed/Safeguarded AI — [agenda].** Dalrymple et al. definieren eine Architektur aus Weltmodell \(W\), Safety Specification \(\varphi\) und Verifier, der einen überprüfbaren Nachweis dafür erzeugen soll, dass Controller plus Weltmodell \(\varphi\) erfüllen. citeturn15search0turn15search4 ARIAs Safeguarded-AI-Programm finanziert inzwischen konkrete Tooling- und Proof-Certificate-Komponenten, beschreibt das Endziel aber weiterhin als zu demonstrierende Fähigkeit. citeturn15search17turn15search21

Das ist daher **kein** Nachweis, dass ein allgemeiner KI-Builder existiert. Ein expliziter Fail wäre beispielsweise: Ein Controller erhält einen gültigen Proof, aber reale relevante Dynamiken liegen außerhalb des Weltmodells; oder die Safety Specification lässt einen katastrophalen Zustand zu; oder die benötigte Modellunsicherheit kann nicht mit einer brauchbaren quantitativen Garantie abgedeckt werden. Ein Proof in \(W\) bleibt ein Proof in \(W\).

**Constitutional AI/RLAIF — [empirical].** Bai et al. haben dagegen tatsächlich ein Trainingsverfahren implementiert: Supervised Self-Critique/Revision und anschließend Reinforcement Learning aus AI-generierten Präferenzen relativ zu einer Prinzipienliste. Sie berichten bessere human-judged Harmlessness/Non-evasiveness-Eigenschaften. citeturn15search6turn15search2 Das ist vernünftigerweise Konstruktion von \(Q/f\) **für die gemessene Verhaltensverteilung**. Es ist kein \(V\), dass jedes Modellverhalten die Constitution semantisch erfüllt. Der starke Claim scheitert, sobald ein systematischer, prinzipienwidriger Verhaltensbereich trotz Trainingsverfahren bestehen bleibt.

**AI Control — [empirical].** Greenblatt et al. sind ebenfalls mehr Konstruktion als bloße Evaluation, aber von einem anderen Teil: Sie bauen Protocols, die zwischen untrusted model und Deployment liegen, etwa suspiciousness monitoring und trusted editing, und testen sie gegen explizite Subversionsstrategien. citeturn15search7turn15search23 In ihrem Coding-Testbed konstruiert das \(\theta/H\): „diese Outputs werden nicht automatisch deployed“. Es konstruiert nicht das Ziel des untrusted Optimizers. Seine Generalisierung auf wesentlich stärkere, langfristig kolludierende oder das Monitoring manipulierende Agenten bleibt offen.

## Amendments, open questions, and sources

**Amendment cluster.** Die praktisch entscheidende Frage ist hier jeweils nicht, ob eine Institution „AI safety“ erwähnt, sondern ob sie einen realen Handle oder Selector aufbaut.

| Bestehende Institution | Konkrete AI-Änderung / Vorschlag | Status & strength | Was würde gebaut? | Handle oder nur Record? | Klarer Fail |
|---|---|---|---|---|---|
| **Courts / liability** | EU AI Liability Directive, 2022 vorgeschlagen, später zurückgezogen | **[historical: failed proposal]**; die Kommission bestätigte 2025 den Rückzug citeturn16search4turn16search17 | ex-post Änderung von \(f/S\): Schadenskosten und Beweisregeln | **kein unmittelbarer H**; primär ex-post payoff/corrector | Betreiber ist judgment-proof, Kausalität unbeweisbar oder Schaden irreversibel, bevor Urteil wirkt |
| **Licensing** | Anderljung et al.: Lizenzregime für Frontier-AI-Modelle plus regulatorische Enforcement Powers | **[agenda]** citeturn17search1turn17search21 | \(\theta/H/C\): Training/Deployment nur mit Lizenz | **potenziell echter H** | unlizenzierter Compute/Deployment leicht substituierbar; Behörde kann Lizenz faktisch nicht entziehen |
| **Insurance** | Trout: mandatory insurance für Critical AI Occurrences; Stetler: mandatory private insurance + Pool/Reinsurance | **[agenda]** citeturn23academia35turn23search18 | \(f/\theta\): Kapital wird vor Deployment exponiert; Underwriter wird zusätzlicher Selector | **H nur wenn Coverage Pflichtbedingung** | keine Kapazität für korrelierte Tail-Risiken, willkürliche Exclusions, Versicherer kann Risiko nicht unterscheiden |
| **Public procurement** | US OMB M-25-22 „Driving Efficient Acquisition of AI in Government“ | **[historical]**: operative Bundes-Procurement-Regel citeturn16search1turn16search5 | \(\theta/E\): Regierung kann Anbieter durch Kaufbedingungen selektieren | **echter θ; nur H, wenn Vertrag Deployment stoppt** | Safety-Bedingungen bleiben freiwillige Dokumentation oder Staat ist kein hinreichend großer Kunde |
| **Technical standards** | EU-Kommission beauftragte CEN/CENELEC mit harmonisierten AI-Act-Standards u.a. für Risk Management, Logging, Human Oversight, Robustness und Cybersecurity | **[historical / work in progress]**; Standardisierungsarbeit lief 2026 weiter citeturn17search2turn17search6turn17search22 | zunächst \(V/R\); bei rechtlicher Konformitätswirkung zusätzlich \(\theta\) | **meist Record/Verifier; Gate nur via Recht** | Standard misst nur Prozessdokumentation oder wird nicht im OJ referenziert/Marktzugang nicht daran gebunden |
| **Compute/cloud access** | US BIS-Lizenzregeln für bestimmte Advanced-Computing-ICs und bestimmte Endnutzer/-verwendungen; 2026 bestätigte BIS fortbestehende Lizenzpflichten für relevante D:5/Macau-Headquartered Entities | **[historical]** citeturn16search6turn16search9 | \(\theta/E/H\): physische Compute-Lieferung kann verboten oder genehmigungspflichtig werden | **echter H auf kontrollierter Supply Chain** | ausreichender alternativer Compute, Smuggling, lokale Fertigung oder Jurisdiktionsarbitrage |
| **Cloud/IaaS** | BIS-Policy von 2025 erfasste unter bestimmten Knowledge-/End-use-Bedingungen auch Advanced-Compute-Lieferungen an IaaS/Data-Center-Provider für bestimmte Trainingzwecke | **[historical]** citeturn16search2 | Cloudanbieter werden potentieller Selector \(\theta\) | **H**, soweit Training auf kontrollierten Chips/Providern beruht | offene Gewichte, alternative Clouds oder eigener Compute umgehen den Provider |

Die **[historical]** Procurement- und Compute-Fälle sind unter den AI-spezifischen Amendments derzeit die stärksten Beispiele echter Konstruktion, weil sie bereits existierende ökonomische oder physische Engpässe benutzen. Licensing und mandatory insurance sind dagegen weiterhin überwiegend **[agenda]**. Ein harmonisierter Standard kann technisch sehr präzise sein und dennoch nur \(R/V\) bleiben, solange kein Käufer, Gericht oder Regulator daran eine bindende Entscheidung koppelt. citeturn16search5turn16search6turn17search6

**Open questions.** Diese Review kann insbesondere die folgenden Punkte nicht schließen:

1. Welche sicherheitsrelevanten KI-Zustände können so operationalisiert werden, dass erwünschte und unerwünschte Lookalikes für Verträge, Verifier oder Regulatoren tatsächlich separierbar werden?
2. Wie klein muss die Reaktionslatenz eines \(H\) werden, wenn autonome KI Aktionen wesentlich schneller ausführen kann als menschliche oder gerichtliche Correctors?
3. Welche Compute-/Cloud-Bottlenecks bleiben bei Distillation, quantisierten Modellen, Edge-Hardware, eigenen Rechenzentren und internationaler Verlagerung tatsächlich geschlossen?
4. Wie baut man einen \(C\), dessen Personal, Informationsfluss, Budget und spätere Karriere nicht ökonomisch vom Promoter endogenisiert werden?
5. Kann ein Versicherungsmarkt hoch korrelierte Frontier-AI-Tail-Risiken mit endlichem Kapital sinnvoll preisen, oder benötigt er zwingend staatliche Rückversicherung beziehungsweise Liability Caps?
6. Welche rechtlich überprüfbaren Transformationen bilden für \(L\) „dieselbe KI“: Fine-Tune, LoRA, Merge, Distillation, Quantisierung, rekonstruierte Gewichte, API-Service?
7. Wie lässt sich Modellunsicherheit in world-model-basierten formalen Garantien so begrenzen, dass der Proof nicht lediglich das falsche Modell perfekt verifiziert?
8. Können DAO-Identitätssysteme gleichzeitig Sybil-Resistance, Privatsphäre, geringe Capture-Risiken und reale One-Person-One-Vote-Eigenschaften liefern?
9. Wie testet man institutionelle Stopps und Correctors mit **echter Möglichkeit des Testversagens**, ohne dabei katastrophale Realweltfehler zu riskieren?
10. Welche Selektionsprozesse bleiben konstruktiv, wenn Fehlervarianten nicht wiederholbar sind und ein einziger Fehlversuch irreversibel sein kann?

Die übergreifende Restunsicherheit ist daher nicht, ob wir *irgendwelche* Teile bauen können. Das können wir. Sie lautet, ob sich die sicherheitsrelevante Grenze eines fortgeschrittenen KI-Systems so legen lässt, dass genügend Teile tatsächlich an ihr greifen.

**Sources.** Die folgenden sind die load-bearing Primärquellen beziehungsweise wissenschaftlichen Quellen dieser Review. Wo nur Abstract/Metadaten und nicht der vollständige Text ausgewertet wurden, ist dies markiert.

Cox, M., Arnold, G., & Villamayor-Tomás, S. (2010). *A review of design principles for community-based natural resource management*. *Ecology and Society, 15*(4), 38. https://doi.org/10.5751/ES-03704-150438. citeturn0search21

Ostrom, E. (1990). *Governing the Commons*. Cambridge University Press. **[Nur als Ausgangswerk bibliographisch eingeordnet; die empirischen Claims hier stützen sich auf Cox et al., nicht auf eine direkte Volltextlektüre.]**

U.S. Nuclear Regulatory Commission. *Governing Legislation / Energy Reorganization Act history*. citeturn0search1turn0search28

Public Company Accounting Oversight Board. Enron/Arthur-Andersen testimony and auditor-independence material. citeturn0search5

Acemoglu, D., & Robinson, J. A. (2008). Persistence of power, elites, and institutions. *American Economic Review, 98*(1), 267–293. https://doi.org/10.1257/aer.98.1.267. citeturn21search0

Lloyd’s Register. *Rules, regulations and standards for ships*. https://www.lr.org/en/knowledge/lloyds-register-rules/ citeturn21search1

Federal Aviation Administration. *Airworthiness Certification of Aircraft*. https://www.faa.gov/aircraft/air_cert/aw_cert citeturn21search2

Federal Aviation Administration. *General Requirements for Certification — Insurance*. https://www.faa.gov/licenses_certificates/airline_certification/135_certification/general_req citeturn21search26

U.S. Food and Drug Administration. *New Drug Application*. https://www.fda.gov/drugs/types-applications/new-drug-application-nda citeturn21search19

GNU/OSI/SPDX. *GNU General Public License version 3*, especially §6 Installation Information. citeturn6search15turn6search16

Gibbard, A. (1973). Manipulation of voting schemes: A general result. *Econometrica, 41*(4), 587–601. https://www.jstor.org/stable/1914083 citeturn18search0

Maskin, E. (1999). Nash equilibrium and welfare optimality. *Review of Economic Studies, 66*(1), 23–38. https://academic.oup.com/restud/article-abstract/66/1/23/1666384 citeturn18search13

Myerson, R. B., & Satterthwaite, M. A. (1983). Efficient mechanisms for bilateral trading. *Journal of Economic Theory, 29*(2), 265–281. https://doi.org/10.1016/0022-0531(83)90048-0. citeturn20view0

Grossman, S. J., & Hart, O. D. (1986). The costs and benefits of ownership: A theory of vertical and lateral integration. *Journal of Political Economy, 94*(4), 691–719. https://doi.org/10.1086/261404. citeturn2search0

Hart, O., & Moore, J. (1999). Foundations of incomplete contracts. *Review of Economic Studies*. **[Abstract/Metadaten ausgewertet.]** citeturn2search2

Sandholm, W. H. (2005). Negative externalities and evolutionary implementation. *Review of Economic Studies, 72*, 885–915. https://users.ssc.wisc.edu/~whs/research/ne.pdf citeturn19view1

Bergemann, D., & Morris, S. (2005). Robust mechanism design. *Econometrica, 73*(6), 1771–1813. **[Abstract/Metadaten ausgewertet.]** citeturn4search15turn4search21

Huang, Tharas, Marro, et al. (2026). *Mechanism Design Is Not Enough*. arXiv:2605.08426. https://doi.org/10.48550/arXiv.2605.08426. citeturn2search3turn3view0

U.S. Securities and Exchange Commission. (2017). *Report of Investigation Pursuant to Section 21(a) of the Securities Exchange Act of 1934: The DAO*. https://www.sec.gov/files/litigation/investreport/34-81207.pdf citeturn9view1

Ethereum Foundation. (2016). *Hard Fork Completed*. citeturn7search1

MakerDAO. *Maker Protocol documentation / Emergency Shutdown*. citeturn10search0turn10search4

Optimism. (2023). *The Future of Optimism Governance*. https://optimism.io/blog/the-future-of-optimism-governance citeturn22search1

Optimism. *Introducing the Citizens’ House*. citeturn22search3

Arbitrum Foundation Governance Forum. *AIP-1: Arbitrum Improvement Proposal Framework*. https://forum.arbitrum.foundation/t/aip-1-arbitrum-improvement-proposal-framework/30 citeturn22search16

Arbitrum Foundation Governance Forum. *AIP-1.1 — Lockup, Budget, Transparency*. https://forum.arbitrum.foundation/t/proposal-aip-1-1-lockup-budget-transparency/13360 citeturn22search4

Sharma et al. (2024). Empirical DAO-governance analysis covering 100 DAOs. arXiv. **[Abstract ausgewertet.]** citeturn11search4

Pahari et al. (2026). Empirical study of governance and voting-power concentration in 48 active Ethereum DAOs. arXiv. **[Abstract ausgewertet.]** citeturn11search7

National Institute of Standards and Technology. *Multi-Party Threshold Cryptography*. https://csrc.nist.gov/Projects/threshold-cryptography citeturn24search9

OpenZeppelin. *TimelockController*. https://docs.openzeppelin.com/contracts-cairo/3.x/governance/timelock citeturn24search0

Van Bulck et al. (2018). *Foreshadow: Extracting the Keys to the Intel SGX Kingdom with Transient Out-of-Order Execution*. USENIX Security. citeturn13search0

AMD. Security advisory AMD-SB-3034 / CVE-2025-54510. citeturn13search2

Intel. Security advisory INTEL-SA-01397 for TDX. citeturn13search23

Klein, G., et al. (2009). seL4: Formal verification of an OS kernel. *Proceedings of SOSP*. https://doi.org/10.1145/1629575.1629596. citeturn14search8

CompCert Project. *CompCert formally verified C compiler*. https://compcert.org/ citeturn14search1turn14search29

Federal Aviation Administration. *AC 20-115D: Airborne Software Development Assurance Using EUROCAE ED-12 and RTCA DO-178*. https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1032046 citeturn14search22

Common Criteria Portal. https://www.commoncriteriaportal.org/ citeturn14search7

Dalrymple, D., Skalse, J., Bengio, Y., Russell, S., Tegmark, M., Seshia, S., et al. (2024). *Towards Guaranteed Safe AI: A Framework for Ensuring Robust and Reliable AI Systems*. arXiv:2405.06624. https://doi.org/10.48550/arXiv.2405.06624. citeturn15search0

Advanced Research + Invention Agency. *Safeguarded AI*. https://www.aria.org.uk/programme-safeguarded-ai/ citeturn15search1turn15search21

Bai, Y., et al. (2022). *Constitutional AI: Harmlessness from AI Feedback*. arXiv:2212.08073. https://arxiv.org/abs/2212.08073 citeturn15search6

Greenblatt, R., Shlegeris, B., Sachan, K., & Roger, F. (2024). AI Control: Improving safety despite intentional subversion. *Proceedings of ICML / PMLR 235*. https://proceedings.mlr.press/v235/greenblatt24a.html citeturn15search23

Anderljung, M., Barnhart, J., Leung, J., Korinek, A., O’Keefe, C., Whittlestone, J., et al. (2023). *Frontier AI Regulation: Managing Emerging Risks to Public Safety*. arXiv:2307.03718. https://arxiv.org/abs/2307.03718 citeturn17search1

European Commission. *Standardisation of the AI Act*. https://digital-strategy.ec.europa.eu/en/policies/ai-act-standardisation citeturn17search2turn17search6

U.S. Office of Management and Budget. (2025). *M-25-22, Driving Efficient Acquisition of Artificial Intelligence in Government*. citeturn16search1turn16search5

U.S. Bureau of Industry and Security. (2026). *Guidance Regarding Enforcement of License Requirements for Advanced Computing Items for Entities Headquartered in Country Group D:5 and Macau*. https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf citeturn16search6

Trout, C. (2024). *Liability and Insurance for Catastrophic Losses: The Nuclear Power Precedent and Lessons for AI*. arXiv:2409.06673. https://arxiv.org/abs/2409.06673 citeturn23academia35

Stetler, N. (2025). *Reinsuring AI: Energy, Agriculture, Finance & Medicine as Precedents for Scalable Governance of Frontier Artificial Intelligence*. arXiv:2504.02127. https://arxiv.org/abs/2504.02127 citeturn23search18