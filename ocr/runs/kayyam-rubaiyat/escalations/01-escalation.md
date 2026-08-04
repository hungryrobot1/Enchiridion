# Escalation

Two related decisions block taking this text beyond the current machine-checked
draft.

1. **Which edition scope does the library intend?** The supplied Gutenberg
   volume contains both a 75-stanza `First Edition` and a 101-stanza `Fifth
   Edition`, and the current draft retains both. But `source/metadata.json` gives
   `year_translated: 1859`, which describes the First Edition rather than the
   undated dual-edition volume as a whole. The stage documents do not say whether
   multiple revisions by the same translator are one collected text or whether
   the metadata year should narrow the source to one revision. If the intended
   work is the 1859 text only, the Fifth Edition must be excluded by the
   converter. If both belong, the adopted metadata needs review so it does not
   imply that the whole file is the 1859 version.

2. **What may serve as the correctness witness?** The EPUB and PDF are sibling
   renderings of one Project Gutenberg transcription. Exact agreement proves
   that the converter is faithful to that transcription, but it cannot expose a
   shared copying error. The PDF itself demonstrates the problem: p.18 visibly
   renders the First Edition's stanza 49 as `XLVIX.`, while the Fifth Edition
   uses the regular `XLIX.`. I preserved the supplied mark and did not invent a
   correction. Further proofreading needs either an independent scan of the
   relevant printed edition(s), supplied in `source/`, or permission to search
   the network for one. Network acquisition was not attempted because the run's
   instructions make that permission a user decision.

Please say whether to keep both editions or only the First, and either provide
an independent scan or authorize a network search if correctness checking beyond
Gutenberg-source fidelity is wanted.
