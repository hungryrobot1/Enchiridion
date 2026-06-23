# Observing the Celestial Sphere

> Identifying the zodiac and the ecliptic, watching a planet wander, and computing the Sun's position in Ptolemy's own sexagesimal arithmetic — then checking the prediction against the real sky

Ptolemy's *Almagest* is a manual for computing where things are in the sky and where they will be. Behind its geometry stands a picture: a spherical Earth at the center of a vast celestial sphere; the fixed stars, tethered to the firmament, rotating in diurnal motion; and the Sun, Moon, and planets moving along their own paths against this backdrop. This picture is, as we understand today, wrong. The Earth is not the center of the universe, and yet, the *Almagest* predicts the positions of the heavenly bodies with an accuracy that held up for over a thousand years. That gap, between a false model and its true predictions, is the most interesting thing this lab has to show you, and the last part lets you produce it with your own hands.

You do not need a clear sky or a telescope. A free planetarium program, **Stellarium**, renders the sky for any time and place; the browser version at https://stellarium-web.org/ needs no installation. Where this lab says "observe," you may observe in the software, and for some parts the software is the only practical option. Use the real sky where you can, for it is always better to see the thing itself, but nothing here requires it.

## Part 1: The Sphere and the Ecliptic

Open Stellarium (or step outside on a clear night). Set the location and let the sky load.

**Find the zodiac.** The zodiac is the band of twelve constellations through which the Sun, Moon, and planets move. In Stellarium, turn on the constellation lines and labels, and turn on the ecliptic line (in the browser version, the bottom toolbar and the settings panel expose these). The **ecliptic** is the Sun's annual path against the stars — the great circle the Sun traces over a year. The zodiac constellations are precisely the ones the ecliptic passes through: Aries, Taurus, Gemini, and the rest, in order.

**Locate the Sun on the ecliptic.** Advance the time to daytime and find the Sun. Notice which zodiac constellation it sits in front of. This is what an astronomer means by the Sun's *position*: not where it is in your sky at this hour (that is just the Earth's daily spin), but where it sits against the fixed background of the stars. Over a year, the Sun walks the full ecliptic, passing through all twelve signs and returning. Step the date forward a month at a time and watch it move from one sign toward the next.

**Find a planet.** Use Stellarium's search to locate Mars, Jupiter, or Saturn. Each sits somewhere on or near the ecliptic — they travel the same zodiac band as the Sun, which is why the ancients grouped them together as the "wandering stars" (πλάνητες, *planētes*, "wanderers"). The fixed stars hold their patterns; these few do not.

That distinction — fixed stars that keep their arrangement and wanderers that drift through it — is a central problem the *Almagest* sets out to solve. A model of the heavens has to account for the wanderers' motion, which as it turns out, is not so simple.

## Part 2: The Wandering Star (Optional)

This part rewards patience with one of the genuinely strange sights of the sky. It is optional: the conceptual point can be made in Stellarium in a minute, but the deeper version asks for a longer commitment, the way charting a gnomon's noon shadow across a year asks for one. Do as much as suits you.

A planet does not merely drift steadily eastward through the zodiac. Every so often it *slows, stops, reverses* — moving backward (westward) against the stars for some weeks — then stops again and resumes its forward march, tracing a loop or zigzag in the sky. This is **retrograde motion**, and it is the central anomaly of planetary astronomy. A model in which planets simply circle the Earth at steady speed cannot produce it.

**The quick version (Stellarium).** Find Mars. Set the time-step to a few days and let the program run, watching Mars against the background stars. Within a couple of simulated years you will catch it in a retrograde loop — pausing, backing up, looping, moving on. Note the dates over which it travels backward.

**The patient version (real sky).** Over a season when a bright planet is well placed, mark its position against nearby stars every clear night — a quick sketch, or note which stars it sits between. Across weeks the planet's drift will reverse and then reverse again. You will have recorded, by hand, the phenomenon that forced the entire apparatus of epicycles into being.

## Part 3: Computing the Sun's Position

Here we turn from observation to calculation, and to the arithmetic in which Ptolemy actually worked.

### Sexagesimal notation

Ptolemy computes in **base sixty**. Where we write fractions of a degree in tenths and hundredths, he writes them in sixtieths, and sixtieths of sixtieths, and so on. It is the same system that survives in our minutes and seconds of angle and of time. A value written `0;59,8,17°` means

$$
0 + \frac{59}{60} + \frac{8}{60^2} + \frac{17}{60^3} \text{ degrees.}
$$

The semicolon separates the whole part from the fractional part; the commas separate successive sixtieths. Toomer, whose translation this curriculum uses, notes that Ptolemy reserved this notation for where precision demanded it:

> Except where it is necessary to be precise, Ptolemy prefers the traditional Greek fractional system to the sexagesimal... I have always retained the fractional form where Ptolemy has it, since it gives a misleading appearance of precision to convert to sexagesimals.

The tables are where precision is demanded, and so the tables are sexagesimal. We are about to use one.

### Ptolemy's mean motion

The single quantity that does the work is the **mean daily motion of the Sun** — how far it advances along the ecliptic, on average, in one day. Ptolemy gives it, in Book III, as

$$
0;59,8,17,13,12,31° \text{ per day,}
$$

just under one degree per day, as it must be, since the Sun circuits the full 360° of the ecliptic in roughly 365¼ days. The first three sexagesimal places are ample for us: `0;59,8,17°`, which in decimal is

$$
0 + \frac{59}{60} + \frac{8}{3600} + \frac{17}{216000} \approx 0.9856343° \text{ per day.}
$$

This number is the heart of the solar theory. Ptolemy's tables are, in effect, this rate pre-multiplied by 18-year periods, single years, months, and days, so that a position can be assembled by addition rather than computed from scratch. We will use the rate directly.

### Choosing an epoch you can check

Ptolemy reckons from the start of the era of Nabonassar — noon, 26 February 747 BC — for which he establishes a mean Sun of 0;45° into Aquarius. We will *not* use that epoch, and the reason is itself instructive. Over the intervening centuries the reference frame of longitudes drifts (the equinox from which longitudes are counted slowly shifts against the stars, by about a degree every seventy-two years). This is called the precession of the equinoxes. Reckoning from 747 BC and comparing against modern software would pit Ptolemy's method against nearly forty degrees of accumulated drift — a real effect, but not the one we are testing here. What we want to test is the **mean motion**: Ptolemy's claim about how fast the Sun moves.

So we will do exactly what Ptolemy did: *establish an epoch from a trusted observation, then propagate it forward by the mean motion*. But in our case, we will take our epoch from Stellarium instead of from Babylon. This keeps both ends of the comparison in the same frame, and isolates the one thing under test.

### The computation

**Step 1 — fix your epoch from the sky.** In Stellarium, choose a starting date, select the Sun, and record its ecliptic longitude. Call this $\lambda_0$ and the date your epoch. (If you start at an equinox, $\lambda_0$ will be near 0° or 180°, which makes the bookkeeping easy, but any date works.)

**Step 2 — choose a target date and count the days.** Pick a second date, some months or years later, that you will also view in Stellarium. Let *N* be the number of days from your epoch to the target. An online "days between dates" calculator gives it directly.

**Step 3 — accumulate the mean motion.** Multiply the mean daily motion by *N*:

$$
\Delta\lambda = N \times 0.9856343°.
$$

This is the arc the Sun travels, in mean motion, over the interval. A calculator handles the multiplication; you are doing by hand what Ptolemy's tables did by lookup.

**Step 4 — add and reduce.** Add the starting longitude and strip away whole revolutions:

$$
\lambda_{\text{mean}} = \left(\lambda_0 + \Delta\lambda\right) \bmod 360°.
$$

The remainder, between 0° and 360°, is the Sun's **mean longitude** on your target date. Read it as a zodiac position if you like: 0–30° is Aries, 30–60° Taurus, and so on around the band. This is where a Sun moving at *perfectly uniform* speed would sit.

**Step 5 — verify, and meet the anomaly.** In Stellarium, jump to your target date, select the Sun, and read its true ecliptic longitude. Compare with your $\lambda_{\text{mean}}$. You will find them close — within a few degrees — but not exact. The gap is not an error in your arithmetic. It is the **equation of anomaly**: the real Sun does not move at perfectly uniform speed but runs a little fast in one half of the year and a little slow in the other, because (in Ptolemy's model) its circle is set off-center from the Earth. The discrepancy you are looking at is that non-uniformity, made visible. The correction is at most about 2;23° at either end of your interval, so the gap you see — which combines the correction at your epoch and at your target — can run a touch larger; both are the same effect. This is exactly what Ptolemy's table of solar anomaly supplies: entering with the Sun's distance from apogee, you add or subtract the tabulated amount to turn a mean position into the true one. Reproducing the table is beyond this pass, but you have now *seen* the quantity it exists to absorb. (To shrink the gap, choose an epoch and a target where the Sun is near apogee or perigee — roughly the start of January and start of July — where the correction is smallest.)

You have computed the position of the Sun from Ptolemy's mean motion, in his sexagesimal rate, by his own procedure of epoch-plus-propagation — and the sky agrees, to the very precision his anomaly table was built to recover.

## Closing

The model underneath the computation is geocentric. It puts the Earth at the center and the Sun in motion around it. This is not the true state of affairs, but even so, the model itself can still be useful.

The propositions, "the Sun goes around the Earth" and "the Earth goes around the Sun" describe the same relative motion; the same apparent path of the Sun along the ecliptic, thus switching between the two yields no difference in predictive power of where the Sun will be.
