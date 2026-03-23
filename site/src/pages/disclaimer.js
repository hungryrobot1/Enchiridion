import '../styles/disclaimer.css';

export function renderDisclaimer(container) {
  container.innerHTML = `
    <div class="page disclaimer">
      <header class="disclaimer__header">
        <h1>Fair Use & Copyright Notice</h1>
      </header>

      <div class="disclaimer__content">
        <p>Enchiridion is a nonprofit, open-source educational project. It is not monetized and will never be used for commercial purposes. All materials are provided free of charge for the purpose of self-directed learning and scholarly engagement.</p>

        <h2>Public Domain Texts</h2>
        <p>The majority of primary texts in this collection are in the public domain. These works and their translations were sourced from publicly available online repositories such as Project Gutenberg, the Internet Archive, and similar digital libraries.</p>

        <h2>Copyrighted Material</h2>
        <p>Some materials included in this collection remain under copyright. These include, but may not be limited to, certain screenplays, academic papers, and other works from the later sections of the program. Where such materials appear, their inclusion is intended solely for nonprofit educational and scholarly purposes, consistent with fair use under 17 U.S.C. &sect; 107.</p>
        <p>Factors supporting fair use in this context include:</p>
        <ul>
          <li>The purpose is exclusively educational and noncommercial.</li>
          <li>Materials are presented in the context of a structured curriculum for study and discussion.</li>
          <li>The project generates no revenue and is freely available to all.</li>
        </ul>

        <h2>Supplementary Materials</h2>
        <p>All supplementary resources — including lab manuals, handbooks, and exercise sets — are original works developed for this project and are released as open source.</p>

        <h2>Copyright Concerns</h2>
        <p>If you are a copyright holder and believe your work has been included in error, or if you would like to request removal or attribution, please contact the maintainer through the project's <a href="https://github.com/hungryrobot1/Enchiridion" target="_blank" rel="noopener">GitHub repository</a>. All reasonable requests will be honored promptly.</p>
      </div>
    </div>
  `;
}
