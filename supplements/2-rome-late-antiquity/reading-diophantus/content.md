# Reading Diophantus

> What Diophantus actually wrote — the syncopated notation of the *Arithmetica* — and why Heath's page reads as modern algebra. The little you need to follow him: the unknown, its powers, and his one move.

The page in front of you looks like algebra. It has an *x*, it has plus and equals signs, it solves for the unknown and reports an answer. You have done hundreds of exercises that look like this.

That resemblance is the one thing about the *Arithmetica* most likely to mislead you, and it is not a matter of old-fashioned symbols. The problems are set up and driven to their answers by a method that is not the one you learned, and the difference will not announce itself. It shows up as a small wrongness — a moment where he does something you would never have done, for no reason you can see.

This guide exists to get you to that moment early, and to make it legible when it comes.

The best equipment you have is Euclid. You have read him, and Diophantus is going to use his words.

## Try it yourself first

Go to [Problem 16](#/text/diophantus-arithmetica?s=book-i/16-to-find-three-numbers-such-that-the-sums-of-pairs-are-given-numbers). Read only the statement and the given numbers:

> To find three numbers such that the sums of pairs are given numbers.
>
> Let (1) + (2) = 20, (2) + (3) = 30, (3) + (1) = 40.

Stop there. Before reading his solution, work it the way you would.

You almost certainly wrote three unknowns and three equations, added them, halved, and subtracted. Three names for three unknown things, and a system relating them. It is the obvious move. It may not even feel like a move.

Now read what he does.

He names **one** thing, and it is not any of the numbers you were asked to find. He calls *x* the **sum of all three**. From that the three fall out as x−30, x−40, x−20; their sum is x by construction and 3x−90 by addition; so x = 45, and the answers follow.

Sit with how strange that is. Nothing he named is a thing the problem wanted. And ask the question that the rest of this guide is really about:

**Why didn't he just write a system of equations?**

## Because he has only one unknown

Go back to the [Preliminary](#/text/diophantus-arithmetica?s=book-i/preliminary) and count the signs Diophantus actually defines. Not the marks on the printed page — the ones the text introduces and names.

There are four kinds:

- the **species** of number: Δ^Y for the square, K^Y for the cube, then square-square, square-cube, cube-cube for the fourth, fifth and sixth
- the **unknown**, ς
- the **unit**, M̅
- **minus**, Λ — "a truncated Ψ turned upside down"

That is the whole apparatus, and the gap in it is the answer to your question. **There is no sign for a second unknown.** He has ς. There is no second letter to set beside it, and no way to write one.

So a system of three equations in three unknowns is not a technique he declined to use. It is a sentence he cannot form. Every problem in the book, however many quantities it asks for, has to be driven down to that single ς.

Read his own rule with that in view:

> if a problem leads to an equation in which certain terms are equal to terms of the same species but with different coefficients, it will be necessary to subtract like from like on both sides, until one term is found equal to one term.

One term equal to one term. Not a stylistic preference — the only place a man with one unknown can finish.

His stock of species is closed in the same way. The list stops at the sixth power and the names of the higher ones are compounds of the lower: the sixth is *cube-cube*, though it could as well have been square-square-square. These are not exponents generating a series. They are the names of the things he knows how to handle, and the list ends where his handling does.

## Everything turns on what he calls *x*

Once you see that one unknown is all he gets, the whole art moves to a place you are not used to looking. Not the manipulation — you already have that, and his is nothing special. The art is in **choosing what to call *x* so that the conditions collapse into one.**

Watch it again in [Problem 27](#/text/diophantus-arithmetica?s=book-i/27-to-find-two-numbers-such-that-their-sum-and-product-are-given-numbers). Sum and product are given; find the two numbers. He calls neither number *x*. He names **2x the difference between them**.

Look at what that buys. The numbers become 10+x and 10−x. Their sum is 20 *whatever x turns out to be* — the first condition is satisfied before any work has been done, permanently, by the act of naming. Only the product is left to force, and it forces at once.

That is the Diophantine gesture, and it is in every problem in the book. Two questions to carry, problem after problem:

**What did he name, and what did naming it buy him?**

**How would anyone have thought of that?**

The second question is the one worth staying with, because he never answers it. The choices arrive already made, exactly as Euclid's auxiliary lines do. He does not show you the search. Reconstructing the reasoning he left unsaid is not a detour from reading the *Arithmetica* — for long stretches, it is the only way to read it at all. Do it often enough and you begin to see the problems the way he must have: not as things to be solved, but as things to be *arranged* until they fall.

One practical warning while you work. Several problems open with a **Necessary condition** — Problem 16 wants half the sum of the given numbers to exceed any one of them; Problem 27 wants the square of half the sum to exceed the product by a square. This is the διορισμός, and you know it from Euclid: the statement of when a construction is possible at all. It is a precondition, not the first line of the working. Read it as a step and the harder problems will come apart in your hands.

## What a number has become

There is a quieter shift underneath all this, and it is the one that makes his arithmetic possible.

The Preliminary opens by agreeing with Euclid: all numbers are "made up of some multitude of units." That is *Elements* VII, definition 2, almost word for word.

Now look at the answer to [Problem 21](#/text/diophantus-arithmetica?s=book-i/21-to-find-three-numbers-such-that-the-greatest-exceeds-the-middle-number-by-a-given-fraction-of-the-least-the-middle-exceeds-the-least-by-a-given-fraction-of-the-greatest-but-the-least-exceeds-a-given-fraction-of-the-middle-number-by-a-given-number):

> The numbers are 45, 37½, 22½.

Of what multitude of units is 37½ composed?

Something has happened between the definition and the answer. In Euclid, a ratio is a *relation* between magnitudes — something two numbers stand in, not a third thing alongside them. Proportion is then a relation between relations. That is why the *Elements* is so careful, and so unlike modern habit: a reader today will ask why one cannot simply write A/B = C/D, since it seems to say the same thing. In Euclid it does not, because there is no object A/B to put on either side of the equals.

Diophantus writes 37½ as an answer. The relation has become a thing — an object that can be produced, named, and handed back as the solution to a problem. This is why his page can look like arithmetic where Euclid's looks like geometry, and it is a genuine change in what a number is, not a change of notation.

It leaves a real puzzle, and you should not let anyone tidy it away for you. If a number is a multitude of units, and 37½ is a number, then what is the half doing? Does the denominator say something about the unit itself — that it has been divided, and that division is permitted? Or has "number" simply come to mean something wider, with the old definition carried along out of respect?

Diophantus does not say. He agrees with Euclid on the first page and then works, without comment, in a way the agreement does not license. Notice it, hold it open, and let it sit against everything else you have read about number.

One older word survives to remind you where this came from. Most problems, he says, are formed from the addition, subtraction or multiplication of these numbers, or from the ratios they bear to one another "or to their own **sides** respectively." A square number has a *side*. Euclid's word, doing Euclid's work, inside an arithmetic that has otherwise walked away from the figure.

## What to carry

Return to [Problem 1](#/text/diophantus-arithmetica?s=book-i/1-to-divide-a-given-number-into-two-having-a-given-difference), the simplest thing in the book. Divide 100 into two numbers differing by 40. He calls the lesser *x*, gets 2x + 40 = 100, and finds x = 30.

The middle of that will feel familiar and you can move through it quickly — equals taken from equals leave equals, and the same for halving. You have Euclid's common notions for it, and Diophantus says as much himself in the Preliminary.

But notice that *x* is not the answer. Nobody asked for 30. The problem asked for a division of 100, and the answer is 70 and 30. The unknown was never the object; it was the instrument — posited so the conditions could be brought to bear on each other, and discarded once they had.

That is the habit to bring to the rest of the book. Not *solve for x*, but: what did he posit, why that, and what did it let him say?

The notation you can learn in ten minutes. The positing is the *Arithmetica*.
