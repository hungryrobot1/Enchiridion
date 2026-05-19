# Chapter 5: Verbs — Tense, Mood, and the Participle

Greek verbs are more complex than Greek nouns. Where a noun changes for five cases and two numbers (ten forms), a verb can change for tense, mood, voice, person, and number — hundreds of possible forms for a single verb. This sounds overwhelming, and it would be if you tried to memorize it all.

Instead, this chapter follows the same strategy as Chapters 3 and 4: understand the *concepts* first (what do the tenses mean? what are moods?), learn to recognize the most common patterns, and let Perseus handle the rest. In Euclid, the verb system you actually encounter is surprisingly narrow — present, aorist, and perfect tenses; indicative and imperative moods; active and passive voices. In philosophical prose the range expands, but by then you'll have the framework.

By the end of this chapter you should be able to:

- Understand what each Greek tense expresses (it's not just time)
- Recognize the indicative, imperative, and infinitive in context
- Use Perseus to parse any verb form you encounter
- Understand what a participle is and why Greek uses them everywhere
- Read a Heraclitus fragment or Sappho verse with dictionary support

## The Greek Verb: An Overview

A Greek verb form encodes five pieces of information:

1. **Tense** — when and what kind of action (present, aorist, imperfect, future, perfect, pluperfect)
2. **Mood** — the speaker's attitude toward the action (indicative, imperative, subjunctive, optative)
3. **Voice** — who does the action (active, middle, passive)
4. **Person** — who is the subject (first, second, third)
5. **Number** — singular or plural

When Perseus parses a verb and tells you "3rd person singular aorist indicative active," these are the five categories it's reporting.

## Tense: Not Just Time

In English, tense is mostly about time: past, present, future. In Greek, tense conveys two things: **time** (when) and **aspect** (what kind of action). Aspect is often more important than time.

The three aspects are:

- **Continuous/repeated** (present stem) — the action is ongoing, habitual, or viewed as a process
- **Simple/completed-in-one-go** (aorist stem) — the action is viewed as a single event, without regard to duration
- **Completed-with-ongoing-results** (perfect stem) — the action is finished but its effects persist

### The Key Tenses

**Present** (ἐστίν — "is," "is being"). Ongoing or habitual action in present time. This is the most common tense in definitions and general statements.

> Σημεῖόν **ἐστιν**, οὗ μέρος οὐθέν. — "A point **is** that of which there is no part."

**Imperfect** (ἦν — "was," "was being"). Ongoing or habitual action in past time. Common in narrative but rare in Euclid.

**Aorist** (ἔδειξεν — "showed," "proved"). A single completed action in past time (in the indicative). The aorist is the default narrative tense — "this happened, then that happened." Outside the indicative, the aorist simply means "simple action" without implying past time.

**Perfect** (γέγραπται — "has been written," "stands written"). A completed action whose results are still in effect. In Euclid: ἐδείχθη — "it was shown [and the result still holds]." The perfect often signals that a previous proof is being cited.

**Future** (ἔσται — "will be"). Relatively rare in mathematical writing but common in philosophical prose.

**Pluperfect** (rare — "had been"). Past action completed before another past action. You can safely ignore this until you encounter it.

### A Note on Aspect

The distinction between present and aorist is clearest outside the indicative mood. Consider two infinitives:

- λέγειν (present infinitive) — to be speaking, to speak habitually
- εἰπεῖν (aorist infinitive) — to say (a specific thing, once)

Or two imperatives:

- γράφε (present imperative) — keep writing, write habitually
- γράψον (aorist imperative) — write [this particular thing]

Euclid uses the aorist imperative constantly: γεγράφθω ("let it have been drawn"), ἐπεζεύχθω ("let it have been joined"). These are aorist — a single completed construction, not an ongoing process.

## Mood

Mood expresses how the speaker relates to the action — as fact, command, possibility, or wish.

**Indicative** — states facts or assertions. The default mood. "The angles are equal." "It was shown." Most sentences you read will be in the indicative.

**Imperative** — gives commands or makes requests. In Euclid, the third-person imperative is ubiquitous: ἔστω ("let there be"), γεγράφθω ("let it have been drawn"). English has a weak imperative ("go," "stop"); Greek has a full system for all persons.

**Infinitive** — the "to" form of the verb (technically not a mood but behaves like one). δεῖξαι ("to show"), ποιῆσαι ("to construct"), ἀγαγεῖν ("to draw"). These appear in Euclid's enunciations: the proposition states what is *to be done*.

**Subjunctive** — expresses possibility, purpose, or expectation. Common in conditional statements and purpose clauses. You will encounter it in philosophical prose more than in Euclid.

**Optative** — expresses wishes or remote possibility. Less common in prose; more frequent in Plato and in older poetry. You can look it up when you encounter it.

For reading Euclid and basic philosophical prose, you need the indicative, imperative, and infinitive. The subjunctive and optative can wait.

## Verbs of Being and the Copula

Before turning to voice, a note about the most common verb in Greek: εἰμί ("to be"). This is a *copulative* verb — it links a subject to a predicate rather than expressing an action. In the sentence σημεῖόν **ἐστιν**, οὗ μέρος οὐθέν ("a point **is** that of which there is no part"), ἐστιν connects σημεῖον to its definition. The grammatical pattern is **subject + copula + predicate**, and both subject and predicate are in the nominative case.

Greek sometimes omits the copula entirely, especially in definitions and general statements. When you see two nominative nouns or a nominative noun and adjective with no verb between them, supply "is": γραμμὴ δὲ μῆκος ἀπλατές means "a line [is] breadthless length." The verb ἐστιν is understood. This is common enough that you should learn to expect it.

## Transitive and Intransitive Verbs

A useful distinction before we discuss voice: verbs are either *transitive* (they take a direct object — "I see **the line**") or *intransitive* (they don't — "the line **lies** evenly"). This distinction matters because only transitive verbs can be made passive: "the line is seen" works, but "the line is lied" doesn't.

In Greek, some verbs that are transitive in English are intransitive, and vice versa. Perseus and the LSJ will tell you how a verb behaves. The key thing to notice is whether a verb takes an accusative object (transitive) or not (intransitive).

## Voice

**Active** — the subject performs the action. "The line *joins* the points."

**Passive** — the subject receives the action. "The line *has been joined*." Very common in Euclid's construction steps.

**Middle** — the subject acts on or for itself, or is closely affected by the action. This voice has no single English equivalent, but modern languages offer analogies. French uses reflexive pronouns for similar ideas: *se laver* ("to wash oneself"), *se battre* ("to fight [for oneself]"). Spanish does the same: *lavarse*, *vestirse* ("to dress oneself"). In Greek, the middle voice handles all of these without needing a separate pronoun — the verb form itself signals the reflexive or self-interested quality.

Some common middle-voice meanings:
- **Reflexive**: λούομαι, "I wash (myself)" — the subject acts on itself
- **Self-interested**: αἱρέομαι, "I choose (for myself)" — the subject acts for its own benefit
- **Reciprocal**: μάχονται, "they fight (each other)" — subjects act on one another

Some verbs exist *only* in the middle voice (called "deponent" verbs). γίγνομαι ("I become") and ἔρχομαι ("I go/come") have no active forms. When you see a middle-form verb in Perseus, check whether it has an active counterpart.

In many tenses, the middle and passive forms are identical. Perseus will tell you which is which, and context usually makes it clear.

## The Participle

The participle is the most important construction to understand for reading Greek prose. A participle is a verb form that functions as an adjective — it modifies a noun while retaining verbal properties (tense, voice). English has participles too ("the running man," "the broken vase"), but Greek uses them far more extensively.

In English, we would write:

> "Since the point A is the center of the circle BCD, AC is equal to AB."

Greek can compress this:

> τοῦ Α σημείου κέντρου **ὄντος** τοῦ ΒΓΔ κύκλου, ἴση ἐστὶν ἡ ΑΓ τῇ ΑΒ.

The participle ὄντος ("being," from εἰμί) packs the whole "since A is the center" clause into a single word that agrees with σημείου in the genitive. This construction — a noun + participle in the genitive, standing independent of the main clause — is called the **genitive absolute**, and it is everywhere in Greek prose.

### Common Participle Patterns

**Circumstantial participle** — provides background: "being," "having," "when," "since," "although." Translated according to context.

**Attributive participle** — acts like an adjective: ἡ δοθεῖσα εὐθεῖα, "the given straight line." Here δοθεῖσα ("having been given") is a participle modifying εὐθεῖα.

**Supplementary participle** — completes the meaning of certain verbs: φαίνεται ὤν, "he appears to be" (literally "appears being").

**Substantive participle** — a participle used as a noun, typically with the article. This is extremely common in Greek and one of the language's most elegant features. οἱ φιλοσοφοῦντες means "the ones philosophizing" = "those who philosophize" = "philosophers." τὸ ὄν means "the being [thing]" = "that which is" = "being" (as an abstract concept). A substantive participle can serve as the subject of a sentence, its object, or any other noun role. When you see article + participle with no accompanying noun, you are looking at a substantive participle.

### Recognizing Participles

Participles decline like adjectives — they have case, gender, and number, and they agree with the noun they modify. Present active participles typically end in -ων, -ουσα, -ον (masculine, feminine, neuter nominative singular). Aorist passive participles end in -θείς, -θεῖσα, -θέν.

You do not need to memorize all participle forms. The strategy remains: when you encounter an unfamiliar word, use Perseus. If it tells you "aorist passive participle, feminine genitive singular," you now know what that means.

## Verbs in Euclid: A Small Set

Euclid uses a remarkably restricted verb vocabulary. You have already met most of the key verbs in Chapters 1 and 2. Here they are organized by function:

**Being and letting:**

| Greek | Form | Meaning |
|-------|------|---------|
| ἐστίν | 3rd sg present indicative | is |
| εἰσίν | 3rd pl present indicative | are |
| ἔστω | 3rd sg present imperative | let it be |
| ἔστωσαν | 3rd pl present imperative | let them be |

**Showing and doing:**

| Greek | Form | Meaning |
|-------|------|---------|
| δεῖξαι | aorist infinitive | to show |
| ποιῆσαι | aorist infinitive | to do, construct |
| ἐδείχθη | 3rd sg aorist passive indicative | it was shown |
| δέδεικται | 3rd sg perfect passive indicative | it has been shown |

**Geometric constructions** (all 3rd sg aorist passive imperative — "let it have been..."):

| Greek | Meaning |
|-------|---------|
| γεγράφθω | let [a circle] have been drawn |
| ἐπεζεύχθω | let [a line] have been joined |
| ἀφῃρήσθω | let [a segment] have been cut off |
| ἐκβεβλήσθω | let [a line] have been extended |
| κείσθω | let [a line] have been placed |

Notice the pattern: Euclid constructs by issuing passive imperatives. "Let a circle *have been drawn*" — the construction is stated as already completed. This is a distinctive feature of Greek mathematical style.

## Beyond Euclid: Philosophical Verbs

As you begin reading Heraclitus, Aristotle, and Plato, the verb vocabulary expands. Here are high-frequency verbs worth recognizing:

| Greek | Meaning | Notes |
|-------|---------|-------|
| εἶναι | to be | The infinitive of ἐστί. Ubiquitous. |
| γίγνεσθαι | to become, come to be | Key philosophical verb — being vs. becoming |
| λέγειν | to say, to speak | Also "to mean," "to reason" |
| ἔχειν | to have, to hold | Also "to be in a state" (ἔχει = "it is the case") |
| φαίνεσθαι | to appear, to seem | Crucial for epistemology — appearance vs. reality |
| δοκεῖν | to seem, to think | "It seems" (δοκεῖ) introduces opinions |
| ποιεῖν | to make, to do | Active creation/action |
| πάσχειν | to suffer, to experience | The passive counterpart of ποιεῖν |
| κινεῖν | to move | Central to Aristotle's physics |
| νοεῖν | to think, to perceive | Related to νοῦς (mind) |

## Smyth Reference

The following Smyth sections cover this chapter's material.

- Voices, moods, tenses (overview): §355-366
- The tenses and their meanings: §474-601
- The indicative mood: §357, 359
- The imperative: §1835-1844
- The infinitive: §469
- The participle: §470
- Genitive absolute: §2070-2075
- ω-verb conjugation (present system): §602-606
- εἰμί (to be): §768

## Exercises

### Exercise 1: Tense and Aspect in Euclid

Read through Proposition I.1 and categorize every verb by tense and mood. You should find:

- Present indicative (ἐστίν — in the enunciation and proof)
- Aorist imperative (γεγράφθω, ἐπεζεύχθω — in the construction)
- Perfect indicative (possibly in back-references to earlier proofs)
- Aorist infinitive (in the enunciation: "to construct")

Use Perseus to check your parsings. Notice how narrow Euclid's verb usage actually is.

### Exercise 2: Participles in Proposition I.4

Proposition I.4 (the Side-Angle-Side congruence theorem) is rich in participles. Read through it and identify every participle:

1. Note what noun it agrees with (check case, gender, number)
2. Determine whether it's circumstantial ("since/when"), attributive ("the given line"), or part of a genitive absolute
3. Try translating the participle phrase before checking the English

This is challenging. Don't worry about getting everything right — the goal is to start seeing how participles work in real text.

### Exercise 3: Heraclitus Fragments

The fragments of Heraclitus are short, enigmatic, and grammatically manageable. Using the Burnet edition (in your references), work through the following fragments. For each, parse the main verb and any participles.

**Fragment 1** (Burnet numbering may differ — look for the fragment that begins with τοῦ λόγου):

> τοῦ δὲ λόγου τοῦδ᾽ ἐόντος ἀεὶ ἀξύνετοι γίνονται ἄνθρωποι

- τοῦ ... λόγου ... ἐόντος — genitive absolute: "this logos being [true] always" / "although this logos exists always"
- γίνονται — 3rd pl present middle indicative: "become" / "prove to be"
- ἀξύνετοι — nominative pl adjective: "uncomprehending"

"Although this logos exists always, people prove uncomprehending."

The genitive absolute carries the concessive force ("although"). The main verb γίνονται is present tense — ongoing, habitual. People *keep on* failing to understand.

**Fragment 12** (the river fragment):

> ποταμοῖσι τοῖσιν αὐτοῖσιν ἐμβαίνουσιν ἕτερα καὶ ἕτερα ὕδατα ἐπιρρεῖ.

- ἐμβαίνουσιν — dative plural participle: "to those stepping in"
- ἐπιρρεῖ — 3rd sg present indicative: "flows upon"

"Upon those stepping into the same rivers, different and different waters flow."

Notice ἐμβαίνουσιν is a participle used substantively (with the article τοῖσιν) — "those [who are] stepping in." This is a common Greek pattern: article + participle = "the one(s) who..."

### Exercise 4: Sappho Fragment 31

Open the Wharton edition. Fragment 31 (φαίνεταί μοι κῆνος ἴσος θέοισιν...) is Sappho's most famous poem and is cited by Longinus in *On the Sublime*. It uses vocabulary you know (φαίνεται, ἴσος) alongside unfamiliar Aeolic dialect forms.

Read it aloud first — the sounds matter in lyric poetry. Then:

1. Identify φαίνεται (present middle indicative: "appears")
2. Note the dative μοι ("to me")
3. Look up unfamiliar words on Perseus

You will not understand everything. Sappho's dialect differs from Attic (broader α for η, different verb endings). But the core grammar is the same, and the emotional directness of the poem is accessible even with partial understanding.

### Exercise 5: Verb Parsing Practice

Parse the following verb forms using Perseus. For each, give the tense, mood, voice, person, and number, and the dictionary form (lemma).

1. ἐστίν
2. γεγράφθω
3. ἐδείχθη
4. δεῖξαι
5. γίνονται
6. φαίνεται
7. ἐπεζεύχθω
8. ἔστω
9. λέγω
10. ἐόντος

<details>
<summary>Answers</summary>

1. ἐστίν — present indicative active, 3rd sg, from εἰμί (to be)
2. γεγράφθω — perfect imperative passive, 3rd sg, from γράφω (to draw/write)
3. ἐδείχθη — aorist indicative passive, 3rd sg, from δείκνυμι (to show)
4. δεῖξαι — aorist infinitive active, from δείκνυμι (to show)
5. γίνονται — present indicative middle, 3rd pl, from γίγνομαι (to become)
6. φαίνεται — present indicative middle, 3rd sg, from φαίνω (to appear/show)
7. ἐπεζεύχθω — perfect imperative passive, 3rd sg, from ἐπιζεύγνυμι (to join)
8. ἔστω — present imperative active, 3rd sg, from εἰμί (to be)
9. λέγω — present indicative active, 1st sg, from λέγω (to say)
10. ἐόντος — present participle, masculine/neuter genitive sg, from εἰμί (to be) — Ionic form of ὄντος

</details>

## Further Practice

With verbs and participles, you can now translate Euclid's propositions — not just definitions. The [Euclid exercises](exercises-euclid.md) include Propositions I.1, I.4, I.5, I.32, I.41, and the Pythagorean theorem (I.47). Start with I.1, which you have already read aloud and discussed; translating it fully is a different and deeper exercise.

The [philosophy and literature exercises](exercises-philosophy.md) are also open to you now. The shorter Heraclitus fragments (93, 119, 123) and the one-liners at the end of the file are good starting points — aphoristic, self-contained, and grammatically manageable. The longer fragments and the shorter Sappho poems follow naturally. Fragment 31, which you worked with above, has more to yield on a second pass.

## What Comes Next

You now have the grammatical framework to read Greek with reference support: cases and declensions for nouns, tenses and moods for verbs, the article as your decoder ring, and the participle as the construction that holds Greek prose together. In Chapter 6, you will put it all together with a capstone translation of a passage from Plato's *Meno* — the slave boy geometry scene — where Greek, geometry, and philosophy converge.
