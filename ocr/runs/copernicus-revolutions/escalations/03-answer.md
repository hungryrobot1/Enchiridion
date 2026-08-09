Stopping was right, and every proposal you made is authorized as stated.

- `[Earlier version:]` and both of its long forms → like `[Earlier draft:]`:
  remove the label and the variant.
- `[Printed version:]` → like `[Printed text:]`: **remove the label, keep the
  passage.** You spotted the asymmetry without being told it, and it is the one
  that matters: that passage is the received text, so deleting it would delete
  the work.
- `[Deleted in the autograph:]` → like `[Deleted version:]`: remove label and
  passage.

The prose labels and the standalone notices go too, with the passages they
introduce. They are the editor speaking about the manuscript's history.

## One guard, on the prose labels only

The bracketed labels are safe because they are delimited: the label names its
own extent. The prose labels are not, and your rule for them — "stop at the next
explicit received-text label or validated chapter boundary" — is a heuristic
standing where a delimiter should be. If it overshoots, it eats Copernicus, and
nothing downstream can tell: the result is well-formed, passes every check, and
reads fluently because what follows a deleted passage is also his prose.

So for **each** prose-label removal, and only these:

1. Render the printed page and read where the rejected passage actually ends.
2. Record the page, the label, and the **first six words kept after the cut**.
3. If the boundary is not legible on the page, do not cut. Leave the passage in
   place, marked, and list it for the reviewer.

That gives a reviewer a bounded list they can check without re-deriving your
analysis, and it turns the one unbounded operation in this run into a witnessed
one. Four prose labels and a handful of notices is a small enough set to afford
this.

## Then the counts, as before

Report removals by label form, including the new ones. Give the before/after
count of all bracketed spans and account for the difference exactly — the
translator's in-sentence interpolations must survive untouched, and that
subtraction is what proves it.

Everything else stands: verify the 140 images resolve where the text calls for
them, leave doubtful table figures unrepaired and page-indexed, propose at
`needs-review`, and open `NOTES.md` with `## For the reviewer`.
