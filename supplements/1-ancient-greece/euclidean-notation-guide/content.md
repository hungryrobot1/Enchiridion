# Euclidean Notation Guide

Euclid's *Elements* uses geometric language that differs significantly from modern
mathematical notation. This guide maps Euclid's expressions to their modern equivalents
so you can follow the proofs while building fluency in both systems.

---

## Lengths and Segments

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "the line AB" | $\overline{AB}$ | Line segment from A to B |
| "AB is equal to CD" | $AB = CD$ | The lengths are equal |
| "let AB be produced to E" | Extend $\overline{AB}$ past B to E | Extend a line segment |
| "the point D on AB" | $D \in \overline{AB}$ | A point lying on a segment |

## Areas

Euclid describes areas in terms of the figures they bound, not as numerical quantities.

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "the square on AB" | $AB^2$ | Area of a square with side AB |
| "the rectangle contained by AB and CD" | $AB \cdot CD$ | Area of a rectangle with those sides |
| "the triangle ABC" | $\triangle ABC$ | The triangle with vertices A, B, C |

### Example: Proposition I.47 (Pythagorean Theorem)

Euclid states:

> In right-angled triangles the square on the side subtending the right angle
> is equal to the squares on the sides containing the right angle.

In modern notation:

$$a^2 + b^2 = c^2$$

where $c$ is the hypotenuse and $a$, $b$ are the other two sides.

## Proportion and Ratio

Euclid's Book V develops a theory of proportion that avoids irrational numbers
by comparing ratios geometrically.

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "A is to B as C is to D" | $\frac{A}{B} = \frac{C}{D}$ | The ratios are equal |
| "A has a greater ratio to B than C has to D" | $\frac{A}{B} > \frac{C}{D}$ | Ratio comparison |
| "A and B are commensurable" | $\frac{A}{B} \in \mathbb{Q}$ | Their ratio is rational |
| "A and B are incommensurable" | $\frac{A}{B} \notin \mathbb{Q}$ | Their ratio is irrational |

### Example: Incommensurability of the diagonal

Euclid proves (Book X, Proposition 117) that the diagonal of a square is
incommensurable with its side. In modern terms:

$$\frac{d}{s} = \sqrt{2} \notin \mathbb{Q}$$

## Angles

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "the angle BAC" | $\angle BAC$ | Angle at vertex A |
| "a right angle" | $90°$ or $\frac{\pi}{2}$ | A quarter turn |
| "the angles at the base are equal" | $\angle B = \angle C$ | Base angles of isosceles triangle |

## Circles

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "a circle with center A and radius AB" | Circle centered at $A$ with radius $r = AB$ | |
| "the circumference of the circle" | The circle itself (the curve, not the interior) | |
| "a straight line drawn from the center to the circumference" | Radius $r$ | |

## Common Notions and Postulates

Euclid's five common notions function as algebraic axioms:

1. Things equal to the same thing are equal to each other: if $a = c$ and $b = c$, then $a = b$
2. If equals are added to equals, the wholes are equal: if $a = b$, then $a + c = b + c$
3. If equals are subtracted from equals, the remainders are equal: if $a = b$, then $a - c = b - c$
4. Things which coincide with one another are equal
5. The whole is greater than the part: if $B \subset A$, then $A > B$

---

## Reading Strategy

When working through a Euclidean proposition:

1. **Read the enunciation** — the general statement of what will be proved
2. **Draw the diagram** — Euclid always constructs before proving; the diagram is part of the proof
3. **Follow the proof** — translate each step into modern notation if it helps
4. **Verify the conclusion** — check that the general statement has been established
