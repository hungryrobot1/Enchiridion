# The Guide for the Perplexed — review record

What is known about this text as a text: where it came from, what can check it, and what is doubtful. Generated at adoption from the processing run, then maintained by whoever reviews it.

**Status is a claim about process, not about correctness.** `needs-review` means machine-processed and unread. `complete` means a person performed the review below and judged the text shippable — not that it is free of errors. Every text is an ongoing project.

## Provenance

- Source file: `maimonides-guide-for-the-perplexed.md`
- Translator: M. Friedländer (1904)
- Processed by run [`ocr/runs/maimonides-guide-for-the-perplexed`](../../../ocr/runs/maimonides-guide-for-the-perplexed) (gpt-5.6-sol, 2026-08-04)
- Full processing notes: [`ocr/runs/maimonides-guide-for-the-perplexed/NOTES.md`](../../../ocr/runs/maimonides-guide-for-the-perplexed/NOTES.md)

## What the processing run found

Copied from the run's notes at adoption. These are the text's open questions, not the pipeline's.

### Outcome

Produced `maimonides-guide-for-the-perplexed.md` through source-native
extraction and reader post-processing. It is proposed for adoption as
`needs-review`, not as complete or fully proofread. `ocr_status` in the supplied
metadata remains `pending`; this run did not alter or inflate it.

Stage 4 remains unperformed because neither supplied source is an independent
printed-page witness. The escalation was resolved with no scan to be supplied
and no network search authorized; the proposal was accepted at `needs-review`,
which is this source set's present verification ceiling. See `ANSWER.md`.

### Recon and source choice

- Read the pipeline README and the stage contracts for recon, preparation,
  extraction, post-processing, verification, figures, and proofreading, plus
  the delegated-proofreading manual.
- Ran `recon-pdf.py`. The PDF has 441 pages, a dense clean text layer, 212
  outline entries, and only three images. Its metadata identifies Calibre as the
  creator, and its creation date is 2026-03-18.
- Chose the EPUB source-native track. It carries structured XHTML divisions,
  paragraphs, headings, italics, language annotations, correction spans, and
  page markers. The PDF was generated from the same Project Gutenberg
  transcription and is therefore a rendered witness only.
- Stage 1 preparation was unnecessary: this is not a scan/OCR track and the
  desired work is already a structurally bounded span in the EPUB. Duplicate-
  scan detection and PDF cropping do not apply.
- The figure track does not apply. The selected authorial span contains zero
  `img` elements; the EPUB's images are cover/title-page matter outside it.

### Edition and metadata

The source title page matches the held title, author, and translator:
*The Guide for the Perplexed*, Moses Maimonides, translated by M. Friedländer.
It states “SECOND EDITION, REVISED THROUGHOUT,” London/New York, 1910. The same
page states “Second Edition, 1904; Reprinted, 1910.” Thus the metadata's
`year_translated: 1904` describes the revised translation/edition, while 1910 is
the supplied reprint's publication year. I did not silently replace one with the
other.

### Apparatus decision

The XHTML makes the boundary explicit. I omitted Gutenberg boilerplate and
licence, title/imprint matter, Friedländer's two prefaces, *The Life of Moses
Maimonides*, *The Moreh Nebuchim Literature*, the translator's analysis and
contents, all indexes, correction history, and colophon.

I retained the final front-matter division identified as `introduction`, because
it contains Maimonides' dedicatory letter to Joseph ibn Aknin and his authorial
prefatory remarks, directions, and introductory remarks. I then retained Parts
I–III in full. The selected span contains no footnote or note-reference
structures, so no authorial/editorial footnote judgment was required. Bracketed
interpolations inside sentences and italics remain.

### Verification

After conversion, `audit_maimonides.py` reported:

- exact deterministic rebuild;
- 3 parts, 178 chapters, and 970 paragraphs;
- matching title-page metadata, with second edition 1904 / reprinted 1910;
- exact EPUB/PDF agreement across 244,172 word/number tokens.

That agreement establishes conversion fidelity only. EPUB and PDF are two
renderings of the same Project Gutenberg transcription, not independent acts of
copying.

The post-processing diagnostic triad returned exit 0 for all three checks:
`lint-math.py`, `check-math.js`, and `check-raw-latex.js`. Before trusting those
zeros, I ran a temporary positive-control Markdown file containing an unbalanced
`$`, an undefined KaTeX command, and raw LaTeX. The three checks respectively
returned exit 1 and identified the intended defect; the temporary control was
then removed.

This work has zero dollar signs and zero math blocks. Accordingly, the triad is
only a reader/debris check here, and the math-vocabulary census would have no
notation to adjudicate; it was not treated as evidence of textual correctness.
Additional exact hygiene checks found no replacement characters, NULs, tabs,
CRs, backslashes, raw HTML tags, Markdown links/images, encoded HTML entities,
or trailing whitespace. No Cyrillic, CJK, Arabic-script, or Hebrew-script
characters occur; Hebrew and Arabic terms are transliterated in this edition.

<!-- BEGIN GENERATED PG CORRECTION LEDGER -->

### Project Gutenberg correction ledger

The converter retained the visible adopted reading of every `span.corr` in the selected authorial span; it did not alter or independently adjudicate any of them. There are exactly **93**: **57 replacements** whose earlier reading survives in the EPUB's `title="Source: …"` attribute, and **36 editorial insertions** marked `title="Not in source"`. Locations use the edition's embedded printed-page marker and the stable correction ID; `h-N` identifies the EPUB XHTML chunk.

1. **AUTHORIAL INTRODUCTION / [Prefatory Remarks.]; printed p. 3; h-1; xd32e4108** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…m with the heads of the different sections of the subject.” (Babyl. Talm. Ḥagigah, fol. 11 b). You must, therefore, n…</q>

2. **AUTHORIAL INTRODUCTION / [Prefatory Remarks.]; printed p. 5; h-1; xd32e4136** — adopted <code>(</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…their dark sayings” (Prov. i. 6); and we read in Midrash, (Shir ha-shirim Rabba, i. 1); “To what were the words of th…</q>

3. **PART I / CHAPTER I; printed p. 13; h-3; xd32e4239** — adopted <code>toär</code>; source <code>toar</code>. Context: <q>…h its form (toär) with a line,” “and he marketh its form (toär) with the compass” (Isa. xliv. 13). This term is not at a…</q>

4. **PART I / CHAPTER I; printed p. 14; h-3; xd32e4288** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ion applies also to the phrase “the likeness of the ḥayyot” (“living creatures,” Ezek. i. 13).</q>

5. **PART I / CHAPTER VI; printed p. 19; h-3; xd32e4526** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ything designed and prepared for union with another object. Thus we read, “The five curtains shall be coupled togethe…</q>

6. **PART I / CHAPTER VII; printed p. 20; h-3; xd32e4584** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…the 130 years when Adam was under rebuke he begat spirits,” i.e., demons; when, however, he was again restored to div…</q>

7. **PART I / CHAPTER VIII; printed p. 21; h-3; xd32e4631** — adopted <code>meaning</code>; source <code>meanling</code>. Context: <q>…on (not of ocular inspection), in addition to its literal meaning “a place,” viz., the mountain which was pointed out to Mo…</q>

8. **PART I / CHAPTER XI; printed p. 23; h-3; xd32e4715** — adopted <code>,</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…o God, the verb is to be taken in that latter sense: “Thou, O Lord, remainest (tesheb) for ever” (Lam. v. 19); “O tho…</q>

9. **PART I / CHAPTER XVIII; printed p. 27; h-3; xd32e4965** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…e camp” (Exod. xxxii. 19); “And Pharaoh drew near (hikrib)” (Exod. xiv. 10). Nagaʻ, in the first sense, viz., express…</q>

10. **PART I / CHAPTER XVIII; printed p. 27; h-3; xd32e4988** — adopted <code>second</code>; source <code>seecond</code>. Context: <q>…ehension,” not in reference to space. As to nagaʻ in this second sense, comp. “for her judgment reacheth (nagaʻ) unto heav…</q>

11. **PART I / CHAPTER XVIII; printed p. 28; h-3; xd32e5012** — adopted <code>)</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…be explained (Part I. chap, xxi., and Part II. chap, xli.); also in “Forasmuch as this people draw near (niggash) me…</q>

12. **PART I / CHAPTER XX; printed p. 29; h-3; xd32e5100** — adopted <code>)</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…d (harimoti) one chosen out of the people” (Ps. lxxxix. 20); “Forasmuch as I have exalted (harimoti) thee from amongs…</q>

13. **PART I / CHAPTER XXIV; printed p. 34; h-3; xd32e5329** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…n is called in the Bible “the hiding of God’s countenance,” as in Deuteronomy xxxi. 18, “As for me, I will hide my co…</q>

14. **PART I / CHAPTER XXIV; printed p. 34; h-3; xd32e5331** — adopted <code>,</code>; source <code>.</code>. Context: <q>…” (Num. xii. 9), the two meanings of the verb are combined, viz., the withdrawal of the Divine protection, expressed…</q>

15. **PART I / CHAPTER XXVI; printed p. 35; h-3; xd32e5359** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ound, to sit, to dwell, to depart, to enter, to pass, etc.”</q>

16. **PART I / CHAPTER XXVII; printed p. 36; h-3; xd32e5369** — adopted <code>him</code>; source <code>Him</code>. Context: <q>…expressions denoting any mode of motion, are explained by him to mean the appearance or manifestation of a certain ligh…</q>

17. **PART I / CHAPTER XXVIII; printed p. 37; h-3; xd32e5428** — adopted <code>Uzziel</code>; source <code>Uziel</code>. Context: <q>…in permanently.” To this explanation does Jonathan son of Uzziel incline in paraphrasing the passage, “And he will appear…</q>

18. **PART I / CHAPTER XXVIII; printed p. 37; h-3; xd32e5431** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…appear in his might on that day upon the Mount of Olives.” He generally expresses terms denoting those parts of the…</q>

19. **PART I / CHAPTER XXVIII; printed p. 37; h-3; xd32e5441** — adopted <code>,</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ot show us what they (the nobles of the children of Israel, Exod. xxiv. 10) perceived, [38]or what is meant by that f…</q>

20. **PART I / CHAPTER XXX; printed p. 40; h-3; xd32e5548** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…et with in the Talmud, e.g., “Come, eat fat meat at Raba’s” (Baba Bathra 22a); comp. “All expressions of ‘eating’ and…</q>

21. **PART I / CHAPTER XXXIV; printed p. 47; h-3; xd32e5641** — adopted <code>“</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…r purpose. The passage may therefore be paraphrased thus: “And the righteous man devotes his ways to wisdom, and does…</q>

22. **PART I / CHAPTER XL; printed p. 55; h-4; xd32e5914** — adopted <code>ruaḥ</code>; source <code>ruah</code>. Context: <q>Next, it signifies “breath.” Comp. “A breath (ruaḥ) that passeth away, and does not come again” (Ps. lxxviii…</q>

23. **PART I / CHAPTER XLI; printed p. 56; h-4; xd32e5985** — adopted <code>“</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…o bind his princes at his will” (be-nafsho) (Ps. cv. 22); “Thou wilt not deliver me unto the will (be-nefesh) of my e…</q>

24. **PART I / CHAPTER XLIII; printed p. 57; h-4; xd32e6124** — adopted <code>uttermost</code>; source <code>utttermost</code>. Context: <q>…ends (kanfoth) of the earth” (Job xxxviii. 13); “From the uttermost part (kenaf) of the earth have we heard songs” (Isa. xxiv…</q>

25. **PART I / CHAPTER XLV; printed p. 58; h-4; xd32e6198** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ses” (Exod. vi. 9). “If they obey (yishmeʻü) and serve him” (Job xxxvi. 11); “Shall we then hearken (nishmaʻ) unto yo…</q>

26. **PART I / CHAPTER XLVI; printed p. 60; h-4; xd32e6233** — adopted <code>.</code>; source <code>,</code>. Context: <q>…nfluence has emanated from Him, as will be explained (chap. lxv. and chap. lxvi.). The physical organs which are attr…</q>

27. **PART I / CHAPTER XLVI; printed p. 60; h-4; xd32e6236** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…nce has emanated from Him, as will be explained (chap. lxv. and chap. lxvi.). The physical organs which are attribute…</q>

28. **PART I / CHAPTER XLVI; printed p. 63; h-4; xd32e6257** — adopted <code>ḥaliẓah</code>; source <code>ḥali ah</code>. Context: <q>…]phrase; e.g., a certain Rabbi has performed the act (of “ḥaliẓah”) with a slipper, alone and by night. Another Rabbi, ther…</q>

29. **PART I / CHAPTER XLVIII; printed p. 65; h-4; xd32e6312** — adopted <code>ib.</code>; source <code>ih.</code>. Context: <q>…gum of the passage, “And God saw the children of Israel” (ib. ii. 25), which is equal to “He saw their affliction and t…</q>

30. **PART I / CHAPTER LIV; printed p. 75; h-4; xd32e6446** — adopted <code>long-suffering</code>; source <code>longsuffering</code>. Context: <q>…r exclusively to His works, viz., “merciful and gracious, long-suffering and abundant in goodness,” etc., (Exod. xxxiv. 6). It is…</q>

31. **PART I / CHAPTER LX; printed p. 87; h-4; xd32e6577** — adopted <code>sense</code>; source <code>senst</code>. Context: <q>It is in this sense that some men come very near to God, and others remain ex…</q>

32. **PART I / CHAPTER LX; printed p. 88; h-4; xd32e6584** — adopted <code>knowledge</code>; source <code>knowlenge</code>. Context: <q>…that he who affirms attributes of God has not sufficient knowledge concerning the Creator, admits some association with God,…</q>

33. **PART I / CHAPTER LXI; printed p. 89; h-5; xd32e6632** — adopted <code>(</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…n Adoni, “my lord,” (with ḥirek under the nun), or Adonay (with kameẓ) is similar to the difference between Sari, “my…</q>

34. **PART I / CHAPTER LXII; printed p. 92; h-5; xd32e6763** — adopted <code>.</code>; source <code>,</code>. Context: <q>…cate it except to a son or a disciple, once in seven years. When, however, unprincipled men had become acquainted wit…</q>

35. **PART I / CHAPTER LXII; printed p. 92; h-5; xd32e6766** — adopted <code>Tetragrammaton</code>; source <code>Tetragrammeton</code>. Context: <q>…ce it when they blessed the people in the Temple; for the Tetragrammaton was then no longer uttered in the sanctuary on account of…</q>

36. **PART I / CHAPTER LXIII; printed p. 93; h-5; xd32e6797** — adopted <code>.</code>; source <code>,</code>. Context: <q>…is His name? what shall I say unto them?” (Exod. iii. 13). How far was this question, anticipated by Moses, appropri…</q>

37. **PART I / CHAPTER LXIII; printed p. 94; h-5; xd32e6809** — adopted <code>,</code>; source <code>.</code>. Context: <q>…e, you shall do this thing, or you shall not do that thing,” or “God has sent me to you.” Far from it! for God spoke…</q>

38. **PART I / CHAPTER LXIII; printed p. 95; h-5; xd32e6839** — adopted <code>the</code>; source <code>the the</code>. Context: <q>…m; or, in other words, He is “the existing Being which is the existing Being,” that is to say, the Being whose existenc…</q>

39. **PART I / CHAPTER LXIV; printed p. 96; h-5; xd32e6893** — adopted <code>?”</code>; source <code>”?</code>. Context: <q>…, as in the phrase “They shall say to me, What is his name?” Sometimes it stands for “the word of God,” so that “the n…</q>

40. **PART I / CHAPTER LXV; printed p. 97; h-5; xd32e6965** — adopted <code>congregation</code>; source <code>congragation</code>. Context: <q>…desire (omer) to slay me” (Exod. ii. 14); “And the whole congregation intended (va-yomeru) to stone them” (Num. xiv. 10). Insta…</q>

41. **PART I / CHAPTER LXVI; printed p. 98; h-5; xd32e7000** — adopted <code>,</code>; source <code>.</code>. Context: <q>…he same as that of “the work of thy fingers” (Ps. viii. 4), this being said of the heavens; of the latter it has been…</q>

42. **PART I / CHAPTER LXVI; printed p. 98; h-5; xd32e7005** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…iguratively expressed by terms denoting “word” and “speech.” The same thing which according to one passage has been m…</q>

43. **PART I / CHAPTER LXVI; printed p. 99; h-5; xd32e7012** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ngs were created on Friday in the twilight of the evening,” and “the writing” is one of the ten things. This shows ho…</q>

44. **PART I / CHAPTER LXVIII; printed p. 100; h-5; xd32e7127** — adopted <code>.</code>; source <code>,.</code>. Context: <q>…ple refute at once our principle by using such comparisons. Even amongst those who imagine that they are wise, many f…</q>

45. **PART I / CHAPTER LXVIII; printed p. 101; h-5; xd32e7149** — adopted <code>essence</code>; source <code>assence</code>. Context: <q>…thing different from its action, for the true nature and essence of the intellect is comprehension, and you must not think…</q>

46. **PART I / CHAPTER LXIX; printed p. 103; h-5; xd32e7314** — adopted <code>let</code>; source <code>ler</code>. Context: <q>…alet by hé—and as the series does not extend to infinity, let us stop at hé—there is no doubt that the hé moves the let…</q>

47. **PART I / CHAPTER LXXI; printed p. 108; h-5; xd32e7522** — adopted <code>Muʻtazilah</code>; source <code>Mu’tazilah</code>. Context: <q>…the Kalam, there arose among them a certain sect, called Muʻtazilah, i.e., Separatists. In certain things our scholars follow…</q>

48. **PART I / CHAPTER LXXI; printed p. 108; h-5; xd32e7525** — adopted <code>Muʻtazilah</code>; source <code>Mu’tazilah</code>. Context: <q>…our scholars followed the theory and the method of these Muʻtazilah. Although another sect, the Asha’ariyah, with their own p…</q>

49. **PART I / CHAPTER LXXI; printed p. 108; h-5; xd32e7528** — adopted <code>Muʻtazilah</code>; source <code>Mu’tazilah</code>. Context: <q>…chanced first to become acquainted with the theory of the Muʻtazilah, which they adopted and treated as demonstrated truth. On…</q>

50. **PART I / CHAPTER LXXI; printed p. 108; h-5; xd32e7531** — adopted <code>Muʻtazilah</code>; source <code>Mu’tazilah</code>. Context: <q>…uld also know that whatever the Mohammedans, that is, the Muʻtazilah and the Asha’ariyah, said on those subjects, [109]consist…</q>

51. **PART I / CHAPTER LXXI; printed p. 110; h-5; xd32e7552** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ligionists who imitated them and walked in their footsteps. Although the Mutakallemim disagree in the methods of thei…</q>

52. **PART I / CHAPTER LXXI; printed p. 111; h-5; xd32e7561** — adopted <code>.</code>; source <code>,</code>. Context: <q>…ustified, if it were assumed that the universe was eternal. We will not now expatiate on that subject. You should, ho…</q>

53. **PART I / CHAPTER LXXII; printed p. 118; h-5; xd32e7620** — adopted <code>benefactor</code>; source <code>benefector</code>. Context: <q>…hatever it grants, is granted in the manner of a generous benefactor, not from any selfish motive, but from a natural generosi…</q>

54. **PART I / CHAPTER LXXIII; printed p. 120; h-5; xd32e7695** — adopted <code>Mutakallemim</code>; source <code>Mutakellemim</code>. Context: <q>…bodies, a theory which in fact has been proposed by some Mutakallemim. All these atoms are perfectly alike; they do not differ…</q>

55. **PART I / CHAPTER LXXIII; printed p. 124; h-5; xd32e7749** — adopted <code>Muʻtazilah</code>; source <code>Mu’tazilah</code>. Context: <q>…Some of them, however, and they belong to the sect of the Muʻtazilah, say that there are accidents which endure for a certain…</q>

56. **PART I / CHAPTER LXXIII; printed p. 125; h-5; xd32e7772** — adopted <code>Muʻtazilah</code>; source <code>Mu’tazilah</code>. Context: <q>…or, in reality, no act can be ascribed to that power. The Muʻtazilah contend that man acts by virtue of the power which has be…</q>

57. **PART I / CHAPTER LXXIII; printed p. 127; h-5; xd32e7790** — adopted <code>Muʻtazilah</code>; source <code>Mu’tazilah</code>. Context: <q>…sts, death was continually replaced by death. Some of the Muʻtazilah hold that there are cases in which the absence of a physi…</q>

58. **PART I / CHAPTER LXXIV; printed p. 136; h-6; xd32e7923** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…is alike; why then is this flower red and that one yellow?” Some being must have determined the colour of each, and t…</q>

59. **PART I / CHAPTER LXXVI; printed p. 142; h-6; xd32e8024** — adopted <code>Kalām</code>; source <code>kalâm</code>. Context: <q>…and this would be contrary to the doctrine adopted by the Kalām that God is one. An examination of this argument shows th…</q>

60. **PART II / INTRODUCTION; printed p. 145; h-7; xd32e8095** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…e of an infinite number of finite magnitudes is impossible.</q>

61. **PART II / INTRODUCTION; printed p. 148; h-7; xd32e8261** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>Proposition XXVI.</q>

62. **PART II / CHAPTER IV; printed p. 157; h-7; xd32e8384** — adopted <code>intellectual</code>; source <code>intellecual</code>. Context: <q>…ossible in intellectual beings, the heavenly sphere is an intellectual being. But even a being that is endowed with the faculty…</q>

63. **PART II / CHAPTER IV; printed p. 157; h-7; xd32e8389** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ts rising and setting noticed in the circle of the horizon. This point, however, does not concern us at present; let…</q>

64. **PART II / CHAPTER XIII; printed p. 172; h-7; xd32e8632** — adopted <code>.</code>; source <code>,</code>. Context: <q>…tion of an agent, and for this reason it cannot be changed. Similarly there is, according to them, no defect in the g…</q>

65. **PART II / CHAPTER XIX; printed p. 185; h-7; xd32e8818** — adopted <code>has</code>; source <code>hass</code>. Context: <q>…eader of this treatise hear what I have to say. Aristotle has proved that the difference of forms becomes evident by th…</q>

66. **PART II / CHAPTER XX; printed p. 189; h-8; xd32e8848** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…d that it came into existence by itself, without any cause. Some assume that the heavens and the whole Universe came…</q>

67. **PART II / CHAPTER XX; printed p. 189; h-8; xd32e8850** — adopted <code>absurdity</code>; source <code>adsurdity</code>. Context: <q>…blished their present order. This opinion implies a great absurdity. They admit that animals and plants do not owe their exis…</q>

68. **PART II / CHAPTER XXIV; printed p. 196; h-8; xd32e8933** — adopted <code>thus</code>; source <code>thu</code>. Context: <q>…ronomy in describing all distances and magnitudes. It has thus been shown that the point round which the sun moves lies…</q>

69. **PART II / CHAPTER XXIX; printed p. 211; h-8; xd32e9087** — adopted <code>knowledge</code>; source <code>knowedge</code>. Context: <q>…criptural texts by the intellect, after having acquired a knowledge of demonstrative science, and of the true hidden meaning…</q>

70. **PART II / CHAPTER XXXVIII; printed p. 230; h-9; xd32e9568** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…dge of one thing leads us to the knowledge of other things. But [what we said of the extraordinary powers of our imag…</q>

71. **PART II / CHAPTER XL; printed p. 234; h-9; xd32e9609** — adopted <code>villainy</code>; source <code>villany</code>. Context: <q>…Babylon roasted in the fire. Because they have committed villainy in Israel, and have committed adultery with their neighbo…</q>

72. **PART II / CHAPTER XLI; printed p. 235; h-9; xd32e9637** — adopted <code>,</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…nsequence of the perfect action of the imaginative faculty, and after that the prophecy follows. This was the case wi…</q>

73. **PART II / CHAPTER XLI; printed p. 235; h-9; xd32e9639** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…that the prophecy follows. This was the case with Abraham. The commencement of the prophecy is, “The word of the Lor…</q>

74. **PART II / CHAPTER XLI; printed p. 235; h-9; xd32e9645** — adopted <code>unto</code>; source <code>unt</code>. Context: <q>…f the second form are these: “And Elohim (an angel), said unto Jacob, Rise, go up to Bethel” (Gen. xxxv. 1); “And Elohim…</q>

75. **PART II / CHAPTER XLIII; printed p. 239; h-9; xd32e9773** — adopted <code>.</code>; source <code>,</code>. Context: <q>…both contain the same letters, though in a different order. Take, e.g., the allegories of Zechariah (chap. xi. 7, sqq…</q>

76. **PART II / CHAPTER XLVII; printed p. 248; h-9; xd32e9963** — adopted <code>it is</code>; source <code>is it</code>. Context: <q>…s greater than the person that sleeps therein; as a rule, it is by a third longer. If, therefore, the bed of Og was nine…</q>

77. **PART III / CHAPTER II; printed p. 253; h-10; xd32e10130** — adopted <code>Ḥayyah</code>; source <code>Hayyah</code>. Context: <q>…ll; for “to whichever side it is the Divine Will that the Ḥayyah should move, thither the Ḥayyah moves,” in that quick man…</q>

78. **PART III / CHAPTER IV; printed p. 257; h-10; xd32e10515** — adopted <code>gilgal</code>; source <code>galgal</code>. Context: <q>…eaning the word has in the phrase: “Like a rolling thing (gilgal) before the whirlwind” (Isa. xvii. 13). The poll of the h…</q>

79. **PART III / CHAPTER V; printed p. 258; h-10; xd32e10598** — adopted <code>maʻaseh</code>; source <code>maaseh</code>. Context: <q>…exact words of the discussion are as follows:—Where does maʻaseh mercabhah end? Rabbi says, with the last va-ereh; Rabbi Y…</q>

80. **PART III / CHAPTER VII; printed p. 259; h-10; xd32e10668** — adopted <code>(</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…likeness of a firmament was over the heads of the Ḥayyot” (ver. 22); “as the appearance of a sapphire stone, the like…</q>

81. **PART III / CHAPTER X; printed p. 266; h-10; xd32e10813** — adopted <code>Consider</code>; source <code>Considet</code>. Context: <q>…. xlv. 7), for darkness and evil are non-existing things. Consider that the prophet does not say, I make (ʻoseh) darkness, I…</q>

82. **PART III / CHAPTER X; printed p. 267; h-10; xd32e10829** — adopted <code>permanence</code>; source <code>permanenee</code>. Context: <q>…e source of death and all evils, is likewise good for the permanence of the Universe and the continuation of the order of thin…</q>

83. **PART III / CHAPTER XXII; printed p. 296; h-11; xd32e11100** — adopted <code>Uẓ</code>; source <code>Uz</code>. Context: <q>First, consider the words: “There was a man in the land Uẓ.” The term Uẓ has different meanings; it is used as a pro…</q>

84. **PART III / CHAPTER XXII; printed p. 296; h-11; xd32e11103** — adopted <code>Uẓ</code>; source <code>Uz</code>. Context: <q>…s different meanings; it is used as a proper noun. Comp. “Uẓ, his first-born” (Gen. xxii. 21); it is also imperative o…</q>

85. **PART III / CHAPTER XXII; printed p. 296; h-11; xd32e11111** — adopted <code>Uẓ</code>; source <code>Uz</code>. Context: <q>…ice.” Comp. uẓu, “take counsel” (Isa. viii. 10). The name Uẓ therefore expresses the exhortation to consider well this…</q>

86. **PART III / CHAPTER XXIII; printed p. 302; h-11; xd32e11179** — adopted <code>Muʻtazilah</code>; source <code>Mu’tazilah</code>. Context: <q>…Scripture, Bildad’s opinion is identical with that of the Muʻtazilah, whilst Zofar defends the theory of the Asha’riyah. These…</q>

87. **PART III / CHAPTER XXXIV; printed p. 329; h-11; xd32e11482** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…ceed to the exposition of that which I intended to explain.</q>

88. **PART III / CHAPTER XXXVII; printed p. 338; h-12; xd32e11640** — adopted <code>at</code>; source <code>as</code>. Context: <q>…and the mixed species sown in a vineyard. I am surprised at the dictum of Rabbi Joshiyah, which has been adopted as l…</q>

89. **PART III / CHAPTER XL; printed p. 343; h-12; xd32e11725** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…king of the neck of the heifer in discovering the murderer. Force is added to the law by the rule that the place in w…</q>

90. **PART III / CHAPTER XLIII; printed p. 353; h-12; xd32e11839** — adopted <code>,</code>; source <code>.</code>. Context: <q>…on this day, as we have shown in Mishneh-torah. The day is, as it were, a preparation for and an introduction to the…</q>

91. **PART III / CHAPTER XLVI; printed p. 363; h-12; xd32e11968** — adopted <code>”</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…sun, the moon, the stars; they even worship their babuah.” The word babuah signifies “shadow.” Let us now return to…</q>

92. **PART III / CHAPTER XLIX; printed p. 380; h-13; xd32e12228** — adopted <code>,</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…“statutes” (ḥukkim), the reason of which is unknown to us, serve as a fence against idolatry. That I cannot explain…</q>

93. **PART III / CHAPTER LI; printed p. 388; h-13; xd32e12332** — adopted <code>.</code>; source <code>[absent — editorial insertion]</code>. Context: <q>…hat he is able to lead men up to this degree of perfection. It is only the next degree to it that can be attained by…</q>

<!-- END GENERATED PG CORRECTION LEDGER -->

### What remains unknown

- The words have not been checked against photographic pages of the 1910
  edition. The supplied PDF cannot answer that question because Calibre made it
  from the same transcription as the EPUB.
- Project Gutenberg marked 93 adopted corrections in the selected XHTML. Their
  visible adopted readings are retained and individually inventoried above,
  but their correctness cannot be verified without the print pages.
- No independent witness was supplied, so the exact token agreement must not be
  described as corroboration.

## Review

The pass that sets `complete`: read the run's escalations and notes to learn what the processing actually encountered, then read the text in the rendered reader, comparing against the source where something looks wrong. Not a full proofread — a judgement about whether it is shippable.

- [ ] Escalations and notes read
- [ ] Rendered in the reader; structure, headings and contents look right
- [ ] Spot-checked against the source where the notes flagged doubt
- [ ] Remaining known issues recorded below

<!-- review log — hand-written, never regenerated -->
