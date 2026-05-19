# Buoyancy and Displacement

> Reading Archimedes's *On Floating Bodies* alongside hands-on experiments — the postulate, three propositions, and the crown problem

Where *On the Equilibrium of Planes* introduces a short list of postulates and theorems about levers, *On Floating Bodies* is about how fluids behave; and what happens when solids are placed into them. The work proceeds deductively. As before, the propositions are testable, but the justification given for them is not experimental; it is a chain of reasoning from the postulate.

This lab pairs the postulate and three propositions with experiments that test them. As with the lever lab, reading the proofs and running the experiments are different activities. The proofs establish what *must* be true given the postulate; the experiments establish what *is* true with this kettle and this water and these objects. They illuminate one another, but neither replaces the other.

## The Postulate

The treatise begins:

> Let it be supposed that a fluid is of such a character that, its parts lying evenly and being continuous, that part which is thrust the less is driven along by that which is thrust the more; and that each of its parts is thrust by the fluid which is above it in a perpendicular direction if the fluid be sunk in anything and compressed by anything else.

Two claims are bundled here.

The first is that a fluid is *continuous and even*: its parts are uniform, and adjacent parts are in contact with one another. The fluid has no internal boundaries, no gaps, no privileged points. This is an idealization — real water has dissolved gases, currents, surface tension at boundaries, density variations with depth and temperature — but Archimedes is asserting that for the purposes of statics, a fluid can be treated as a single connected medium.

The second is the operational rule: *the part which is thrust less is driven along by the part which is thrust more*. If two adjacent regions of a fluid experience different amounts of compression, the less-compressed region will move. Equivalently: at rest, every part of a fluid must be compressed equally by its neighbors at the same depth. This is the seed of what we now call hydrostatic pressure equilibrium.

The postulate does not name pressure. Archimedes has no word for it as a quantitative field, and no machinery for assigning it a value at each point in the fluid. What he has is a *comparative* notion — *more thrust* and *less thrust* — and a rule about what comparative imbalances do. From this, with sheer geometry, he derives consequences that we would today phrase in the language of pressure and density. The fluid postulate is genuinely subtle. Archimedes phrases his foundational claim entirely in terms of *what happens when one part of a fluid is thrust more or less than another*. Reading him, one might sense a vocabulary that is doing more work than it has the words for.

## Proposition 3: Equal-Density Solids

> Of solids those which, size for size, are of equal weight with a fluid will, if let down into the fluid, be immersed so that they do not project above the surface but do not sink lower.

Translated: a solid whose density equals the fluid's density will float at neutral buoyancy — neither rising to break the surface nor sinking to the bottom, but resting fully submerged at whatever depth it is placed.

Archimedes proves this by contradiction. If such a solid did partly project above the surface, the fluid below the projecting part would be under less compression than the fluid at the same depth elsewhere, and the postulate forces motion. If it sank lower than full immersion, a similar imbalance arises in the other direction. Therefore neither happens, and the solid rests fully but exactly submerged.

The result is, in modern terms, the boundary case between Propositions 5 and 7 — between "lighter than the fluid" (floats with part above the surface) and "heavier than the fluid" (sinks to the bottom). It is the proposition you reach for when you want to demonstrate that *density*, not weight, is what determines buoyant behavior.

### Experiment 1: Neutral buoyancy

Most household liquids and household objects do not happen to match in density. The classic demonstration uses an egg in salt water, where you can tune the salt concentration to match the egg's density.

**Materials.** A fresh raw egg. A tall clear glass or jar. Table salt. Water. A spoon for stirring.

**Procedure.**
1. Fill the glass two-thirds full with plain tap water. Place the egg in. It sinks. (A fresh egg's density is slightly greater than that of pure water — this is one of the standard tests for egg freshness.)
2. Remove the egg. Add salt to the water, a tablespoon at a time, stirring fully between additions. Each addition increases the water's density.
3. After each addition, return the egg to the glass and observe. At some salt concentration, the egg neither sinks to the bottom nor floats to the top. It hangs suspended at whatever depth you place it. This is Proposition 3.
4. Add a little more salt. The egg now rises. Add fresh water on top, gently, so it does not mix. The egg sinks again at the boundary between the saltier water below and the fresher water above — and may stop at that boundary, neutrally buoyant in the layer that matches its own density.

What the experiment shows: density is the relevant variable, and the neutrally buoyant configuration is a real physical state, not a mathematical idealization. The egg holds its position because every part of the surrounding fluid at every depth is exerting exactly the compression needed to support exactly that mass of egg. Move the egg up or down by a millimeter and the configuration is unchanged. Archimedes's proof says this must be so. The water and the egg agree.

## Proposition 5: Floating Solids

> Any solid lighter than a fluid will, if placed in the fluid, be so far immersed that the weight of the solid will be equal to the weight of the fluid displaced.

This is the principle of flotation. A solid less dense than water (a piece of wood, a hollow boat, an iceberg) will sink into the water until the *weight of the water it has pushed aside* equals the *weight of the solid itself*. The submerged fraction is exactly whatever it needs to be to make these two weights match.

Archimedes's proof reuses the postulate via the same kind of pyramidal-region argument as Proposition 3. He considers a column of fluid that, if the floating solid were absent, would occupy the same volume as the submerged portion of the solid. For the fluid to be at rest, that hypothetical column of fluid would have to weigh exactly what the solid weighs — otherwise the postulate gives the surrounding fluid a reason to move, contradicting the assumed rest.

### Experiment 2: Floating ratio

The submerged fraction of a floating object equals the ratio of its density to the fluid's density. For ice in water, that ratio is approximately 0.917; about 91.7% of an ice cube floats below the waterline, with only ~8.3% above. This is the famous tip-of-the-iceberg fact.

**Materials.** An ice cube (or any small floating object whose density you can estimate). A clear glass of water. A ruler.

**Procedure.**
1. Place the ice cube in the water and let it settle.
2. Measure the height of the cube total, and the height of the part above the water line. Compute the ratio of submerged height to total height.
3. The submerged fraction should be approximately 0.917 — that is, the part above the water should be about 8% of the total height.

The measurement is rough — ice cubes are rarely uniform cuboids, and surface tension at the water line affects small objects — but the order-of-magnitude agreement is the point. Try the same with a piece of wood; if you know its species you can look up its density and predict the floating fraction in advance.

**Variation.** A small bowl, plastic cup, or piece of folded foil shaped like a boat: place it on the water and add weight (coins, marbles, beans) to it incrementally, measuring how much further it sinks each time. Each added unit of weight requires displacing an additional matching weight of water. Plot weight added against submerged depth if you want to make this quantitative — the relationship is linear until the boat takes on water and sinks.

## Proposition 7: Submerged Solids

> A solid heavier than a fluid will, if placed in it, descend to the bottom of the fluid, and the solid will, when weighed in the fluid, be lighter than its true weight by the weight of the fluid displaced.

This is the result that gets popularly attributed to Archimedes — the *Archimedes principle* in its narrow modern sense. A submerged object's apparent weight (what a scale or spring would register if the object were hanging in the fluid) is its true weight minus the weight of the displaced fluid. The buoyant force the fluid exerts upward equals the weight of the fluid the object has pushed aside.

Archimedes proves it by a clever construction: he imagines pairing the heavier-than-fluid solid *A* with a hypothetical lighter-than-fluid solid *B*, chosen such that the two together have the same density as the fluid. By Proposition 3, the combined object is in neutral equilibrium when fully submerged. The downward pull on *A* must therefore exactly balance the upward push on *B* (which, by Proposition 6, equals the weight of fluid displaced by *B* minus *B*'s own weight). Untangling the algebra gives the result: *A*'s apparent submerged weight is its true weight minus the weight of fluid it displaces.

### Experiment 3: Apparent weight loss

This is the experiment that historically *is* attributed to Archimedes — though in the form Vitruvius later reports (next section), not in the form the treatise itself gives. The principle and the procedure here are exactly Proposition 7 in operation.

**Materials.** A kitchen scale that reads to 1 g (a hanging or spring scale is even better, but a flat scale works with the modification below). A sturdy small object dense enough to sink (a metal bolt, a marble, a small stone). A glass or beaker of water tall enough to fully submerge the object. String.

**Procedure (with a hanging scale).**
1. Tie the object to the string, and the string to the hook of the scale. Record the object's weight in air, *W*.
2. Lower the object into the water until it is fully submerged, but not touching the bottom of the container. Record the new reading, *W'*. This is the apparent submerged weight.
3. Compute *W − W'*. This is the buoyant force — equivalently, the weight of the displaced water.
4. To verify: compute the volume of water displaced (mass of displaced water ÷ density of water; for water, density is 1 g/mL, so the mass in grams equals the volume in mL). Then submerge the object in a measuring cup of water and read the volumetric displacement directly. The two numbers should agree.

**Procedure (with only a flat scale).**
1. Place the glass of water on the scale. Record its weight.
2. Submerge the object on a string, holding it so it does not touch the glass. The scale reading increases. The amount of the increase equals the buoyant force on the object — equivalently, the weight of the water it displaces.
3. The object's submerged weight is its weight in air minus this increase. (This procedure exploits Newton's third law as a shortcut: the buoyant force the water exerts upward on the object is equal and opposite to the force the object exerts downward on the water.)

This experiment is the most direct verification of Proposition 7. The buoyant force is real, it is measurable, and its magnitude is exactly the weight of the displaced fluid — to within the accuracy of your scale and your patience.

## The Crown Problem

The most famous Archimedean anecdote is not actually in the treatise. *On Floating Bodies* never mentions Hiero, Syracuse, or a crown. The story comes to us from Vitruvius, the Roman architect and engineer, writing about two centuries after Archimedes in *De Architectura* IX, preface, sections 9–12.

The Vitruvius passage is short enough to read in full. The wording below is from the standard English translation:

> In the case of Archimedes, although he made many wonderful discoveries of diverse kinds, yet of them all, the following, which I shall relate, seems to have been the result of a boundless ingenuity. Hiero, after gaining the royal power in Syracuse, resolved, as a consequence of his successful exploits, to place in a certain temple a golden crown which he had vowed to the immortal gods. He contracted for its making at a fixed price, and weighed out a precise amount of gold to the contractor. At the appointed time the latter delivered to the king's satisfaction an exquisitely finished piece of handiwork, and it appeared that in weight the crown corresponded precisely to what the gold had weighed.

> But afterwards a charge was made that gold had been abstracted and an equivalent weight of silver had been added in the manufacture of the crown. Hiero, thinking it an outrage that he had been tricked, and yet not knowing how to detect the theft, requested Archimedes to consider the matter. The latter, while the case was still on his mind, happened to go to the bath, and on getting into a tub observed that the more his body sank into it the more water ran out over the tub. As this pointed out the way to explain the case in question, without a moment's delay, and transported with joy, he jumped out of the tub and rushed home naked, crying with a loud voice that he had found what he was seeking; for as he ran he shouted repeatedly in Greek, "Ευρηκα, ευρηκα."

> Taking this as the beginning of his discovery, it is said that he made two masses of the same weight as the crown, one of gold and the other of silver. After making them, he filled a large vessel with water to the very brim, and dropped the mass of silver into it. As much water ran out as was equal in bulk to that of the silver sunk in the vessel. Then, taking out the mass, he poured back the lost quantity of water, using a pint measure, until it was level with the brim as it had been before. Thus he found the weight of silver corresponding to a definite quantity of water.

> After this experiment, he likewise dropped the mass of gold into the full vessel and, on taking it out and measuring as before, found that not so much water was lost, but a smaller quantity: namely, as much less as a mass of gold lacks in bulk compared to a mass of silver of the same weight. Finally, filling the vessel again and dropping the crown itself into the same quantity of water, he found that more water ran over for the crown than for the mass of gold of the same weight. Hence, reasoning from the fact that more water was lost in the case of the crown than in that of the mass, he detected the mixing of silver with the gold, and made the theft of the contractor perfectly clear.

A few things are worth saying about the Vitruvius account.

It is a story, not a treatise excerpt. Vitruvius is writing for a Roman audience two centuries after the events; the historical accuracy of the bath, the running through the streets, and the explicit "Eureka!" cannot be verified. The treatise itself nowhere reports an experiment — Archimedes works deductively, and any experiments he ran are not preserved in his writings.

But the *physics* of the story is correct, and it directly applies Proposition 7. If the crown is made of pure gold, and a lump of pure gold of the same weight is also available, both should displace the same volume of water when submerged (because they have the same density and the same mass, hence the same volume). If the crown is adulterated with silver — which is less dense than gold — then for the same total weight, the crown must contain more *volume*, and will therefore displace more water. The procedure Vitruvius describes is a real, working application of the proposition, even if the bathtub realization was added by later storytellers.

One subtlety, sometimes raised by historians of science: the displacement difference for a typical adulteration would be *very* small, possibly within the error of the procedure as described. A more sophisticated method, sometimes also attributed to Archimedes, uses Proposition 7 directly: hang the crown and an equal-weight mass of pure gold from a balance, submerge both in water, and check whether the balance still reads equal. Adulteration would make the crown more voluminous and therefore more buoyant, tipping the balance. This procedure is more sensitive, and corresponds more cleanly to what *On Floating Bodies* itself can prove. Whether Archimedes actually did this is unknown.

### Experiment 4: A crown problem of your own

Set up the inverse of the crown problem with materials at hand.

**Materials.** Two small objects of similar size but different materials — for instance, a steel bolt and an aluminum bolt, or a marble and a plastic bead, or a copper coin and a zinc-cored coin. A scale. A measuring cup. Water.

**Procedure.**
1. Weigh each object. They will likely have different weights.
2. Submerge each in water and measure the volume displaced.
3. Compute density (mass ÷ volume) for each.
4. Compare to published values for the materials. If you do not know what the objects are made of, the densities you compute can sometimes identify the material.

**Variation.** If you can find two objects of nearly the same weight but different materials (a metal bolt and a slightly larger plastic object, sized to weigh the same), test them as Vitruvius describes: same weight, different displacements. Confirm that the denser material displaces less.

This is the practical content of Proposition 7. Density is the discriminating quantity, and submerging a sample is one of the most direct ways to measure it.

## Closing

Archimedes's *On Floating Bodies* runs four propositions deep before it has fully derived the buoyant behavior of solids, and three more before it ventures into the geometry of how floating shapes (paraboloids, in Book II) sit in the water. Book II goes substantially further than this lab does — into the stability conditions of floating curved solids, and into questions a naval architect might recognize. We stop at the threshold of Book II deliberately. The four propositions worked through here are enough to grasp the form of the reasoning and to verify the central claims with kitchen-scale apparatus.

What is striking, on a careful reading, is how much physics Archimedes extracts from a postulate that does not even mention pressure. The whole of buoyancy is derived from a comparative claim about *thrust* and a continuity claim about fluids. The modern reader, accustomed to deriving the same results from a quantitative pressure field, can mistake the brevity of the postulate for thinness. It is not thin. Archimedes is being careful about exactly what he assumes, and he is assuming the minimum needed to get the results he wants.

---

## References for Further Work

- Archimedes, *On Floating Bodies* Book I, in this curriculum at `texts/1-ancient-greece/archimedes-floating-bodies/`. Book II treats stability of floating paraboloids; not required for this lab.
- Heath, T. L., *The Works of Archimedes* (1897). The complete Heath edition, including Floating Bodies alongside the rest of the corpus, is at `texts/1-ancient-greece/archimedes-heath-works/`.
- Vitruvius, *De Architectura* IX, preface, sections 9–12. The crown story. In this curriculum at `texts/2-rome-late-antiquity/vitruvius-de-architectura/`.
- For the historical reliability of the crown story, and the question of whether Archimedes used the displacement method or a balance-based one: Rorres, C. (2017), "The Golden Crown" (online reference), with discussion of the sensitivity of each procedure.
