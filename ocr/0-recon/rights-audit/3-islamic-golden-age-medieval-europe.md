# Section 3: Islamic Golden Age & Medieval Europe — rights audit

Audited all 17 text directories in this slice (12 currently published, 5
withheld). Opened a source file for every one of them — PDF title/copyright
pages for the scans, EPUB `content.opf` `dc:rights` plus the underlying source
for the Project Gutenberg and Wikisource texts — rather than trusting
`metadata.json`. Nothing here overturns the five prior withholding decisions;
the file confirms every one of them, translator, publisher and year alike. The
one surprise: Roger Bacon's Burke translation (1928, University of
Pennsylvania Press) carries a printed `COPYRIGHT 1928` notice on its own title
page and is nonetheless clean, since 1928 falls before the 1931 boundary — the
same "read the date first, the notice second" lesson the charter opens with.
The directory also holds an *un*translated Latin edition (Bridges, Clarendon
Press) alongside the two Burke volumes; only the Burke text is what our
transcription draws from, so only it was audited as the operative source.

## public domain

Al-Khwarizmi, The Algebra of Mohammed ben Musa, public domain — Rosen 1831, Oriental Translation Fund, London; title/imprint page verified
Al-Biruni, Alberuni's India, public domain — Sachau translation, this file is the 1910 Kegan Paul/Trübner reprint (imprint page: "KEGAN PAUL, TRENCH, TRUBNER & CO... 1910"); matches metadata's year_translated 1910
Anselm of Canterbury, Proslogium; Monologium; Cur Deus Homo, public domain — Deane 1903, Open Court Publishing, copyright page verified; Cur Deus Homo (p.213 on) is the same 1903 volume, same translator, not a separate later work
Thomas Aquinas, Summa Theologica Part I (Prima Pars), public domain — PG epub 17611, dc:rights "Public domain in the USA," Dominican Fathers "Complete American Edition" (1920)
Thomas Aquinas, Summa Theologica Part I-II, public domain — PG epub 17897, dc:rights "Public domain in the USA"
Thomas Aquinas, Summa Theologica Part II-II, public domain — PG epub 18755, dc:rights "Public domain in the USA," translated by Fathers of the English Dominican Province
Thomas Aquinas, Summa Theologica Part III, public domain — PG epub 19950, dc:rights "Public domain in the USA"
Brahmagupta (and Bhaskara), Algebra with Arithmetic and Mensuration from the Sanscrit, public domain — Colebrooke 1817, John Murray, London; title page verified
Geoffrey Chaucer, The Canterbury Tales (Chaucer's Works, vol. 4, ed. Skeat), public domain — PG epub 22120, dc:rights "Public domain in the USA," Middle English text, no translator involved
Dante Alighieri, The Divine Comedy, public domain — PG epub 8800, dc:rights "Public domain in the USA," Cary translation (1814), Doré illustrations
René Descartes, Discourse on the Method, public domain — PG epub 59, dc:rights "Public domain in the USA," Veitch translation (1850)
Omar Khayyam, The Quatrains of Omar Khayyam, public domain — Whinfield 1883, Trübner's Oriental Series; this is a Wikisource-sourced epub reproducing that edition, not a PG file, but the underlying translation and imprint (1883) are pre-1931 regardless of host
Omar Khayyam, Rubaiyat of Omar Khayyam, public domain — PG epub 246, dc:rights "Public domain in the USA," FitzGerald translation (1859)
Moses Maimonides, The Guide for the Perplexed, public domain — PG epub 73584, dc:rights "Public domain in the USA," Friedländer translation (1904)
Roger Bacon, Opus Majus, public domain — Burke translation, University of Pennsylvania Press, 1928 ("COPYRIGHT 1928" printed on the title verso); 1928 is before the 1931 boundary, so the printed notice does not change the verdict. Directory also holds the untranslated Latin edition (ed. Bridges, Clarendon Press, 1897) which the transcription does not draw from.

## translation needed

Al-Farabi, Philosophy of Plato and Aristotle, translation needed — WITHHELD. File confirms Mahdi's translation, "Copyright © 1962 by The Free Press of Glencoe," Agora Editions (Allan Bloom, general editor). Work is ~10th century; translate from an Arabic edition (WITHHELD.md says "verify an edition exists" — still unverified by this audit)
Ibn al-Haytham (Alhazen), The Optics of Ibn Al-Haytham, Books I-III, translation needed — WITHHELD. File confirms A.I. Sabra, "© THE WARBURG INSTITUTE, 1989." Translate from Risner's Latin edition, 1572 (per WITHHELD.md; not independently re-verified here)
Averroes (Ibn Rushd), The Incoherence of the Incoherence, translation needed — WITHHELD. File is a web transcription (muslimphilosophy.com, "E-text conversion Muhammad Hozien") but its text is confirmed to be Simon Van Den Bergh's translation for the Gibb Memorial Trust, signed "SIMON VAN DEN BERGH" in the preface — the 1954 translation named in WITHHELD.md. The scrape's own copyright status is irrelevant; the underlying translation is still Van Den Bergh's and still encumbered. Translate from a public-domain Arabic text of the Tahafut al-Tahafut
Leonardo Fibonacci, Liber Abaci, translation needed — WITHHELD. File confirms Laurence Sigler, "© 2002 Springer-Verlag New York, Inc.," first softcover printing 2003 (metadata.json's year_translated 2003 is the printing date, not the copyright date — see corrections below). Translate from Boncompagni's Latin, 1857 (per WITHHELD.md)
Hildegard von Bingen, Book of the Rewards of Life (Liber Vitae Meritorum), translation needed — WITHHELD. File confirms Bruce W. Hozeski, Oxford University Press, New York/Oxford; no copyright page was reached in the pages read but publisher and translator match the known 1994 OUP edition. Translate from Migne's Patrologia Latina (per WITHHELD.md)

## Notes on the withheld five

All five withholding decisions from WITHHELD.md are correct on this audit —
none of them is an Aristotle-style mistake. In each case the file itself
names the copyrighted translator and modern publisher; none is a
misidentified older public-domain edition wearing a later cover.

## Metadata corrections

Fibonacci, fibonacci-liber-abaci/metadata.withheld.json: `year_translated` is `2003`. The copyright page reads "© 2002 Springer-Verlag New York, Inc." with "First softcover printing, 2003" — the translation itself is copyright 2002; 2003 is only the softcover printing date. Doesn't change the verdict (both years postdate 1930) but the field conflates copyright year with a later printing.
