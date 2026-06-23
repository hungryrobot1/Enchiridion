# Measuring with Parallax

> The apparent shift of a near object against a far background, turned into a measurement of distance — the geometric key to every distance in the sky

In the Eratosthenes lab, a single observer measured the *size* of something unreachable. One shadow, one angle, one known distance along the ground, and the geometry handed back the circumference of the Earth. The objective was to bridge the local and the global: a measurement anyone could make in an afternoon became a fact about the whole planet.

This lab takes the next step. Where Eratosthenes used one viewpoint to find how *big* a thing is, parallax uses *two* viewpoints to find how *far away* a thing is. It is the same kind of move — careful observation plus a geometric argument, producing a number about something you could never reach — applied to a different question and with an additional vantage point in play.

## The Effect in Your Own Eyes

Parallax can easily be observed for oneself without equipment. Hold your thumb up at arm's length and look at it against the far wall, first with the left eye alone, then with the right eye alone. The thumb jumps. Its position has not changed, but *you* have shifted viewpoints by the small distance between your two eyes, and the thumb has shifted against the backdrop accordingly.

Now bring the thumb closer — halfway to your face — and repeat. The jump is larger. Closer still, larger again. The size of the apparent shift depends on how near the thumb is: the closer the object, the bigger the jump for the same change of viewpoint. This is the whole of parallax in one simple observation. The shift is not a property of the thumb alone, nor of your eyes alone, but of the *relation* between the separation of your viewpoints and the distance to the object.

The geometry that turns this from a curiosity into a measurement is what the rest of this lab develops.

## The Geometry

Two observation points — call them *A* and *B* — are separated by a known distance, the *baseline*, which we will write *b*. From each, you look at the same near object, *P*, and note its position against a distant background. Because *A* and *B* are not the same point, *P* appears in a slightly different place against that background from each. The angle between the two lines of sight, *A*→*P* and *B*→*P*, is the *parallax angle*, which we will write *p*.

The near object, together with the two observation points, forms a triangle: *A*, *B*, and *P*. The baseline *b* is the side you know. The parallax angle *p* is the angle at *P*, the far vertex. The distance you want — call it *d*, the distance from the baseline out to *P* — is the height of this triangle.

For the long, thin triangles that matter here — where *P* is much farther away than *A* and *B* are apart — a simple relation holds. The parallax angle, measured in radians, is very nearly the baseline divided by the distance:

$$
p \approx \frac{b}{d}
$$

which rearranges to the form we actually use:

$$
d \approx \frac{b}{p}
$$

In words: the distance to the object equals the baseline divided by the parallax angle. A larger baseline, or a larger measured shift, both shrink the distance you compute — exactly the behavior your thumb showed. To find how far away something is, you need only two things you can obtain from the ground: the separation of your two viewpoints, and the angle through which the object appears to shift.

A note on the angle. If you measure *p* in degrees rather than radians, convert first — one radian is about 57.3 degrees — or carry the conversion through the formula. The approximation $p \approx b/d$ is the small-angle approximation, and it is excellent precisely when the triangle is long and thin, which is the only case that arises when the object is far. For a thumb against a wall it is quite good; for the Moon against the stars it is superb.

## Part 1: A Terrestrial Distance

Measure the distance to something you can conveniently walk to such as a tree across a field, a building across a street, or a lamppost down the block.

**Materials.** A protractor, or a smartphone with a compass or angle app. A tape measure or a way to pace a known distance. A distant background behind the target (a far ridgeline, a row of buildings, the horizon) against which the target's position can be judged.

**Procedure.**
1. Choose your target *P* and a far background well beyond it.
2. Stand at a point *A* and sight the target. Note where it falls against the background — line it up with some distant feature, or measure the compass bearing to it.
3. Walk a measured distance sideways — perpendicular to your line of sight to the target — to a second point *B*. This distance is your baseline *b*. The larger it is, the larger the shift you will have to measure, and the more accurate your result; but it must be a distance you can measure, so pace it or tape it carefully.
4. From *B*, sight the target again against the same background. It will have shifted. Measure the angle of that shift — the difference in bearing between your two sightings, or the angle subtended against the background features. This is your parallax angle *p*.
5. Compute *d* = *b* / *p*, with *p* in radians (degrees ÷ 57.3). The result is the distance from your baseline to the target.

**Check it.** If the target is in fact reachable, pace or tape the true distance and compare. Your parallax estimate should land within a modest fraction of it — the error driven mostly by how precisely you could read the shift angle, which is the hard measurement. A target a hundred paces off, sighted from a ten-pace baseline, shifts by only a few degrees; halving your angle-reading error roughly halves your distance error.

**Vary the baseline.** Repeat with a longer baseline and then a shorter one. The longer baseline gives a larger, more readable shift and a better estimate; the shorter one a smaller, noisier shift. You are feeling, directly, the central tension of every parallax measurement: the shift you must measure shrinks as the object recedes, and the only way to keep it readable is to widen the baseline.

## Part 2: Lifting the Method to the Sky

To measure the distance to the Moon, the principle is identical: two observers, separated by a known baseline, sight the Moon against the background of the fixed stars, and the Moon's apparent shift against those stars gives, through *d* = *b* / *p*, its distance.

But the tension you felt with the short baseline now dominates. The Moon is so far away that even a baseline of thousands of kilometres — two observers at widely separated points on the Earth's surface — produces a shift of only about a degree, roughly the width of your finger held at arm's length. The Sun is so much farther that its parallax, across the same earthly baseline, is far too small for any naked-eye observer to detect. The geometry does not fail; the angle simply becomes too small to read.

This is exactly the difficulty that the Greek astronomers met. Ptolemy, gathering the work of his predecessors in the *Almagest*, states the parallax problem with precision. The reason the Moon's position needs correcting at all is that the Earth is not a mere point compared to the Moon's distance — which is to say, two observers on the Earth's surface are two genuinely different viewpoints:

> However, in the case of the moon there is the additional problem that its apparent position does not coincide with its true position, even to the senses. For, as we said, the earth does not bear the ratio of a point to the distance of the moon's sphere.

> Now Hipparchus used the sun as the main basis of his examination of this problem... at one time he assumes that the sun has no perceptible parallax, at another that it has a parallax big enough [to be observed]. As a result the ratio of the moon's distance came out different for him for each of the hypotheses he put forward; for it is altogether uncertain in the case of the sun, not only how great its parallax is, but even whether it has any parallax at all.

> We, in contrast, to avoid taking any uncertain factors into our examination of this topic, constructed an instrument to enable us to observe as accurately as possible the amount of the moon's parallax.

## Closing

You measured the distance to something across a field without crossing to it, using nothing but two vantage points and the angle between them. The same construction, with the Earth's own width for a baseline and the fixed stars for a background, reaches the Moon. With patient enough instruments it reaches farther still.

This mode of calculation is among the most reusable tools in the whole of observational science. You have now built it once by hand, and seen its limitations. When the construction returns later at other scales, it will be this same geometry doing the work.
