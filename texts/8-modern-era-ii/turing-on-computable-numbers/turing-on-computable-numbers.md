# ON COMPUTABLE NUMBERS, WITH AN APPLICATION TO THE ENTSCHEIDUNGSPROBLEM

By A. M. TURING.

[Received 28 May, 1936.—Read 12 November, 1936.]

The “computable” numbers may be described briefly as the real numbers whose expressions as a decimal are calculable by finite means. Although the subject of this paper is ostensibly the computable numbers, it is almost equally easy to define and investigate computable functions of an integral variable or a real or computable variable, computable predicates, and so forth. The fundamental problems involved are, however, the same in each case, and I have chosen the computable numbers for explicit treatment as involving the least cumbrous technique. I hope shortly to give an account of the relations of the computable numbers, functions, and so forth to one another. This will include a development of the theory of functions of a real variable expressed in terms of computable numbers. According to my definition, a number is computable if its decimal can be written down by a machine.

In §§ 9, 10 I give some arguments with the intention of showing that the computable numbers include all numbers which could naturally be regarded as computable. In particular, I show that certain large classes of numbers are computable. They include, for instance, the real parts of all algebraic numbers, the real parts of the zeros of the Bessel functions, the numbers π, e, etc. The computable numbers do not, however, include all definable numbers, and an example is given of a definable number which is not computable.

Although the class of computable numbers is so great, and in many ways similar to the class of real numbers, it is nevertheless enumerable. In § 8 I examine certain arguments which would seem to prove the contrary. By the correct application of one of these arguments, conclusions are reached which are superficially similar to those of Gödel†. These results have valuable applications. In particular, it is shown (§11) that the Hilbertian Entscheidungsproblem can have no solution.

† Gödel, “Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme, I”, Monatshefte Math. Phys., 38 (1931), 173–198.

In a recent paper Alonzo Church† has introduced an idea of “effective calculability”, which is equivalent to my “computability”, but is very differently defined. Church also reaches similar conclusions about the Entscheidungsproblem‡. The proof of equivalence between “computability” and “effective calculability” is outlined in an appendix to the present paper.

## 1. *Computing machines.*

We have said that the computable numbers are those whose decimals are calculable by finite means. This requires rather more explicit definition. No real attempt will be made to justify the definitions given until we reach §9. For the present I shall only say that the justification lies in the fact that the human memory is necessarily limited.

We may compare a man in the process of computing a real number to a machine which is only capable of a finite number of conditions q₁, q₂, ..., qₖ, which will be called “m-configurations”. The machine is supplied with a “tape” (the analogue of paper) running through it, and divided into sections (called “squares”) each capable of bearing a “symbol”. At any moment there is just one square, say the r-th, bearing the symbol 𝔖(r) which is “in the machine”. We may call this square the “scanned square”. The symbol on the scanned square may be called the “scanned symbol”. The “scanned symbol” is the only one of which the machine is, so to speak, “directly aware”. However, by altering its m-configuration the machine can effectively remember some of the symbols which it has “seen” (scanned) previously. The possible behaviour of the machine at any moment is determined by the m-configuration qₙ and the scanned symbol 𝔖(r). This pair qₙ, 𝔖(r) will be called the “configuration”: thus the configuration determines the possible behaviour of the machine. In some of the configurations in which the scanned square is blank (i.e. bears no symbol) the machine writes down a new symbol on the scanned square: in other configurations it erases the scanned symbol. The machine may also change the square which is being scanned, but only by shifting it one place to right or left. In addition to any of these operations the m-configuration may be changed. Some of the symbols written down will form the sequence of figures which is the decimal of the real number which is being computed. The others are just rough notes to “assist the memory”. It will only be these rough notes which will be liable to erasure.

† Alonzo Church, “An unsolvable problem of elementary number theory”, American J. of Math., 58 (1936), 345-363.

‡ Alonzo Church, “A note on the Entscheidungsproblem”, J. of Symbolic Logic, 1 (1936), 40-41.

It is my contention that these operations include all those which are used in the computation of a number. The defence of this contention will be easier when the theory of the machines is familiar to the reader. In the next section I therefore proceed with the development of the theory and assume that it is understood what is meant by “machine”, “tape”, “scanned”, etc.

## 2. Definitions.

### *Automatic machines.*

If at each stage the motion of a machine (in the sense of §1) is *completely* determined by the configuration, we shall call the machine an “automatic machine” (or *a*-machine).

For some purposes we might use machines (choice machines or *c*-machines) whose motion is only partially determined by the configuration (hence the use of the word “possible” in §1). When such a machine reaches one of these ambiguous configurations, it cannot go on until some arbitrary choice has been made by an external operator. This would be the case if we were using machines to deal with axiomatic systems. In this paper I deal only with automatic machines, and will therefore often omit the prefix *a*-.

### *Computing machines.*

If an *a*-machine prints two kinds of symbols, of which the first kind (called figures) consists entirely of 0 and 1 (the others being called symbols of the second kind), then the machine will be called a computing machine. If the machine is supplied with a blank tape and set in motion, starting from the correct initial *m*-configuration, the subsequence of the symbols printed by it which are of the first kind will be called the *sequence computed by the machine*. The real number whose expression as a binary decimal is obtained by prefacing this sequence by a decimal point is called the *number computed by the machine*.

At any stage of the motion of the machine, the number of the scanned square, the complete sequence of all symbols on the tape, and the *m*-configuration will be said to describe the *complete configuration* at that stage. The changes of the machine and tape between successive complete configurations will be called the *moves* of the machine.

### *Circular and circle-free machines.*

If a computing machine never writes down more than a finite number of symbols of the first kind, it will be called *circular*. Otherwise it is said to be *circle-free*.

A machine will be circular if it reaches a configuration from which there is no possible move, or if it goes on moving, and possibly printing symbols of the second kind, but cannot print any more symbols of the first kind. The significance of the term “circular” will be explained in § 8.

### *Computable sequences and numbers.*

A sequence is said to be computable if it can be computed by a circle-free machine. A number is computable if it differs by an integer from the number computed by a circle-free machine.

We shall avoid confusion by speaking more often of computable sequences than of computable numbers.

## 3. *Examples of computing machines.*

I. A machine can be constructed to compute the sequence 010101... The machine is to have the four $m$-configurations “$b$”, “$c$”, “$f$”, “$e$” and is capable of printing “0” and “1”. The behaviour of the machine is described in the following table in which “$R$” means “the machine moves so that it scans the square immediately on the right of the one it was scanning previously”. Similarly for “$L$”. “$E$” means “the scanned symbol is erased” and “$P$” stands for “prints”. This table (and all succeeding tables of the same kind) is to be understood to mean that for a configuration described in the first two columns the operations in the third column are carried out successively, and the machine then goes over into the $m$-configuration described in the last column. When the second column is left blank, it is understood that the behaviour of the third and fourth columns applies for any symbol and for no symbol. The machine starts in the $m$-configuration $b$ with a blank tape.

|  *Configuration* |   | *Behaviour*  |   |
| --- | --- | --- | --- |
|  *m-config.* | *symbol* | *operations* | *final m-config.*  |
|  $b$ | None | $P0, R$ | $c$  |
|  $c$ | None | $R$ | $c$  |
|  $e$ | None | $P1, R$ | $f$  |
|  $f$ | None | $R$ | $b$  |

If (contrary to the description in § 1) we allow the letters L, R to appear more than once in the operations column we can simplify the table considerably.

|  *m-config.* | *symbol* | *operations* | *final m-config.*  |
| --- | --- | --- | --- |
|  b | None | P0 | b  |
|   |  0 | R, R, P1 | b  |
|   |  1 | R, R, P0 | b  |

II. As a slightly more difficult example we can construct a machine to compute the sequence 001011011101111011111... The machine is to be capable of five m-configurations, viz. “o”, “q”, “p”, “f”, “b” and of printing “ə”, “x”, “0”, “1”. The first three symbols on the tape will be “əə0”; the other figures follow on alternate squares. On the intermediate squares we never print anything but “x”. These letters serve to “keep the place” for us and are erased when we have finished with them. We also arrange that in the sequence of figures on alternate squares there shall be no blanks.

|  *Configuration* |   | *Behaviour*  |   |
| --- | --- | --- | --- |
|  *m-config.* | *symbol* | *operations* | *final m-config.*  |
|  b |  | Pə, R, Pə, R, P0, R, R, P0, L, L | o  |
|  o | 1 | R, Px, L, L, L | o  |
|   |  0 |  | q  |
|  q | Any (0 or 1) | R, R | q  |
|   |  None | P1, L | p  |
|  p | x | E, R | q  |
|   |  ə | R | f  |
|   |  None | L, L | p  |
|  f | Any | R, R | f  |
|   |  None | P0, L, L | o  |

To illustrate the working of this machine a table is given below of the first few complete configurations. These complete configurations are described by writing down the sequence of symbols which are on the tape, with the $m$-configuration written below the scanned symbol. The successive complete configurations are separated by colons.

|  : | ə | ə | 0 | 0 : | ə | ə | 0 | 0 : | ə | ə | 0 | 0 | : | ə | ə | 0 | 0 | 1 :  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  b |  |  | o |  |  |  | q |  |  |  |  | q |  |  |  |  |  | p  |
|  ə | ə | 0 | 0 | 1 : | ə | ə | 0 | 0 | 1 : | ə | ə | 0 | 0 | 1 : | ə | ə | 0 | 0  |
|   |  |  | p |  |  |  | p |  |  |  |  | f |  |  |  |  |  | f  |
|  ə | ə | 0 | 0 | 1 : | ə | ə | 0 | 0 | 1 | : | ə | ə | 0 | 0 | 1 | 0 : |  |   |
|   |  |  |  | f |  |  |  |  |  |  | f |  |  |  |  |  |  | o  |
|  ə | ə | 0 | 0 | 1 | x | 0 : | ... |  |  |  |  |  |  |  |  |  |  |   |
|   |  |  |  | o |  |  |  |  |  |  |  |  |  |  |  |  |  |   |

This table could also be written in the form

$$\mathfrak{b} : \text{ə}\,\text{ə}\,\mathfrak{o}\,0\,0 : \text{ə}\,\text{ə}\,\mathfrak{q}\,0\,0 : \dots, \tag{C}$$

in which a space has been made on the left of the scanned symbol and the $m$-configuration written in this space. This form is less easy to follow, but we shall make use of it later for theoretical purposes.

The convention of writing the figures only on alternate squares is very useful: I shall always make use of it. I shall call the one sequence of alternate squares $F$-squares and the other sequence $E$-squares. The symbols on $E$-squares will be liable to erasure. The symbols on $F$-squares form a continuous sequence. There are no blanks until the end is reached. There is no need to have more than one $E$-square between each pair of $F$-squares: an apparent need of more $E$-squares can be satisfied by having a sufficiently rich variety of symbols capable of being printed on $E$-squares. If a symbol $\beta$ is on an $F$-square $S$ and a symbol $\alpha$ is on the $E$-square next on the right of $S$, then $S$ and $\beta$ will be said to be *marked* with $\alpha$. The process of printing this $\alpha$ will be called marking $\beta$ (or $S$) with $\alpha$.

## 4. *Abbreviated tables.*

There are certain types of process used by nearly all machines, and these, in some machines, are used in many connections. These processes include copying down sequences of symbols, comparing sequences, erasing all symbols of a given form, etc. Where such processes are concerned we can abbreviate the tables for the $m$-configurations considerably by the use of "skeleton tables". In skeleton tables there appear capital German letters and small Greek letters. These are of the nature of "variables". By replacing each capital German letter throughout by an $m$-configuration and each small Greek letter by a symbol, we obtain the table for an m-configuration.

The skeleton tables are to be regarded as nothing but abbreviations: they are not essential. So long as the reader understands how to obtain the complete tables from the skeleton tables, there is no need to give any exact definitions in this connection.

Let us consider an example:

m-config. Symbol Behaviour Final m-config.

f(ℭ, 𝔐, a) {ə L f₁(ℭ, 𝔐, a) from the m-configuration
not ə L f(ℭ, 𝔐, a) f(ℭ, 𝔐, a) the machine finds the symbol of form a which is farthest to the left (the “first a”) and the m-configuration then becomes ℭ. If there is no a then the m-configuration becomes 𝔐.
f₁(ℭ, 𝔐, a) {a ℭ
not a R f₁(ℭ, 𝔐, a) and the m-configuration then
None R f₂(ℭ, 𝔐, a) becomes 𝔐.
f₂(ℭ, 𝔐, a) {a ℭ
not a R f₁(ℭ, 𝔐, a)
None R 𝔐}

If we were to replace ℭ throughout by q (say), 𝔐 by r, and a by x, we should have a complete table for the m-configuration f(q, r, x). f is called an “m-configuration function” or “m-function”.

The only expressions which are admissible for substitution in an m-function are the m-configurations and symbols of the machine. These have to be enumerated more or less explicitly: they may include expressions such as p(r, x); indeed they must if there are any m-functions used at all. If we did not insist on this explicit enumeration, but simply stated that the machine had certain m-configurations (enumerated) and all m-configurations obtainable by substitution of m-configurations in certain m-functions, we should usually get an infinity of m-configurations; e.g., we might say that the machine was to have the m-configuration q and all m-configurations obtainable by substituting an m-configuration for ℭ in p(ℭ). Then it would have q, p(q), p(p(q)), p(p(p(q))), ... as m-configurations.

Our interpretation rule then is this. We are given the names of the m-configurations of the machine, mostly expressed in terms of m-functions. We are also given skeleton tables. All we want is the complete table for the m-configurations of the machine. This is obtained by repeated substitution in the skeleton tables.

### *Further examples.*

(In the explanations the symbol “→” is used to signify “the machine goes into the m-configuration. . . .”)

$$\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a) \quad f\left(\mathfrak{c}_1(\mathfrak{C}, \mathfrak{B}, a), \mathfrak{B}, a\right)$$

$$\mathfrak{c}_1(\mathfrak{C}, \mathfrak{B}, a) \quad E \quad \mathfrak{C}$$

$$\mathfrak{c}(\mathfrak{B}, a) \quad \mathfrak{c}\left(\mathfrak{c}(\mathfrak{B}, a), \mathfrak{B}, a\right)$$

From $\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a)$ the first $a$ is erased and $\rightarrow \mathfrak{C}$. If there is no $a \rightarrow \mathfrak{B}$.

From $\mathfrak{c}(\mathfrak{B}, a)$ all letters $a$ are erased and $\rightarrow \mathfrak{B}$.

The last example seems somewhat more difficult to interpret than most. Let us suppose that in the list of m-configurations of some machine there appears $\mathfrak{c}(\mathfrak{b}, x)$ ($= \mathfrak{q}$, say). The table is

$$\mathfrak{c}(\mathfrak{b}, x) \quad \mathfrak{c}\left(\mathfrak{c}(\mathfrak{b}, x), \mathfrak{b}, x\right)$$

or $\mathfrak{q} \quad \mathfrak{c}(\mathfrak{q}, \mathfrak{b}, x)$.

Or, in greater detail:

$$\mathfrak{q} \quad \mathfrak{c}(\mathfrak{q}, \mathfrak{b}, x)$$

$$\mathfrak{c}(\mathfrak{q}, \mathfrak{b}, x) \quad f\left(\mathfrak{c}_1(\mathfrak{q}, \mathfrak{b}, x), \mathfrak{b}, x\right)$$

$$\mathfrak{c}_1(\mathfrak{q}, \mathfrak{b}, x) \quad E \quad \mathfrak{q}.$$

In this we could replace $\mathfrak{c}_1(\mathfrak{q}, \mathfrak{b}, x)$ by $\mathfrak{q}'$ and then give the table for $f$ (with the right substitutions) and eventually reach a table in which no m-functions appeared.

$$\mathfrak{pc}(\mathfrak{C}, \beta) \quad f\left(\mathfrak{pc}_1(\mathfrak{C}, \beta), \mathfrak{C}, a\right)$$

$$\mathfrak{pc}_1(\mathfrak{C}, \beta) \begin{cases} \text{Any} & R, R \\ \text{None} & P\beta \end{cases} \quad \mathfrak{pc}_1(\mathfrak{C}, \beta) \quad \mathfrak{C}$$

$$\mathfrak{l}(\mathfrak{C}) \quad L \quad \mathfrak{C}$$

$$\mathfrak{r}(\mathfrak{C}) \quad R \quad \mathfrak{C}$$

$$f'(\mathfrak{C}, \mathfrak{B}, a) \quad f\left(\mathfrak{l}(\mathfrak{C}), \mathfrak{B}, a\right)$$

$$f''(\mathfrak{C}, \mathfrak{B}, a) \quad f\left(\mathfrak{r}(\mathfrak{C}), \mathfrak{B}, a\right)$$

$$\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a) \quad f'\left(\mathfrak{c}_1(\mathfrak{C}), \mathfrak{B}, a\right)$$

$$\mathfrak{c}_1(\mathfrak{C}) \quad \beta \quad \mathfrak{pc}(\mathfrak{C}, \beta)$$

From $\mathfrak{pc}(\mathfrak{C}, \beta)$ the machine prints $\beta$ at the end of the sequence of symbols and $\rightarrow \mathfrak{C}$.

From $f'(\mathfrak{C}, \mathfrak{B}, a)$ it does the same as for $f(\mathfrak{C}, \mathfrak{B}, a)$ but moves to the left before $\rightarrow \mathfrak{C}$.

$\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a)$. The machine writes at the end the first symbol marked $a$ and $\rightarrow \mathfrak{C}$.

The last line stands for the totality of lines obtainable from it by replacing $\beta$ by any symbol which may occur on the tape of the machine concerned.

$$\mathfrak{c}\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a) \quad \mathfrak{c}\left(\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a), \mathfrak{B}, a\right)$$

$$\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a) \quad \mathfrak{c}\mathfrak{c}\left(\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a), \mathfrak{B}, a\right)$$

$$\mathfrak{c}\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a, \beta) \quad \mathfrak{f}\left(\mathfrak{c}\mathfrak{c}_1(\mathfrak{C}, \mathfrak{B}, a, \beta), \mathfrak{B}, a\right)$$

$$\mathfrak{c}\mathfrak{c}_1(\mathfrak{C}, \mathfrak{B}, a, \beta) \quad E, P\beta \quad \mathfrak{C}$$

$$\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a, \beta) \quad \mathfrak{c}\mathfrak{c}\left(\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a, \beta), \mathfrak{B}, a, \beta\right)$$

$$\mathfrak{c}\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a) \quad \mathfrak{c}\left(\mathfrak{c}\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a, a), \mathfrak{B}, a\right)$$

$$\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a) \quad \mathfrak{c}\mathfrak{c}\left(\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a), \mathfrak{c}\mathfrak{c}(\mathfrak{B}, a, a), a\right)$$

$\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a)$. The machine copies down in order at the end all symbols marked $a$ and erases the letters $a; \rightarrow \mathfrak{B}$.

$\mathfrak{c}\mathfrak{c}(\mathfrak{C}, \mathfrak{B}, a, \beta)$. The machine replaces the first $a$ by $\beta$ and $\rightarrow \mathfrak{C} \rightarrow \mathfrak{B}$ if there is no $a$. $\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a, \beta)$. The machine replaces all letters $a$ by $\beta; \rightarrow \mathfrak{B}$.

$\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a)$ differs from $\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a)$ only in that the letters $a$ are not erased. The $m$-configuration $\mathfrak{c}\mathfrak{c}(\mathfrak{B}, a)$ is taken up when no letters "$a$" are on the tape.

$$\mathfrak{c}\mathfrak{c}(\mathfrak{C}, \mathfrak{A}, \mathfrak{C}, a, \beta) \quad \mathfrak{f}'\left(\mathfrak{c}\mathfrak{p}_1(\mathfrak{C}_1, \mathfrak{A}, \beta), \mathfrak{f}(\mathfrak{A}, \mathfrak{C}, \beta), a\right)$$

$$\mathfrak{c}\mathfrak{p}_1(\mathfrak{C}, \mathfrak{A}, \beta) \quad \gamma \quad \mathfrak{f}'\left(\mathfrak{c}\mathfrak{p}_2(\mathfrak{C}, \mathfrak{A}, \gamma), \mathfrak{A}, \beta\right)$$

$$\mathfrak{c}\mathfrak{p}_2(\mathfrak{C}, \mathfrak{A}, \gamma) \quad \left\{ \begin{array}{ll} \gamma & \mathfrak{C} \\ \text{not } \gamma & \mathfrak{A}. \end{array} \right.$$

The first symbol marked $a$ and the first marked $\beta$ are compared. If there is neither $a$ nor $\beta, \rightarrow \mathfrak{C}$. If there are both and the symbols are alike, $\rightarrow \mathfrak{C}$. Otherwise $\rightarrow \mathfrak{A}$.

$$\mathfrak{c}\mathfrak{p}\mathfrak{c}(\mathfrak{C}, \mathfrak{A}, \mathfrak{C}, a, \beta) \quad \mathfrak{c}\mathfrak{p}\left(\mathfrak{c}\left(\mathfrak{c}(\mathfrak{C}, \mathfrak{C}, \beta), \mathfrak{C}, a\right), \mathfrak{A}, \mathfrak{C}, a, \beta\right)$$

$\mathfrak{c}\mathfrak{p}\mathfrak{c}(\mathfrak{C}, \mathfrak{A}, \mathfrak{C}, a, \beta)$ differs from $\mathfrak{c}\mathfrak{p}(\mathfrak{C}, \mathfrak{A}, \mathfrak{C}, a, \beta)$ in that in the case when there is similarity the first $a$ and $\beta$ are erased.

$$\mathfrak{c}\mathfrak{p}\mathfrak{c}(\mathfrak{A}, \mathfrak{C}, a, \beta) \quad \mathfrak{c}\mathfrak{p}\mathfrak{c}\left(\mathfrak{c}\mathfrak{p}\mathfrak{c}(\mathfrak{A}, \mathfrak{C}, a, \beta), \mathfrak{A}, \mathfrak{C}, a, \beta\right).$$

$\mathfrak{c}\mathfrak{p}\mathfrak{c}(\mathfrak{A}, \mathfrak{C}, a, \beta)$. The sequence of symbols marked $a$ is compared with the sequence marked $\beta$. $\rightarrow \mathfrak{C}$ if they are similar. Otherwise $\rightarrow \mathfrak{A}$. Some of the symbols $a$ and $\beta$ are erased.

$$\mathfrak{q}(\mathfrak{C}) \quad \left\{ \begin{array}{l l} \text{Any} & R \\ \text{None} & R \end{array} \right. \quad \mathfrak{q}(\mathfrak{C}) \quad \mathfrak{q}(\mathfrak{C}, \alpha). \text{ The machine} \\ \text{finds the last symbol of} \\ \text{form } \alpha. \to \mathfrak{C}.$$

$$\mathfrak{q}_1(\mathfrak{C}) \quad \left\{ \begin{array}{l l} \text{Any} & R \\ \text{None} & \end{array} \right. \quad \mathfrak{q}(\mathfrak{C}) \quad \mathfrak{C}$$

$$\mathfrak{q}(\mathfrak{C}, \alpha) \quad \mathfrak{q}\left(\mathfrak{q}_1(\mathfrak{C}, \alpha)\right)$$

$$\mathfrak{q}_1(\mathfrak{C}, \alpha) \quad \left\{ \begin{array}{l l} \alpha & \mathfrak{C} \\ \text{not } \alpha & L \end{array} \right. \quad \mathfrak{q}_1(\mathfrak{C}, \alpha)$$

$$\mathfrak{p}\mathfrak{e}_2(\mathfrak{C}, \alpha, \beta) \quad \mathfrak{p}\mathfrak{e}\left(\mathfrak{p}\mathfrak{e}(\mathfrak{C}, \beta), \alpha\right)$$

$$\mathfrak{c}\mathfrak{e}_2(\mathfrak{B}, \alpha, \beta) \quad \mathfrak{c}\mathfrak{e}\left(\mathfrak{c}\mathfrak{e}(\mathfrak{B}, \beta), \alpha\right)$$

$$\mathfrak{c}\mathfrak{e}_3(\mathfrak{B}, \alpha, \beta, \gamma) \quad \mathfrak{c}\mathfrak{e}\left(\mathfrak{c}\mathfrak{e}_2(\mathfrak{B}, \beta, \gamma), \alpha\right)$$

$\mathfrak{q}(\mathfrak{C}, \alpha)$. The machine finds the last symbol of form $\alpha$. $\to \mathfrak{C}$.

$\mathfrak{p}\mathfrak{e}_2(\mathfrak{C}, \alpha, \beta)$. The machine prints $\alpha \beta$ at the end.

$\mathfrak{c}\mathfrak{e}_3(\mathfrak{B}, \alpha, \beta, \gamma)$. The machine copies down at the end first the symbols marked $\alpha$, then those marked $\beta$, and finally those marked $\gamma$; it erases the symbols $\alpha, \beta, \gamma$.

$$\mathfrak{c}(\mathfrak{C}) \quad \left\{ \begin{array}{l l} \mathfrak{o} & R \\ \text{Not } \mathfrak{o} & L \end{array} \right. \quad \mathfrak{c}_1(\mathfrak{C}) \quad \text{From } \mathfrak{c}(\mathfrak{C}) \text{ the marks are} \\ \text{erased from all marked sym-} \\ \text{bols.} \to \mathfrak{C}.$$

$$\mathfrak{c}_1(\mathfrak{C}) \quad \left\{ \begin{array}{l l} \text{Any} & R, E, R \\ \text{None} & \end{array} \right. \quad \mathfrak{c}_1(\mathfrak{C}) \quad \mathfrak{C}$$

From $\mathfrak{c}(\mathfrak{C})$ the marks are erased from all marked symbols. $\to \mathfrak{C}$.

## 5. *Enumeration of computable sequences.*

A computable sequence $\gamma$ is determined by a description of a machine which computes $\gamma$. Thus the sequence 001011011101111... is determined by the table on p. 234, and, in fact, any computable sequence is capable of being described in terms of such a table.

It will be useful to put these tables into a kind of standard form. In the first place let us suppose that the table is given in the same form as the first table, for example, I on p. 233. That is to say, that the entry in the operations column is always of one of the forms $E: E, R: E, L: Pa: Pa, R: Pa, L: R: L$: or no entry at all. The table can always be put into this form by introducing more $m$-configurations. Now let us give numbers to the $m$-configurations, calling them $q_1, \ldots, q_R$, as in §1. The initial $m$-configuration is always to be called $q_1$. We also give numbers to the symbols $S_1, \ldots, S_m$ and, in particular, blank = $S_0$, $0 = S_1$, $1 = S_2$. The lines of the table are now of form

|  *m-config.* | *Symbol* | *Operations* | *Final m-config.* |   |
| --- | --- | --- | --- | --- |
|  $q_i$ | $S_j$ | $PS_k, L$ | $q_m$ | $(N_1)$  |
|  $q_i$ | $S_j$ | $PS_k, R$ | $q_m$ | $(N_2)$  |
|  $q_i$ | $S_j$ | $PS_k$ | $q_m$ | $(N_3)$  |
|  Lines such as  |   |   |   |   |
|  $q_i$ | $S_j$ | $E, R$ | $q_m$ |   |
|  are to be written as  |   |   |   |   |
|  $q_i$ | $S_j$ | $PS_0, R$ | $q_m$ |   |
|  and lines such as  |   |   |   |   |
|  $q_i$ | $S_j$ | $R$ | $q_m$ |   |
|  to be written as  |   |   |   |   |
|  $q_i$ | $S_j$ | $PS_j, R$ | $q_m$ |   |

In this way we reduce each line of the table to a line of one of the forms $(N_1), (N_2), (N_3)$.

From each line of form $(N_1)$ let us form an expression $q_i S_j S_k L q_m$; from each line of form $(N_2)$ we form an expression $q_i S_j S_k R q_m$; and from each line of form $(N_3)$ we form an expression $q_i S_j S_k N q_m$.

Let us write down all expressions so formed from the table for the machine and separate them by semi-colons. In this way we obtain a complete description of the machine. In this description we shall replace $q_i$ by the letter “$D$” followed by the letter “$A$” repeated $i$ times, and $S_j$ by “$D$” followed by “$C$” repeated $j$ times. This new description of the machine may be called the *standard description* (S.D). It is made up entirely from the letters “$A$”, “$C$”, “$D$”, “$L$”, “$R$”, “$N$”, and from “;”.

If finally we replace “$A$” by “$1$”, “$C$” by “$2$”, “$D$” by “$3$”, “$L$” by “$4$”, “$R$” by “$5$”, “$N$” by “$6$”, and “;” by “$7$” we shall have a description of the machine in the form of an arabic numeral. The integer represented by this numeral may be called a *description number* (D.N) of the machine. The D.N determine the S.D and the structure of the machine uniquely. The machine whose D.N is $n$ may be described as $\mathcal{M}(n)$.

To each computable sequence there corresponds at least one description number, while to no description number does there correspond more than one computable sequence. The computable sequences and numbers are therefore enumerable.

Let us find a description number for the machine I of §3. When we rename the $m$-configurations its table becomes:

|  $q_1$ | $S_0$ | $PS_1, R$ | $q_2$  |
| --- | --- | --- | --- |
|  $q_2$ | $S_0$ | $PS_0, R$ | $q_3$  |
|  $q_3$ | $S_0$ | $PS_2, R$ | $q_4$  |
|  $q_4$ | $S_0$ | $PS_0, R$ | $q_1$  |

Other tables could be obtained by adding irrelevant lines such as

|  $q_1$ | $S_1$ | $PS_1, R$ | $q_2$  |
| --- | --- | --- | --- |

Our first standard form would be

$$q_1 S_0 S_1 R q_2; \quad q_2 S_0 S_0 R q_3; \quad q_3 S_0 S_2 R q_4; \quad q_4 S_0 S_0 R q_1;$$

The standard description is

$DADDCRDAA; DAADDRDAAA;$

$DAAADDCCRDAAAA; DAAAADDRDA;$

A description number is

31332531173113353111731113322531111731111335317

and so is

3133253117311335311173111332253111173111133531731323253117

A number which is a description number of a circle-free machine will be called a *satisfactory* number. In §8 it is shown that there can be no general process for determining whether a given number is satisfactory or not.

## 6. *The universal computing machine.*

It is possible to invent a single machine which can be used to compute any computable sequence. If this machine $\mathcal{U}$ is supplied with a tape on the beginning of which is written the S.D of some computing machine $\mathcal{M}$, then $\mathcal{U}$ will compute the same sequence as $\mathcal{M}$. In this section I explain in outline the behaviour of the machine. The next section is devoted to giving the complete table for $\mathcal{U}$.

Let us first suppose that we have a machine $\mathcal{M}'$ which will write down on the $F$-squares the successive complete configurations of $\mathcal{M}$. These might be expressed in the same form as on p. 235, using the second description, (C), with all symbols on one line. Or, better, we could transform this description (as in § 5) by replacing each $m$-configuration by “$D$” followed by “$A$” repeated the appropriate number of times, and by replacing each symbol by “$D$” followed by “$C$” repeated the appropriate number of times. The numbers of letters “$A$” and “$C$” are to agree with the numbers chosen in § 5, so that, in particular, “$0$” is replaced by “$DC$”, “$1$” by “$DCC$”, and the blanks by “$D$”. These substitutions are to be made after the complete configurations have been put together, as in (C). Difficulties arise if we do the substitution first. In each complete configuration the blanks would all have to be replaced by “$D$”, so that the complete configuration would not be expressed as a finite sequence of symbols.

If in the description of the machine II of § 3 we replace “$\mathfrak{o}$” by “$DAA$”, “$\text{ə}$” by “$DCCC$”, “$\mathfrak{q}$” by “$DAAA$”, then the sequence (C) becomes:

$$DA : DCCCDCCCDAADCDDC : DCCCDCCCDAAADCDDC : \dots (C_1)$$

(This is the sequence of symbols on $F$-squares.)

It is not difficult to see that if $\mathcal{M}$ can be constructed, then so can $\mathcal{M}'$. The manner of operation of $\mathcal{M}'$ could be made to depend on having the rules of operation (*i.e.*, the S.D) of $\mathcal{M}$ written somewhere within itself (*i.e.* within $\mathcal{M}'$); each step could be carried out by referring to these rules. We have only to regard the rules as being capable of being taken out and exchanged for others and we have something very akin to the universal machine.

One thing is lacking: at present the machine $\mathcal{M}'$ prints no figures. We may correct this by printing between each successive pair of complete configurations the figures which appear in the new configuration but not in the old. Then (C₁) becomes

$$DDA : 0 : 0 : DCCCDCCCDAADCDDC : DCCC \dots \quad (C_2)$$

It is not altogether obvious that the $E$-squares leave enough room for the necessary “rough work”, but this is, in fact, the case.

The sequences of letters between the colons in expressions such as (C₁) may be used as standard descriptions of the complete configurations. When the letters are replaced by figures, as in § 5, we shall have a numerical description of the complete configuration, which may be called its description number.

## 7. *Detailed description of the universal machine.*

A table is given below of the behaviour of this universal machine. The m-configurations of which the machine is capable are all those occurring in the first and last columns of the table, together with all those which occur when we write out the unabbreviated tables of those which appear in the table in the form of m-functions. E.g., e(anf) appears in the table and is an m-function. Its unabbreviated table is (see p. 239)

|  e(anf) | $$\begin{cases} \text{ə} & R \\ \text{not } \text{ə} & L \end{cases}$$ | $$e_1(\text{anf})$$  |
| --- | --- | --- |
|   |   | $$e(\text{anf})$$  |
|  $$e_1(\text{anf})$$ | $$\begin{cases} \text{Any} & R, E, R \\ \text{None} & \end{cases}$$ | $$e_1(\text{anf})$$  |
|   |   | $$\text{anf}$$  |

Consequently $$e_1(\text{anf})$$ is an m-configuration of $$\mathfrak{U}$$.

When $$\mathfrak{U}$$ is ready to start work the tape running through it bears on it the symbol $$\text{ə}$$ on an F-square and again $$\text{ə}$$ on the next E-square; after this, on F-squares only, comes the S.D of the machine followed by a double colon “::” (a single symbol, on an F-square). The S.D consists of a number of instructions, separated by semi-colons.

Each instruction consists of five consecutive parts

(i) “D” followed by a sequence of letters “A”. This describes the relevant m-configuration.

(ii) “D” followed by a sequence of letters “C”. This describes the scanned symbol.

(iii) “D” followed by another sequence of letters “C”. This describes the symbol into which the scanned symbol is to be changed.

(iv) “L”, “R”, or “N”, describing whether the machine is to move to left, right, or not at all.

(v) “D” followed by a sequence of letters “A”. This describes the final m-configuration.

The machine $$\mathfrak{U}$$ is to be capable of printing “A”, “C”, “D”, “0”, “1”, “u”, “v”, “w”, “x”, “y”, “z”. The S.D is formed from “;”, “A”, “C”, “D”, “L”, “R”, “N”.

### *Subsidiary skeleton table.*

$$\text{con}(\mathfrak{C}, a) \begin{cases} \text{Not } A & R, R & \text{con}(\mathfrak{C}, a) \\ A & L, Pa, R & \text{con}_1(\mathfrak{C}, a) \end{cases}$$

$$\text{con}_1(\mathfrak{C}, a) \begin{cases} A & R, Pa, R & \text{con}_1(\mathfrak{C}, a) \\ D & R, Pa, R & \text{con}_2(\mathfrak{C}, a) \end{cases}$$

$$\text{con}_2(\mathfrak{C}, a) \begin{cases} C & R, Pa, R & \text{con}_2(\mathfrak{C}, a) \\ \text{Not } C & R, R & \mathfrak{C} \end{cases}$$

con($\mathfrak{C}$, $a$). Starting from an $F$-square, $S$ say, the sequence $C$ of symbols describing a configuration closest on the right of $S$ is marked out with letters $a$. $\rightarrow \mathfrak{C}$.

$\operatorname{con}(\mathfrak{C},\,)$. In the final configuration the machine is scanning the square which is four squares to the right of the last square of $C$. $C$ is left unmarked.

The table for $\mathcal{U}$.

$\mathfrak{b}$ f($\mathfrak{b}_1, \mathfrak{b}_2, ::$)

$\mathfrak{b}_1$ $R, R, P:, R, R, PD, R, R, PA$ $\text{anf}$

$\text{anf}$ g($\text{anf}_1, :$)

$\text{anf}_1$ con($\mathfrak{fom}, y$)

$$\mathfrak{fom} \begin{cases} ; & R, Pz, L & \text{con}(\mathfrak{fmp}, x) \\ z & L, L & \mathfrak{fom} \\ \text{not } z \text{ nor } ; & L & \mathfrak{fom} \end{cases}$$

$$\mathfrak{fmp} \quad \text{cpc}(\mathfrak{c}(\mathfrak{fom}, x, y), \mathfrak{sim}, x, y)$$

$\mathfrak{b}$. The machine prints : $DA$ on the $F$-squares after $:: \rightarrow \text{anf}$.

$\text{anf}$. The machine marks the configuration in the last complete configuration with $y$. $\rightarrow \mathfrak{fom}$.

$\mathfrak{fom}$. The machine finds the last semi-colon not marked with $z$. It marks this semi-colon with $z$ and the configuration following it with $x$.

$\mathfrak{fmp}$. The machine compares the sequences marked $x$ and $y$. It erases all letters $x$ and $y$. $\rightarrow \mathfrak{sim}$ if they are alike. Otherwise $\rightarrow \mathfrak{fom}$.

$\text{anf}$. Taking the long view, the last instruction relevant to the last configuration is found. It can be recognised afterwards as the instruction following the last semi-colon marked $z$. $\rightarrow \mathfrak{sim}$.

sim f'(sim₁, sim₁, z)

sim₁ con (sim₂, )

sim₂ { A sim₃
not A R, Pu, R, R, R sim₂

sim₃ { not A L, Py ε(mf, z)
A L, Py, R, R, R sim₃

mf g(mf, :)

mf₁ { not A R, R mf₁
A L, L, L, L mf₂

mf₂ { C R, Px, L, L, L mf₂
: mf₄
D R, Px, L, L, L mf₃

mf₃ { not : R, Pv, L, L, L mf₃
: mf₄

mf₄ con (l(l(mf₅)), )

mf₅ { Any R, Pw, R mf₅
None P: s6

s6 f(s6₁, inst, u)

s6₁ L, L, L s6₂

s6₂ { D R, R, R, R s6₂
not D inst

s6₃ { C R, R s6₄
not C inst

s6₄ { C R, R s6₅
not C pe₂(inst, 0, :)

s6₅ { C inst
not C pe₂(inst, 1, :)

sim. The machine marks out the instructions. That part of the instructions which refers to operations to be carried out is marked with u, and the final m-configuration with y. The letters z are erased.

mf. The last complete configuration is marked out into four sections. The configuration is left unmarked. The symbol directly preceding it is marked with x. The remainder of the complete configuration is divided into two parts, of which the first is marked with v and the last with w. A colon is printed after the whole. → s6.

s6. The instructions (marked u) are examined. If it is found that they involve "Print 0" or "Print 1", then 0: or 1: is printed at the end.

|  inst |  | g(i(inst_{1}), u) | inst. The next complete configuration is written down, carrying out the marked instructions. The letters u, v, w, x, y are erased. → anf.  |
| --- | --- | --- | --- |
|  inst_{1} | a | R, E | inst_{1}(a)  |
|  inst_{1}(L) |  | cc_{5}(ov, v, y, x, u, w) |   |
|  inst_{1}(R) |  | cc_{5}(ov, v, x, u, y, w) |   |
|  inst_{1}(N) |  | cc_{5}(ov, v, x, y, u, w) |   |
|  ov |  | c(anf) |   |

## 8. *Application of the diagonal process.*

It may be thought that arguments which prove that the real numbers are not enumerable would also prove that the computable numbers and sequences cannot be enumerable*. It might, for instance, be thought that the limit of a sequence of computable numbers must be computable. This is clearly only true if the sequence of computable numbers is defined by some rule.

Or we might apply the diagonal process. "If the computable sequences are enumerable, let a$_{n}$ be the n-th computable sequence, and let φ$_{n}$(m) be the m-th figure in a$_{n}$. Let β be the sequence with 1-$\phi_n(n)$ as its n-th figure. Since β is computable, there exists a number K such that 1-$\phi_n(n)$ = φ$_{K}$(n) all n. Putting n = K, we have 1 = 2φ$_{K}$(K), i.e. 1 is even. This is impossible. The computable sequences are therefore not enumerable".

The fallacy in this argument lies in the assumption that β is computable. It would be true if we could enumerate the computable sequences by finite means, but the problem of enumerating computable sequences is equivalent to the problem of finding out whether a given number is the D.N of a circle-free machine, and we have no general process for doing this in a finite number of steps. In fact, by applying the diagonal process argument correctly, we can show that there cannot be any such general process.

The simplest and most direct proof of this is by showing that, if this general process exists, then there is a machine which computes β. This proof, although perfectly sound, has the disadvantage that it may leave the reader with a feeling that "there must be something wrong". The proof which I shall give has not this disadvantage, and gives a certain insight into the significance of the idea "circle-free". It depends not on constructing β, but on constructing β', whose n-th figure is $\phi_n(n)$.

* Cf. Hobson, Theory of functions of a real variable (2nd ed., 1921), 87, 88.

Let us suppose that there is such a process; that is to say, that we can invent a machine $\mathfrak{O}$ which, when supplied with the S.D of any computing machine $\mathcal{M}$ will test this S.D and if $\mathcal{M}$ is circular will mark the S.D with the symbol “$u$” and if it is circle-free will mark it with “$s$”. By combining the machines $\mathfrak{O}$ and $\mathfrak{M}$ we could construct a machine $\mathfrak{M}$ to compute the sequence $\beta'$. The machine $\mathfrak{O}$ may require a tape. We may suppose that it uses the $E$-squares beyond all symbols on $F$-squares, and that when it has reached its verdict all the rough work done by $\mathfrak{O}$ is erased.

The machine $\mathfrak{M}$ has its motion divided into sections. In the first $N-1$ sections, among other things, the integers $1, 2, \dots, N-1$ have been written down and tested by the machine $\mathfrak{O}$. A certain number, say $R(N-1)$, of them have been found to be the D.N’s of circle-free machines. In the $N$-th section the machine $\mathfrak{O}$ tests the number $N$. If $N$ is satisfactory, *i.e.*, if it is the D.N of a circle-free machine, then $R(N) = 1 + R(N-1)$ and the first $R(N)$ figures of the sequence of which a D.N is $N$ are calculated. The $R(N)$-th figure of this sequence is written down as one of the figures of the sequence $\beta'$ computed by $\mathfrak{M}$. If $N$ is not satisfactory, then $R(N) = R(N-1)$ and the machine goes on to the $(N+1)$-th section of its motion.

From the construction of $\mathfrak{M}$ we can see that $\mathfrak{M}$ is circle-free. Each section of the motion of $\mathfrak{M}$ comes to an end after a finite number of steps. For, by our assumption about $\mathfrak{O}$, the decision as to whether $N$ is satisfactory is reached in a finite number of steps. If $N$ is not satisfactory, then the $N$-th section is finished. If $N$ is satisfactory, this means that the machine $\mathcal{M}(N)$ whose D.N is $N$ is circle-free, and therefore its $R(N)$-th figure can be calculated in a finite number of steps. When this figure has been calculated and written down as the $R(N)$-th figure of $\beta'$, the $N$-th section is finished. Hence $\mathfrak{M}$ is circle-free.

Now let $K$ be the D.N of $\mathfrak{M}$. What does $\mathfrak{M}$ do in the $K$-th section of its motion? It must test whether $K$ is satisfactory, giving a verdict “$s$” or “$u$”. Since $K$ is the D.N of $\mathfrak{M}$ and since $\mathfrak{M}$ is circle-free, the verdict cannot be “$u$”. On the other hand the verdict cannot be “$s$”. For if it were, then in the $K$-th section of its motion $\mathfrak{M}$ would be bound to compute the first $R(K-1)+1 = R(K)$ figures of the sequence computed by the machine with $K$ as its D.N and to write down the $R(K)$-th as a figure of the sequence computed by $\mathfrak{M}$. The computation of the first $R(K)-1$ figures would be carried out all right, but the instructions for calculating the $R(K)$-th would amount to “calculate the first $R(K)$ figures computed by $H$ and write down the $R(K)$-th”. This $R(K)$-th figure would never be found. *I.e.*, $\mathfrak{M}$ is circular, contrary both to what we have found in the last paragraph and to the verdict “$s$”. Thus both verdicts are impossible and we conclude that there can be no machine $\mathfrak{O}$.

We can show further that *there can be no machine $\mathcal{E}$ which, when supplied with the S.D of an arbitrary machine $\mathcal{U}$, will determine whether $\mathcal{U}$ ever prints a given symbol (0 say).*

We will first show that, if there is a machine $\mathcal{E}$, then there is a general process for determining whether a given machine $\mathcal{U}$ prints 0 infinitely often. Let $\mathcal{U}_1$ be a machine which prints the same sequence as $\mathcal{U}$, except that in the position where the first 0 printed by $\mathcal{U}$ stands, $\mathcal{U}_1$ prints $\overline{0}$. $\mathcal{U}_2$ is to have the first two symbols 0 replaced by $\overline{0}$, and so on. Thus, if $\mathcal{U}$ were to print

$$A B A 0 1 A A B 0 0 1 0 A B \dots,$$

then $\mathcal{U}_1$ would print

$$A B A \overline{0} 1 A A B 0 0 1 0 A B \dots$$

and $\mathcal{U}_2$ would print

$$A B A \overline{0} 1 A A B \overline{0} 0 1 0 A B \dots.$$

Now let $\mathcal{E}$ be a machine which, when supplied with the S.D of $\mathcal{U}$, will write down successively the S.D of $\mathcal{U}$, of $\mathcal{U}_1$, of $\mathcal{U}_2$, ... (there is such a machine). We combine $\mathcal{E}$ with $\mathcal{E}$ and obtain a new machine, $\mathcal{G}$. In the motion of $\mathcal{G}$ first $\mathcal{E}$ is used to write down the S.D of $\mathcal{U}$, and then $\mathcal{E}$ tests it: 0: is written if it is found that $\mathcal{U}$ never prints 0; then $\mathcal{E}$ writes the S.D of $\mathcal{U}_1$, and this is tested, 0: being printed if and only if $\mathcal{U}_1$ never prints 0, and so on. Now let us test $\mathcal{G}$ with $\mathcal{E}$. If it is found that $\mathcal{G}$ never prints 0, then $\mathcal{U}$ prints 0 infinitely often; if $\mathcal{G}$ prints 0 sometimes, then $\mathcal{U}$ does not print 0 infinitely often.

Similarly there is a general process for determining whether $\mathcal{U}$ prints 1 infinitely often. By a combination of these processes we have a process for determining whether $\mathcal{U}$ prints an infinity of figures, *i.e.* we have a process for determining whether $\mathcal{U}$ is circle-free. There can therefore be no machine $\mathcal{E}$.

The expression "there is a general process for determining ..." has been used throughout this section as equivalent to "there is a machine which will determine ...". This usage can be justified if and only if we can justify our definition of "computable". For each of these "general process" problems can be expressed as a problem concerning a general process for determining whether a given integer $n$ has a property $G(n)$ [e.g. $G(n)$ might mean "$n$ is satisfactory" or "$n$ is the Gödel representation of a provable formula"], and this is equivalent to computing a number whose $n$-th figure is 1 if $G(n)$ is true and 0 if it is false.

## 9. *The extent of the computable numbers.*

No attempt has yet been made to show that the “computable” numbers include all numbers which would naturally be regarded as computable. All arguments which can be given are bound to be, fundamentally, appeals to intuition, and for this reason rather unsatisfactory mathematically. The real question at issue is “What are the possible processes which can be carried out in computing a number?”

The arguments which I shall use are of three kinds.

(a) A direct appeal to intuition.

(b) A proof of the equivalence of two definitions (in case the new definition has a greater intuitive appeal).

(c) Giving examples of large classes of numbers which are computable.

Once it is granted that computable numbers are all “computable”, several other propositions of the same character follow. In particular, it follows that, if there is a general process for determining whether a formula of the Hilbert function calculus is provable, then the determination can be carried out by a machine.

I. [Type (a)]. This argument is only an elaboration of the ideas of § 1.

Computing is normally done by writing certain symbols on paper. We may suppose this paper is divided into squares like a child’s arithmetic book. In elementary arithmetic the two-dimensional character of the paper is sometimes used. But such a use is always avoidable, and I think that it will be agreed that the two-dimensional character of paper is no essential of computation. I assume then that the computation is carried out on one-dimensional paper, *i.e.* on a tape divided into squares. I shall also suppose that the number of symbols which may be printed is finite. If we were to allow an infinity of symbols, then there would be symbols differing to an arbitrarily small extent†. The effect of this restriction of the number of symbols is not very serious. It is always possible to use sequences of symbols in the place of single symbols. Thus an Arabic numeral such as 17 or 999999999999999 is normally treated as a single symbol. Similarly in any European language words are treated as single symbols (Chinese, however, attempts to have an enumerable infinity of symbols). The differences from our point of view between the single and compound symbols is that the compound symbols, if they are too lengthy, cannot be observed at one glance. This is in accordance with experience. We cannot tell at a glance whether 999999999999999 and 999999999999999 are the same.

† If we regard a symbol as literally printed on a square we may suppose that the square is $0 \leq x \leq 1$, $0 \leq y \leq 1$. The symbol is defined as a set of points in this square, viz. the set occupied by printer’s ink. If these sets are restricted to be measurable, we can define the “distance” between two symbols as the cost of transforming one symbol into the other if the cost of moving unit area of printer’s ink unit distance is unity, and there is an infinite supply of ink at $x = 2$, $y = 0$. With this topology the symbols form a conditionally compact space.

The behaviour of the computer at any moment is determined by the symbols which he is observing, and his "state of mind" at that moment. We may suppose that there is a bound $B$ to the number of symbols or squares which the computer can observe at one moment. If he wishes to observe more, he must use successive observations. We will also suppose that the number of states of mind which need be taken into account is finite. The reasons for this are of the same character as those which restrict the number of symbols. If we admitted an infinity of states of mind, some of them will be "arbitrarily close" and will be confused. Again, the restriction is not one which seriously affects computation, since the use of more complicated states of mind can be avoided by writing more symbols on the tape.

Let us imagine the operations performed by the computer to be split up into "simple operations" which are so elementary that it is not easy to imagine them further divided. Every such operation consists of some change of the physical system consisting of the computer and his tape. We know the state of the system if we know the sequence of symbols on the tape, which of these are observed by the computer (possibly with a special order), and the state of mind of the computer. We may suppose that in a simple operation not more than one symbol is altered. Any other changes can be split up into simple changes of this kind. The situation in regard to the squares whose symbols may be altered in this way is the same as in regard to the observed squares. We may, therefore, without loss of generality, assume that the squares whose symbols are changed are always "observed" squares.

Besides these changes of symbols, the simple operations must include changes of distribution of observed squares. The new observed squares must be immediately recognisable by the computer. I think it is reasonable to suppose that they can only be squares whose distance from the closest of the immediately previously observed squares does not exceed a certain fixed amount. Let us say that each of the new observed squares is within $L$ squares of an immediately previously observed square.

In connection with "immediate recognisability", it may be thought that there are other kinds of square which are immediately recognisable. In particular, squares marked by special symbols might be taken as immediately recognisable. Now if these squares are marked only by single symbols there can be only a finite number of them, and we should not upset our theory by adjoining these marked squares to the observed squares. If, on the other hand, they are marked by a sequence of symbols, we cannot regard the process of recognition as a simple process. This is a fundamental point and should be illustrated. In most mathematical papers the equations and theorems are numbered. Normally the numbers do not go beyond (say) 1000. It is, therefore, possible to recognise a theorem at a glance by its number. But if the paper was very long, we might reach Theorem 157767733443477; then, further on in the paper, we might find "... hence (applying Theorem 157767733443477) we have ...". In order to make sure which was the relevant theorem we should have to compare the two numbers figure by figure, possibly ticking the figures off in pencil to make sure of their not being counted twice. If in spite of this it is still thought that there are other "immediately recognisable" squares, it does not upset my contention so long as these squares can be found by some process of which my type of machine is capable. This idea is developed in III below.

The simple operations must therefore include:

(a) Changes of the symbol on one of the observed squares.

(b) Changes of one of the squares observed to another square within $L$ squares of one of the previously observed squares.

It may be that some of these changes necessarily involve a change of state of mind. The most general single operation must therefore be taken to be one of the following:

(A) A possible change (a) of symbol together with a possible change of state of mind.

(B) A possible change (b) of observed squares, together with a possible change of state of mind.

The operation actually performed is determined, as has been suggested on p. 250, by the state of mind of the computer and the observed symbols. In particular, they determine the state of mind of the computer after the operation is carried out.

We may now construct a machine to do the work of this computer. To each state of mind of the computer corresponds an "$m$-configuration" of the machine. The machine scans $B$ squares corresponding to the $B$ squares observed by the computer. In any move the machine can change a symbol on a scanned square or can change any one of the scanned squares to another square distant not more than $L$ squares from one of the other scanned squares. The move which is done, and the succeeding configuration, are determined by the scanned symbol and the m-configuration. The machines just described do not differ very essentially from computing machines as defined in § 2, and corresponding to any machine of this type a computing machine can be constructed to compute the same sequence, that is to say the sequence computed by the computer.

II. [Type (b)].

If the notation of the Hilbert functional calculus† is modified so as to be systematic, and so as to involve only a finite number of symbols, it becomes possible to construct an automatic‡ machine M, which will find all the provable formulae of the calculus§.

Now let a be a sequence, and let us denote by G_a(x) the proposition "The x-th figure of a is 1", so that -G_a(x) means "The x-th figure of a is 0". Suppose further that we can find a set of properties which define the sequence a and which can be expressed in terms of G_a(x) and of the propositional functions N(x) meaning "x is a non-negative integer" and F(x, y) meaning "y = x + 1". When we join all these formulae together conjunctively, we shall have a formula, M say, which defines a. The terms of M must include the necessary parts of the Peano axioms, viz.,

$$(\exists u) N(u) \& (x) \left( N(x) \rightarrow (\exists y) F(x, y) \right) \& \left( F(x, y) \rightarrow N(y) \right),$$

which we will abbreviate to P.

When we say "M defines a", we mean that -M is not a provable formula, and also that, for each n, one of the following formulae (A_n) or (B_n) is provable.

$$\mathfrak{M} \& F^{(n)} \rightarrow G_a(u^{(n)}), \tag{$A_n$}$$

$$\mathfrak{M} \& F^{(n)} \rightarrow \left( -G_a(u^{(n)}) \right), \tag{$B_n$},$$

where F^{(n)} stands for F(u, u') & F(u', u'') & ... F(u^{(n-1)}, u^{(n)}).

† The expression "the functional calculus" is used throughout to mean the restricted Hilbert functional calculus.

‡ It is most natural to construct first a choice machine (§ 2) to do this. But it is then easy to construct the required automatic machine. We can suppose that the choices are always choices between two possibilities 0 and 1. Each proof will then be determined by a sequence of choices i_1, i_2, ..., i_n (i_1 = 0 or 1, i_2 = 0 or 1, ..., i_n = 0 or 1), and hence the number 2^n + i_1 2^{n-1} + i_2 2^{n-2} + ... + i_n completely determines the proof. The automatic machine carries out successively proof 1, proof 2, proof 3, ...

§ The author has found a description of such a machine.

|| The negation sign is written before an expression and not over it.

¶ A sequence of r primes is denoted by 'r'.

I say that $\alpha$ is then a computable sequence: a machine $\mathcal{H}_{\alpha}$ to compute $\alpha$ can be obtained by a fairly simple modification of $\mathcal{H}$.

We divide the motion of $\mathcal{H}_{\alpha}$ into sections. The $n$-th section is devoted to finding the $n$-th figure of $\alpha$. After the $(n-1)$-th section is finished a double colon :: is printed after all the symbols, and the succeeding work is done wholly on the squares to the right of this double colon. The first step is to write the letter “$A$” followed by the formula $(A_n)$ and then “$B$” followed by $(B_n)$. The machine $\mathcal{H}_{\alpha}$ then starts to do the work of $\mathcal{H}$, but whenever a provable formula is found, this formula is compared with $(A_n)$ and with $(B_n)$. If it is the same formula as $(A_n)$, then the figure “1” is printed, and the $n$-th section is finished. If it is $(B_n)$, then “0” is printed and the section is finished. If it is different from both, then the work of $\mathcal{H}$ is continued from the point at which it had been abandoned. Sooner or later one of the formulae $(A_n)$ or $(B_n)$ is reached; this follows from our hypotheses about $\alpha$ and $\mathcal{H}$, and the known nature of $\mathcal{H}$. Hence the $n$-th section will eventually be finished. $\mathcal{H}_{\alpha}$ is circle-free; $\alpha$ is computable.

It can also be shown that the numbers $\alpha$ definable in this way by the use of axioms include all the computable numbers. This is done by describing computing machines in terms of the function calculus.

It must be remembered that we have attached rather a special meaning to the phrase “$\mathcal{H}$ defines $\alpha$”. The computable numbers do not include all (in the ordinary sense) definable numbers. Let $\delta$ be a sequence whose $n$-th figure is 1 or 0 according as $n$ is or is not satisfactory. It is an immediate consequence of the theorem of § 8 that $\delta$ is not computable. It is (so far as we know at present) possible that any assigned number of figures of $\delta$ can be calculated, but not by a uniform process. When sufficiently many figures of $\delta$ have been calculated, an essentially new method is necessary in order to obtain more figures.

III. This may be regarded as a modification of I or as a corollary of II.

We suppose, as in I, that the computation is carried out on a tape; but we avoid introducing the “state of mind” by considering a more physical and definite counterpart of it. It is always possible for the computer to break off from his work, to go away and forget all about it, and later to come back and go on with it. If he does this he must leave a note of instructions (written in some standard form) explaining how the work is to be continued. This note is the counterpart of the “state of mind”. We will suppose that the computer works in such a desultory manner that he never does more than one step at a sitting. The note of instructions must enable him to carry out one step and write the next note. Thus the state of progress of the computation at any stage is completely determined by the note of instructions and the symbols on the tape. That is, the state of the system may be described by a single expression (sequence of symbols), consisting of the symbols on the tape followed by $\Delta$ (which we suppose not to appear elsewhere) and then by the note of instructions. This expression may be called the "state formula". We know that the state formula at any given stage is determined by the state formula before the last step was made, and we assume that the relation of these two formulae is expressible in the functional calculus. In other words, we assume that there is an axiom $\mathfrak{A}$ which expresses the rules governing the behaviour of the computer, in terms of the relation of the state formula at any stage to the state formula at the preceding stage. If this is so, we can construct a machine to write down the successive state formulae, and hence to compute the required number.

## 10. *Examples of large classes of numbers which are computable.*

It will be useful to begin with definitions of a computable function of an integral variable and of a computable variable, etc. There are many equivalent ways of defining a computable function of an integral variable. The simplest is, possibly, as follows. If $\gamma$ is a computable sequence in which 0 appears infinitely† often, and $n$ is an integer, then let us define $\xi(\gamma, n)$ to be the number of figures 1 between the $n$-th and the $(n+1)$-th figure 0 in $\gamma$. Then $\phi(n)$ is computable if, for all $n$ and some $\gamma$, $\phi(n) = \xi(\gamma, n)$. An equivalent definition is this. Let $H(x, y)$ mean $\phi(x) = y$. Then, if we can find a contradiction-free axiom $\mathfrak{A}_{\phi}$, such that $\mathfrak{A}_{\phi} \rightarrow P$, and if for each integer $n$ there exists an integer $N$, such that

$$\mathfrak{A}_{\phi} \ \& \ F^{(N)} \rightarrow H(u^{(n)}, u^{(\phi(n))}),$$

and such that, if $m \neq \phi(n)$, then, for some $N'$,

$$\mathfrak{A}_{\phi} \ \& \ F^{(N')} \rightarrow \left( -H(u^{(n)}, u^{(m)}) \right),$$

then $\phi$ may be said to be a computable function.

† If $\mathfrak{M}$ computes $\gamma$, then the problem whether $\mathfrak{M}$ prints 0 infinitely often is of the same character as the problem whether $\mathfrak{M}$ is circle-free.

We cannot define general computable functions of a real variable, since there is no general method of describing a real number, but we can define a computable function of a computable variable. If $n$ is satisfactory, let $\gamma_n$ be the number computed by $\mathfrak{A}(n)$, and let

$$a_n = \tan \left( \pi(\gamma_n - \frac{1}{2}) \right),$$

unless $\gamma_n = 0$ or $\gamma_n = 1$, in either of which cases $a_n = 0$. Then, as $n$ runs through the satisfactory numbers, $a_n$ runs through the computable numbers†. Now let $\phi(n)$ be a computable function which can be shown to be such that for any satisfactory argument its value is satisfactory‡. Then the function $f$, defined by $f(a_n) = a_{\phi(n)}$, is a computable function and all computable functions of a computable variable are expressible in this form.

† A function $a_n$ may be defined in many other ways so as to run through the computable numbers.

‡ Although it is not possible to find a general process for determining whether a given number is satisfactory, it is often possible to show that certain classes of numbers are satisfactory.

Similar definitions may be given of computable functions of several variables, computable-valued functions of an integral variable, etc.

I shall enunciate a number of theorems about computability, but I shall prove only (ii) and a theorem similar to (iii).

(i) A computable function of a computable function of an integral or computable variable is computable.

(ii) Any function of an integral variable defined recursively in terms of computable functions is computable. *I.e.* if $\phi(m, n)$ is computable, and $r$ is some integer, then $\eta(n)$ is computable, where

$$\eta(0) = r,$$

$$\eta(n) = \phi(n, \eta(n-1)).$$

(iii) If $\phi(m, n)$ is a computable function of two integral variables, then $\phi(n, n)$ is a computable function of $n$.

(iv) If $\phi(n)$ is a computable function whose value is always 0 or 1, then the sequence whose $n$-th figure is $\phi(n)$ is computable.

Dedekind's theorem does not hold in the ordinary form if we replace "real" throughout by "computable". But it holds in the following form:

(v) If $G(a)$ is a propositional function of the computable numbers and

$$(a) \quad (\exists \alpha)(\exists \beta) \{ G(\alpha) \ \& \ \left( -G(\beta) \right) \},$$

$$(b) \quad G(\alpha) \ \& \ \left( -G(\beta) \right) \rightarrow (\alpha < \beta),$$

and there is a general process for determining the truth value of $G(a)$, then there is a computable number $\xi$ such that

$$G(a) \rightarrow a \leqslant \xi,$$
$$-G(a) \rightarrow a \geqslant \xi.$$

In other words, the theorem holds for any section of the computables such that there is a general process for determining to which class a given number belongs.

Owing to this restriction of Dedekind's theorem, we cannot say that a computable bounded increasing sequence of computable numbers has a computable limit. This may possibly be understood by considering a sequence such as

$$-1, -\frac{1}{2}, -\frac{1}{4}, -\frac{1}{8}, -\frac{1}{16}, \frac{1}{2}, \dots.$$

On the other hand, (v) enables us to prove

(vi) If $a$ and $\beta$ are computable and $a < \beta$ and $\phi(a) < 0 < \phi(\beta)$, where $\phi(a)$ is a computable increasing continuous function, then there is a unique computable number $\gamma$, satisfying $a < \gamma < \beta$ and $\phi(\gamma) = 0$.

### *Computable convergence.*

We shall say that a sequence $\beta_n$ of computable numbers *converges computably* if there is a computable integral valued function $N(\epsilon)$ of the computable variable $\epsilon$, such that we can show that, if $\epsilon > 0$ and $n > N(\epsilon)$ and $m > N(\epsilon)$, then $|\beta_n - \beta_m| < \epsilon$.

We can then show that

(vii) A power series whose coefficients form a computable sequence of computable numbers is computably convergent at all computable points in the interior of its interval of convergence.

(viii) The limit of a computably convergent sequence is computable.

And with the obvious definition of "uniformly computably convergent":

(ix) The limit of a uniformly computably convergent computable sequence of computable functions is a computable function. Hence

(x) The sum of a power series whose coefficients form a computable sequence is a computable function in the interior of its interval of convergence.

From (viii) and $\pi = 4(1 - \frac{1}{3} + \frac{1}{5} - \dots)$ we deduce that $\pi$ is computable.

From $e = 1 + 1 + \frac{1}{2!} + \frac{1}{3!} + \dots$ we deduce that $e$ is computable.

From (vi) we deduce that all real algebraic numbers are computable.

From (vi) and (x) we deduce that the real zeros of the Bessel functions are computable.

### *Proof of (ii).*

Let $H(x, y)$ mean “$\eta(x) = y$”, and let $K(x, y, z)$ mean “$\phi(x, y) = z$”. $\mathfrak{A}_{\phi}$ is the axiom for $\phi(x, y)$. We take $\mathfrak{A}_{\eta}$ to be

$$\mathfrak{A}_{\phi} \ \& \ P \ \& \ \left( F(x, y) \to G(x, y) \right) \ \& \ \left( G(x, y) \ \& \ G(y, z) \to G(x, z) \right)$$

$$\& \ \left( F^{(r)} \to H(u, u^{(r)}) \right) \ \& \ \left( F(v, w) \ \& \ H(v, x) \ \& \ K(w, x, z) \to H(w, z) \right)$$

$$\& \ \left[ H(w, z) \ \& \ G(z, t) \ \vee \ G(t, z) \to \left( -H(w, t) \right) \right].$$

I shall not give the proof of consistency of $\mathfrak{A}_{\eta}$. Such a proof may be constructed by the methods used in Hilbert and Bernays, Grundlagen der Mathematik (Berlin, 1934), p. 209 et seq. The consistency is also clear from the meaning.

Suppose that, for some $n$, $N$, we have shown

$$\mathfrak{A}_{\eta} \ \& \ F^{(N)} \to H(u^{(n-1)}, u^{(\eta(n-1))}),$$

then, for some $M$,

$$\mathfrak{A}_{\phi} \ \& \ F^{(M)} \to K(u^{(n)}, u^{(\eta(n-1))}, u^{(\eta(n))}),$$

$$\mathfrak{A}_{\eta} \ \& \ F^{(M)} \to F(u^{(n-1)}, u^{(n)}) \ \& \ H(u^{(n-1)}, u^{(\eta(n-1))})$$

$$\& \ K(u^{(n)}, u^{(\eta(n-1))}, u^{(\eta(n))}),$$

and

$$\mathfrak{A}_{\eta} \ \& \ F^{(M)} \to [F(u^{(n-1)}, u^{(n)}) \ \& \ H(u^{(n-1)}, u^{(\eta(n-1))})$$

$$\& \ K(u^{(n)}, u^{(\eta(n-1))}, u^{(\eta(n))}) \to H(u^{(n)}, u^{(\eta(n))})].$$

Hence $\mathfrak{A}_{\eta} \ \& \ F^{(M)} \to H(u^{(n)}, u^{(\eta(n))}).$

Also $\mathfrak{A}_{\eta} \ \& \ F^{(r)} \to H(u, u^{(\eta(0))}).$

Hence for each $n$ some formula of the form

$$\mathfrak{A}_{\eta} \ \& \ F^{(M)} \to H(u^{(n)}, u^{(\eta(n))})$$

is provable. Also, if $M' \geqslant M$ and $M' \geqslant m$ and $m \neq \eta(n)$, then

$$\mathfrak{A}_{\eta} \ \& \ F^{(M')} \to G(u^{(\eta(n))}, u^{(m)}) \ \vee \ G(u^{(m)}, u^{(\eta(n))})$$

and

$$\mathfrak{A}_{\eta} \& F^{(M')} \rightarrow \left[ \{G(u^{(\eta(n))}, u^{(m)}) \vee G(u^{(m)}, u^{(\eta(n))}) \} \& H(u^{(n)}, u^{(\eta(n))}) \rightarrow (-H(u^{(n)}, u^{(m)})) \right].$$

Hence $$\mathfrak{A}_{\eta} \& F^{(M')} \rightarrow (-H(u^{(n)}, u^{(m)})).$$

The conditions of our second definition of a computable function are therefore satisfied. Consequently $\eta$ is a computable function.

### *Proof of a modified form of (iii).*

Suppose that we are given a machine $\mathfrak{N}$, which, starting with a tape bearing on it $\text{ə}\text{ə}$ followed by a sequence of any number of letters "F" on $F$-squares and in the $m$-configuration $b$, will compute a sequence $\gamma_n$ depending on the number $n$ of letters "F". If $\phi_n(m)$ is the $m$-th figure of $\gamma_n$, then the sequence $\beta$ whose $n$-th figure is $\phi_n(n)$ is computable.

We suppose that the table for $\mathfrak{N}$ has been written out in such a way that in each line only one operation appears in the operations column. We also suppose that $\Xi, \Theta, \overline{0}$, and $\overline{1}$ do not occur in the table, and we replace $\text{ə}$ throughout by $\Theta, 0$ by $\overline{0}$, and $1$ by $\overline{1}$. Further substitutions are then made. Any line of form

$$\mathfrak{A} \quad a \quad P\overline{0} \quad \mathfrak{B}$$

we replace by

$$\mathfrak{A} \quad a \quad P\overline{0} \quad \operatorname{re}(\mathfrak{B}, u, h, k)$$

and any line of the form

$$\mathfrak{A} \quad a \quad P\overline{1} \quad \mathfrak{B}$$

by $$\mathfrak{A} \quad a \quad P\overline{1} \quad \operatorname{re}(\mathfrak{B}, v, h, k)$$

and we add to the table the following lines:

$$u \quad \operatorname{pe}(u_1, 0)$$

$$u_1 \quad R, Pk, R, P\Theta, R, P\Theta \quad u_2$$

$$u_2 \quad \operatorname{re}(u_3, u_3, k, h)$$

$$u_3 \quad \operatorname{pe}(u_2, F)$$

and similar lines with $v$ for $u$ and $1$ for $0$ together with the following line

$$c \quad R, P\Xi, R, Ph \quad b.$$

We then have the table for the machine $\mathfrak{N}'$ which computes $\beta$. The initial $m$-configuration is $c$, and the initial scanned symbol is the second $\text{ə}$.

## 11. *Application to the Entscheidungsproblem.*

The results of § 8 have some important applications. In particular, they can be used to show that the Hilbert Entscheidungsproblem can have no solution. For the present I shall confine myself to proving this particular theorem. For the formulation of this problem I must refer the reader to Hilbert and Ackermann's *Grundzüge der Theoretischen Logik* (Berlin, 1931), chapter 3.

I propose, therefore, to show that there can be no general process for determining whether a given formula $\mathfrak{A}$ of the functional calculus $\mathbf{K}$ is provable, *i.e.* that there can be no machine which, supplied with any one $\mathfrak{A}$ of these formulae, will eventually say whether $\mathfrak{A}$ is provable.

It should perhaps be remarked that what I shall prove is quite different from the well-known results of Gödel†. Gödel has shown that (in the formalism of Principia Mathematica) there are propositions $\mathfrak{A}$ such that neither $\mathfrak{A}$ nor $-\mathfrak{A}$ is provable. As a consequence of this, it is shown that no proof of consistency of Principia Mathematica (or of $\mathbf{K}$) can be given within that formalism. On the other hand, I shall show that there is no general method which tells whether a given formula $\mathfrak{A}$ is provable in $\mathbf{K}$, or, what comes to the same, whether the system consisting of $\mathbf{K}$ with $-\mathfrak{A}$ adjoined as an extra axiom is consistent.

If the negation of what Gödel has shown had been proved, *i.e.* if, for each $\mathfrak{A}$, either $\mathfrak{A}$ or $-\mathfrak{A}$ is provable, then we should have an immediate solution of the Entscheidungsproblem. For we can invent a machine $\mathfrak{M}$ which will prove consecutively all provable formulae. Sooner or later $\mathfrak{M}$ will reach either $\mathfrak{A}$ or $-\mathfrak{A}$. If it reaches $\mathfrak{A}$, then we know that $\mathfrak{A}$ is provable. If it reaches $-\mathfrak{A}$, then, since $\mathbf{K}$ is consistent (Hilbert and Ackermann, p. 65), we know that $\mathfrak{A}$ is not provable.

† *Loc. cit.*

Owing to the absence of integers in $\mathbf{K}$ the proofs appear somewhat lengthy. The underlying ideas are quite straightforward.

Corresponding to each computing machine $\mathfrak{M}$ we construct a formula $\text{Un}(\mathfrak{M})$ and we show that, if there is a general method for determining whether $\text{Un}(\mathfrak{M})$ is provable, then there is a general method for determining whether $\mathfrak{M}$ ever prints 0.

The interpretations of the propositional functions involved are as follows :

$R_{S_i}(x, y)$ is to be interpreted as "in the complete configuration $x$ (of $\mathfrak{M}$) the symbol on the square $y$ is $S$".

$I(x, y)$ is to be interpreted as "in the complete configuration $x$ the square $y$ is scanned".

$K_{q_m}(x)$ is to be interpreted as "in the complete configuration $x$ the $m$-configuration is $q_m$."

$F(x, y)$ is to be interpreted as "$y$ is the immediate successor of $x$".

Inst $\{q_i S_j S_k L q_l\}$ is to be an abbreviation for

$$
\begin{array}{l}
(x, y, x', y') \left\{ \left( R_{S_j}(x, y) \& I(x, y) \& K_{q_i}(x) \& F(x, x') \& F(y', y) \right) \right. \\
\quad \rightarrow \left( I(x', y') \& R_{S_k}(x', y) \& K_{q_l}(x') \right. \\
\quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \& (z) \left[ F(y', z) \vee \left( R_{S_j}(x, z) \rightarrow R_{S_k}(x', z) \right) \right] \Bigg\}.
\end{array}
$$

Inst $\{q_i S_j S_k R q_l\}$ and Inst $\{q_i S_j S_k N q_l\}$

are to be abbreviations for other similarly constructed expressions.

Let us put the description of $\mathfrak{M}$ into the first standard form of § 6. This description consists of a number of expressions such as "$q_i S_j S_k L q_l$" (or with $R$ or $N$ substituted for $L$). Let us form all the corresponding expressions such as Inst $\{q_i S_j S_k L q_l\}$ and take their logical sum. This we call Des $(\mathfrak{M})$.

The formula Un $(\mathfrak{M})$ is to be

$$
\begin{aligned}
(\exists u) [&N(u) \& (x)(N(x) \rightarrow (\exists x')F(x,x')) \\
&\& (y,z)(F(y,z) \rightarrow N(y) \& N(z)) \& (y)R_{S_0}(u,y) \\
&\& I(u,u) \& K_{q_1}(u) \& \text{Des}(\mathfrak{M})] \\
&\rightarrow (\exists s)(\exists t)[N(s) \& N(t) \& R_{S_1}(s,t)].
\end{aligned}
$$

$[N(u) \& \dots \& \text{Des}(\mathfrak{M})]$ may be abbreviated to $A(\mathfrak{M})$.

When we substitute the meanings suggested on p. 259-60 we find that Un $(\mathfrak{M})$ has the interpretation "in some complete configuration of $\mathfrak{M}$, $S_1$ (i.e. 0) appears on the tape". Corresponding to this I prove that

(a) If $S_1$ appears on the tape in some complete configuration of $\mathfrak{M}$, then $\operatorname{Un}(\mathfrak{M})$ is provable.
(b) If $\operatorname{Un}(\mathfrak{M})$ is provable, then $S_1$ appears on the tape in some complete configuration of $\mathfrak{M}$.

When this has been done, the remainder of the theorem is trivial.

LEMMA 1. If $S_1$ appears on the tape in some complete configuration of $\mathcal{M}$, then $\text{Un}(\mathcal{M})$ is provable.

We have to show how to prove $\text{Un}(\mathcal{M})$. Let us suppose that in the $n$-th complete configuration the sequence of symbols on the tape is $S_{r(n,0)}, S_{r(n,1)}, \ldots, S_{r(n,n)}$, followed by nothing but blanks, and that the scanned symbol is the $i(n)$-th, and that the $m$-configuration is $q_{k(n)}$. Then we may form the proposition

$$
\begin{array}{l}
R_{S_{r(n,0)}}(u^{(n)}, u) \ \& \ R_{S_{r(n,1)}}(u^{(n)}, u') \ \& \ \ldots \ \& \ R_{S_{r(n,n)}}(u^{(n)}, u^{(n)}) \\
\quad \ \& \ I(u^{(n)}, u^{(i(n))}) \ \& \ K_{q_{k(n)}}(u^{(n)}) \\
\quad \ \& \ (y) \left[ F(y, u') \ \vee \ F(u, y) \ \vee \ F(u', y) \ \vee \ \ldots \ \vee \ F(u^{(n-1)}, y) \ \vee \ R_{S_0}(u^{(n)}, y) \right],
\end{array}
$$

which we may abbreviate to $CC_n$.

As before, $F(u, u') \ \& \ F(u', u'') \ \& \ \ldots \ \& \ F(u^{(r-1)}, u^{(r)})$ is abbreviated to $F^{(r)}$.

I shall show that all formulae of the form $A(\mathcal{M}) \ \& \ F^{(n)} \to CC_n$ (abbreviated to $CF_n$) are provable. The meaning of $CF_n$ is "The $n$-th complete configuration of $\mathcal{M}$ is so and so", where "so and so" stands for the actual $n$-th complete configuration of $\mathcal{M}$. That $CF_n$ should be provable is therefore to be expected.

$CF_0$ is certainly provable, for in the complete configuration the symbols are all blanks, the $m$-configuration is $q_1$, and the scanned square is $u$, i.e. $CC_0$ is

$$
(y) \ R_{S_0}(u, y) \ \& \ I(u, u) \ \& \ K_{q_1}(u).
$$

$A(\mathcal{M}) \to CC_0$ is then trivial.

We next show that $CF_n \to CF_{n+1}$ is provable for each $n$. There are three cases to consider, according as in the move from the $n$-th to the $(n+1)$-th configuration the machine moves to left or to right or remains stationary. We suppose that the first case applies, i.e. the machine moves to the left. A similar argument applies in the other cases. If $r(n, i(n)) = a$, $r(n+1, i(n+1)) = c$, $k(i(n)) = b$, and $k(i(n+1)) = d$, then $\text{Des}(\mathcal{M})$ must include $\text{Inst}\{q_a S_b S_d L q_c\}$ as one of its terms, i.e.

$$
\text{Des}(\mathcal{M}) \to \text{Inst}\{q_a S_b S_d L q_c\}.
$$

Hence $A(\mathcal{M}) \ \& \ F^{(n+1)} \to \text{Inst}\{q_a S_b S_d L q_c\} \ \& \ F^{(n+1)}$.

But $\text{Inst}\{q_a S_b S_d L q_c\} \ \& \ F^{(n+1)} \to (CC_n \to CC_{n+1})$

is provable, and so therefore is

$$
A(\mathcal{M}) \ \& \ F^{(n+1)} \to (CC_n \to CC_{n+1})
$$

and $$\left(A(\mathcal{M}) \& F^{(n)} \to CC_n\right) \to \left(A(\mathcal{M}) \& F^{(n+1)} \to CC_{n+1}\right),$$

i.e. $$CF_n \to CF_{n+1}.$$

$CF_n$ is provable for each $n$. Now it is the assumption of this lemma that $S_1$ appears somewhere, in some complete configuration, in the sequence of symbols printed by $\mathcal{M}$; that is, for some integers $N, K, CC_N$ has $R_{S_1}(u^{(N)}, u^{(K)})$ as one of its terms, and therefore $CC_N \to R_{S_1}(u^{(N)}, u^{(K)})$ is provable. We have then

$$CC_N \to R_{S_1}(u^{(N)}, u^{(K)})$$

and $$A(\mathcal{M}) \& F^{(N)} \to CC_N.$$

We also have

$$(\exists u) A(\mathcal{M}) \to (\exists u) (\exists u') \dots (\exists u^{(N')}) \left(A(\mathcal{M}) \& F^{(N)}\right),$$

where $N' = \max(N, K)$. And so

$$\begin{array}{l} (\exists u) A(\mathcal{M}) \to (\exists u) (\exists u') \dots (\exists u^{(N')}) R_{S_1}(u^{(N)}, u^{(K)}), \\ (\exists u) A(\mathcal{M}) \to (\exists u^{(N)}) (\exists u^{(K)}) R_{S_1}(u^{(N)}, u^{(K)}), \\ (\exists u) A(\mathcal{M}) \to (\exists s) (\exists t) R_{S_1}(s, t), \end{array}$$

i.e. $\text{Un}(\mathcal{M})$ is provable.

This completes the proof of Lemma 1.

LEMMA 2. If $\text{Un}(\mathcal{M})$ is provable, then $S_1$ appears on the tape in some complete configuration of $\mathcal{M}$.

If we substitute any propositional functions for function variables in a provable formula, we obtain a true proposition. In particular, if we substitute the meanings tabulated on pp. 259-260 in $\text{Un}(\mathcal{M})$, we obtain a true proposition with the meaning "$S_1$ appears somewhere on the tape in some complete configuration of $\mathcal{M}$".

We are now in a position to show that the Entscheidungsproblem cannot be solved. Let us suppose the contrary. Then there is a general (mechanical) process for determining whether $\text{Un}(\mathcal{M})$ is provable. By Lemmas 1 and 2, this implies that there is a process for determining whether $\mathcal{M}$ ever prints 0, and this is impossible, by §8. Hence the Entscheidungsproblem cannot be solved.

In view of the large number of particular cases of solutions of the Entscheidungsproblem for formulae with restricted systems of quantors, it is interesting to express $\text{Un}(\mathcal{M})$ in a form in which all quantors are at the beginning. $\text{Un}(\mathcal{M})$ is, in fact, expressible in the form

$$(u) (\exists x) (w) (\exists u_1) \dots (\exists u_n) \mathfrak{B}, \quad \text{(I)}$$

where $\mathfrak{B}$ contains no quantors, and $n = 6$. By unimportant modifications we can obtain a formula, with all essential properties of $\text{Un}(\mathcal{M})$, which is of form (I) with $n = 5$.

*Added 28 August, 1936.*

## APPENDIX.

### *Computability and effective calculability*

The theorem that all effectively calculable ($\lambda$-definable) sequences are computable and its converse are proved below in outline. It is assumed that the terms "well-formed formula" (W.F.F.) and "conversion" as used by Church and Kleene are understood. In the second of these proofs the existence of several formulae is assumed without proof; these formulae may be constructed straightforwardly with the help of, *e.g.*, the results of Kleene in "A theory of positive integers in formal logic", *American Journal of Math.*, 57 (1935), 153-173, 219-244.

The W.F.F. representing an integer $n$ will be denoted by $N_n$. We shall say that a sequence $\gamma$ whose $n$-th figure is $\phi_\gamma(n)$ is $\lambda$-definable or effectively calculable if $1 + \phi_\gamma(u)$ is a $\lambda$-definable function of $n$, *i.e.* if there is a W.F.F. $M_\gamma$ such that, for all integers $n$,

$$\{M_\gamma\} (N_n) \text{ conv } N_{\phi_\gamma(n)+1},$$

*i.e.* $\{M_\gamma\} (N_n)$ is convertible into $\lambda xy.x(x(y))$ or into $\lambda xy.x(y)$ according as the $n$-th figure of $\lambda$ is 1 or 0.

To show that every $\lambda$-definable sequence $\gamma$ is computable, we have to show how to construct a machine to compute $\gamma$. For use with machines it is convenient to make a trivial modification in the calculus of conversion. This alteration consists in using $x, x', x'', \dots$ as variables instead of $a, b, c, \dots$. We now construct a machine $\mathcal{L}$ which, when supplied with the formula $M_\gamma$, writes down the sequence $\gamma$. The construction of $\mathcal{L}$ is somewhat similar to that of the machine $\mathcal{K}$ which proves all provable formulae of the functional calculus. We first construct a choice machine $\mathcal{L}_1$, which, if supplied with a W.F.F., $M$ say, and suitably manipulated, obtains any formula into which $M$ is convertible. $\mathcal{L}_1$ can then be modified so as to yield an automatic machine $\mathcal{L}_2$ which obtains successively all the formulae into which $M$ is convertible (cf. foot-note p. 252). The machine $\mathcal{L}$ includes $\mathcal{L}_2$ as a part. The motion of the machine $\mathcal{L}$ when supplied with the formula $M_\gamma$ is divided into sections of which the $n$-th is devoted to finding the $n$-th figure of $\gamma$. The first stage in this $n$-th section is the formation of $\{M_\gamma\}(N_n)$. This formula is then supplied to the machine $\mathcal{L}_2$, which converts it successively into various other formulae. Each formula into which it is convertible eventually appears, and each, as it is found, is compared with

$$\lambda x \left[ \lambda x' \left[ \{x\} \left( \{x\} (x') \right) \right] \right], \quad i.e. \ N_2,$$

and with $$\lambda x \left[ \lambda x' \left[ \{x\} (x') \right] \right], \quad i.e. \ N_1.$$

If it is identical with the first of these, then the machine prints the figure 1 and the $n$-th section is finished. If it is identical with the second, then 0 is printed and the section is finished. If it is different from both, then the work of $\mathcal{L}_2$ is resumed. By hypothesis, $\{M_\gamma\}(N_n)$ is convertible into one of the formulae $N_2$ or $N_1$; consequently the $n$-th section will eventually be finished, *i.e.* the $n$-th figure of $\gamma$ will eventually be written down.

To prove that every computable sequence $\gamma$ is $\lambda$-definable, we must show how to find a formula $M_\gamma$ such that, for all integers $n$,

$$\{M_\gamma\}(N_n) \text{ conv } N_{1+\phi_\gamma(n)}.$$

Let $\mathfrak{M}$ be a machine which computes $\gamma$ and let us take some description of the complete configurations of $\mathfrak{M}$ by means of numbers, *e.g.* we may take the D.N of the complete configuration as described in §6. Let $\xi(n)$ be the D.N of the $n$-th complete configuration of $\mathfrak{M}$. The table for the machine $\mathfrak{M}$ gives us a relation between $\xi(n+1)$ and $\xi(n)$ of the form

$$\xi(n+1) = \rho_\gamma(\xi(n)),$$

where $\rho_\gamma$ is a function of very restricted, although not usually very simple, form: it is determined by the table for $\mathfrak{M}$. $\rho_\gamma$ is $\lambda$-definable (I omit the proof of this), *i.e.* there is a W.F.F. $A_\gamma$ such that, for all integers $n$,

$$\{A_\gamma\}(N_{\xi(n)}) \text{ conv } N_{\xi(n+1)}.$$

Let $U$ stand for

$$\lambda u \left[ \{u\} (A_\gamma)\} (N_r) \right],$$

where $r = \xi(0)$; then, for all integers $n$,

$$\{U_\gamma\}(N_n) \text{ conv } N_{\xi(n)}.$$

It may be proved that there is a formula $V$ such that

$$\left\{ \{V\} (N_{\ell(n+1)}) \} (N_{\ell(n)}) \right\} \begin{cases} \text{conv } N_1 & \text{if, in going from the } n\text{-th to the } (n+1)\text{-th} \\ & \text{complete configuration, the figure 0 is} \\ & \text{printed.} \\ \text{conv } N_2 & \text{if the figure 1 is printed.} \\ \text{conv } N_3 & \text{otherwise.} \end{cases}$$

Let $W_\gamma$ stand for

$$\lambda u \left[ \left\{ \{V\} \left( \{A_\gamma\} \left( \{U_\gamma\} (u) \right) \right) \right\} \left( \{U_\gamma\} (u) \right) \right],$$

so that, for each integer $n$,

$$\left\{ \{V\} (N_{\ell(n+1)}) \} (N_{\ell(n)}) \text{ conv } \{W_\gamma\} (N_n), \right.$$

and let $Q$ be a formula such that

$$\left\{ \{Q\} (W_\gamma) \} (N_s) \text{ conv } N_{r(s)}, \right.$$

where $r(s)$ is the $s$-th integer $q$ for which $\{W_\gamma\} (N_q)$ is convertible into either $N_1$ or $N_2$. Then, if $M_\gamma$ stands for

$$\lambda w \left[ \{W_\gamma\} \left( \{Q\} (W_\gamma) \} (w) \right) \right],$$

it will have the required property†.

The Graduate College,
Princeton University,
New Jersey, U.S.A.

† In a complete proof of the $\lambda$-definability of computable sequences it would be best to modify this method by replacing the numerical description of the complete configurations by a description which can be handled more easily with our apparatus. Let us choose certain integers to represent the symbols and the $m$-configurations of the machine. Suppose that in a certain complete configuration the numbers representing the successive symbols on the tape are $s_1 s_2 \dots s_n$, that the $m$-th symbol is scanned, and that the $m$-configuration has the number $t$; then we may represent this complete configuration by the formula

$$\left[ [N_{s_1}, N_{s_2}, \dots, N_{s_{m-1}}], [N_t, N_{s_m}], [N_{s_{m+1}}, \dots, N_{s_n}] \right],$$

where $[a, b]$ stands for $\lambda u \left[ \{u\} (a) \} (b) \right]$,

$$[a, b, c] \text{ stands for } \lambda u \left[ \{u\} (a) \} (b) \right] (c),$$

etc.
