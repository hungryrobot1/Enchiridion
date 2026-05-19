# Quadrature of the Parabola

> "When I heard that Conon, who was my friend in his lifetime, was dead, but that you were acquainted with Conon and withal versed in geometry, while I grieved for the loss not only of a friend but of an admirable mathematician, I set myself the task of communicating to you, as I had intended to send to Conon, a certain geometrical theorem which had not been investigated before but has now been investigated by me, and which I first discovered by means of mechanics and then exhibited by means of geometry. Now some of the earlier geometers tried to prove it possible to find a rectilineal area equal to a given circle and a given segment of a circle; and after that they endeavoured to square the area bounded by the section of the whole cone and a straight line, assuming lemmas not easily conceded, so that it was recognised by most people that the problem was not solved. But I am not aware that any one of my predecessors has attempted to square the segment bounded by a straight line and a section of a right-angled cone [a parabola], of which problem I have now discovered the solution. For it is here shown that every segment bounded by a straight line and a section of a right-angled cone [a parabola] is four-thirds of the triangle which has the same base and equal height with the segment, and for the demonstration of this property the following lemma is assumed: that the excess by which the greater of (two) unequal areas exceeds the less can, by being added to itself, be made to exceed any given finite area. The earlier geometers have also used this lemma; for it is by the use of this same lemma that they have shown that circles are to one another in the duplicate ratio of their diameters, and that spheres are to one another in the triplicate ratio of their diameters, and further that every pyramid is one third part of the prism which has the same base with the pyramid and equal height; also, that every cone is one third part of the cylinder having the same base as the cone and equal height they proved by assuming a certain lemma similar to that aforesaid. And, in the result, each of the aforesaid theorems has been accepted no less than those proved without the lemma. As therefore my work now published has satisfied the same test as the propositions referred to, I have written out the proof and send it to you, first as investigated by means of mechanics, and afterwards too as demonstrated by geometry. Prefixed are, also, the elementary propositions in conics which are of service in the proof (στοιχεία κωνικά χρείαν ἔχοντα ἐς τὰν ἀπόδειξιν). Farewell."
>
> — Archimedes to Dositheus, prefatory letter to the *Quadrature of the Parabola*

## What Archimedes Set Out to Do

The letter to Dositheus states the result plainly. Take a parabola, and cut it with a straight line — the straight line is the *base* of the segment, and the part of the parabola cut off by it is the *segment*. Inside the segment, inscribe a triangle whose base is the same straight line and whose third vertex is the point on the parabola farthest from that base (the point where the tangent is parallel to the base). Archimedes claims:

> The area of the parabolic segment is four-thirds the area of the inscribed triangle.

This is the *quadrature*: the construction of a rectilineal area equal to a curvilinear one. The Greeks had quadratures for several special figures — the rectangle, the triangle, the parallelogram, certain lunes — but they did not have a general method for curved regions. Squaring the circle remained out of reach. Squaring the parabolic segment, Archimedes shows, is possible.

The treatise gives two proofs of this single result. The first is *mechanical*: Archimedes weighs the segment against the triangle on an imaginary lever, treating geometric figures as physical objects with weight distributed by area. The second is *geometric*: a strict, synthetic proof by exhaustion, using only the methods of Euclid. Archimedes himself describes the relation between the two: *first as investigated by means of mechanics, and afterwards too as demonstrated by geometry.* The mechanical proof is how he found the result. The geometric proof is how he established it.

This supplement follows that order. We sketch the mechanical reasoning first — briefly, since the central pedagogical work belongs to the rigorous proof — and then walk through the exhaustion argument step by step, with exercises that ask you to reconstruct each part for yourself.

## Prerequisites

Before working through this supplement, you should be comfortable with:

- The structure of a Euclidean proposition (see [Reading Greek Mathematics](../greek-math-companion/content.md))
- Euclid's theory of proportion (Book V), particularly the meaning of *A is to B as C is to D* and the technique of comparing magnitudes
- The basic elements of conic sections — at least, what a parabola is and how it is generated as a section of a cone (see again [Reading Greek Mathematics](../greek-math-companion/content.md))

You do not need to have read Apollonius's *Conics* in full. Archimedes assumes a handful of properties of the parabola, which we will state when needed.

## The Setup

Throughout the proof, fix the following configuration. Let $Qq$ be the chord that cuts off the segment of the parabola. Let $P$ be the point on the parabola whose tangent is parallel to $Qq$ — this is the *vertex* of the segment, the point of the parabola farthest from the base. The triangle $PQq$ is the *inscribed triangle*; call its area $T$. The parabolic segment is the region bounded by the chord $Qq$ and the curve.

The line through $P$ parallel to the axis of the parabola is the *diameter* of the segment. It bisects every chord parallel to $Qq$, including $Qq$ itself. Call $V$ the midpoint of $Qq$; then $PV$ lies along the diameter.

<!-- TODO: diagram showing parabolic segment with chord Qq, vertex P, midpoint V, inscribed triangle PQq -->

We want to show:

$$\text{(area of segment)} = \frac{4}{3} T$$

## Part I: The Mechanical Discovery

In the first part of the *Quadrature*, Archimedes weighs the parabolic segment against a triangle using the law of the lever — the same law established in *On the Equilibrium of Planes* and recapitulated in this program in the [Levers Lab](../archimedes-levers-lab/content.md). The argument runs roughly as follows.

Construct a lever, with the parabolic segment hanging from one end and a triangle (a different one, larger than $T$) placed along the other arm. Decompose both figures into thin strips parallel to the diameter of the segment. For each pair of corresponding strips — one from the segment, one from the triangle — Archimedes shows, using a property of the parabola, that they balance about a chosen fulcrum when the segment-strip is moved out to the end of the lever.

Summing over all the strips, the entire segment, hung at the end of the lever, balances the triangle distributed along its arm. The center of gravity of the triangle is known (it lies one-third of the way from base to vertex, by an earlier proposition), and so the lever-equation tells us the area of the segment in terms of the area of the triangle. The result that emerges is precisely

$$\text{(area of segment)} = \frac{4}{3} T.$$

Archimedes is candid that this argument is *not* a proof. It treats geometric figures as if they had weight; it assumes that an area can be decomposed into a sum of indivisible strips, each balanced individually. The Greek standard of demonstration does not admit such reasoning. But the argument *finds* the answer, and once the answer is known, the work of proving it rigorously can begin.

This is the procedure Archimedes elsewhere calls his *method*: discover by mechanics, demonstrate by geometry. He returns to it explicitly in his letter to Eratosthenes, in the treatise known as *The Method of Mechanical Theorems*. For now, what matters is that the value $\frac{4}{3} T$ is not pulled from the air. It is the conclusion of a physical argument, which the geometric proof must now justify.

### Exercise 1: The discovery vs. demonstration distinction

Explain why the mechanical argument, however suggestive, is not acceptable as a proof in the Greek tradition. What features of the argument make it *heuristic* rather than *demonstrative*? What would have to be added or replaced for it to meet the standard of the *Elements*?

Recall that the Greek standard of demonstration, as established in the *Elements*, requires every step to be justified by prior propositions, postulates, or definitions — never by appeals to physical intuition or to the behavior of infinitely many parts.

---

## Part II: The Geometric Proof by Exhaustion

The geometric proof — Propositions 18 through 24 of the *Quadrature* — establishes the result by an entirely different route. There is no lever, no balance, no decomposition into infinitesimal strips. There is a triangle, then triangles inside the gaps, then triangles inside those gaps, and a careful argument that the inscribed polygons exhaust the segment.

The strategy has three stages:

1. **Geometric construction**: build a sequence of inscribed polygons, each obtained from the previous one by adding triangles in the gaps, and show that the areas of the added triangles form a specific ratio at each stage.
2. **Summation**: sum the areas, recognizing that they form a geometric progression with ratio $\frac{1}{4}$, and show that the total approaches $\frac{4}{3} T$.
3. **Double reductio**: prove rigorously that the area of the segment cannot be greater than $\frac{4}{3} T$, and cannot be less than $\frac{4}{3} T$. Therefore it equals $\frac{4}{3} T$.

We take these in turn.

### Stage 1: The Inscribed Polygons

The first inscribed figure is the triangle $PQq$, with area $T$. The segment, however, contains regions outside this triangle: two smaller parabolic segments, one on each side, with bases $PQ$ and $Pq$ respectively.

For each of these smaller segments, repeat the construction. In the segment with base $PQ$, find the point on the parabola whose tangent is parallel to $PQ$; call it $P_1$. Inscribe the triangle $P_1 P Q$. Similarly, find $P_2$ in the segment with base $Pq$, and inscribe triangle $P_2 P q$. We now have an inscribed pentagon (or hexagon, depending on how you count): the original triangle plus two more triangles in the side-segments.

Archimedes proves a key lemma about the areas of these new triangles:

> Each of the two new triangles has area equal to one-eighth of $T$.

Together, the two new triangles add area $\frac{2}{8} T = \frac{1}{4} T$ to the inscribed figure. Continuing, each of the four new gaps will yield a triangle of area $\frac{1}{64} T$, four of which add $\frac{4}{64} T = \frac{1}{16} T$. The total inscribed area at each stage is:

$$T, \quad T + \tfrac{1}{4} T, \quad T + \tfrac{1}{4} T + \tfrac{1}{16} T, \quad T + \tfrac{1}{4} T + \tfrac{1}{16} T + \tfrac{1}{64} T, \quad \ldots$$

<!-- TODO: diagram showing the first three stages of inscribed polygons within the parabolic segment -->

The lemma — that each new triangle is one-eighth the area of the triangle in the segment that contains it — is the geometric core of the construction, and it depends on a specific property of the parabola, which Archimedes establishes earlier in the treatise. The property in modern paraphrase: if $V$ is the midpoint of a chord $Qq$ of a parabola and $P$ is the vertex of the corresponding segment, and if $V'$ is the midpoint of $PQ$ with $P'$ the vertex of the smaller segment cut off by $PQ$, then the distance from $P'$ to $PQ$ is one-quarter the distance from $P$ to $Qq$, while the base $PQ$ is half the corresponding base $Qq$. The triangles' areas — base times height, halved — are then in the ratio $\frac{1}{2} \times \frac{1}{4} = \frac{1}{8}$.

### Exercise 2: The one-eighth lemma

Using the property of the parabola stated above (that the distance from the new vertex $P'$ to the chord $PQ$ is one-quarter the distance from $P$ to $Qq$, and that the new base $PQ$ is half the original base $Qq$), verify directly that the area of the new triangle $P_1 P Q$ is one-eighth the area of $PQq$.

Hint: write the area of each triangle as half base times height, and form the ratio. Do not use coordinates; reason about the segments and their lengths.

### Stage 2: The Sum

The areas of the inscribed figures form a series:

$$S_n = T + \tfrac{1}{4} T + \tfrac{1}{16} T + \cdots + \tfrac{1}{4^n} T.$$

Archimedes does not have a notion of an infinite sum, nor does he take any limit. What he has, and what is in fact stronger for his purposes, is a finite identity that holds at every stage. He proves (Proposition 23):

> $T + \tfrac{1}{4} T + \tfrac{1}{16} T + \cdots + \tfrac{1}{4^n} T + \tfrac{1}{3} \cdot \tfrac{1}{4^n} T = \tfrac{4}{3} T.$

In other words, at each stage, if you add to the inscribed sum a *correction term* equal to one-third of the last triangle added, you obtain exactly $\frac{4}{3} T$. This identity is purely arithmetic, provable by direct manipulation, and it holds for every $n$.

The correction term $\frac{1}{3} \cdot \frac{1}{4^n} T$ is the bridge to the limit-style argument that follows. As $n$ increases, the last triangle added becomes arbitrarily small — and so does the correction. But Archimedes never says "in the limit." He says: at every stage, the inscribed sum differs from $\frac{4}{3} T$ by exactly this much, and this much can be made smaller than any specified area.

### Exercise 3: The geometric identity

Prove Proposition 23 directly: that for every positive integer $n$,

$$T + \tfrac{1}{4} T + \tfrac{1}{16} T + \cdots + \tfrac{1}{4^n} T + \tfrac{1}{3} \cdot \tfrac{1}{4^n} T = \tfrac{4}{3} T.$$

Do this by multiplying both sides by an appropriate factor and simplifying. The identity is purely about powers of $\frac{1}{4}$ and the constant $T$; no geometry is needed at this stage.

### Stage 3: The Double Reductio

We now have:

- A sequence of inscribed polygons whose areas approach $\frac{4}{3} T$ from below.
- The fact that at every stage, the inscribed sum is exactly $\frac{1}{3} \cdot \frac{1}{4^n} T$ short of $\frac{4}{3} T$.
- A general lemma — stated in the prefatory letter and used throughout exhaustion proofs — that *the excess by which the greater of two unequal magnitudes exceeds the less can, by being added to itself, be made to exceed any given finite area*. Equivalently: any positive magnitude, repeatedly halved, eventually becomes less than any prescribed magnitude. (This is sometimes called the Archimedean axiom, and it is essentially Euclid's Book X, Proposition 1.)

Let $K$ denote the area of the parabolic segment. Archimedes wants to show $K = \frac{4}{3} T$. He does this by ruling out the two alternatives.

**Case 1: Suppose $K > \frac{4}{3} T$.**

Then the difference $K - \frac{4}{3} T$ is a definite positive area. By the lemma, we can choose $n$ large enough that $\frac{1}{3} \cdot \frac{1}{4^n} T < K - \frac{4}{3} T$ — in fact, we can do better, and ensure that the area *outside* the inscribed polygon at stage $n$ (i.e., the union of the small remaining segments) is less than $K - \frac{4}{3} T$. But this means the inscribed polygon itself has area greater than $\frac{4}{3} T$. From the identity in Stage 2, however, the inscribed polygon at stage $n$ has area less than $\frac{4}{3} T$. Contradiction.

**Case 2: Suppose $K < \frac{4}{3} T$.**

Then the difference $\frac{4}{3} T - K$ is a definite positive area. Choose $n$ large enough that $\frac{1}{3} \cdot \frac{1}{4^n} T < \frac{4}{3} T - K$. Then by the identity, the inscribed polygon at stage $n$ has area greater than $\frac{4}{3} T - \frac{1}{3} \cdot \frac{1}{4^n} T > K$. But the inscribed polygon is contained in the segment, so its area cannot exceed $K$. Contradiction.

Both alternatives are impossible. Therefore $K = \frac{4}{3} T$.

### Exercise 4: Reconstructing Case 1

Write out Case 1 of the double reductio in your own words, paying attention to the use of the Archimedean lemma. Specifically, justify the step where we claim the area outside the inscribed polygon can be made smaller than any specified amount. Why does this follow from the lemma?

Hint: the area outside the inscribed polygon at stage $n$ is the sum of small "leftover" parabolic segments. Each is contained in a triangle (a circumscribed triangle with the same base, of which the inscribed triangle is one-half — Archimedes proves this in an earlier proposition). At each stage of subdivision, the leftover area is more than halved. Apply the lemma.

### Exercise 5: Why two cases?

Why does Archimedes need *both* cases — ruling out both greater and less — of the reductio to prove equality? Couldn't he prove the result by showing only that $K \leq \frac{4}{3} T$, since the inscribed polygons are always contained in the segment? Explain why or why not.

---

## Closing

The *Quadrature of the Parabola* contains a result and a method. The result is striking enough on its own — that an irrational, curvilinear area can be expressed exactly as a rational multiple of a triangle. But the method is the deeper achievement. Archimedes demonstrates that geometric reasoning can handle figures bounded by curves, provided one is patient enough to inscribe polygons within them and rigorous enough to rule out, by reductio, every alternative to the result one wishes to establish.

The double reductio depends critically on the Archimedean lemma — the principle that any positive magnitude, halved enough times, becomes smaller than any prescribed magnitude. This lemma is what makes the proof work without taking limits, without summing infinite series, without anything that the Greek standard of demonstration would refuse. The inscribed polygons never *reach* $\frac{4}{3} T$; they only get close enough that no other value can be the segment's area. That is enough.

You have now seen, in the act, what the method of exhaustion can do. Hold onto the experience. You will encounter related techniques again — both within Archimedes's own corpus and in the long arc of mathematical reasoning about curves and the regions they bound.

The full text of the *Quadrature* is in your library at `texts/1-ancient-greece/archimedes-heath-works`, in Heath's translation of the *Works of Archimedes*. The two proofs — mechanical and geometric — are presented in full there, with Heath's editorial commentary explaining the technical conic-section properties Archimedes assumes.
