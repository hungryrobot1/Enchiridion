# Explanation of Binary Arithmetic — adjudicated

Composed 2026-09-04 from two independent passes (pass 1 by hand, pass 2 by
Codex gpt-5.6-sol with only the French and the ledger). Where the passes
agreed, that text stands; where they diverged, the choice and its reason are
in `adjudication.md`. Segment IDs mirror `transcription-pass-a.md`. Source
misprints are corrected here and footnoted — the witness keeps them.

<!-- seg:title -->
## EXPLANATION OF BINARY ARITHMETIC, WHICH USES ONLY THE CHARACTERS 0 AND 1, WITH REMARKS ON ITS UTILITY, AND ON ITS GIVING THE MEANING OF THE ANCIENT CHINESE FIGURES OF FOHY

<!-- seg:1 -->
The ordinary calculation of Arithmetic is done according to the progression by
tens. One uses ten characters, which are 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, which
signify zero, one, and the following numbers up to nine inclusively. And
then, going on to ten, one begins again, and writes ten as 10, and ten times
ten or a hundred as 100, and ten times a hundred or a thousand as 1000, and
ten times a thousand as 10000, and so on.

<!-- seg:2 -->
But instead of the progression by tens, I have for several years employed the
simplest progression of all, which goes by twos, having found that it serves
toward the perfection of the science of Numbers. Thus I employ no characters
in it other than 0 and 1, and then, going on to two, I begin again. This is
why two is written here as 10, and two times two or four as 100, and two
times four or eight as 1000, and two times eight or sixteen as 10000, and so
on. Here is the Table of Numbers of this fashion, which one may continue as
far as one likes.

<!-- seg:table-des-nombres -->
| | | | | | | |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 0 | 0 | 0 | 1 | 0 | 2 |
| 0 | 0 | 0 | 0 | 1 | 1 | 3 |
| 0 | 0 | 0 | 1 | 0 | 0 | 4 |
| 0 | 0 | 0 | 1 | 0 | 1 | 5 |
| 0 | 0 | 0 | 1 | 1 | 0 | 6 |
| 0 | 0 | 0 | 1 | 1 | 1 | 7 |
| 0 | 0 | 1 | 0 | 0 | 0 | 8 |
| 0 | 0 | 1 | 0 | 0 | 1 | 9 |
| 0 | 0 | 1 | 0 | 1 | 0 | 10 |
| 0 | 0 | 1 | 0 | 1 | 1 | 11 |
| 0 | 0 | 1 | 1 | 0 | 0 | 12 |
| 0 | 0 | 1 | 1 | 0 | 1 | 13 |
| 0 | 0 | 1 | 1 | 1 | 0 | 14 |
| 0 | 0 | 1 | 1 | 1 | 1 | 15 |
| 0 | 1 | 0 | 0 | 0 | 0 | 16 |
| 0 | 1 | 0 | 0 | 0 | 1 | 17 |
| 0 | 1 | 0 | 0 | 1 | 0 | 18 |
| 0 | 1 | 0 | 0 | 1 | 1 | 19 |
| 0 | 1 | 0 | 1 | 0 | 0 | 20 |
| 0 | 1 | 0 | 1 | 0 | 1 | 21 |
| 0 | 1 | 0 | 1 | 1 | 0 | 22 |
| 0 | 1 | 0 | 1 | 1 | 1 | 23 |
| 0 | 1 | 1 | 0 | 0 | 0 | 24 |
| 0 | 1 | 1 | 0 | 0 | 1 | 25 |
| 0 | 1 | 1 | 0 | 1 | 0 | 26 |
| 0 | 1 | 1 | 0 | 1 | 1 | 27 |
| 0 | 1 | 1 | 1 | 0 | 0 | 28 |
| 0 | 1 | 1 | 1 | 0 | 1 | 29 |
| 0 | 1 | 1 | 1 | 1 | 0 | 30 |
| 0 | 1 | 1 | 1 | 1 | 1 | 31 |
| 1 | 0 | 0 | 0 | 0 | 0 | 32 |

etc.

<!-- seg:3 -->
One sees here at a glance the reason for a celebrated property of the double
Geometric progression in whole Numbers, which holds that if one has only one
of these numbers of each degree, one can compose from them all the other
whole numbers below the double of the highest degree. For here it is as if
one said, for example, that 111 or 7 is the sum of four, of two, and of one,
and that 1101 or 13 is the sum of eight, four, and one. This property serves
Assayers for weighing all sorts of masses with few weights, and could serve
in coinage to give several values with few pieces.

<!-- seg:3-inline-tables -->
     100 | 4          1000 | 8
      10 | 2           100 | 4
       1 | 1             1 | 1
     ---------        ----------
     111 | 7          1101 | 13
<!-- seg:4 -->
This expression of the Numbers, once established, serves to perform all
sorts of operations very easily.[^1]

<!-- seg:ops-addition -->
For Addition, for example.  ☽

      110 |  6        101 |  5       1110 | 14
      111 |  7       1011 | 11      10001 | 17
     ----------     -----------    ------------
     1101 | 13      10000 | 16      11111 | 31

[^2]

<!-- seg:ops-soustraction -->
For Subtraction.

     1101 | 13      10000 | 16      11111 | 31
      111 |  7       1011 | 11      10001 | 17
     ----------     -----------    ------------
      110 |  6        101 |  5       1110 | 14

<!-- seg:ops-multiplication -->
For Multiplication.  ⊙

       11 | 3        101 | 5        101 |  5
       11 | 3         11 | 3        101 |  5
     --------      ---------      ----------
       11            101            101
      11             101           101
     --------      ---------      ----------
     1001 | 9       1111 | 15     11001 | 25

<!-- seg:ops-division -->
For Division.

     15 | ~~11~~11 | 101 ‖ 5
      3 | ~~111~~
          ~~1~~1

<!-- seg:5 -->
And all these operations are so easy that one never has need to try anything
or to guess, as one must do in ordinary division. Nor has one any need to
learn anything by heart here, as one must do in ordinary calculation, where one
has to know, for example, that 6 and 7 taken together make 13, and that 5
multiplied by 3 gives 15, according to the Table of once one is one, which is
called Pythagorean. But here all of that is found and proved from the source,
as one sees in the preceding examples under the signs ☽ and ⊙.

<!-- seg:6 -->
However, I do not at all recommend this manner of counting with a view to
introducing it in place of the ordinary practice by ten. For besides the fact
that one is accustomed to the latter, one has there no need to learn what one
has already learned by heart: thus the practice by ten is shorter, and the
numbers in it are less long. And if one were accustomed to go by twelve or by
sixteen, there would be still more advantage. But calculation by two, that is,
by 0 and by 1, in recompense for its length, is the most fundamental for
science, and gives new discoveries, which are then found useful even for the
practice of numbers, and above all for Geometry — the reason being that, the
numbers being reduced to the simplest principles, like 0 and 1, a marvelous
order appears throughout. For example, in the Table of Numbers itself, one
sees in each column periods reign which always begin again. In the first
column it is 01, in the second 0011, in the third 00001111, in the fourth
0000000011111111, and so on. And little zeros have been put into the Table to
fill the empty space at the head of the column, and the better to mark these
periods. Lines have also been drawn in the Table, which mark that what these
lines enclose returns always beneath them. And it is found further that the
square Numbers, the Cubic, and other powers, likewise the Triangular Numbers,
the Pyramidal, and other figurate numbers, have similar periods as well, so
that one can write out their Tables straightaway, without calculating. And a
prolixity[^3] at the beginning, which afterwards gives the means of sparing
calculation and of going to infinity by rule, is infinitely advantageous.

<!-- seg:7 -->
What is surprising in this calculation is that this Arithmetic by 0 and 1 is
found to contain the mystery of the lines of an ancient King and Philosopher
named Fohy,[^4] who is believed to have lived more than four thousand years
ago, and whom the Chinese regard as the Founder of their Empire and of their
sciences. There are several linear figures attributed to him; they all come
back to this Arithmetic; but it suffices to set down here the Figure of eight
Cova,[^5] as it is called, which passes for fundamental, and to join to it
the explanation, which is manifest, provided one remarks first that a whole
line — signifies unity or 1, and second that a broken line -- signifies zero
or 0.

<!-- seg:figure-cova -->
| figure | | | |
|---|---|---|---|
| ¦ ¦ ¦ | 000 | 0 | 0 |
| ¦ ¦ | | 001 | 1 | 1 |
| ¦ | ¦ | 010 | 10 | 2 |
| ¦ | | | 011 | 11 | 3 |
| | ¦ ¦ | 100 | 100 | 4 |
| | ¦ | | 101 | 101 | 5 |
| | | ¦ | 110 | 110 | 6 |
| | | | | 111 | 111 | 7 |

<!-- seg:8 -->
The Chinese have lost the signification of the Cova or Lineations of Fohy,
perhaps for more than a millennium of years, and they have made Commentaries upon
them in which they have sought I know not what far-off meanings, so that the
true explanation has had to come to them now from the Europeans. Here is how:
hardly more than two years ago I sent to the R. P. Bouvet,[^6] the celebrated
French Jesuit who resides at Peking, my manner of counting by 0 and 1, and no
more was needed for him to recognize that this is the key of the figures of
Fohy. And so, writing to me on 14 November 1701, he sent me the great figure
of that Prince and Philosopher, which goes to 64, and leaves no more room to
doubt the truth of our interpretation, so that one may say that this Father
has deciphered the enigma of Fohy, with the aid of what I had communicated to
him. And as these figures are perhaps the most ancient monument of science in
the world, this restitution of their meaning, after so great an interval of
time, will appear all the more curious.

<!-- seg:9 -->
The agreement between the figures of Fohy and my Table of Numbers is made
better visible when in the Table one supplies the initial zeros, which appear
superfluous, but which serve the better to mark the period of the column, as
I have indeed supplied them there with little rings, to distinguish them from
the necessary zeros; and this accord gives me a great opinion of the depth of
the meditations of Fohy. For what appears easy to us now was not entirely
so[^7] in those far-off times. The Binary or Dyadic Arithmetic is indeed
very easy today, for whoever gives it a little thought, because our manner of
counting aids it greatly, so that it seems only the excess is cut away. But
this ordinary Arithmetic by ten does not appear very ancient; at least the
Greeks and the Romans were ignorant of it, and were deprived of its
advantages. It seems that Europe owes its introduction to Gerbert, afterwards
Pope under the name of Sylvester II, who had it from the Moors of Spain.

<!-- seg:10 -->
Now, as it is believed in China that Fohy is also the author of the Chinese
characters, although greatly altered by the passage of time, his essay in
Arithmetic gives ground to judge that there might well be found in them
something considerable in relation to numbers and to ideas, if one could
unearth the foundation of Chinese writing — all the more since it is believed
in China that he had regard to numbers in establishing it. The R. P. Bouvet
is strongly inclined to press this point, and very capable of succeeding in
it in many ways. However, I do not know whether there was ever in Chinese
writing an advantage approaching the one that must necessarily be in a
Characteristic such as I project: namely, that every reasoning that can be
drawn from notions could be drawn from their Characters by a manner of
calculation, which would be one of the most important means of aiding the human
mind.

---

[^1]: Gerhardt prints *"Cette expressions"*; the plural is a misprint,
corrected here.

[^2]: In the first addition example Gerhardt's decimal labels are swapped —
110 is marked 7 and 111 marked 6. The tables here print the correct labels;
the subtraction immediately below, which Gerhardt prints correctly, proves
the swap.

[^3]: Gerhardt prints *"prolixtié"*, a misprint for *prolixité*.

[^4]: Fohy: Fuxi, the legendary first sovereign; Leibniz's spelling, from
Bouvet's letters, is kept throughout.

[^5]: Cova: Leibniz's transliteration of *gua* 卦, the trigrams.

[^6]: R. P.: Révérend Père — the Reverend Father Joachim Bouvet, Jesuit
missionary at the Kangxi court and Leibniz's correspondent.

[^7]: Gerhardt prints *"ne l'étoit pas tout"* — "was not entirely so" — and
two further witnesses confirm the printing. The expected idiom is *"pas du
tout"*, "not at all", and the 1705 Mémoires may read so. The printed text is
translated; the reader should weigh the likelier sense.
