# The computation arc against the rights ledger

The question this file exists to answer, together: **which texts are
non-negotiable for the curriculum, irrespective of copyright status?** Not
because copyright will be ignored, but because the design question has to be
asked cleanly before the rights question is allowed to answer it. §8 is where
this bites — the least settled canon in the program, and the most load-bearing
for the practical-skills culmination.

The evidence base is `RIGHTS_AUDIT.md` (per-text verdicts, 2026-08-14, with the
renewal-cluster corrections of 2026-08-19) and the module metadata, which
records what each chapter actually plans to read. Every claim below traces to
one of those. Verdicts as of 2026-08-25.

One structural fact first, from the audit work: **no encumbered text is in the
syllabus, and all 25 supplements that point at encumbered texts are stubs.**
Nothing built depends on anything we cannot keep. The cost of any decision
below is the cost of a plan.

## Module 5 — Computation from First Principles

The spine of this module is now almost entirely clear, which was not true two
weeks ago.

- Boole, *Laws of Thought* — clear (1854)
- Leibniz, *Explanation of Binary Arithmetic* — translation needed; **the
  chosen pilot**, from the public-domain French (Gerhardt VII / the 1703
  *Mémoires*)
- Shannon, *A Symbolic Analysis of Relay and Switching Circuits* — **clear**,
  settled 2026-08-19
- Shannon, *A Mathematical Theory of Communication* — **clear**, settled
  2026-08-19
- von Neumann, *First Draft of a Report on the EDVAC* — **clear**; the 1945
  Moore School typescript is treated as public domain by every archive that
  hosts it, including the Smithsonian's own copy
- Lovelace, *Sketch of the Analytical Engine* — clear (1843)
- Turing, *On Computable Numbers* — **the tension.** In copyright in the US
  until 1 January 2032 (URAA; UK-PD since 2025). Chapter 8 is built around it,
  and there is no substitute: the chapter's argument *is* Turing's construction.
  Options: ask LMS/Wiley for permission now, or teach the chapter around a text
  we cannot show until 2032.

**Design question 5.** Is chapter 8 deferrable to 2032, or is the Turing ask
worth making this year? (My read: this is the single most non-negotiable text
in the era, and the ask costs a letter.)

## Module 6 — Programming Languages

This is where the ACM wall stands. The module's plan touches eleven texts;
the wall holds six of them.

- Backus, *Can Programming Be Liberated…* — copyrighted, ACM 1978
- Church, *Calculi of Lambda-Conversion* — copyrighted, renewal found, until
  2037
- Church, *An Unsolvable Problem…* — **clear**, settled 2026-08-19
- Curry, *Functionality in Combinatory Logic* — **clear**, settled 2026-08-19
- McCarthy, *Recursive Functions…* — copyrighted; the CACM issue was
  positively renewed
- Ritchie, *Development of C* / Ritchie-Thompson, *UNIX* — undetermined, ACM
  author-agreement era; our UNIX copy is also a third-party re-creation, not
  the published text
- Dijkstra, *Go To Statement* — copyrighted, CACM 1968
- Dijkstra, *Notes on Structured Programming* — copyrighted, Academic Press,
  in print
- Wadler, *Propositions as Types* — undetermined; no licence in the file;
  the author's own free posting is not a licence. **Wadler is alive and
  famously open — this is the era's most promising permission ask.**
- Martin-Löf, *On the Meanings of the Logical Constants* — copyrighted; the
  1996 typescript carries no licence
- Hoare, *An Axiomatic Basis* — copyrighted, CACM 1969

The lambda-calculus chapter can stand on cleared texts alone (Church 1936 +
Curry). The chapters that cannot currently show their primary text at all:
LISP (McCarthy), C/UNIX (Ritchie), structured programming (Dijkstra), Hoare
logic (Hoare), and the Backus opening.

**Design question 6a.** Are McCarthy, Dijkstra's *Go To*, and Hoare
non-negotiable? All three are short CACM papers; permission from ACM would
clear the module's spine in one ask. ACM made its 1951–2000 backfile free to
*read* in 2022, which is not a redistribution licence but is evidence of
posture, and names exactly who to write to.

**Design question 6b.** Where primary texts stay walled, does the module teach
from the *ideas with attribution* (a supplement that presents Hoare triples,
which no one owns) while linking out to the paper? That is a real pedagogical
mode, but it is the lecture-shaped thing the program refuses everywhere else.
Deciding it here decides it for the era.

## Module 7 — DSA / Complexity

- Cook, *Complexity of Theorem-Proving Procedures* — copyrighted, ACM 1971
- Karp, *Reducibility Among Combinatorial Problems* — **our file is not the
  paper** (a course slide deck); the real thing is Springer-held, 1972

Cook-Karp is the NP-completeness chapter. Same ACM ask as 6a covers Cook;
Karp needs sourcing before any rights question is even real.

## Module 4 — Foundations of Modern Mathematics (the older tensions)

- Abel, memoir — translation needed; **Pesic permission lead recorded in
  WITHHELD.md**, else retranslate from Sylow-Lie 1881
- Galois, memoir — translation already on the standing backlog; same chapter
- Gödel — parked; every English translation blocked or partial. The German
  original clears US term on 1 January 2027, which makes an Enchiridion
  translation from the original a **2027 project, not a blocked one**
- Riemann, *On the Hypotheses…* — **no source file at all**; Clifford's 1873
  translation is public domain, so this is acquisition, not rights

## The information-theory and biology threads (§8, outside the modules)

- RSA — undetermined, CACM 1978; same ACM conversation as 6a
- Diffie-Hellman — copyrighted, IEEE 1976
- Watson-Crick / Wilkins / Franklin — Springer Nature; ask recorded in
  WITHHELD.md. The 1953 DNA papers are three pages each; if any fair-use
  position survives anywhere, short papers read whole in a teaching context
  is where — but that is a deliberation, not a default
- Woese ×2, Sanger, Nirenberg-Matthaei, Mullis — journal-held; Mullis closed
  (Nobel Foundation asserts regardless of age)

## What falls out

1. **Three permission asks cover most of the era's spine**: ACM (McCarthy,
   Dijkstra, Hoare, Cook, Backus, Codd, RSA in one conversation), LMS/Wiley
   (Turing), Wadler (his own paper). A fourth, Springer Nature, covers the
   DNA thread.
2. **The translation pilot (Leibniz) is already the right first move** — it
   serves module 5 directly and its chapter is otherwise fully clear.
3. **The humanities strays in §8** (Arendt, McLuhan, Fanon, Weil, Strauss,
   O'Connor, the screenplays) carry no module load at all. Their question is
   purely curricular — does the era *need* them — and can wait without
   blocking anything.

