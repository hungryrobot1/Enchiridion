All three components come out. The apparatus policy in ocr/README.md covers
them, and this is the case it was written for: the text's markdown carries the
text itself and nothing else.

1. MARGINAL SYNOPSES — remove. They are the editor's navigational furniture, not
   Al-Biruni's words, and printed in the margin precisely because they are not
   part of the sentence. That OCR has dropped them into the middle of sentences
   is the strongest argument for removing rather than relocating them: keeping
   them means guessing where each one belongs, and a wrong guess is invisible in
   the finished text. Join the interrupted sentences mechanically, with asserted
   anchors and counts as usual.

2. SACHAU'S ANNOTATIONS — remove, both volumes. Scholarly commentary and textual
   criticism by the translator is exactly what the policy names.

3. INDEX I and INDEX II — remove. A printed-book index addresses page numbers
   that no longer exist in a reflowed text; it is furniture of the paper object.

The smaller and safer main-text cleanup is the right outcome, not a compromise.
The apparatus is not destroyed — it remains in the source PDF.

On the images: that was our bug, not a gap in the text. Your source/ was
assembled by a script that copied files but not directories, so the three
images the corpus already holds never reached you. They exist. The dispatcher
has been fixed and source/images/ has been re-synced for this resume — you
should find img-0.jpeg, img-1.jpeg and img-2.jpeg there now. Do not reconstruct
them from the scan; just verify the references resolve.

Two notes for NOTES.md, since they are about us rather than the text. First,
you were right to stop rather than guess on the synopses; the relocation
question is genuinely ours. Second, if the missing images had not been raised,
we would not have found the bug — another run rebuilt eighteen figures from the
scan rather than ask, and that work was wasted.
