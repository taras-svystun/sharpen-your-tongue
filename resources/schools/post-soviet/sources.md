# Sources: post-soviet

The catalogue of this school. The reference may cite only sources listed here, by ID (`ps:src:02`). A video is cited as `ps:src:01 / <video-id> @ m:ss`. Fields and the reliability scale: `GLOSSARY.md` (scope, reliability). Transcripts live in git-ignored `data/transcripts/`.

**Access** says whether we can actually read it. **Checked** says what was confirmed and how. "From memory" means the bibliographic details are not yet confirmed: fix them before the first citation.

## Catalogue

### ps:src:01 Lebed & Shaman (БУ Lebed & Shaman), YouTube channel

- Genre: video (two former prisoners talk; series «НаКумаре», «Культяпка» and «Ломовая Культяпка» on juvenile prison, «Зона строгого режима», «Чёрная берлога», single talks on понятия, conflicts, tattoos, red and black zones).
- Scope: Ukraine. Places named in titles: Бучанская колония (строгий режим), Бердянская колония 77, Лукьяновское СИЗО (Kyiv), Чернигов, a juvenile colony («малолетка»). Years: one host was sentenced to 7 years in 2009 (transcript `BWE9JSvtrng` @ 1:05). Russian speech.
- Reliability: medium. First-hand, but two narrators with one shared story, entertainment format, uploads 2019-2025.
- Guests (Костя Белый, Толя Лютый, Юра Слон and others) are other witnesses: a guest's own story may count as a separate source when cited by name.
- Size: 732 videos, about 169 on prison by title (list: `data/catalogue/lebed-shaman.tsv`, made with `tools/transcribe.py --list`).
- Link: https://www.youtube.com/@LebedShaman
- Access: transcripts through `tools/transcribe.py`; YouTube captions worked on the one video tried (seconds, no punctuation, jargon sometimes garbled).
- Checked: channel listing 2026-10-25; one transcript.

### ps:src:02 «Азбука тюрьмы», documentary series, Настоящее Время

- Genre: video documentary (12 episodes from 50 interviews with former prisoners), plus a podcast (author Виктор Кульганек, 2022).
- Scope: Russia, 2000s-2010s, mostly political and high-profile prisoners. Director Андрей Сильвестров, premiere summer 2021.
- Reliability: high for what people lived through (edited journalism, many narrators); their view is of outsiders thrown into the system, not of блатные.
- Link: https://www.currenttime.tv/a/azbuka-tyurmy-podkast/31682968.html
- Access: video on the Current Time site and YouTube; transcripts through the tool; not tried yet.
- Checked: the page above, 2026-10-25.

### ps:src:03 Медиазона (zona.media), journalism on Russian prisons

- Genre: journalism. Key pieces: complaints to the ECHR that the informal hierarchy is degrading (2019, https://zona.media/article/2019/07/26/degraded); Азат Мифтахов, a political prisoner placed among «обиженные» (2025, https://zona.media/article/2025/08/08/miftakhov); an excerpt from Абрамкин's book (2021, https://zona.media/article/2021/05/19/abramkin-75).
- Scope: Russia, 2014 onward.
- Reliability: high (named sources, documents).
- Access: free full text; the 2019 article read in full on 2026-10-25.
- Checked: URLs via web search; the 2019 article (А. Бородихин, a Kostroma colony) read in full, 2026-10-25.

### ps:src:04 Новая газета, «Откуда берутся «опущенные». К истории вопроса» (А. Виноградов, written 2019-11-10, published 2020-08-08)

- Genre: expert commentary with history; cites Кузнецов «Мордовский марафон» (1979) and Амальрик «Записки диссидента» (1982), and the 2001 suicide in the Kostroma juvenile colony.
- Scope: Russia; history of the lowest caste over about 80 years.
- Reliability: high for the present, medium for the history (secondary).
- Link: https://novayagazeta.ru/articles/2020/08/08/86581-otkuda-berutsya-opuschennye-k-istorii-voprosa
- Access: free full text, read on 2026-10-25.
- Checked: read in full, 2026-10-25.

### ps:src:05 Варлам Шаламов, «Очерки преступного мира»

- Genre: memoir and essay. Part of «Колымские рассказы», written around 1959 (late 1950s-early 1960s).
- Scope: Kolyma camps, 1930s-1950s; the блатной world seen by a political prisoner who hated it.
- Reliability: high as a witness, openly hostile to блатные; old: shows the roots, not today's rules.
- Link: https://shalamov.ru/library/6/
- Access: free full text on shalamov.ru. Chapters 2, 3, 4 and 6 («Жульническая кровь», «Сучья война» and others) saved as text in `data/sources/text/7_shalamov_<n>.txt`, 2026-10-25. Cite by chapter: `ps:src:05, ch. 3`.
- Checked: dating via booksite.ru (web search, 2026-10-25); the link opens the cycle's table of contents (2026-10-25).

### ps:src:06 Д. С. Лихачёв, «Черты первобытного примитивизма воровской речи» (1935)

- Genre: linguistics; the author studied thieves' speech as a prisoner of Соловки.
- Scope: Соловецкий лагерь and Белбалтлаг, late 1920s-early 1930s.
- Reliability: high, scholarly; old.
- Published in «Язык и мышление», т. 3-4, М.; Л., 1935, с. 47-100. Written in 1933.
- Access: copy in `data/sources/5_cherti_perv.pdf` (scan, 40 pages), OCR text in `data/sources/text/`. The scan is the reprint inside ps:src:08 (1992), pages 54-93; cite those pages.
- Checked: the reprint's own footnote gives the 1933 writing date and the 1935 publication (scan p. 40), 2026-10-25.

### ps:src:07 Жак Росси, «Справочник по ГУЛАГу»

- Genre: dictionary and encyclopaedia of camp words and life by a former prisoner (19 years in the GULAG).
- Scope: USSR camps, 1937-1950s.
- Reliability: high, careful, old.
- Editions: London 1987 (Russian, first); English "The Gulag Handbook", Paragon House, New York 1989; Moscow, «Просвет», 1991 (2nd, expanded).
- Access: copy of the London 1987 edition in `data/sources/2_rossi_spravochnik_po_gulagu_1987_text.pdf` (560 pages, with a text layer). Cite by headword: `ps:src:07, s.v. мужик`.
- Method (preface): material gathered 1937-1958 (Лубянка, Бутырки, transit prisons, Норильск camps, Владимирский централ), cards written from 1961 and checked with other former prisoners. Tags before a word: (Д) specifically criminal, (Г) general prison and camp, (Е) guards' jargon, (А) popular.
- Checked: title page and preface of the copy, 2026-10-25.

### ps:src:08 Д. С. Балдаев, В. К. Белко, И. М. Исупов, «Словарь тюремно-лагерно-блатного жаргона (речевой и графический портрет советской тюрьмы)» («Края Москвы», 1992)

- Genre: dictionary, about 11 000 entries, plus proverbs, tattoo abbreviations, a catalogue of tattoos, prisoners' drawings, and reprints of Лихачёв (ps:src:06).
- Scope: USSR, mostly 1950s-1980s, all regions; place names only for Leningrad and its oblast.
- Reliability: medium-high; large, but compiled by a criminalist (Балдаев, about 40 years of collecting) and two journalists, so seen from outside; no dates or places per entry.
- Access: copy in `data/sources/4_Baldaev_Slovar_Tyuremno-Lagerno-Blatnogo_Zhargona_rechev.pdf` (scan, 527 pages), OCR text in `data/sources/text/`. Printed page = PDF page − 1. Cite as `ps:src:08, s.v. МУЖИК, p. 145`.
- A later two-volume edition («Словарь блатного воровского жаргона», Кампана, 1997) is known from one bibliography only.
- Checked: title page, ISBN 5-900310-01-9, publisher's note, 2026-10-25.

### ps:src:09 А. Н. Олейник, «Тюремная субкультура в России: от повседневной жизни до государственной власти»

- Genre: sociology (surveys and interviews with prisoners), the main academic study of the topic.
- Scope: Russia, 1990s colonies. One of his later articles (Мир России, 2005, № 2) studies Ukrainian colonies.
- Reliability: high, scholarly.
- Editions: Инфра-М, Москва, 2001; a 2010 edition is cited by an HSE course.
- Access: no free text found; his articles (e.g. Мир России, 2005) are free.
- Checked: cited as «Олейник 2001» in https://mirros.hse.ru/article/download/5238/5599; publisher and year from memory.

### ps:src:10 Mark Galeotti, "The Vory: Russia's Super Mafia" (Yale University Press, 2018)

- Genre: history and journalism on the воры в законе, from the gulag to today.
- Scope: USSR and Russia, 1920s-2010s; also Georgia and Ukraine.
- Reliability: high (about 20 years of research), English, secondary.
- Access: paid book.
- Checked: library catalogue records (web search, 2026-10-25).

### ps:src:11 А. Н. Олейник, «Театр недоверия и пессимизма (опыт социологического анализа арт-проекта)», Мир России, 2005, № 2, с. 160-173

- Genre: sociology. How prisoners, prison staff and ordinary viewers reacted to a play about betrayal and informers.
- Scope: Ukraine, five penal institutions of Kharkiv oblast, April-May 2003.
- Reliability: high, scholarly; about trust and informing, not a list of rules.
- Link: https://mirros.hse.ru/article/download/5238/5599
- Access: free PDF; read the first pages, 2026-10-25.
- Checked: title, author, journal, scope from the PDF itself, 2026-10-25.

### ps:src:12 MSPRING ONLINE, «Тюремные понятия в Беларуси» (talk show, 2019-03-28, 1:44:02)

- Genre: video, a talk show: former prisoners and human-rights experts on понятия, козлы, those who "signed the papers" to cooperate, life по понятиям in Belarusian colonies.
- Scope: Belarus, 2000s-2010s colonies and СИЗО; Russian and Belarusian speech.
- Reliability: medium-high (several witnesses and experts in one room).
- Link: https://www.youtube.com/watch?v=fL9vcSlAIXk
- Access: transcript `data/transcripts/fL9vcSlAIXk.md` (YouTube captions, 13 170 words; music and Belarusian passages garbled).
- Checked: transcript skimmed for key terms, 2026-10-25.

### ps:src:13 hromadske, «Виправити, а не карати. Фільм про підліткові колонії» (2022-01-25, 24:48)

- Genre: video documentary: teenagers, staff and a psychologist in a juvenile colony.
- Scope: Ukraine, Кременчуцька виховна колонія, 2021. Mostly about how teenagers end up inside and come back; little on rules, but it shows the one "on понятия" refusing to clean.
- Reliability: high (journalism, many speakers, named place); thin on понятия.
- Link: https://www.youtube.com/watch?v=R6bgO2gqXaM
- Access: transcript `data/transcripts/R6bgO2gqXaM.md` (YouTube captions, 2 852 words, punctuated; Ukrainian and Russian).
- Checked: transcript skimmed, 2026-10-25.

### ps:src:14 Tsira Chanturia, "Deep-rooted problem of criminal subculture conducive to ill-treatment" (Open Society Georgia Foundation policy brief, Tbilisi, November 2022)

- Genre: policy brief by Penal Reform International's regional director; draws on CPT and Ombudsman reports.
- Scope: Georgia, prisons 2018-2022 (e.g. Ksani prison 15): staff delegating order to informal prisoner leaders.
- Reliability: high (named author, official reports cited).
- Link: https://csf.ge/wp-content/uploads/2022/12/Tsira-Chanturia_ForWeb.pdf
- Access: free PDF, 8 pages; read the first pages, 2026-10-25.
- Checked: title, author, date from the PDF itself, 2026-10-25.

### ps:src:15 Андрей Кудин, «Как выжить в тюрьме»

- Genre: memoir and survival guide for a first-time prisoner, with a chapter on prison words (ch. 4), cellmates (ch. 12) and games (ch. 13).
- Scope: Ukraine, Kyiv: КПЗ on Подол, then Лукьяновское СИЗО, 1997 to February 1998. A pre-trial prison, not a colony; Russian with Ukrainian quotes.
- Reliability: medium. One first-hand witness, educated, openly scornful of other prisoners and of блатные; acquitted, his arrest ruled illegal (ХПГ). He names some words as local to Kyiv ("пальма" here, "груша" in Dnipropetrovsk).
- Access: text copy `data/sources/3_kak_vyzhit_v_tyurme.u.txt`. No page numbers: cite by chapter, `ps:src:15, ch. 4`. Publication year unknown.
- Checked: author and dates from О. Крижанівська, ХПГ, 2001-12-12 (https://archive.khpg.org/1008168656), which says he wrote the book in Лукьяновка; the copy's chapters match (Kyiv, Лукьяновка, Подол). Not the Абрамкин book it was taken for. 2026-10-25.

### ps:src:16 Вясна, «"Это всё одно огромное преступление против человечности", — бывший политзаключённый шкловской колонии» (2023-04-04)

- Genre: human-rights journalism; one anonymous former political prisoner's testimony.
- Scope: Belarus, ИК-17 (Шклов), spring-summer 2022, from the side of political prisoners in a colony run by the administration.
- Reliability: medium-high: one witness, but a human-rights organisation that collects many such accounts; names 19 staff.
- Link: https://spring96.org/ru/news/111309
- Access: saved page `data/sources/6_viasna.pdf`, read in full.
- Checked: read in full, 2026-10-25. Not the 18-witness ИК-17 report (still a candidate below).

### ps:src:17 Виталий Лозовский, «Как выжить и провести время с пользой в тюрьме. Часть 1»

- Genre: survival guide grown from the author's mailing list, with readers' letters and his answers. Only the author's own voice is cited; a reader's letter is a separate, anonymous witness.
- Scope: Russia and Ukraine, 1990s-early 2000s: 4 prisons in Russia, 7 in Ukraine, one year in a Ukrainian усиленный режим camp (3 years in all). Afterword dated Прага, 2004.
- Reliability: medium: one first-hand witness, reflective; convicted of embezzlement, which he denies.
- Access: online text of part 1 (about 8 000 words) saved as `data/sources/text/8_lozovsky_part1.txt`; it may be incomplete. Cite by section title.
- Checked: author's background from the text itself; the phrase «На тюрьме не спрашивают, а интересуются» is quoted from this book on mybook.ru (citation page, 2020-01-22), but is not in the saved part. 2026-10-25.

## Candidates

Found, not yet checked. A candidate is cited only after it moves to the catalogue with all fields.

- Federico Varese, "The Russian Mafia: Private Protection in a New Market Economy" (Oxford University Press, 2001): Perm region, 1990s; from memory.
- Валерий Абрамкин, books from the Центр содействия реформе уголовного правосудия: «Как выжить в советской тюрьме» (1992?), «Тюремный мир глазами политзаключённых» (with Ю. Чеснокова, 1993?). Titles and years from memory; the Center's 2021 collection «Романтик тюрьмы» exists.
- Эдуард Кузнецов, «Мордовский марафон» (1979), and Андрей Амальрик, «Записки диссидента» (1982): political prisoners' memoirs on the lowest caste in the 1970s; cited by ps:src:04.
- Laura Piacentini, "Surviving Russian Prisons" (2004): from memory.
- Леся Ставицька, «Український жаргон. Словник» (2005): Ukrainian, includes criminal slang; from memory.
- Ukrainian Ombudsman, National Preventive Mechanism visit reports: record "informal groups of prisoners" and segregation (e.g. Старобабанівська колонія 92, 2024: https://ombudsman.gov.ua/en/news_details/vidviduvannya-derzhavnoyi-ustanovi-starobabanivska-vipravna-koloniya-92). Official, Ukrainian, recent; thin on detail.
- Джужа, Колб, on criminal subculture in Ukrainian places of detention (Історико-правовий часопис, 2016): https://evnuir.vnu.edu.ua/bitstream/123456789/10812/1/%d0%b4%d0%b6%d1%83%d0%b6%d0%b0.pdf (the link opens only a DSpace page).
- YouTube, from one search on 2026-10-25 (scope to check for each):
  - PRO DОБРО: a man who served 28 years explains понятия, slang and words you must not say; country and colonies unknown.
  - Onliner, «Опустить можно любого: #монолог отсидевшего 15 лет» (Belarusian media).
  - СПЕКТР: a women's colony; a tattooist from the zone.
  - Доброе семя: Леонид Семиколенов, six years as положенец, Novosibirsk.
  - Телеканал Дождь: a former prisoner of ИК-2 (Покров).
  - МЫ ВЕРНЕМСЯ (Руслан Кулевич): interview on low status and смотрящий.
  - Черная Хата: short videos on the rules for «неприкасаемые».
- YouTube, Ukrainian journalism, from one search on 2026-10-25 (a second Ukrainian view beside ps:src:01):
  - Радіо Свобода, «Тюремне братство | #ВУКРАЇНІ»: a second YouTube search did not find it.
  - Харківська правозахисна група (khpg.org): human-rights monitoring of Ukrainian prisons since the 1990s.
- Other post-Soviet voices, from searches on 2026-10-25:
  - vitaminE, «Закон в натуре»: a series on prison in Belarus and Russia (e.g. https://www.youtube.com/watch?v=oxLEZT8GiCU, «Политика в белорусской тюрьме» https://www.youtube.com/watch?v=zlVjjA-iinU).
  - Onliner, «Опустить можно любого: #монолог отсидевшего 15 лет» (Belarus).
  - Вясна and the International Committee for the Investigation of Torture in Belarus: a report on ИК-17 (Шклов) from 18 former political prisoners, 2020-2024; full text not yet found.
  - Gavin Slade, "Reorganizing Crime: Mafia and Anti-Mafia in Post-Soviet Georgia" (Oxford University Press, 2013): has a chapter on prison and recruitment of воры.
  - Kazakhstan: searches found only news about torture, no testimony on понятия yet.
- Newcomer riddles («прописка»), from searches on 2026-10-25; all low reliability so far:
  - vse42.ru, «Тюремные загадки: как и зачем в тюрьме проверяют новеньких» (2020-09-15, no author, no witness): the train riddle, «кенты» on one track and the mother on the other.
  - YouTube channels «Криминал ТВ», «Криминальный Мир», «Криминальный Аналитик», «Арестант ТВ»: many videos on прописка and riddles (e.g. yZPTMttbTQQ, JmHBUhEsCk4); narrators unnamed, scope unknown.
  - Wanted: a named former prisoner telling the riddles he was asked, with place and years.
- Rejected: «Мопс дядя Пес» (Сергей Новик, Ukraine, about 27 years inside): famous for humiliation streams for money (Медуза, 2017); entertainment, not testimony.

## Ask Taras

Worth having, but I could not open it. Taras spends a few minutes on each; a copy he finds goes to git-ignored `data/sources/<id-or-name>.<ext>` (agreement 18 in `docs/PLAN.md`). Most valuable first.

Found on 2026-10-25: Росси (now ps:src:07), Балдаев 1992 (ps:src:08), Лихачёв (ps:src:06), a Вясна interview (ps:src:16), and Кудин (ps:src:15), which came in place of Абрамкин.

1. Олейник, «Тюремная субкультура в России» (2001 or 2010): the main study; no free text found. Not found by Taras either.
2. Абрамкин, «Как выжить в советской тюрьме» (around 1992): written by an ex-prisoner for prisoners; title and year unconfirmed. The file found under this title is Кудин's book.
3. Вясна, the ИК-17 (Шклов) report, 2024: the only Belarusian document with many witnesses.
4. Lenta.ru, «Арестантский канал един» (2018-04-22, https://lenta.ru/articles/2018/04/22/zeki): a list of ex-prisoners' YouTube channels; did not open for me or for Taras.
