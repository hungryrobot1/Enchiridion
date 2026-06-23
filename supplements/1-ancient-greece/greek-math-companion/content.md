# Reading Greek Mathematics

If you were born in the last 100 years then it's likely that Greek mathematics will look unusual. The language is geometric instead of algebraic. Arguments are conveyed through the use of prose and diagrams, the notation is sparse, and its proofs are followed using deduction. This guide is meant to help make Greek style mathematics more legible so that you can engage the primary sources on their own terms rather than translating them into something that they are not.

The primary backdrop is Euclid. The *Elements* establishes the form of a Greek mathematical proposition and the conventions you will see echoed, across thousands of years, throughout the rest of the corpus. Most of this guide is therefore about reading Euclid. Two shorter sections at the end orient you to Apollonius and Ptolemy — both of whom assume Euclidean fluency and add their own concerns: Apollonius extends the geometric method to the curves obtained from cones, and Ptolemy uses geometry to build a working model of the heavens. This supplement need not be fully understood all at once. Give it a quick read to gain an impression of things, then revisit as necessary.

---

## The Structure of a Greek Proposition

A proposition in the Euclidean style has a distinctive form. Once you learn to see it, the prose stops feeling dense and starts feeling clear. The traditional six parts are:

1. **Enunciation (πρότασις)** — the general statement of what is to be proved or constructed. No letters yet, no diagram. Just the claim in its general form.
2. **Setting-out (ἔκθεσις)** — the general claim is instantiated in a specific figure. Letters are introduced. "Let ABC be a triangle..."
3. **Specification (διορισμός)** — a restatement of what is to be proved, but now in terms of the lettered figure. "I say that the angle BAC is equal to the angle ACB."
4. **Construction (κατασκευή)** — auxiliary lines, points, and circles are added to the figure as needed for the proof. Every construction step is justified by a postulate or a previous proposition.
5. **Proof (ἀπόδειξις)** — the demonstration proper, drawing on the constructed figure, the common notions, postulates, and previous propositions.
6. **Conclusion (συμπέρασμα)** — a restatement of the original enunciation, now established. Often closes with "which was to be demonstrated" (ὅπερ ἔδει δεῖξαι, the famous Q.E.D.).

Not every proposition has all six parts, and sometimes they blur the boundaries, but the shape is always there. If a proposition feels disorienting, remember that it follows this structure.

In Euclid, a diagram is not a mere illustration. It is part of the argument. A proposition reasons about the figure in front of it, constructed in a way that is permitted by previous assumptions and proofs. When working through propositions for yourself, draw — and label — your own version in a separate notebook. Reading without drawing the figures is only half-reading.

Also, diagrams are seldom static. The construction step rarely produces the final figure all at once; the proof itself often adds further lines, points, or circles as the argument requires, and indirect proofs frequently introduce a hypothetical configuration that is then shown to lead to a contradiction. Expect the figure to grow and shift as you read. When a proof introduces a new line "let CD be drawn" mid-argument, add it to your own diagram before continuing.

The final version of the diagram is usually the one provided in the text. When doing initial constructions for yourself, follow what is said in the proposition instead of simply copying the diagram.

---

## Reading Euclid

The notation that follows is what Euclid actually uses, paired with the modern symbols you may already know. Use the modern column to anchor the meaning; use the Euclid column to recognize the phrasing when you encounter it.

### Lengths and Segments

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "the line AB" | $\overline{AB}$ | Line segment from A to B |
| "AB is equal to CD" | $AB = CD$ | The lengths are equal |
| "let AB be produced to E" | Extend $\overline{AB}$ past B to E | Extend a line segment |
| "the point D on AB" | $D \in \overline{AB}$ | A point lying on a segment |
| "AB is parallel to CD" | $AB \parallel CD$ (also written $AB \mathbin{/\mkern-5mu/} CD$) | The lines do not meet, however far produced |

### Areas

Euclid describes areas in terms of the figures they bound, not as numerical quantities.

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "the square on AB" | $AB^2$ | Area of a square with side AB |
| "the rectangle contained by AB and CD" | $AB \cdot CD$ | Area of a rectangle with those sides |
| "the triangle ABC" | $\triangle ABC$ | The triangle with vertices A, B, C |

#### Example: Proposition I.47 (Pythagorean Theorem)

Euclid states:

> In right-angled triangles the square on the side subtending the right angle
> is equal to the squares on the sides containing the right angle.

In modern notation:

$$a^2 + b^2 = c^2$$

where $c$ is the hypotenuse and $a$, $b$ are the other two sides.

### Proportion and Ratio

Euclid's Book V develops a theory of proportion that compares ratios geometrically rather than reducing them to numerical fractions. This was essential because the Greeks had no general notion of irrational numbers — and yet they needed to reason about ratios like that of a square's diagonal to its side.

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "A is to B as C is to D" | $A : B :: C : D$ or $\frac{A}{B} = \frac{C}{D}$ | The ratios are equal (a *proportion*) |
| "A has a greater ratio to B than C has to D" | $\frac{A}{B} > \frac{C}{D}$ | Ratio comparison |
| "A and B are commensurable" | $\frac{A}{B} \in \mathbb{Q}$ | Their ratio is rational |
| "A and B are incommensurable" | $\frac{A}{B} \notin \mathbb{Q}$ | Their ratio is irrational |

The four-term form $A : B :: C : D$ is the classical written form of a proportion and you will see it throughout older mathematical texts. Read the double colon as "as": "A is to B as C is to D."

#### The definition of "same ratio" (Book V, Definition 5)

The technical heart of the theory of proportion is the definition of when two ratios are the same. It is attributed to Eudoxus, and it is one of the most sophisticated definitions in pre-modern mathematics:

> Magnitudes are said to be in the same ratio, the first to the second and the third to the fourth, when equal multiples of the first and the third either both exceed, are both equal to, or are both less than, equal multiples of the second and the fourth, respectively, being taken in corresponding order, according to any kind of multiplication whatever.

In symbols: $A : B :: C : D$ exactly when, for every pair of positive integers $m$ and $n$, the comparisons $mA$ vs $nB$ and $mC$ vs $nD$ always come out the same way (both greater, both equal, or both less).

What makes this definition powerful is that it works for incommensurable magnitudes. It does not assume the ratios are expressible as fractions; it characterizes equality of ratio entirely in terms of comparisons. It is worthwhile to become very familiar with this definition.

#### Example: Incommensurability of the diagonal

Euclid proves (Book X, Proposition 117) that the diagonal of a square is incommensurable with its side. In modern terms:

$$\frac{d}{s} = \sqrt{2} \notin \mathbb{Q}$$

### Angles

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "the angle BAC" | $\angle BAC$ | Angle at vertex A |
| "a right angle" | $90°$ or $\frac{\pi}{2}$ | A quarter turn |
| "the angles at the base are equal" | $\angle B = \angle C$ | Base angles of isosceles triangle |

### Circles

| Euclid | Modern | Meaning |
|--------|--------|---------|
| "a circle with center A and radius AB" | Circle centered at $A$ with radius $r = AB$ | |
| "the circumference of the circle" | The circle itself (the curve, not the interior) | |
| "a straight line drawn from the center to the circumference" | Radius $r$ | |

### Common Notions and Postulates

Euclid's five common notions function as algebraic axioms:

1. Things equal to the same thing are equal to each other: if $a = c$ and $b = c$, then $a = b$
2. If equals are added to equals, the wholes are equal: if $a = b$, then $a + c = b + c$
3. If equals are subtracted from equals, the remainders are equal: if $a = b$, then $a - c = b - c$
4. Things which coincide with one another are equal
5. The whole is greater than the part: if $B \subset A$, then $A > B$

The five postulates state what constructions are permitted: drawing a straight line between any two points, extending a finite line, drawing a circle with any center and radius, the equality of all right angles, and — the famous fifth — the parallel postulate.

#### The Parallel Postulate

The fifth postulate stands apart from the other four. Where they are short and immediately self-evident, this one is longer and feels more like a theorem than an assumption:

> If a straight line falling on two straight lines makes the interior angles on the same side less than two right angles, the two straight lines, if produced indefinitely, meet on that side on which are the angles less than two right angles.

In plainer terms: if a transversal cuts two lines such that the interior angles on one side sum to less than 180°, the two lines, extended far enough, will meet on that side.

For roughly two thousand years, mathematicians tried to prove this postulate from the other four to no avail. The persistence of the attempt, and its eventual resolution, are part of the long arc of geometry as a discipline. For now it is enough to notice the postulate's awkwardness and how sparingly it is used in Book I.

### Reading Strategy

When working through a Euclidean proposition:

1. **Read the enunciation** — the general statement of what will be proved.
2. **Draw the diagram** — Euclid always constructs before proving; the diagram is part of the proof.
3. **Identify the parts** — find the setting-out, specification, construction, and proof. Knowing where you are in the proposition makes the prose easier to follow.
4. **Translate as needed** — render each step into modern notation if it helps, but do not lose contact with the geometric statement; the geometric statement is the proof.
5. **Verify the conclusion** — check that the general statement has been established by what was demonstrated in the specific figure.

---

## Reading Apollonius

Apollonius of Perga wrote the *Conics* roughly a century after the *Elements*, and the work assumes the reader is fluent in Euclid. The propositions follow the same six-part structure, the diagrams carry the same argumentative weight, and the notation is the same. What is new is the subject and the method.

### Conics from cones, literally

![img-0.jpeg](images/img-0.jpeg)

A *conic section* is exactly what its name says: a curve obtained by slicing a cone. Imagine a double cone — two cones joined at their apex, opening in opposite directions — and pass a plane through it. Depending on the angle of the cut, you get a different curve:

- A cut parallel to the base of the cone yields a **circle**.
- A cut at a slight angle to the base yields an **ellipse** — a closed, oval curve.
- A cut parallel to the slant side of the cone yields a **parabola** — an open curve that goes off to infinity.
- A cut steep enough to pass through both halves of the double cone yields a **hyperbola** — two separate open branches.

Apollonius derives the properties of these curves directly from this geometric origin. When he establishes a relation between distances on the curve and distances along reference lines, the relation is read off the cone, not posited algebraically. This is what makes the *Conics* feel so different from a modern treatment: every property of every curve has a geometric provenance traced back to the original solid.

### The parameter

A central technical idea in Apollonius is the *parameter* of a conic, or what later mathematicians call the *latus rectum*. For a parabola, the parameter is the length of a particular line segment associated with the curve, defined so that the square on any ordinate (the perpendicular from a point on the curve to the axis) is equal to the rectangle contained by the abscissa (the corresponding distance along the axis) and the parameter.

In modern algebraic notation, this is the relation $y^2 = px$, where $p$ is the parameter. But Apollonius does not write it as an equation. He states it as an equality of areas: *the square on the ordinate is equal to the rectangle contained by the abscissa and the parameter.* The geometric content is the same, but the framing is areal, not algebraic.

The names *parabola* (παραβολή, "application"), *ellipse* (ἔλλειψις, "deficiency"), and *hyperbola* (ὑπερβολή, "excess") refer precisely to whether this areal relation holds exactly, falls short, or exceeds — a vocabulary inherited from Greek techniques of "application of areas" that goes back to Pythagorean mathematics.

### Analysis within geometry

The deeper methodological move in Apollonius is the introduction of analytic reasoning into a still-synthetic framework. Euclid's *Elements* is almost entirely synthetic: it builds outward from postulates and earlier propositions, constructing what is needed and then proving the desired result. Apollonius does this too — but he also uses what was called *analysis*: assuming the desired result, working backwards to determine what conditions or constructions would make it true, and then reversing the reasoning into a synthetic proof.

When you read Apollonius, expect propositions that feel longer and more involved than Euclid's. The diagrams have more lines. The proofs chain more steps. But the structure is the same, and the reward for sustained attention is seeing the whole apparatus of conic geometry built up from nothing more than the Greek geometer's standard tools.

---

## Reading Ptolemy

Ptolemy's *Almagest* is a different kind of book from the *Elements* or the *Conics*. It is a geometric model of the heavens, based on observational data. This model is capable of forecasting the positions of celestial bodies: the sun, moon, planets, and stars. While propositions still have the Euclidean shape, they support a larger work whose aim was not purely mathematical, but practical, philosophical, and metaphysical. Reading Ptolemy well requires some orientation to the sky he is describing and the conventions he uses to describe it.

### The celestial sphere and the fixed stars

To a naked-eye observer, the stars appear to be set on the inside of an enormous sphere — the *celestial sphere* — that rotates once a day around an axis passing through the Earth. The sphere carries the patterns of the constellations, and these patterns do not change perceptibly over a human lifetime; this is what the ancients meant by the *fixed stars*. Ptolemy treats the celestial sphere as a working geometric object: he identifies its poles (the celestial poles, around which it appears to rotate), its equator (the great circle equidistant from the poles), and the great circles of reference used to locate any object on it.

The sun, moon, and planets do not stay fixed relative to the stars. They move against the stellar background, each on its own schedule. Most of the *Almagest* is concerned with these moving bodies — building geometric models that reproduce their observed motions as precisely as their measurements would allow.

### The ecliptic and the zodiac

The sun's apparent path against the fixed stars over the course of a year is a great circle on the celestial sphere called the *ecliptic*. It is tilted relative to the celestial equator by about 23° — the obliquity of the ecliptic — which is what produces the seasons.

The band of sky extending a few degrees on either side of the ecliptic, within which the moon and planets are always found, is the *zodiac*. The Greeks divided this band into twelve equal segments of 30° each, named after the constellations that originally fell within them: Aries, Taurus, Gemini, and so on. When Ptolemy gives the position of a planet, he typically gives its longitude along the ecliptic — measured in degrees within a particular zodiacal sign — and its latitude perpendicular to the ecliptic.

The zodiacal coordinate system is older than Ptolemy and is the standard frame of reference throughout the *Almagest*. Once you can read positions in this system — "the planet is at 15° Taurus" meaning 15° into the second sign of the zodiac, i.e., 45° from the vernal equinox — most of the observational reports become legible.

### The sexagesimal system

Ptolemy inherits his number system from Babylonian astronomy. Where the Greeks normally counted in tens, astronomical computation in the *Almagest* uses *sexagesimal*: base 60. A circle is divided into 360 degrees; each degree into 60 minutes; each minute into 60 seconds. Lengths and times are similarly subdivided into sixtieths.

The system survives today: it is why an hour has 60 minutes and a minute has 60 seconds, and why a degree of arc has the same subdivisions. When you see a value like "23° 51′ 20″" in the *Almagest*, that is 23 degrees, 51 minutes, 20 seconds — read it the way you would read a duration in hours, minutes, and seconds.

Ptolemy also uses sexagesimal fractions for purely numerical quantities, including the chord-table values that underlie all his trigonometric calculation. The chord table — the *Almagest*'s analog of a sine table — gives the length of the chord subtended by any arc of a circle of given radius, with arc and chord both expressed in sexagesimal units.

### Deferents and epicycles

The geometric model at the center of the *Almagest* is built from circles. Each celestial body — the sun, the moon, and each of the five visible planets — moves on a circle called the *deferent*, whose center is at or near the Earth. For the sun and moon this is most of the picture, but for the planets, this is not enough.

The planets exhibit an irregularity that simple deferent motion cannot reproduce: every so often, a planet appears to slow, stop, reverse direction against the background of the fixed stars, stop again, and then resume its forward motion. This anomaly is *retrograde motion*. Ptolemy accounts for it with a second circle: the planet does not ride on the deferent itself, but on a smaller circle called the *epicycle*, whose center moves along the deferent. The planet's actual position is determined by combining two motions — the slow circulation of the epicycle's center along the deferent, and the faster circulation of the planet around the epicycle. When the two motions reinforce each other, the planet appears to move forward; when they oppose each other, it appears to move backward.

This is the fundamental shape of Ptolemaic astronomy: circles upon circles, deferent and epicycle, modeled to account for observational data. To make the model match observation more precisely, Ptolemy introduces a further refinement called the *equant* — a point near, but not at, the center of the deferent, about which the motion of the epicycle's center is uniform. The equant is mathematically subtle and was the most controversial element of the model, both in late antiquity and in the centuries that followed; for now it is enough to know that it exists and that it is what allows the model to fit the data.

When you encounter the planetary models in the later books of the *Almagest*, you will see this apparatus in action: a deferent, an epicycle, often an equant, and a careful argument linking the geometry of the configuration to the longitude of the planet at a given moment.

### What to expect from the propositions

The propositions in the *Almagest* tend to be longer than those in Euclid because they often combine geometric demonstration with numerical computation. A typical proposition might prove a geometric relation among angles or chords, then apply the chord table to compute a specific value, then compare that value with observation. The Euclidean structure is still present underneath, but it is in service of an astronomical conclusion rather than a purely geometric one. The diagrams are abstract — circles and chords on a page — but they are always representing real configurations of the heavens, real observations, and your understanding will deepen if you keep that correspondence active.
