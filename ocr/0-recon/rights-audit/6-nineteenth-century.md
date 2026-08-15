I audited all 38 text directories under `texts/6-nineteenth-century/`. I opened
the source PDF or EPUB (title page and copyright/publisher's-note page) for
every text that has one — 36 of 38 — using PyMuPDF text extraction, and where
a PDF was a pure image scan with no text layer (Cantor, Galton, Hertz) I
rendered the relevant pages to PNG and read them directly. Two directories
(Humboldt, Riemann) have no source file at all. The surprise of this slice:
almost nothing here is actually a 19th-century edition on disk — nearly every
text is a later authorized translation (1887–1923) or a Project Gutenberg
transcription of one, and exactly two are genuinely dangerous: Abel and
Galvani are both sourced from modern copyrighted books (2003 and 1953) that
happen to be the only translation in the corpus, even though the underlying
work is long free. Both are `translation needed`, not `copyrighted`, because
the original work is free — only Enchiridion's specific source text is not.

## translation needed

Abel, Memoir on the Impossibility of Solving the General Equation of the Fifth Degree, translation needed — source files are Peter Pesic's *Abel's Proof* (MIT Press, copyright 2003, "all rights reserved") and a scanned extract of its Appendix A ("Abel's 1824 Paper," Pesic's translation); Abel's 1824 French memoir itself is public domain — translate fresh from Sylow & Lie's 1881 *Œuvres complètes de Niels Henrik Abel* (Christiania, public domain) or another pre-1931 edition
Galvani, Commentary on the Effect of Electricity on Muscular Motion, translation needed — the only source file is Robert Montraville Green's translation (Elizabeth Licht, publisher, copyright 1953, "may not be reproduced... without permission"); its own preface says this is the *first-ever* English translation of Galvani's 1791 Latin *De Viribus Electricitatis*, which is itself public domain — translate fresh from the 1791 Latin (Bologna, *De Bononiensi Scientiarum et Artium Instituto atque Academia Commentarii*, vol. VII) or the 1792 Modena reprint with Aldini's notes, both public domain

## no source

Humboldt, Views of Nature, no source — directory has no PDF or EPUB; metadata.json claims the E.C. Otté/Henry G. Bohn translation of 1850, which would be public domain if verified, but there is nothing here to check it against
Riemann, On the Hypotheses Which Lie at the Bases of Geometry, no source — directory has no PDF or EPUB; metadata.json claims the W.K. Clifford translation of 1873, which would be public domain if verified, but there is nothing here to check it against

## public domain

Arrhenius, On the Influence of Carbonic Acid in the Air upon the Temperature of the Ground, public domain — Philosophical Magazine, 1896; PDF is a modern photocopy (Global Warming Art / Robert Rohde) of the public-domain original, no new translation or copyrightable apparatus in the paper itself
Beecher Stowe, Uncle Tom's Cabin, public domain — first published 1852, Stowe's own English, Project Gutenberg text
Boole, An Investigation of the Laws of Thought, public domain — 1854, Boole's own English, Project Gutenberg text
Cantor, Contributions to the Founding of the Theory of Transfinite Numbers, public domain — Philip Jourdain's English translation first published 1915 (Open Court); source file is an "unabridged and unaltered reprint" from Dover, verified on the copyright page
Carnot, Reflections on the Motive Power of Heat, public domain — R.H. Thurston's translation, copyright 1890, John Wiley & Sons / Chapman & Hall, verified on the copyright page
Cayley, A Memoir on the Theory of Matrices, public domain — Philosophical Transactions of the Royal Society, received Dec. 1857, read Jan. 1858, Cayley's own English
Darwin, On the Origin of Species, public domain — first edition, 1859, Project Gutenberg text
Dedekind, Essays on the Theory of Numbers, public domain — Wooster Woodruff Beman's authorized translation, copyright 1901, Open Court, verified on the title and copyright pages
Dostoyevsky, Notes from the Underground, public domain — Constance Garnett's translation, per Project Gutenberg's front matter first published 1918
Douglass, Narrative of the Life of Frederick Douglass, public domain — 1845, Boston Anti-Slavery Office, Douglass's own English, verified on the title page
Dred Scott v. Sandford, public domain — official U.S. Supreme Court report, 19 Howard, Washington: Cornelius Wendell, 1857; government-adjacent report of that age
Faraday, Experimental Researches in Electricity (Vol. 1), public domain — second edition, "reprinted from the Philosophical Transactions of 1831–1838," Faraday's own English
Franklin, Experiments and Observations on Electricity, public domain — London, printed by E. Cave, 1751, Franklin's own English, verified on the title page
Galois, Œuvres mathématiques d'Évariste Galois, public domain — French original, 1897 Gauthier-Villars edition (ed. Émile Picard for the Société mathématique de France), Project Gutenberg transcription; note this source is French-only, no English translation present
Galton, Natural Inheritance, public domain — Macmillan, 1889, confirmed by embedded PDF metadata ("Natural Inheritance by Francis Galton (Macmillan, 1889)") and page content; Galton's own English
Gauss, General Investigations of Curved Surfaces of 1827 and 1825, public domain — James Caddall Morehead and Adam Miller Hiltebeitel's translation, copyright 1902, Princeton University Library, verified on the title and copyright pages
Hertz, Electric Waves, public domain — D.E. Jones's "authorised English translation," first published by Macmillan in 1893; source file is Dover's "unabridged and unaltered republication," verified by rendering the copyright page
James, Pragmatism: A New Name for Some Old Ways of Thinking, public domain — 1907, James's own English, Project Gutenberg text
Keats, Poems Published in 1820, public domain — poems originally 1820; this edition (ed. M. Robertson), Clarendon Press, 1898/1909, verified on the title page
Lincoln, Gettysburg Address, public domain — delivered 1863, Project Gutenberg text
Lobachevsky, Geometrical Researches on the Theory of Parallels, public domain — George Bruce Halsted's translation, "new edition," Open Court, copyright 1914, verified on the title and copyright pages
Marx, Capital, Volume I, public domain — Progress Publishers (Moscow) edition explicitly states it "reproduces the text of the English edition of 1887," the Samuel Moore/Edward Aveling translation edited by Frederick Engels, with only Engels's own changes from the 1890 4th German edition incorporated; the publisher's note adding this context is brief and factual, not a new copyrightable work
Marx and Engels, Manifesto of the Communist Party, public domain — "Authorized English Translation, Edited and Annotated by Frederick Engels" (Samuel Moore's 1888 translation), this printing New York Labor News Co., 1908, verified on the title page
Marx and Engels, Revolution and Counter-Revolution; or, Germany in 1848, public domain — written directly in English by Engels (under Marx's byline) as New York Tribune correspondence, 1851–52; this edition ed. Eleanor Marx Aveling, Chicago: Charles H. Kerr & Co., 1912, verified on the title page
Maxwell, An Elementary Treatise on Electricity, public domain — second edition, Clarendon Press, 1888, Maxwell's own English, verified on the title page
Maxwell, A Treatise on Electricity and Magnetism (Vol. I), public domain — first edition, Clarendon Press, 1873, Maxwell's own English, verified on the title page
Mendel, Experiments on Plant Hybridization, public domain — William Bateson's English translation of Mendel's papers, published within Bateson's *Mendel's Principles of Heredity: A Defence*, Cambridge University Press, 1902, verified in the front matter
Mendeleev, The Principles of Chemistry, Vol. 1, public domain — George Kamensky's authorized translation (first English edition 1891); this source is the P.F. Collier & Son "Library of Universal Literature" printing, 1901 (MCMI), verified on the title page
Mendeleev, The Principles of Chemistry, Vol. 2, public domain — same translation and situation as Vol. 1, Collier & Son, 1901
Mill, On Liberty, public domain — 1859 original; source is a Walter Scott Publishing Co. edition with an introduction by W.L. Courtney, undated in the front matter but from Walter Scott's early-1900s "New Universal Library" series, well before 1931 either way
Mill, Utilitarianism, public domain — "seventh edition," Longmans, Green, and Co., 1879, verified on the title page
Peirce, Chance, Love, and Logic: Philosophical Essays, public domain — essays originally 1877–1893; this edition, ed. and introduced by Morris R. Cohen with a concluding essay by John Dewey, Kegan Paul / International Library of Psychology, Philosophy and Scientific Method, 1923 (confirmed via web search of publication history)
Twain, Adventures of Huckleberry Finn, public domain — 1885 original, Project Gutenberg text
Wilde, The Picture of Dorian Gray, public domain — 1890/1891 original, Project Gutenberg text

## Metadata corrections

Gauss, `metadata.json` — `year_translated` is `2011`, which is the Project Gutenberg ebook's release date, not the translation date. The actual Morehead/Hiltebeitel translation was published in 1902 (Princeton University Library), confirmed on the source PDF's copyright page.
