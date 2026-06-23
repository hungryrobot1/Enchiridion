# Measuring the Earth

> Estimating the Earth's circumference à la Eratosthenes — turning a shadow, a known distance, and a single geometric argument into the size of the planet

Around 240 BC, a librarian from Alexandria measured the Earth with a stick.

He had no satellites, no aerial photography, no reliable maps. He had a vertical pole, a flat patch of ground, the testimony of travelers about a well in Syene that cast no shadow at midsummer noon, and a known distance between two cities. From these — and a single geometric argument — he derived a number for the circumference of the entire planet that was within a few percent of the modern value. Whichever stadion you assume he used, his estimate is at worst off by about 15% and at best within 1%.

This lab is about reproducing his measurement and understanding what its methodology truly achieved. It is repeatable today with the same resources that Eratosthenes had: a stick, a flat surface, the sun, and ideally, a friend in another city.

You will need clear weather, a free morning and afternoon for an observation day, and (for the full version) a collaborator at a known distance to your north or south. If those conditions are not available, the lab includes fallback procedures that let you complete the calculation using freely available reference values.

## Eratosthenes's Method

Eratosthenes' achievement in measuring the earth was not merely the number itself. The number he gave is approximate, and the chain of assumptions behind it would not survive modern scrutiny for long: he assumed Syene and Alexandria lay on the same meridian (they don't, quite), that the distance between them was 5,000 stadia (this is a guess, possibly based on the camel-caravan travel time), and that the sun's rays are parallel (true enough at planetary scale, but not exactly).

The achievement was the process by which his argument took shape. Eratosthenes derived a global fact — the size of the Earth — from purely local observations. Using the length of a shadow at noon in one city, the report that there was no shadow at noon in another, and the distance between them, he bridged the local and the global with geometry. The two-dimensional cross-section of an alternate-angle argument, of the kind met in Euclid's Book I, serves as the mathematical armature for measuring the planet.

Thus, while we are interested in computing a number, we are also interested in reproducing the methodology: turning *appearances* from the natural world (a shadow) into *measurements* (an angle, a distance), turning measurements into a *proportion* (arc to circle), and deriving from the proportion a *fact about the world*.

## The Source Passage

Eratosthenes' original treatise *On the Measure of the Earth* (*Περὶ τῆς ἀναμετρήσεως τῆς γῆς*) unfortunately did not survive intact. Instead, we are left with summaries, paraphrases, and descriptions of its contents. The most detailed account comes from Cleomedes' *On the Motion of the Heavenly Bodies* (*Κυκλικὴ Θεωρία Μετεώρων*).

The original Greek of Cleomedes' full work (including the Eratosthenes section) is available online from the Thesaurus Linguae Graecae (TLG) corpus, hosted at: https://www.astrologicon.org/cleomedes/cleomedes-circular-theory-meteors.html. This includes the detailed passage on the Syene-Alexandria gnomon method.

The translation below is from Heath (1932). It includes Cleomedes' presentation of both Posidonius' method (using the star Canopus and the cities of Rhodes and Alexandria) and Eratosthenes' (using the gnomon and Syene–Alexandria). The Posidonius account is included because the methods illuminate one another: both reduce a global question to a measured angle and a known distance, but they choose different angles to measure.

*The geometric argument turns on the alternate-angles theorem from Euclid Book I (Proposition 29). If you have not yet worked through that proposition, do so before continuing — the entire lab rests on it.*

> About the size of the earth the physicists, or natural philosophers, have held different views, but those of Posidonius and Eratosthenes are preferable to the rest. The latter shows the size of the earth by a geometrical method; the method of Posidonius is simpler. Both lay down certain hypotheses, and, by successive inferences from the hypotheses, arrive at their demonstrations.

> Posidonius says that Rhodes and Alexandria lie under the same meridian. Now meridian circles are circles which are drawn through the poles of the universe and through the point which is above the head of any individual standing on the earth. The poles are the same for all these circles, but the vertical point is different for different persons. Hence we can draw an infinite number of meridian circles. Now Rhodes and Alexandria lie under the same meridian circle, and the distance between the cities is reputed to be 5,000 stades. Suppose this to be the case.

> All the meridian circles are among the great circles in the universe, dividing it into two equal parts and being drawn through the poles. With these hypotheses, Posidonius proceeds to divide the zodiac circle, which is equal to the mendian circles, because it also divides the universe into two equal parts, into forty-eight parts, thereby cutting each of the twelfth parts of it (i.e., signs) into four. If, then, the meridian circle through Rhodes and Alexandria is divided into the same number of parts, forty-eight, as the zodiac circle, the segments of it are equal to the aforesaid segments of the zodiac. For, when equal magnitudes are divided into (the same number of) equal parts, the parts of the divided magnitudes must be respectively equal to the parts. This being so, Posidonius goes on to say that the very bright star called Canopus lies to the south, practically on the Rudder of Argo. The said star is not seen at all in Greece; hence Aratus does not even mention it in his Phaenomena. But, as you go from north to south, it begins to be visible at Rhodes and, when seen on the horizon there, it sets again immediately as the universe revolves. But when we have sailed the 5,000 stades and are at Alexandria, this star, when it is exactly in the middle of the heaven, is found to be at a height above the horizon of one-fourth of a sign, that is, one forty-eighth part of the zodiac circle. It follows, therefore, that the segment of the same meridian circle which lies above the distance between Rhodes and Alexandria is one forty-eighth part of the said circle, because the horizon of the Rhodians is distant from that of the Alexandrians by one forty-eighth of the zodiac circle. Since, then, the part of the earth under this segment is reputed to be 5,000 stades, the parts (of the earth) under the other (equal) segments (of the meridian circle) also measure 5,000 stades; and thus the great circle of the earth is found to measure 240,000 stades, assuming that from Rhodes to Alexandria is 5,000 stades; but, if not, it is in (the same) ratio to the distance. Such then is Posidonius’ way of dealing with the size of the earth.

> The method of Eratosthenes depends on a geometrical argument and gives the impression of being slightly more difficult to follow. But his statement will be made clear if we premise the following. Let us suppose, in this case too, first, that Syene and Alexandria he under the same meridian circle, secondly, that the distance between the two cities is 5,000 stades; and thirdly, that the rays sent down from different parts of the sun on different parts of the earth are parallel; for this is the hypothesis on which geometers proceed. Fourthly, let us assume that, as proved by the geometers, straight lines falling on parallel straight lines make the alternate angles equal, and fifthly, that the arcs standing on (i e., subtended by) equal angles are similar, that is, have the same proportion and the same ratio to their proper circles—this, too, being a fact proved by the geometers. Whenever, therefore, arcs of circles stand on equal angles, if any one of these is (say) one-tenth of its proper circle, all the other arcs will be tenth parts of their proper circles.

> Any one who has grasped these facts will have no difficulty in understanding the method of Eratosthenes, which is this. Syene and Alexandria lie, he says, under the same meridian circle. Since meridian circles are great circles in the universe, the circles of the earth which lie under them are necessarily also great circles. Thus, of whatever size this method shows the circle on the earth passing through Syene and Alexandria to be, this will be the size of the great circle of the earth. Now Eratosthenes asserts, and it is the fact, that Syene lies under the summer tropic. Whenever, therefore, the sun, being in the Crab (Cancer) at the summer solstice, is exactly in the middle of the heaven, the gnomons (pointers) of sundials necessarily throw no shadows, the position of the sun above them being exactly vertical; and it is said that this is true throughout a space three hundred stades in diameter. But in Alexandria, at the same hour, the pointers of sundials throw shadows, because Alexandria lies further to the north than Syene. The two cities lying under the same meridian great circle, if we draw an arc from the extremity of the shadow to the base of the pointer of the sundial in Alexandria, the arc will be a segment of a great circle in the (hemispherical) bowl of the sundial, since the bowl of the sundial lies under the great circle (of the meridian). If now we conceive straight lines produced from each of the pointers through the earth, they will meet at the centre of the earth. Since then the sundial at Syene is vertically under the sun, if we conceive a straight line coming from the sun to the top of the pointer of the sundial, the line reaching from the sun to the centre of the earth will be one straight line. If now we conceive another straight line drawn upwards from the extremity of the shadow of the pointer of the sundial in Alexandria, through the top of the pointer to the sun, this straight line and the aforesaid straight line will be parallel, since they are straight lines coming through from different parts of the sun to different parts of the earth. On these straight lines, therefore, which are parallel, there falls the straight line drawn from the centre of the earth to the pointer at Alexandria, so that the alternate angles which it makes arc equal. One of these angles is that formed at the centre of the earth, at the intersection of the straight lines which were drawn from the sundials to the centre of the earth; the other is at the point of intersection of the top of the pointer at Alexandria and the straight line drawn from the extremity of its shadow to the sun through the point (the top) where it meets the pointer. Now on this latter angle stands the arc carried round from the extremity of the shadow of the pointer to its base, while on the angle at the centre of the earth stands the arc reaching from Syene to Alexandria. But the arcs are similar, since they stand on equal angles. Whatever ratio, therefore, the arc in the bowl of the sundial has to its proper circle, the arc reaching from Syene to Alexandria has that ratio to its proper circle. But the arc in the bowl is found to be one-fiftieth of its proper circle. Therefore the distance from Syene to Alexandria must necessarily be one-fiftieth part of the great circle of the earth. And the said distance is 5,000 stades; therefore the complete great circle measures 250,000 stades. Such is Eratosthenes’ method.

## Part 1: The Gnomon

A gnomon (γνώμων, *gnōmōn*, "indicator" or "one who knows") is any vertical object that casts a shadow. Eratosthenes' instrument was likely a sundial bowl with a vertical pointer; for our purposes, a stick driven into the ground works equally well.

**Construction.** Find a flat, level patch of ground that receives sun from at least mid-morning to mid-afternoon. Drive a straight vertical stick into the ground — anything from a meter stick to a wooden dowel rod to a section of broom handle. The exact height does not matter, but record it. Use a small bubble level (or a plumb line — a string with a weight on the end) to check that the stick is truly vertical. Vertical accuracy matters more than height; a tilted gnomon corrupts every measurement that follows.

If you cannot drive a stick into the ground, mount one to a flat board and place the board on level ground. The gnomon must be perpendicular to the surface its shadow falls on.

**The day-long observation.** On a clear day, mark the position of the shadow's tip every 30 minutes from mid-morning to mid-afternoon. Use a pebble, a coin, a piece of chalk on pavement, anything that holds its place. Record the clock time of each mark.

You will find:

1. The shadow shortens through the morning, reaches a minimum, and lengthens through the afternoon.
2. The path traced by the shadow tip is a smooth curve. (It is, in fact, a hyperbola for most of the year, a straight line at the equinoxes, and an ellipse near the poles. You do not need to derive this.)
3. The shortest shadow points along a single line — the *local meridian*. This is the north-south line at your specific location on Earth.

The moment of the shortest shadow is *solar noon* at your location. This will not, in general, coincide with 12:00 on your clock. Your clock noon is fixed by your time zone, which averages over a wide longitudinal band; solar noon depends on your specific longitude and on the date (the *equation of time*, which can shift solar noon by up to ±16 minutes from the time-zone average). The discrepancy can easily be 30 minutes or more.

Two pieces of vocabulary fall out of this observation, both of which the Greeks already had:

- **Meridian** (μεσημβρινός, *mesēmbrinos*, "of midday"): the north-south line through your location, traced by the noon shadow. The same word in modern usage refers to the great circle on Earth passing through your location and both poles.
- **Zenith** (from Arabic *samt*, via medieval Latin; the Greek term is κατὰ κορυφήν, "down from the top"): the direction directly above you, opposite the direction a plumb line falls. At solar noon at Syene on the summer solstice, the sun stands at the zenith — directly overhead.

You now know what Eratosthenes meant when he said the gnomons at Syene cast no shadow on the solstice. The sun was at the zenith there. At Alexandria, on the same day at the same moment, the sun was *not* at the zenith; the angle between the sun and the zenith at Alexandria is precisely the angle Eratosthenes needed to measure.

## Part 2: The Seasonal Motion

The noon shadow length changes through the year because the Earth's axis is tilted (by approximately 23.5°) relative to the plane of its orbit. As Earth circles the sun, the apparent height of the sun at noon — measured from your local horizon — rises and falls in an annual cycle.

The four cardinal moments of this cycle are:

- **Summer solstice** (around June 20–22 in the northern hemisphere): the sun reaches its highest noon position of the year. At latitudes on the Tropic of Cancer (≈23.5°N — where Syene sits, near modern Aswan), the noon sun is exactly overhead.
- **Winter solstice** (around December 20–22): the sun reaches its lowest noon position.
- **Vernal and autumnal equinoxes** (around March 20 and September 22): the sun is at intermediate heights; day and night are nearly equal length everywhere on Earth.

At Syene on the summer solstice, the noon sun stands at the zenith and the gnomon casts no shadow at all. This makes Syene a fixed reference point for the measurement — there is no angle to measure there, only an angle to measure in Alexandria. The geometry collapses to a single observation.

It is worth dwelling on what kind of leap Eratosthenes is actually making here. He was relying on travelers' reports — secondhand testimony, well-known in his time, that there was a deep well at Syene whose bottom was illuminated by direct sunlight at noon on the summer solstice, and that vertical pointers there cast no shadow on that day.

A well is a long vertical shaft with water at the bottom. Sunlight reaches the water only if the sun is directly overhead, that is, when the sun is at the zenith. The well at Syene, in other words, was a naturally-occurring zenith detector: a piece of unintentional astronomical apparatus whose output (water at the bottom illuminated, or not) was an unmistakable observable signal about the configuration of the sky.

This is its own small breakthrough. The move from "travelers say there is a well there with these properties" to "therefore the sun stands at the zenith over Syene at noon on the solstice" requires a reconceptualization of what counts as data. The well becomes an instrument; the testimony becomes an observation; the mundane becomes suitable for use in a geometric argument.

For your own measurement, the ideal day is also the summer solstice. The arithmetic is cleanest then, because you can use the fact that the sun's angle from vertical equals (your latitude − the sun's declination), and the sun's declination at the summer solstice is +23.44°. On any other day, the sun's declination differs and must be looked up or computed.

If you cannot wait for or work around the solstice, the lab still works on any clear day; Part 3 explains the adjustment.

## Part 3: The Measurement and the Calculation

The measurement and calculation come in three versions, depending on what is available to you.

### A Note on the Method, and a Concession to Convenience

Eratosthenes did not compute an angle from a tangent. Trigonometry as we know it — sines, cosines, tangents as functions defined on numerical angles — was developed centuries later. Eratosthenes worked with a *physical* arc, measured directly.

His instrument was likely a *skaphe* (σκάφη, "bowl") — a hemispherical sundial with a vertical pointer (the gnomon proper) at the bowl's center. As the sun moved, the tip of the gnomon's shadow traced a path along the bowl's interior surface. At noon, the shadow rested at a specific point. The arc from the gnomon's base to the shadow's tip, measured *along the bowl's interior*, was a literal arc on a great circle. Eratosthenes measured this arc as a fraction of the bowl's full circumference — "one-fiftieth of its proper circle," as Cleomedes reports. No angle, no ratio of sides, no tangent function. Just an arc, and the circle it lay on.

The geometric content is identical to what we will compute below using arctan(*s* / *h*). But the move is more direct in Eratosthenes' version, and worth noticing: he did not translate his measurement into degrees and then back into a fraction of a circle. He measured a fraction of a circle. The Earth's circumference, in his calculation, is the Syene-Alexandria distance multiplied by the reciprocal of that fraction — a pure ratio of one arc to another, without ever passing through the language of trigonometry.

We use arctan in the procedures below as a modern convenience. The geometry has not changed; only our way of writing it down. If you have built a hemispherical bowl with a centered pointer, you can measure the arc directly and skip the arctan step entirely. The arc-to-circle ratio, multiplied into your distance, gives you the same answer.

### Version A: The Two-City Measurement (preferred)

This is the direct repetition of Eratosthenes' procedure. You need a collaborator — a friend, a family member, anyone willing — at a known distance to your north or south, ideally several hundred kilometers away. The greater the distance, the larger the angle to measure, and the smaller the relative error.

**On the chosen day:**

1. Both observers set up a vertical gnomon and identify solar noon by the shortest-shadow method (Part 2). The two solar noons will occur at different clock times because of the longitude difference between you, but each observer measures their own local noon.
2. At their own solar noon, each observer measures the height of the gnomon, *h*, and the length of the shadow, *s*.
3. The angle of the sun from the vertical (zenith) at each location is:

   *θ* = arctan(*s* / *h*)

4. The difference between the two observers' angles equals the arc between them along the meridian (in degrees of latitude), provided the two cities lie at nearly the same longitude. If they do not, the calculation still works for north–south distance, but the *D* used below should be the north–south component, not the straight-line distance.
5. The Earth's circumference is then:

   *C* = *D* × (360° / Δ*θ*)

   where *D* is the north–south distance between the two observers and Δ*θ* is the difference in their measured zenith angles.

### Version B: The One-City Measurement (fallback)

If you have no collaborator at a known distance, measure your own shadow angle and pair it with a published reference.

1. At solar noon on your chosen day, measure *h* and *s*. Compute *θ* = arctan(*s* / *h*).
2. Look up your latitude *φ* (any modern map or phone GPS suffices) and the sun's declination *δ* on that day (on the summer solstice, *δ* = +23.44°; you can use the calculator here: https://sagecalculator.com/sun-declination-calculator/).
3. Confirm that *θ* matches *φ* − *δ*, within your measurement error. (This is a sanity check: if it does not match, your gnomon was not vertical, your timing was off, or your shadow measurement was inaccurate.)
4. To estimate the Earth's circumference: choose any city to your north or south whose latitude *φ′* and great-circle distance *D* from you are known. The arc between you in degrees is |*φ* − *φ′*|, and:

   *C* = *D* × (360° / |*φ* − *φ′*|)

### Version C: The Historical Calculation (fallback)

If clear weather and time prevent any measurement, walk through Eratosthenes' own numbers. He measured the shadow angle at Alexandria as 1/50 of a full circle (7.2°). He took the Syene–Alexandria distance as 5,000 stadia. Therefore:

*C* = 5,000 stadia × 50 = 250,000 stadia.

To convert: at the Attic stadion of ~185 m, this is ~46,250 km. At the Egyptian stadion of ~157.5 m, ~39,375 km. The modern measured circumference of Earth (polar) is 40,008 km. Eratosthenes' estimate is therefore between ~1% and ~16% of the true value, depending on which stadion you grant him. We do not know which one he actually used.

### A Note on Accuracy

Whichever version you do, your answer might be off, only by a few percent if you are careful and lucky. The sources of error are several: the gnomon may not be perfectly vertical; you may have missed solar noon by some time; the shadow tip is fuzzy (the sun is not a point source — it subtends about half a degree on the sky, which softens the shadow's edge); the ground may not be perfectly level; the distance between two cities not exactly known. Eratosthenes' own measurement was off by some percentage as well. He was working with imperfect assumptions that we cannot verify.

## Closing

The Earth is round; approximately 40,000 kilometers around. You have learned this the same way Eratosthenes did.

What this lab ultimately seeks to convey is the *episteme* — the kind of knowing that science makes possible. Eratosthenes did not circumnavigate the globe to confirm its shape and size. He did not need to. Instead, the careful measurement of shadows and some geometry told him what the Earth was. This is the kind of move that physical science makes again and again, ranging from subatomic to cosmological in scale: a local measurement is made, a rigorous chain of inference is applied, and a fact about something not directly observable emerges.
