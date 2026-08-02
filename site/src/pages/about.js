import '../styles/about.css';

export function renderAbout(container) {
  const root = document.createElement('article');
  root.className = 'about';

  root.innerHTML = `
    <h1 class="about__title">About</h1>

    <section class="about__section">
      <h2 class="about__heading">The idea</h2>
      <p>
        Enchiridion began as "the program I wished I had" when first starting
        computer programming. I came to it from the Great Books program at St.
        John's College, where mathematics and natural science are studied through
        the works in which they first took shape. Those books gave me Euclid,
        Ptolemy, Newton, and Maxwell. But it stopped short of information theory,
        computer science, and programming languages.
      </p>
      <p>
        Crossing that gap on one's own is difficult. Most paths
        into technical work outside of academia begin near the present:
        learn a language, pick a framework, internalize a useful collection of patterns.
        They can teach software engineering and practical skills for employment,
        but they rarely ask where the abstractions came from: what is a computer,
        and what sort of things do programming languages make possible? The
        first principles are treated as depth to be sought after learning to code
        rather than the ground coding stands on.
      </p>
      <p>
        The first purpose of Enchiridion is to trace a different path: to follow
        mathematics and science through their primary works until the history
        reaches the mechanisms, theories, and technical practices of the present.
        It is a research project, a reading program, and a proposal for what a modern
        education could become.
      </p>
    </section>

    <section class="about__section">
      <h2 class="about__heading">The program</h2>
      <p>
        The Grand Tour begins in Ancient Greece and proceeds roughly in the order
        the works were written. Mathematics, astronomy, physics, chemistry,
        biology, logic, and computation develop alongside philosophy, history,
        politics, and literature. While Enchiridion is STEM-focused, the humanities
        are not just added flavor to the technical curriculum. They belong to the same
        tradition, exist in dialogue with the sciences, and reveal to us a richer account
        of life.
      </p>
      <p>
        Later modules carry the historical sequence into practice: algebra and
        calculus, modern mathematics, computation from first principles,
        programming languages, data structures and algorithms, and formal methods.
        The aim is practical competence built on foundations. A reader who
        completes the program should be prepared to enter demanding technical
        study or work without having been trained only for the tools currently in
        use.
      </p>
      <p>
        Enchiridion is designed as roughly two years of sustained, self-directed
        work, though it imposes no formal calendar. Some books ask to be read slowly over
        months; some exercises take an afternoon; some readers will follow one
        thread and leave the rest. The sequence is a path, not a deadline. The program is yours.
      </p>
      <p>
        The intended result is not merely more knowledge, but a person. One who
        has reconstructed pivotal ideas across the centuries, worked through texts that
        advanced human understanding, and learned to wield technology thoughtfully.
        In an age of fluent, plausible machine output and pattern-matching, the ability
        to discern, to judge, and to ask a worthwhile question is a civilizational asset.
      </p>
    </section>

    <section class="about__section">
      <h2 class="about__heading">The method</h2>
      <p>
        Letting the books speak for themselves is at the center. Enchiridion favors
        primary texts over summaries and arranges them so that one can work through
        them without lecture. The program does not provide key takeaways or interpretation.
        Difficulty is an essential part of the encounter.
      </p>
      <p>
        Supplements enter where they can add another dimension to the reading or
        where a practical barrier would otherwise hinder it. A notation guide
        can make an unfamiliar page legible; a lab can put a proposition into the
        reader's hands; an exercise can supply the practice a text assumes.
        Their task is to make further work possible and then get out of the way.
      </p>
      <p>
        Enchiridion is for adult learners, college students, autodidacts,
        homeschoolers, and anyone else willing to spend time in the
        books. It is free to use, open source, and made in public so that its
        texts, sources, editorial decisions, and unfinished parts can be examined.
      </p>
    </section>

    <section class="about__section">
      <h2 class="about__heading">A work in progress</h2>
      <p>
        The program is being built era by era. Some texts have been processed
        into clean, rendered editions; others remain as source PDFs. Some
        supplements and modules are complete, while others reserve a place in the
        sequence for work still to be written. The library and syllabus remain
        under active construction and revision; books may be added or removed.
        What appears here is an honest snapshot of the project, not necessarily
        what will be there when it's fully built.
      </p>
      <p>
        The original source of a text remains available in the GitHub repository
        when a rendered edition has been made. An unwritten supplement is shown as
        a planning artifact &mdash; a place in the design, not a promise of what will
        inevitably be there.
      </p>
    </section>

    <section class="about__section">
      <h2 class="about__heading">Rights</h2>
      <p>
        Enchiridion includes some materials that may be under copyright,
        concentrated mostly in the modern era &mdash; certain screenplays,
        works like Hannah Arendt's <em>Eichmann in Jerusalem</em>, and a
        handful of translations. These were sourced from publicly accessible
        locations on the open internet (most often the Internet Archive and
        Project Gutenberg) and are included here under a good-faith claim of
        fair use, in service of a non-commercial educational project. If you
        hold rights to any work included here and would like it removed,
        please open an issue or contact us via the repository; we will take
        it down promptly.
      </p>
    </section>

    <section class="about__section">
      <h2 class="about__heading">Contributing</h2>
      <p>
        Enchiridion lives at
        <a href="https://github.com/hungryrobot1/Enchiridion" target="_blank" rel="noopener">github.com/hungryrobot1/Enchiridion</a>.
        The repository contains every text, supplement, and module, along with
        the processing tools and site source. Issues, pull requests, and
        discussions are welcome.
      </p>
      <p>
        Particular help is welcome on: cleanup of OCR'd texts, drafting of
        scaffolded-but-empty supplements, translation work
        (a few sources remain in French, Latin, and German), and curatorial
        feedback on sequencing within and between eras.
      </p>
      <p>
        The project is licensed permissively. See the
        <a href="https://github.com/hungryrobot1/Enchiridion/blob/main/LICENSE" target="_blank" rel="noopener">LICENSE</a>
        file for details.
      </p>
    </section>
  `;

  container.appendChild(root);
}
