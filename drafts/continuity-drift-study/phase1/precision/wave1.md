# Consolidation and precision wave 1

## Wikipedia lister

Agent `295cfc15-b1ea-475f-b11a-dce5caf9accd`. English Wikipedia **category and list pages** (Christian denominations; religious orgs 18th/19th c.; legal orgs/bar associations; Great Twelve livery companies; list of oldest companies; sovereign states by formation; learned societies; temperance/abolitionist categories). **73 rows**; **42 names new** vs first pass.

## Union (first pass + Wikipedia)

File: `consolidated-union.tsv`

| Domain | Unique names | Lister notes flagged incomplete | Not flagged |
|--------|-------------:|-------------------------------:|------------:|
| religions | 29 | 12 | 17 |
| legal traditions | 36 | 26 | 10 |
| professions / guilds | 109 | 76 | 33 |
| firms | 84 | 72 | 12 |
| states / administrations | 23 | 5 | 18 |
| scholarly disciplines | 31 | 4 | 27 |
| civic / fraternal orders | 26 | 17 | 9 |
| reform movements | 28 | 7 | 21 |
| **Total** | **366** | **219** | **147** |

“Not flagged” is a note heuristic, not a precisioner verdict. Full catalog not yet precisioned.

## Precisioner packet

Frozen hash `0ef4901ccdd1bed07912fb3ad6d389e21b1648168878498b6761be479cbefa53`. One unflagged name per domain (shortest-name heuristic; not a quality ranking).

**Usable** = frozen founding aims quoted/paraphrased from earliest-period **own** primary sources with citation.

| Domain | Case | Usable? |
|--------|------|---------|
| religions | Teutonic Order | **no** — no contemporaneous own-aim text |
| legal traditions | Gulating | **no** — no own-aim founding instrument |
| professions / guilds | Drapers’ Company | **yes** — 1371 ordinances |
| firms | Barings | **no** — 1762 articles not publicly transcribable |
| states / administrations | Canada | **yes** — 1864 Québec Resolutions / 1867 Act |
| scholarly disciplines | Leopoldina | **yes*** — 1662 printed statutes (1651/52 MS not independently quoted) |
| civic / fraternal orders | B’nai B’rith | **no** — 1843/1851 constitution not in public text |
| reform movements | Prohibition Party | **yes** — 2 Sep 1869 resolutions |

\*Count as usable only if later protocol accepts the 1662 print as earliest recoverable own source.

**Usable this wave by domain:** religions 0; legal 0; guilds 1; firms 0; states 1; scholarly 1; civic 0; reform 1.

Catalog precision is complete in `results.tsv` (**366 / 366** in-union; extras Jean Roze, Iwasaki, Kitagawa Honke, Kikkoman not counted). **Usable** = `earliest_own_aim` yes (own earliest-period aims with citation).

| Domain | n | usable | not usable |
|--------|--:|-------:|-----------:|
| civic / fraternal orders | 26 | 23 | 3 |
| firms | 84 | 22 | 62 |
| legal traditions | 36 | 24 | 12 |
| professions / guilds | 109 | 87 | 22 |
| reform movements | 28 | 27 | 1 |
| religions | 29 | 28 | 1 |
| scholarly disciplines | 31 | 29 | 2 |
| states / administrations | 23 | 20 | 3 |
| **Total** | **366** | **260** | **106** |

## Usage-limit retries (2026-08-29)

First-pass precisioners on these names failed with usage-limit errors (`gpt-5.6-sol-medium`). Not counted as precisioned. Retries complete:

| Case | Retry agent |
|------|-------------|
| Leeds Law Society | logged `ca34b352` (drop `d71a0adb`, `4bd5755b`) |
| Society of Writers to His Majesty’s Signet | logged `41d6380d` (drop `2cf1b49d`, `6cd1208f`) |
| Somerset Law Society | logged `fc07b828` (drop `a0b497e2`, `5ef22f93`) |
| Sunderland Law Society | logged `c12c8831` |
| Water Tribunal of Valencia | logged `2abfeee2` |
| Yorkshire Law Society | logged `dc586dd0` **no** (drop `6648d962`, `9787daa7`) |
| American Institute of Architects | logged `9eb5d997` (drop `adaf360c`, `50bdb644`) |

## Precision catalog (logged)

Remaining catalog **0 / 366**.

| Case | Agent |
|------|--------|
| American Institute of Mining Engineers predecessor | logged `894c7a54` |
| American Medical Association | logged `3ca36040` |
| Apothecaries’ Society | logged `437d68af` |
| Armourers and Brasiers’ Company | logged `9a1f8f4e` |
| Bakers’ Company | logged `baaac9a6` |
| Basketmakers’ Company | logged `91c93861` |
| Blacksmiths’ Company | logged `21a98301` |
| Bowyers’ Company | logged `8144bc50` |
| Brewers’ Company | logged `0ea9dd4c` |
| British Medical Association | logged `e31a0734` |
| Broderers’ Company | logged `49f6ed60` |
| Butchers’ Company | logged `961e2b56` |
| Carmen | logged `f70652c8` |
| Carpenters’ Company | logged `98e3521a` |
| Chartered College of Teaching / College of Preceptors | logged `e03f4829` |
| Clockmakers’ Company | logged `d37f483e` |
| Clothworkers’ Company | logged `13572f5e` |
| Coachmakers and Coach Harness Makers | logged `6af777aa` |
| Company of Cutlers in Hallamshire | logged `35a3c124` |
| Company of Merchants of the Staple of England | logged `97abec0f` |
| Cooks’ Company | logged `a97de0e2` |
| Coopers’ Company | logged `686d7164` |
| Cordwainers’ Company | logged `e5cdf495` |
| Corporation of Trinity House | logged `e41c089a` |
| Curriers’ Company | logged `6030749a` |
| Cutlers’ Company | logged `e7646573` |
| Distillers’ Company | logged `937561b3` |
| Dyers’ Company | logged `5114e1d4` |
| Faculty of Actuaries | logged `f7e9e2ad` |
| Fan Makers | logged `137b0519` |
| Farriers’ Company | logged `7e2e80a3` |
| Feltmakers’ Company | logged `9109e076` |
| Fishmongers’ Company | logged `6c0afc3a` |
| Fletchers’ Company | logged `2c879970` |
| Founders’ Company | logged `5a71dff9` |
| Framework Knitters’ Company | logged `62776e19` |
| Fruiterers’ Company | logged `4b9a13ac` |
| Gardeners’ Company | logged `c1089cd3` |
| Girdlers’ Company | logged `8da0167e` |
| Glass Sellers’ Company | logged `29e60cc1` |
| Glaziers and Painters of Glass | logged `7f285eb8` |
| Glovers’ Company | logged `3f937fff` |
| Gold and Silver Wyre Drawers | logged `1c0c6f08` |
| Goldsmiths’ Company | logged `0a8d18b0` |
| Grocers’ Company | logged `636d0390` |
| Gunmakers’ Company | logged `7663d5d1` |
| Grocers—see above | logged `20b29418` |
| Haberdashers’ Company | logged `d3e7e488` |
| Haberdashers—see above | logged `65d4669a` |
| Horners’ Company | logged `9dcb67b5` |
| Incorporation of Surgeons and Barbers of Edinburgh / RCSEd | logged `8267a922` |
| Innholders’ Company | logged `fa36502d` |
| Institute of Actuaries | logged `6a049149` |
| Institution of Civil Engineers | logged `2050b1b0` |
| Institution of Mechanical Engineers | logged `9a5f8ce7` |
| Ironmongers’ Company | logged `83988029` |
| Joiners and Ceilers’ Company | logged `e064ed3f` (drop `b5a3e641`) |
| Law Society of England and Wales | logged `b642c433` |
| Leathersellers’ Company | logged `d248662f` |
| Makers of Playing Cards | logged `d019394b` |
| Masons’ Company | logged `82589bc2` |
| Mercers’ Company | logged `16d92935` |
| Merchant Adventurers of York | logged `04986efe` |
| Merchant Taylors’ Company | logged `d435d29a` |
| Musicians’ Company | logged `6d8690c7` |
| Needlemakers’ Company | logged `35fba2f8` |
| Painter-Stainers’ Company | logged `a63ac4a5` |
| Pattenmakers’ Company | logged `f5de7c8f` |
| Paviors’ Company | logged `6132f5c5` |
| Pewterers’ Company | logged `06a60440` |
| Pharmaceutical Society of Great Britain / Royal Pharmaceutical Society | logged `877fba0f` |
| Plaisterers’ Company | logged `2c778fab` |
| Plumbers’ Company | logged `d6be2aeb` |
| Poulters’ Company | logged `779963ae` |
| Royal Aeronautical Society | logged `09c6eace` |
| Royal College of Physicians of London | logged `35fa53f8` |
| Royal College of Surgeons of England | logged `ab05292b` |
| Royal College of Veterinary Surgeons | logged `3eeb5fde` |
| Royal Institute of British Architects | logged `45139d8e` |
| Royal Institution of Chartered Surveyors | logged `e45ce6f3` |
| Saddlers’ Company | logged `87cd0521` |
| Salters’ Company | logged `955b04fe` |
| Scriveners’ Company | logged `cc75a642` |
| Shipwrights’ Company | logged `afceb332` |
| Shrewsbury Drapers Company | logged `d6010a4c` |
| Skinners’ Company | logged `0c9a1acb` |
| Society of Engineers | logged `40bfbde4` |
| Society of Merchant Venturers, Bristol | logged `caedbc13` |
| Spectacle Makers’ Company | logged `91213785` |
| Stationers’ Company | logged `4c805f74` |
| Tallow Chandlers’ Company | logged `fcb58f3b` |
| Tin Plate Workers alias Wire Workers | logged `7beda083` |
| Trades House of Glasgow | logged `b45bda88` |
| Turners’ Company | logged `0519b9c2` |
| Tylers and Bricklayers’ Company | logged `62cd6f98` |
| Upholders’ Company | logged `66b1dc0e` |
| Vintners’ Company | logged `7af6f774` |
| Watermen and Lightermen of the Thames | logged `34bed79c` |
| Wax Chandlers’ Company | logged `bf909f1a` |
| Weavers, Fullers and Shearmen of Exeter | logged `c9de65ba` |
| Weavers’ Company | logged `1d1699a6` |
| Wheelwrights’ Company | logged `39340d60` |
| Woolmen’s Company | logged `19c241d2` |
| Worcester Clothiers’ Company | logged `ab51d4d1` |
| Worshipful Company of Parish Clerks | logged `11b1030b` |
| York Cordwainers | logged `a876f64c` |
| York Merchant Taylors | logged `1c813550` |
| American Anti-Slavery Society | logged `dd2c890a` |
| American Colonization Society | logged `c1c49bba` |
| American Equal Rights Association | logged `4e76aa41` |
| American Peace Society | logged `5a219f6f` |
| American Society for the Prevention of Cruelty to Animals | logged `c630c45d` |
| American Temperance Society | logged `1a2f9ed1` |
| American Temperance Union | logged `064bbcd5` |
| American Woman Suffrage Association | logged `2af98596` (drop `2df06305`, `b4a7dc8f`) |
| American and Foreign Anti-Slavery Society | logged `39e506c0` (drop `58c2e579`, `3e44abb5`) |
| Anti-Corn Law League | logged `81b05426` (drop `28c27f3b`) |
| Anti-Saloon League of America | logged `12f2909f` (drop `59f4cdfd`) |
| Anti-Slavery International / British and Foreign Anti-Slavery Society | logged `ae60b4a0` |
| Congressional Union / National Woman’s Party | logged `3adbf826` |
| Howard League for Penal Reform / Howard Association | logged `98d20111` |
| Massachusetts Peace Society | logged `1f96a57a` |
| Movendi International / Independent Order of Good Templars | logged `a81d73b6` **no** |
| National American Woman Suffrage Association | logged `f16bc9bc` |
| National Woman Suffrage Association | logged `85a97271` |
| New York Female Moral Reform Society / American Female Guardian Society | logged `67394782` |
| New York Manumission Society | logged `7997e917` |
| Pennsylvania Abolition Society | logged `9e9f3c1a` |
| Philadelphia Female Anti-Slavery Society | logged `365a566b` |
| Providence Society for Abolishing the Slave Trade | logged `96baee7e` |
| Royal Society for the Prevention of Cruelty to Animals | logged `26ed99f5` |
| Society for Effecting the Abolition of the Slave Trade | logged `bde3367f` |
| Washingtonian Temperance Society | logged `e11efe6b` |
| Woman’s Christian Temperance Union | logged `1b46db3b` |
| Arya Samaj | logged `b9fe2573` |
| Baháʼí community | logged `686c1347` |
| Brahmo Samaj | logged `c1bac531` |
| Carmelite Order | logged `7a3f4e8d` |
| Carthusian Order | logged `19ea63b0` |
| Church of Jesus Christ of Latter-day Saints | logged `a06ddf19` |
| Cistercian Order | logged `1718a200` |
| Congregation of the Mission / Vincentians | logged `64fd9688` (replacement; prior `112426a5` produced no packet) |
| Dominican Order / Order of Preachers | logged `1849dac6` |
| Franciscan Order / Friars Minor | logged `7d02c337` |
| Knights Hospitaller / Order of St John | logged `ba95eabb` |
| Knights Templar | logged `f866e461` |
| Methodist Episcopal Church | logged `5970179a` |
| Methodist United Societies | logged `d50b537e` |
| Moravian Church / Unitas Fratrum | logged `793d189a` |
| Order of Friars Minor Capuchin | logged `f08682e1` |
| Order of Saint Augustine / Augustinian Hermits | logged `021c090e` |
| Order of Saint Benedict / Benedictines | logged `8243f6e5` |
| Poor Clares / Order of St Clare | logged `af98408d` |
| Premonstratensian Order / Norbertines | logged `75c671f9` |
| Religious Society of Friends | logged `ab55d29d` |
| Religious Society of Friends / Quakers | logged `26ec0719` |
| Salvation Army / Christian Mission | logged `c3ebc480` |
| Servite Order | logged `5b46e0e3` |
| Seventh-day Adventist Church / General Conference | logged `668a5b5b` |
| Society of Jesus | logged `558e66ea` |
| Society of Jesus / Jesuits | logged `1ae4ee94` |
| Tenrikyo | logged `efe6f33e` |
| Académie des Jeux floraux | logged `a7ff50fa` |
| Académie des Jeux floraux / Consistori del Gay Saber | logged `6358c29c` |
| Académie française | logged `c9f235ac` |
| Académie française, original/restored body | logged `f9d5803f` |
| Académie royale des sciences, original body | logged `587847d8` |
| Accademia dei Lincei | logged `9c180752` |
| Accademia dei Lincei, original body | logged `6d3a687a` |
| Accademia della Crusca | logged `3850bae4` |
| American Academy of Arts and Sciences | logged `783ff77c` |
| American Philosophical Society | logged `6384faae` |
| American Society for Premodern Asia, formerly American Oriental Society | logged `52438bd9` |
| Berlin Society/Prussian Academy of Sciences | logged `1cb5ebb6` |
| British Association for the Advancement of Science | logged `261c270b` |
| Chemical Society of London | logged `56a41ea8` |
| French Academy of Sciences | logged `91356a38` |
| Geological Society of London | logged `fc39b7e2` |
| Linnean Society of London | logged `78ccf5ab` |
| Royal Astronomical Society | logged `130805b7` |
| Royal Dublin Society | logged `ff431eb9` |
| Royal Geographical Society | logged `81125d27` |
| Royal Historical Society | logged `19170b84` |
| Royal Irish Academy | logged `32c10efe` |
| Royal Society | logged `a6b646a1` |
| Royal Society of Antiquaries of Ireland | logged `4645f413` |
| Royal Society of Edinburgh | logged `110eff8e` |
| Royal Society of London | logged `7fd3735e` |
| Royal Statistical Society | logged `8064fc1e` |
| Society of Antiquaries of London | logged `55192dcc` |
| Society of Antiquaries of Scotland | logged `518ba374` |
| Sodalitas Litterarum Vistulana | logged `e4e4eb7b` |
| Austrian Empire | logged `89ad919b` |
| Belgium | logged `a8cc8ecf` |
| Board of Admiralty | logged `ff3f8ac5` |
| Board of Trade and Plantations | logged `6bcda7fd` |
| British Foreign Office | logged `153e8880` |
| British Home Office | logged `48b000e1` |
| British Privy Council | logged `3687afd8` |
| Colonial Office (separate department) | logged `fc1aea96` |
| Conseil d’État (France) | logged `a9a2b2c7` |
| Council of the Indies | logged `8c3b68a8` |
| Danish Secret Archive (Gehejmearkivet) | logged `9c74d286` |
| General Land Office | logged `61213fb0` |
| German Empire | logged `0c4480ce` |
| Kingdom of Italy | logged `3b800bd1` |
| Kingdom of Norway | logged `d7e1e841` |
| Kingdom of the Netherlands | logged `db72f71f` |
| Swedish National Archives (Riksarkivet) | logged `5d209ae5` |
| Swiss federal state | logged `64428fa1` |
| United States Department of State | logged `089dbb2a` |
| United States Department of the Treasury | logged `1844b199` |
| United States Post Office Department | logged `e8595974` |
| United States federal government | logged `de184948` |
