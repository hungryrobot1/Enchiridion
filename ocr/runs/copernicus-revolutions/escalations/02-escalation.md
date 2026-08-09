# ESCALATION: do authorial draft variants stay?

The OCR reveals critical apparatus interleaved with the translated work. The
editors print Copernicus's deleted or earlier draft wording, introduced by
editorial labels such as `[Earlier draft:]`, `[Printed text:]`, `[Deleted
version:]`, and `[In the autograph ... Copernicus subsequently deleted:]`.

Should the proposed text:

1. remove both the editorial labels and the rejected/alternate authorial
   passages as critical apparatus, retaining only the printed text selected by
   the edition; or
2. retain the alternate authorial passages, while mechanically preserving the
   editorial labels that distinguish them from the received text?

This is not the ordinary bracket rule. Translator-supplied brackets inside
sentences clearly stay, and editor-written comments clearly come out. Here the
words following the editor's label are Copernicus's, but they are presented as
deleted or superseded variants rather than as part of the finished work.
Removing them risks deleting the author; retaining them risks making rejected
drafts read as the work. The current apparatus policy does not say which side
critical variants fall on.

Representative printed pages (printed number = prepared/OCR page + 1 after the
front matter) are:

- pp. 25-27: more than two manuscript pages deleted by Copernicus, followed by
  editorial explanations of the original Book I/II plan;
- pp. 80, 125, 128, and 134: alternating `[Earlier draft:]` / `[Printed text:]`
  blocks and a passage Copernicus subsequently deleted;
- p. 154: a `[Deleted version:]` plus a marginal note described as inserted in
  the wrong place, deleted, and restored by the editors;
- pp. 226-227, 277, 305, 312, and 321: further printed/deleted/earlier-version
  blocks.

What turns on the answer: the stage-3 builder, heading sequence, paragraph
rejoins, image-context windows, and final word count. I have not edited the OCR
text while this is unresolved. `raw/copernicus-revolutions-ocr.md` preserves the
returned OCR byte-for-byte; `copernicus-revolutions.md` is currently an
identical working copy.

Work completed safely before stopping:

- baseline triad/census diagnostics were run;
- all 140 image references resolve one-to-one to all 140 files, with no orphan
  or duplicate paths;
- all 140 image/context mappings were visually reviewed on 14 contact sheets;
  every diagram agreed with its immediate geometric context, and no wrong
  attachment was found;
- no table digit was changed.
