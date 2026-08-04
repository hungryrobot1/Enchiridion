# Escalation — single-title documents still do not reach `h2`

The requested converter correction is applied: all 75 generated section
headings changed from `###` to `##`, while the single `#` title, poem text,
hardbreaks, ordering, and plain `XLVIX.` label are unchanged. The converter still
validates 75 numbered stanzas and all 76 retained source blocks.

The repository's current reader code does not appear to make those `h2`s into
sections. Executing `site/src/lib/section-tree.js::buildToc()` on the corrected
Markdown returns:

```text
title: RUBAIYAT OF OMAR KHAYYAM
toc sections: 0
level-1 sections: 0
direct level-2 sections: 75
```

The cause is visible in both consumers:

- `buildToc()` calls `splitMarkdownIntoSections(text, 1)` and recurses only
  through the sections that call returns.
- `md-reader.js` likewise calls `splitMarkdownIntoSections(text, 1)` and invokes
  `buildSection()` only for those returned sections.
- At level 1, `splitMarkdownIntoSections()` deliberately treats the first `h1`
  as the title and starts sections at the second `h1`. With only one `h1`, it
  returns no sections, so neither consumer reaches level 2.

A minimal positive control confirmed the behavior: `# T` followed by `## I`
produces zero TOC sections, while `# T`, `# BOOK`, `## I` produces one top-level
section with one child.

This conflicts with the premise that promoting the stanza headings to `##`
alone restores generated contents, `data-section` anchors, and `?s=` links. I
have not changed the requested single-`h1` structure, invented a second `h1`, or
modified the read-only site code.

Please clarify which additional change is intended: should this text gain a
second `h1` wrapper despite the instruction to keep a single `#` title, or is
the reader/build sectioning logic expected to change so a title-only `h1` can
recurse directly into `h2` sections?
