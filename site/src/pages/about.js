import '../styles/about.css';

export function renderAbout(container) {
  const root = document.createElement('article');
  root.className = 'about';

  root.innerHTML = `
    <h1 class="about__title">About</h1>

    <section class="about__section">
      <h2 class="about__heading">Philosophy</h2>
      <div class="about__placeholder">
        <!-- TODO: draft together. The Philosophy section is intentionally left
        for the next pass so we can iterate on it carefully. -->
        This section is being drafted. Check back soon.
      </div>
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
        Where a text exists in OCR'd form, the source PDF remains available
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
