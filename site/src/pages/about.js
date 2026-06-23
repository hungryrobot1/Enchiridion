import '../styles/about.css';

export function renderAbout(container) {
  const root = document.createElement('article');
  root.className = 'about';

  root.innerHTML = `
    <h1 class="about__title">About</h1>

    <section class="about__section">
      <h2 class="about__heading">Philosophy</h2>
      <p>
        Coming from a traditional Great Books program at St. John's College, I
        learned to appreciate the books and their greatness. Newton said, "If I
        have seen further it is only by standing on the shoulders of giants." The
        history of science was built that way &mdash; over generations, with
        fundamental insights at each step. As modern readers, the heights we
        reach from those same shoulders are loftier still.
      </p>
      <p>
        Where traditional Great Books programs tend to fall short is in bridging
        the gap with modern STEM education. After St. John's, I had to learn
        computer science and programming on my own. It was difficult and
        disorienting, and frankly I was rudderless and unproductive for the
        first several years. Modern advice tends to funnel people into
        pre-fabricated pipelines for learning popular tech stacks, without
        exposing the principles the technology is actually built on, or what's
        truly possible. People learn to build React web apps without
        understanding what a browser is or how the web works; they learn to
        deploy AI agents with only a vague sense that inference amounts to matrix
        multiplication; they learn to solve data structures and algorithms
        problems on LeetCode without grappling with the basic question of what a
        programming language really is.
      </p>
      <p>
        This could be called the "what I wish I had when starting out"
        curriculum. It pairs the interdisciplinary rigor of a Great Books
        program &mdash; breadth, history, philosophy &mdash; with the practical
        skills and knowledge needed to pursue employment or higher education. It
        is meant as a synthesis of the old and the new: a vision of what
        education could become, grounded in the traditions that brought us here
        while engaging directly with the present.
      </p>
      <p>
        Enchiridion is for anyone who desires knowledge &mdash; adult learners,
        college students, autodidacts, and homeschoolers alike. It is not a
        replacement for formal education, but in the right hands it can be a
        useful resource. All of it is offered free of charge and open-source,
        for use by anyone.
      </p>
    </section>

    <section class="about__section">
      <h2 class="about__heading">Disclaimer</h2>
      <p>
        Enchiridion is a work in progress. Many supplements are stubs, many
        scanned texts still need cleanup, and the syllabus itself is under
        active revision. What you see here is an honest snapshot of an
        ongoing project, not a finished product.
      </p>
      <p>
        Where a text exists in the in-house rendered form, the source PDF remains available
        as well. Where a supplement is unwritten, its place in the syllabus
        is reserved as a planning artifact &mdash; a slot, not a promise.
      </p>
      <p>
        Nothing here is intended as a substitute for formal study, expert
        instruction, or the slow patient work of reading hard books. It is
        a map and a scaffold, offered in the hope that it lowers the
        barriers to entry and then gets out of the way.
      </p>
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
        the site source. Issues, pull requests, and discussions are welcome.
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
