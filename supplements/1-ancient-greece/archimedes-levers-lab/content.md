# Levers and the Law of the Lever

> Deriving the law of the lever from Archimedes's postulates, then testing it with balance experiments — from ratio to measurement, and back again

If you've already started reading Euclid, then Archimedes's approach will feel somewhat familiar. The key difference is that this work deals with the physical domain instead of pure geometry. Here, Archimedes laid down postulates about balance, and from those postulates he mathematically proved physical facts. This is one of the earliest surviving examples of physics derived *deductively* rather than empirically. No experiments are reported in this treatise. He does not say "I balanced two stones on a ruler and here is what I observed." He says: equal weights at equal distances are in equilibrium. That is a postulate, from which he derived theorems.

It is worth asking: where did these postulates come from?

In his writing, there is no groundwork discussion, no argument from prior authority, no appeal to experiment. Only the seven claims appear, and the propositions follow. The reader is asked to grant the postulates and watch what gets built on top. Seen this way, some of the most consequential intellectual work actually happens *before* the first proposition, in choices Archimedes does not show us when laying out the axiomatic foundations of a physical system.

What results is a geometric argument about weights and distances — an argument whose conclusions are testable, but whose *justification* is not experimental. The justification is in the form of proofs. Here, claims about the physical world are derived through abstraction.

This lab asks you to do two things. First, read his postulates and one of his proofs. Second, build a lever and test whether reality agrees.

When Archimedes writes about *magnitudes* and *distances*, he is not using grams or meters. He has no unit of mass — the concept would not be formalized for another two thousand years. What he has is *ratios*. Two weights are equal, or one is twice the other, or their relation is some other proportion. The distance from the fulcrum to one weight stands in some ratio to the distance from the fulcrum to the other. The physics lives in the *proportion*, not in any absolute measurement. When Archimedes proves that "two magnitudes balance at distances reciprocally proportional to the magnitudes," the claim holds whether the magnitudes are measured in grams, stones, or coins-of-unknown-weight. The proof does not care.

This is the same move Euclid's *Elements* makes in Book V's theory of proportion. The Greeks were extraordinarily careful about ratios because they had no choice — they lacked a standardized scheme for converting a quantity of one kind (weight, length, time) into a number divorced from a physical reference.

The experimental section of this supplement attempts to faithfully respect this approach to science. The work uses ratios only — unlabeled weights, relative distances, the question of whether balance obtains. No object is weighed and no distance is converted to a standard unit. This is not a limitation imposed for period flavor; it is the form in which the law of the lever actually lives, and working inside it surfaces a question about measurement that the convenience of a modern scale would quietly skip over.

## The Postulates

Archimedes opens Book I with seven postulates. They are short enough to read in their entirety. The first three concern balance directly; the remaining four concern centers of gravity and the behavior of plane figures. For our purposes, postulates 1–3 and 6 do the work.

> I postulate the following:
>
> 1. Equal weights at equal distances are in equilibrium, and equal weights at unequal distances are not in equilibrium but incline towards the weight which is at the greater distance.
>
> 2. If, when weights at certain distances are in equilibrium, something be added to one of the weights, they are not in equilibrium but incline towards that weight to which the addition was made.
>
> 3. Similarly, if anything be taken away from one of the weights, they are not in equilibrium but incline towards the weight from which nothing was taken.
>
> 4. When equal and similar plane figures coincide if applied to one another, their centres of gravity similarly coincide.
>
> 5. In figures which are unequal but similar the centres of gravity will be similarly situated. By points similarly situated in relation to similar figures I mean points such that, if straight lines be drawn from them to the equal angles, they make equal angles with the corresponding sides.
>
> 6. If magnitudes at certain distances be in equilibrium, (other) magnitudes equal to them will also be in equilibrium at the same distances.
>
> 7. In any figure whose perimeter is concave in (one and) the same direction the centre of gravity must be within the figure.

Upon reading the postulates, it is worth asking: Which postulates feel like idealizations of the visible world, and which ones feel like logical assertions about an abstract category? Each postulate is a different kind of move.

Postulate 1 is an idealization of something easily observed physically. It contains two claims: equal weights at equal distances balance; equal weights at unequal distances do not, and the side with the greater distance is the heavier side. The second half is the genuinely substantive physical assertion. It is the reason a long lever gives you mechanical advantage.

Postulates 2 and 3 are about perturbation: add weight to a balanced system, and the system tips toward the addition. Remove weight, and it tips toward what is left. These sound obvious, but they are what let Archimedes run proofs by *taking differences* — if two unequal weights did balance at equal distances, he argues, then removing the difference from the heavier side should still leave them balanced (by Postulate 3), which contradicts Postulate 1. Therefore they do not balance in the first place. This is the shape of Proposition 2. It is also the shape of Proposition 1, and of most of what follows.

Postulate 6 is the one that feels trivial but is actually doing deep work. It says that *if two specific magnitudes balance at specific distances, then any two other magnitudes equal to them (at those same distances) also balance.* This postulate is a *conservation rule* for the abstract category of "weight," asserting that what matters about a weight, for purposes of balance, is its magnitude and nothing else. This is what makes the law of the lever a statement about ratios rather than about specific objects: the identity of the weights doesn't matter, only their magnitudes.

Postulate 7 is closer to a definition than an observation; it presupposes that figures *have* centers of gravity, treating those centers as objects we can locate and reason about.

## Proposition 6: The Law of the Lever

The celebrated result is Proposition 6: *Two magnitudes, whether commensurable or incommensurable, balance at distances reciprocally proportional to the magnitudes.* In modern notation:

$$
\frac{w_1}{w_2} = \frac{d_2}{d_1}
$$

or equivalently, *w*₁ *d*₁ = *w*₂ *d*₂.

![img-98.jpeg](images/img-98.jpeg)

Archimedes actually proves this in two stages. Proposition 6 handles the *commensurable* case — when the two magnitudes stand in a rational ratio, like 2:1 or 3:2. Proposition 7 extends the result to the *incommensurable* case, using the double-contradiction technique developed in Euclid Book V. For our purposes, the commensurable proof carries the essential insight; the incommensurable extension is a matter of careful completion.

The commensurable proof works by *redistributing* the weights. Archimedes takes the two magnitudes A and B balancing at C with distances in the ratio DC:CE, then subdivides each weight into a number of equal parts (using a common measure *O*), and redistributes those parts evenly along the beam. The resulting system is *equal weights at equal distances* — a configuration already known to balance, by Postulate 1. Since the redistribution preserves the location of the center of gravity (by Postulate 6 and Proposition 5), the original configuration must also have balanced at C.

It is worth noting that Archimedes does not derive the law of the lever from a more fundamental principle about force or energy — those concepts are centuries away. He derives it from the claim that a *specific case* balances (equal weights at equal distances, Postulate 1) combined with a *conservation rule* for centers of gravity (Postulate 6). The law of the lever, in his hands, is a theorem about how to re-express any balanced configuration as a chain of equivalent configurations, ending at one whose balance is postulated.

## Part 1: Build the Apparatus

You need a beam, a fulcrum, and weights. The simplest serviceable apparatus is a ruler balanced on a pencil.

**Materials.**
- A rigid ruler or straight stick, 30 cm or longer. A wooden meter stick is ideal; a plastic ruler will also work.
- A pencil (for the fulcrum).
- A collection of identical small objects to use as unit weights: coins of the same denomination, identical washers, identical nuts, dry beans, or identical paperclips. You want at least 20.
- (For Part 3) Stiff cardboard, a pin, and string, to find the center of gravity of a cut-out triangle.

**Construction.**
1. Place the pencil on a flat surface, oriented perpendicular to the direction the beam will lie.
2. Rest the ruler on the pencil, centered as closely as you can. The pencil serves as the fulcrum; the ruler as the beam.
3. If the ruler has numerical markings, these give you a ready-made distance scale. If not, make your own — mark the center and equally-spaced points on either side. The spacing does not need to correspond to any metric unit.

Find the ruler's true center of gravity. Slide it across the pencil until it balances on its own, without any weights. Mark this point. This is your fulcrum reference for the experiments that follow — all distances are measured *from this point*, not from the ruler's geometric midpoint (which may differ slightly due to the ruler's own non-uniformity).

## Part 2: The Lever Law, in Ratios

This first experimental pass uses only your unit weights (coins, washers, whatever you chose) and your beam's own distance scale. You do not weigh anything. You do not convert to grams or centimeters. The point is to verify Archimedes's propositions using the same kind of information he had — ratios of weights, ratios of distances, and the question of whether balance obtains.

**Experiment 1: Equal weights, equal distances (Postulate 1, Proposition 1).**

Place one coin at the 10-unit mark to the left of the fulcrum and one coin at the 10-unit mark to the right. Release. The beam should balance.

Now try equal weights at *unequal* distances: one coin at position −10, one coin at position +15. The beam tips toward the side with the greater distance. This is the second half of Postulate 1, observed.

**Experiment 2: 2:1 ratio (Proposition 6, commensurable case).**

Place two coins stacked at position −5 (distance 5 from the fulcrum on one side) and one coin at position +10 (distance 10 on the other side). The configuration is 2 weights at distance 5 versus 1 weight at distance 10.

By the law of the lever: *w*₁ *d*₁ = 2 × 5 = 10 = 1 × 10 = *w*₂ *d*₂. The beam should balance.

Release and observe. You may need to nudge the fulcrum a bit — small asymmetries in the ruler or coin placement introduce error — but the system should settle into balance.

**Experiment 3: 3:1 ratio.**

Three coins stacked at position −5, one coin at position +15. Check: 3 × 5 = 15 = 1 × 15. Release. The beam balances.

**Experiment 4: 3:2 ratio.**

Three coins at position −4, two coins at position +6. Check: 3 × 4 = 12 = 2 × 6. Release. Balance.

**Exploratory: find a ratio that does not balance.**

Place 2 coins at −5 and 3 coins at +5. Predict what will happen before releasing. (The side with more coins should tip down — Postulate 1's second clause says that equal distances with unequal weights tip toward the heavier side.) Release and confirm.

Now move one of the coins. At what distance does the 2-coin side need to sit to balance 3 coins at +5? Predict, then test.

**What you have done.** You have verified Propositions 1, 2, and 6 of Book I of *On the Equilibrium of Planes*, using only the equipment Archimedes could have used and information no more precise than he had. You do not know how much each coin weighs in grams. You do not know the beam's length in centimeters. You know only that the coins are equal, that the distances are in certain ratios, and that the beam balances when the ratios are reciprocal.

This is the lever law in its original form.

## Why Stop at Ratios?

The experiments above confirmed the law of the lever multiple times over, yet none of them required knowing the weight of a single coin. Every prediction was a prediction about a ratio — two-to-one, three-to-one, three-to-two — and every ratio was enough. The law is a statement about proportions, and proportions were the only quantities it called for. Archimedes proved the law without a unit of mass because the law does not contain one; the content lies entirely in the relation between one weight and another.

This invites a question to set against the apparatus. A balance is a precise instrument, sensitive to a difference of one coin. Suppose the task were not to compare two weights but to *produce* one — to derive from the lever alone a single definite unit of weight, some standard quantity specifiable enough that anyone could reconstruct it without access to those particular coins. The reader is encouraged to attempt this before continuing, and to note where things run aground.

This is a difference in kind rather than a deficiency in the apparatus. A ratio and a unit are distinct sorts of quantity, and the second is not entailed by the first. A unit enters only by stipulation — a particular object is designated the standard, after which the balance will propagate a number to every other weight faithfully. The designation is not itself an operation the balance can carry out. Put simply, the ratio is prior; the unit is derived.

If the lever can only ever *compare* a unit and never derive one, it remains to be seen whether some other principle might *construct* a unit of mass from the world rather than stipulating it — or whether a unit is unavoidably something carried in from outside, beyond the reach of any instrument to generate. The matter is not settled here.

## Part 3: Centers of Gravity

Archimedes's treatise goes on from the law of the lever to derive the centers of gravity of geometric figures — the center of gravity of a triangle (Proposition 14), of a parallelogram (Propositions 9 and 10), of a trapezium (Proposition 15). These propositions use the law of the lever as a tool: they ask where a compound figure would balance, given what is already known about how weights combine.

You can replicate the core of this reasoning with a piece of cardboard.

**Find the center of gravity of a triangle, experimentally.**

1. Cut a triangle out of stiff cardboard. Any triangle; the more irregular, the more interesting.
2. Punch a small hole near one vertex. Hang the triangle from a pin through the hole, letting it swing freely.
3. With a plumb line (a string with a small weight) attached to the same pin, mark the line the string traces down the face of the cardboard. This is one line passing through the center of gravity.
4. Repeat with a second vertex. You now have two lines. They intersect at a single point.
5. The center of gravity is at the intersection. To confirm, try to balance the triangle on the tip of a pencil at that point. If you were careful, it balances.

What you have just found empirically, Archimedes proves deductively in Proposition 14: *the center of gravity of a triangle is the intersection of its medians.* The medians are the line segments from each vertex to the midpoint of the opposite side. Your plumb lines, if you hung the triangle from each vertex in turn, would coincide with the medians, and all three would meet at a single point, known today as the *centroid*.

## Closing

Physics, for Archimedes, is something one does with postulates and proofs. The world is the testing ground of physics, but is it also the origin of its axioms?

You have tested the law of the lever in pure ratios, and you have found a center of gravity. The first you did the way Archimedes could have done it, if he had cared to. The second you did by a method that *complements* rather than replaces his deductive derivation. Between them sits a question the ratios raised and did not resolve — what it would take to derive a unit rather than declare one — which this lab is not equipped to answer.
