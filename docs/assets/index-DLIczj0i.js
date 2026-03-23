const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["assets/md-reader-C6phV3Oz.js","assets/md-reader-WbfJEqtj.css"])))=>i.map(i=>d[i]);
(function(){const a=document.createElement("link").relList;if(a&&a.supports&&a.supports("modulepreload"))return;for(const l of document.querySelectorAll('link[rel="modulepreload"]'))c(l);new MutationObserver(l=>{for(const t of l)if(t.type==="childList")for(const u of t.addedNodes)u.tagName==="LINK"&&u.rel==="modulepreload"&&c(u)}).observe(document,{childList:!0,subtree:!0});function o(l){const t={};return l.integrity&&(t.integrity=l.integrity),l.referrerPolicy&&(t.referrerPolicy=l.referrerPolicy),l.crossOrigin==="use-credentials"?t.credentials="include":l.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function c(l){if(l.ep)return;l.ep=!0;const t=o(l);fetch(l.href,t)}})();const D=[];let T=null;function E(e,a){D.push({pattern:e,handler:a})}function z(e){const a=e.replace(/^#\/?/,"/");for(const{pattern:o,handler:c}of D){const l=F(o,a);if(l!==null)return{handler:c,params:l}}return null}function F(e,a){const o=e.split("/").filter(Boolean),c=a.split("/").filter(Boolean);if(o.length!==c.length)return null;const l={};for(let t=0;t<o.length;t++)if(o[t].startsWith(":"))l[o[t].slice(1)]=decodeURIComponent(c[t]);else if(o[t]!==c[t])return null;return l}function G(e){async function a(){const o=window.location.hash||"#/",c=z(o);T&&(T(),T=null),c?(e.innerHTML="",T=await c.handler(e,c.params)||null):window.location.hash="#/",document.querySelectorAll(".site-header__link").forEach(l=>{const t=l.getAttribute("href");l.classList.toggle("site-header__link--active",t===o||o==="#/"&&t==="#/")})}window.addEventListener("hashchange",a),a()}function N(){const e=document.createElement("header");e.className="site-header",e.innerHTML=`
    <div class="site-header__inner">
      <a href="#/" class="site-header__title">Enchiridion</a>
      <button class="site-header__toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span class="site-header__toggle-bar"></span>
        <span class="site-header__toggle-bar"></span>
        <span class="site-header__toggle-bar"></span>
      </button>
      <nav class="site-header__nav">
        <a href="#/" class="site-header__link">Home</a>
        <a href="#/syllabus" class="site-header__link">Syllabus</a>
        <a href="#/explore" class="site-header__link">Explore</a>
        <a href="#/supplements" class="site-header__link">Supplements</a>
      </nav>
    </div>
  `;const a=e.querySelector(".site-header__toggle"),o=e.querySelector(".site-header__nav");return a.addEventListener("click",()=>{const c=o.classList.toggle("site-header__nav--open");a.classList.toggle("site-header__toggle--active",c),a.setAttribute("aria-expanded",c)}),o.querySelectorAll(".site-header__link").forEach(c=>{c.addEventListener("click",()=>{o.classList.remove("site-header__nav--open"),a.classList.remove("site-header__toggle--active"),a.setAttribute("aria-expanded","false")})}),e}let q=null;async function L(){return q||(q=await(await fetch("/Enchiridion/text-index.json")).json(),q)}async function V(e){const{texts:a,facets:o}=await L();e.innerHTML=`
    <div class="landing">
      <section class="landing__hero">
        <h1 class="landing__title">Enchiridion</h1>
        <p class="landing__subtitle">An Open Great Books Program for STEM Learning</p>
        <p class="landing__description">
          ${a.length} primary texts spanning 2,500 years of mathematical, scientific,
          and philosophical thought — free and open source.
        </p>
        <p class="landing__principle">
          <em>Timeless learning by letting the books speak for themselves.</em>
        </p>
      </section>

      <section class="landing__stats">
        <div class="landing__stat">
          <span class="landing__stat-number">${a.length}</span>
          <span class="landing__stat-label">Texts</span>
        </div>
        <div class="landing__stat">
          <span class="landing__stat-number">${o.eras.length}</span>
          <span class="landing__stat-label">Eras</span>
        </div>
        <div class="landing__stat">
          <span class="landing__stat-number">2,500</span>
          <span class="landing__stat-label">Years</span>
        </div>
      </section>

      <section class="landing__actions">
        <a href="#/syllabus" class="landing__card">
          <h3>Browse the Syllabus</h3>
          <p>Follow the complete chronological journey through all ${a.length} texts, from ancient Greece to the information age.</p>
        </a>
        <a href="#/explore" class="landing__card">
          <h3>Explore Texts</h3>
          <p>Search, sort, and filter the full library by era, subject, author, or format.</p>
        </a>
        <a href="#/read/${a[0].era_dir}/${a[0].id}" class="landing__card">
          <h3>Start Reading</h3>
          <p>Begin with ${a[0].title} by ${a[0].author} — the traditional starting point.</p>
        </a>
      </section>

      <section class="landing__about">
        <h2>About the Program</h2>
        <div class="landing__about-content">
          <p>Modern technology is advancing faster than our ability to understand it, and risks unleashing unprecedented disruption to our existing civilizational frameworks: economic structures, governmental institutions, the production and dissemination of new ideas, and even the very definition of what it means to be human. The development of artificial general intelligence in particular could become the most transformative event in the intellectual history of mankind since the advent of the written language. It is incumbent on humanity to respond to these mounting forces with reflection and choice before the window for a viable response is lost.</p>
          <p>The purpose of Enchiridion is to advocate for a future-proof model of education that keeps humanity's traditions at the center: one that is resistant to the disruption and the existential challenges raised by radical technological and political change. It strives for neutrality in its presentation of a breadth and juxtaposition of primary sources. It is a STEM-focused curriculum, organized in the format of a Great Books program.</p>
          <p>The Great Books program offers a canonical and historically-minded view of its texts, rooted in philosophy and critical thinking, while the STEM focus equips the reader with the relevant technical skills and knowledge for the modern day. While science, math, and computer science make up the majority of texts, there are also other topics including philosophy, literature, history, economics, psychology, and more.</p>
          <p>The intended audience of Enchiridion is anyone with a desire for knowledge. While not a replacement for formal education, it can supplement the studies of university students and homeschoolers, or provide general guidance for independent reading groups and adult learners.</p>
          <p>The program offers two kinds of materials: primary texts and supplementary resources. Primary texts are original writings from the western canon. Supplementary resources include lab manuals, enchiridia (handbooks), and additional exercises developed in-house to provide tools for engaging with the program more deeply.</p>
          <p>In a Great Books program, texts are meant to be read and rigorously discussed in chronological order. A syllabus called "The Grand Tour" is provided to give readers a general idea of the sequence to read the books in, but readers are also welcome to explore the different sections of the program at any point and choose the texts and topics that interest them most. Additionally, over time, shorter syllabi will be posted in order to provide a more focused examination of specific threads through history.</p>
          <p>All of this is offered free of charge and open-source, for use by anyone.</p>
        </div>
      </section>

      <section class="landing__eras">
        <h2>The Journey</h2>
        <div class="landing__era-list">
          ${o.eras.map(c=>`
            <div class="landing__era">
              <span class="landing__era-name">${c.display}</span>
              <span class="landing__era-count">${c.count} texts</span>
            </div>
          `).join("")}
        </div>
      </section>

      <footer class="landing__footer">
        <a href="#/disclaimer">Fair Use & Copyright</a>
        <span class="landing__footer-sep">&middot;</span>
        <a href="https://github.com/hungryrobot1/Enchiridion" target="_blank" rel="noopener">GitHub</a>
      </footer>
    </div>
  `}async function W(e){const{texts:a,facets:o}=await L(),c={};for(const t of o.eras)c[t.id]={display:t.display,texts:a.filter(u=>u.era===t.id)};e.innerHTML=`
    <div class="page syllabus">
      <header class="syllabus__header">
        <h1>The Grand Tour</h1>
        <p>A chronological journey through ${a.length} texts spanning 2,500 years of thought.</p>
        <p class="syllabus__approach">
          <strong>Recommended approach:</strong> proceed chronologically, taking a
          "some of all, all of some" approach — read broadly across subjects within
          each era, and dive deep into areas of particular interest.
        </p>
      </header>

      ${o.eras.map(t=>{const u=c[t.id].texts,p={};for(const h of u){const n=h.topics[0]||"other";p[n]||(p[n]=[]),p[n].push(h)}return`
          <section class="syllabus__era">
            <button class="syllabus__era-toggle" data-era="${t.id}">
              <h2>${t.display}</h2>
              <span class="syllabus__era-count">${t.count} texts</span>
              <span class="syllabus__era-chevron">&#9662;</span>
            </button>
            <div class="syllabus__era-content" id="era-${t.id}">
              ${Object.entries(p).map(([h,n])=>`
                <div class="syllabus__topic-group">
                  <h3>${Y(h)}</h3>
                  <ol class="syllabus__text-list">
                    ${n.map(r=>`
                      <li>
                        <a href="#/read/${r.era_dir}/${r.id}" class="syllabus__text-link">
                          <span class="syllabus__text-title">${r.title}</span>
                          <span class="syllabus__text-meta">
                            ${r.author}, ${r.year_written}
                          </span>
                        </a>
                      </li>
                    `).join("")}
                  </ol>
                </div>
              `).join("")}
            </div>
          </section>
        `}).join("")}
    </div>
  `,e.querySelectorAll(".syllabus__era-toggle").forEach(t=>{t.addEventListener("click",()=>{const u=t.dataset.era,h=document.getElementById(`era-${u}`).classList.toggle("syllabus__era-content--open");t.querySelector(".syllabus__era-chevron").textContent=h?"▴":"▾"})});const l=e.querySelector(".syllabus__era-content");l&&(l.classList.add("syllabus__era-content--open"),e.querySelector(".syllabus__era-chevron").textContent="▴")}function Y(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const Z="https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main";function j(e){const o=e.split("/").map(c=>encodeURIComponent(c)).join("/");return`${Z}/${o}`}let f={query:"",era:"",topic:"",format:"",sort:"chronological"};async function K(e){const{texts:a,facets:o}=await L();e.innerHTML=`
    <div class="page explorer">
      <div class="explorer__controls">
        <div class="explorer__search">
          <input
            type="text"
            class="explorer__search-input"
            placeholder="Search by title, author, or description..."
            value="${f.query}"
          >
        </div>
        <div class="explorer__filters">
          <select class="explorer__filter-select" data-filter="era">
            <option value="">All Eras</option>
            ${o.eras.map(n=>`
              <option value="${n.id}" ${f.era===n.id?"selected":""}>
                ${n.display}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="topic">
            <option value="">All Topics</option>
            ${o.topics.map(n=>`
              <option value="${n}" ${f.topic===n?"selected":""}>
                ${I(n)}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="format">
            <option value="">All Formats</option>
            ${o.formats.map(n=>`
              <option value="${n}" ${f.format===n?"selected":""}>
                ${n.toUpperCase()}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="sort">
            <option value="chronological" ${f.sort==="chronological"?"selected":""}>Chronological</option>
            <option value="reverse-chrono" ${f.sort==="reverse-chrono"?"selected":""}>Reverse Chronological</option>
            <option value="title" ${f.sort==="title"?"selected":""}>Title A-Z</option>
            <option value="author" ${f.sort==="author"?"selected":""}>Author A-Z</option>
          </select>
          <span class="explorer__results-count"></span>
        </div>
      </div>
      <div class="explorer__grid"></div>
    </div>
  `;const c=e.querySelector(".explorer__search-input"),l=e.querySelector(".explorer__grid"),t=e.querySelector(".explorer__results-count"),u=e.querySelectorAll(".explorer__filter-select");function p(){let n=a;if(f.query){const r=f.query.toLowerCase();n=n.filter(d=>d.title.toLowerCase().includes(r)||d.author.toLowerCase().includes(r)||d.description.toLowerCase().includes(r)||d.topics.some(s=>s.toLowerCase().includes(r)))}switch(f.era&&(n=n.filter(r=>r.era===f.era)),f.topic&&(n=n.filter(r=>r.topics.includes(f.topic))),f.format&&(n=n.filter(r=>r.format===f.format)),n=[...n],f.sort){case"reverse-chrono":n.sort((r,d)=>d.year_sort-r.year_sort);break;case"title":n.sort((r,d)=>r.title.localeCompare(d.title));break;case"author":n.sort((r,d)=>r.author.localeCompare(d.author));break}if(t.textContent=`${n.length} of ${a.length} texts`,n.length===0){l.innerHTML='<div class="explorer__empty">No texts match your filters.</div>';return}l.innerHTML=n.map(r=>`
      <a href="#/read/${r.era_dir}/${r.id}" class="text-card" data-id="${r.id}">
        <div class="text-card__header">
          <span class="text-card__title">${r.title}</span>
          <span class="badge badge--${r.format}">${r.format}</span>
        </div>
        <div class="text-card__author">${r.author}</div>
        <div class="text-card__year">${r.year_written}${r.translator?` · trans. ${r.translator}`:""}</div>
        <div class="text-card__description">${r.description}</div>
        <div class="text-card__footer">
          ${r.topics.slice(0,3).map(d=>`<span class="topic-pill">${I(d)}</span>`).join("")}
          <button class="text-card__download" data-path="${r.path}" data-filename="${r.filename}" title="Download">
            &#8595; Download
          </button>
        </div>
      </a>
    `).join(""),l.querySelectorAll(".text-card__download").forEach(r=>{r.addEventListener("click",d=>{d.preventDefault(),d.stopPropagation();const s=j(r.dataset.path),i=document.createElement("a");i.href=s,i.download=r.dataset.filename,i.click()})})}let h;c.addEventListener("input",()=>{clearTimeout(h),h=setTimeout(()=>{f.query=c.value,p()},200)}),u.forEach(n=>{n.addEventListener("change",()=>{const r=n.dataset.filter;r==="sort"?f.sort=n.value:f[r]=n.value,p()})}),p(),c.focus()}function I(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const J="modulepreload",Q=function(e){return"/Enchiridion/"+e},R={},w=function(a,o,c){let l=Promise.resolve();if(o&&o.length>0){let u=function(n){return Promise.all(n.map(r=>Promise.resolve(r).then(d=>({status:"fulfilled",value:d}),d=>({status:"rejected",reason:d}))))};document.getElementsByTagName("link");const p=document.querySelector("meta[property=csp-nonce]"),h=(p==null?void 0:p.nonce)||(p==null?void 0:p.getAttribute("nonce"));l=u(o.map(n=>{if(n=Q(n),n in R)return;R[n]=!0;const r=n.endsWith(".css"),d=r?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${n}"]${d}`))return;const s=document.createElement("link");if(s.rel=r?"stylesheet":J,r||(s.as="script"),s.crossOrigin="",s.href=n,h&&s.setAttribute("nonce",h),document.head.appendChild(s),r)return new Promise((i,m)=>{s.addEventListener("load",i),s.addEventListener("error",()=>m(new Error(`Unable to preload CSS for ${n}`)))})}))}function t(u){const p=new Event("vite:preloadError",{cancelable:!0});if(p.payload=u,window.dispatchEvent(p),!p.defaultPrevented)throw u}return l.then(u=>{for(const p of u||[])p.status==="rejected"&&t(p.reason);return a().catch(t)})};let k=null;async function A(){if(k)return k;const a=await fetch("/Enchiridion/supplement-index.json");return a.ok?(k=await a.json(),k):(k={supplements:[],facets:{eras:[],types:[]}},k)}const B="enchiridion-bookmarks";function M(){try{return JSON.parse(localStorage.getItem(B))||{}}catch{return{}}}function X(e,a){const o=M();o[e]=a,localStorage.setItem(B,JSON.stringify(o))}function ee(e){return M()[e]||null}async function te(e,{era:a,id:o}){const[{texts:c},{supplements:l}]=await Promise.all([L(),A()]),t=c.find(s=>s.id===o);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Text not found: ${o}</p>
          <a href="#/explore" class="btn">Back to Explorer</a>
        </div>
      </div>
    `;return}const u=j(t.path),p=t.format==="pdf";e.innerHTML=`
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${t.title}</span>
        <div class="reader__toolbar-controls">
          ${p?`
            <div class="reader__page-nav">
              <input type="text" class="reader__page-input" aria-label="Current page">
              <span class="reader__page-total"></span>
            </div>
            <div class="reader__zoom-controls">
              <button class="reader__tool-btn reader__zoom-out" title="Zoom out" aria-label="Zoom out">&minus;</button>
              <span class="reader__zoom-level"></span>
              <button class="reader__tool-btn reader__zoom-in" title="Zoom in" aria-label="Zoom in">+</button>
            </div>
          `:""}
          <button class="btn reader__download" title="Download">&#8595; Download</button>
        </div>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Author</span>
            <span class="reader__meta-value">${t.author}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Written</span>
            <span class="reader__meta-value">${t.year_written}</span>
          </div>
          ${t.translator?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Translator</span>
              <span class="reader__meta-value">${t.translator} (${t.year_translated})</span>
            </div>
          `:""}
          <div class="reader__meta-field">
            <span class="reader__meta-label">Era</span>
            <span class="reader__meta-value">${t.era_display}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Format</span>
            <span class="badge badge--${t.format}">${t.format}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Topics</span>
            <div class="reader__meta-topics">
              ${t.topics.map(s=>`<span class="topic-pill">${se(s)}</span>`).join("")}
            </div>
          </div>
          ${t.description?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${t.description}</span>
            </div>
          `:""}
          ${t.prerequisites.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${t.prerequisites.map(s=>{const i=c.find(m=>m.id===s);return i?`<a href="#/read/${i.era_dir}/${i.id}" class="reader__meta-prereq">${i.title}</a>`:`<span class="reader__meta-value">${s}</span>`}).join("")}
            </div>
          `:""}
          ${(()=>{const s=l.filter(i=>i.texts.includes(t.id));return s.length===0?"":`
              <div class="reader__meta-field">
                <span class="reader__meta-label">Supplements</span>
                ${s.map(i=>`<a href="#/supplement/${encodeURIComponent(i.era_dir)}/${i.id}" class="reader__meta-prereq">${i.title}</a>`).join("")}
              </div>
            `})()}
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading text...</div>
          </div>
        </div>
      </div>
    </div>
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const s=document.createElement("a");s.href=u,s.download=t.filename,s.click()});const h=e.querySelector(".reader__sidebar"),n=e.querySelector(".reader__sidebar-toggle");h.classList.add("reader__sidebar--collapsed"),n.addEventListener("click",()=>{const s=h.classList.toggle("reader__sidebar--collapsed");n.textContent=s?"Show Details":"Hide Details"});const r=e.querySelector(".reader__viewport-inner");let d=null;try{const s=await ae(t.format);if(p){const i=e.querySelector(".reader__page-input"),m=e.querySelector(".reader__page-total"),_=e.querySelector(".reader__zoom-in"),v=e.querySelector(".reader__zoom-out"),$=e.querySelector(".reader__zoom-level");let y=null;d=await s.render(r,u,e,{onReady:b=>{_.addEventListener("click",()=>b.zoomIn()),v.addEventListener("click",()=>b.zoomOut()),i.addEventListener("keydown",g=>{if(g.key==="Enter"){const C=parseInt(i.value,10);isNaN(C)||b.goToPage(C),i.blur()}}),i.addEventListener("blur",()=>{const g=parseInt(i.value,10);isNaN(g)||b.goToPage(g)}),i.addEventListener("focus",()=>i.select());const x=ee(o);if(x&&x>1){const g=document.createElement("div");g.className="reader__resume-banner",g.innerHTML=`
              <span>Continue from page ${x}?</span>
              <button class="reader__resume-btn" data-action="resume">Resume</button>
              <button class="reader__resume-btn reader__resume-btn--dismiss" data-action="dismiss">Start over</button>
            `,e.querySelector(".reader__toolbar").after(g),g.querySelector('[data-action="resume"]').addEventListener("click",()=>{b.goToPage(x),g.remove()}),g.querySelector('[data-action="dismiss"]').addEventListener("click",()=>{g.remove()})}y=setInterval(()=>{const g=b.getCurrentPage();g>1&&X(o,g)},5e3)},onPageChange:(b,x)=>{i.value=b,i.style.width=`${String(x).length+1}ch`,m.textContent=`of ${x}`},onScaleChange:b=>{$.textContent=`${Math.round(b*50)}%`,_.disabled=b>=4,v.disabled=b<=1}});const S=d;d=()=>{y&&clearInterval(y),S&&S()}}else d=await s.render(r,u,e)}catch(s){console.error("Reader error:",s),r.innerHTML=`
      <div class="reader__error">
        <p>Failed to load text. The file may be temporarily unavailable.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${s.message}</p>
        <a href="${u}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{d&&d()}}async function ae(e){switch(e){case"epub":return(await w(async()=>{const{default:a}=await import("./epub-reader-i1hTWVgL.js");return{default:a}},[])).default;case"pdf":return(await w(async()=>{const{default:a}=await import("./pdf-reader-f5QtpnoL.js");return{default:a}},[])).default;case"html":return(await w(async()=>{const{default:a}=await import("./html-reader-BvnsfJ7c.js");return{default:a}},[])).default;case"txt":return(await w(async()=>{const{default:a}=await import("./txt-reader-DQg-AX_E.js");return{default:a}},[])).default;default:throw new Error(`Unsupported format: ${e}`)}}function se(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const H={"exercise-set":"Exercise Sets","lab-manual":"Lab Manuals","notation-guide":"Notation Guides","convention-guide":"Convention Guides"},O=Object.keys(H);async function re(e){const{supplements:a,facets:o}=await A();if(a.length===0){e.innerHTML=`
      <div class="page supplements">
        <header class="supplements__header">
          <h1>Supplements</h1>
          <p>Supplementary materials are being developed. Check back soon for exercise sets,
          lab manuals, notation guides, and convention guides.</p>
        </header>
      </div>
    `;return}const c=a.filter(s=>s.type!=="reference"),l=a.filter(s=>s.type==="reference"),t={};for(const s of o.eras)t[s.id]={display:s.display,count:s.count,supplements:c.filter(i=>i.era===s.id)};const u={};for(const s of l){const i=s.topic||"other";u[i]||(u[i]=[]),u[i].push(s)}const p=o.topics||[],h=o.eras.length,n=l.length,r=c.length;e.innerHTML=`
    <div class="page supplements">
      <header class="supplements__header">
        <h1>Supplements</h1>
        <p>${r>0?`${r} supplementary material${r!==1?"s":""} across ${h} section${h!==1?"s":""}`:"Supplementary materials are being developed"}${n>0?`${r>0?", plus ":""}${n} reference${n!==1?"s":""}`:""}.</p>
      </header>

      ${o.eras.map(s=>{const i=t[s.id];if(!i||i.supplements.length===0)return"";const m={};for(const v of i.supplements){const $=v.type||"other";m[$]||(m[$]=[]),m[$].push(v)}const _=Object.entries(m).sort((v,$)=>{const y=O.indexOf(v[0]),S=O.indexOf($[0]);return(y>=0?y:999)-(S>=0?S:999)});return`
          <section class="supplements__era">
            <button class="supplements__era-toggle" data-era="${s.id}">
              <h2>${s.display}</h2>
              <span class="supplements__era-count">${s.count} supplement${s.count!==1?"s":""}</span>
              <span class="supplements__era-chevron">&#9662;</span>
            </button>
            <div class="supplements__era-content" id="sup-era-${s.id}">
              ${_.map(([v,$])=>`
                <div class="supplements__type-group">
                  <h3>${H[v]||ne(v)}</h3>
                  <ul class="supplements__list">
                    ${$.map(y=>`
                      <li>
                        <a href="#/supplement/${encodeURIComponent(y.era_dir)}/${y.id}" class="supplements__link">
                          <span class="supplements__title">${y.title}</span>
                          <span class="supplements__meta">
                            ${y.texts.length>0?y.texts.join(", "):""}
                          </span>
                        </a>
                      </li>
                    `).join("")}
                  </ul>
                </div>
              `).join("")}
            </div>
          </section>
        `}).join("")}

      ${l.length>0?`
        <div class="supplements__divider">
          <span>References</span>
        </div>

        ${p.map(s=>{const i=u[s.id]||[];return i.length===0?"":`
            <section class="supplements__era">
              <button class="supplements__era-toggle" data-era="ref-${s.id}">
                <h2>${s.display}</h2>
                <span class="supplements__era-count">${s.count} reference${s.count!==1?"s":""}</span>
                <span class="supplements__era-chevron">&#9662;</span>
              </button>
              <div class="supplements__era-content" id="sup-era-ref-${s.id}">
                <ul class="supplements__list">
                  ${i.map(m=>`
                    <li>
                      <a href="#/supplement/${encodeURIComponent(m.era_dir)}/${m.id}" class="supplements__link">
                        <span class="supplements__title">${m.title}</span>
                        ${m.description?`<span class="supplements__meta">${m.description}</span>`:""}
                      </a>
                    </li>
                  `).join("")}
                </ul>
              </div>
            </section>
          `}).join("")}
      `:""}
    </div>
  `,e.querySelectorAll(".supplements__era-toggle").forEach(s=>{s.addEventListener("click",()=>{const i=s.dataset.era,_=document.getElementById(`sup-era-${i}`).classList.toggle("supplements__era-content--open");s.querySelector(".supplements__era-chevron").textContent=_?"▴":"▾"})});const d=e.querySelector(".supplements__era-content");d&&(d.classList.add("supplements__era-content--open"),e.querySelector(".supplements__era-chevron").textContent="▴")}function ne(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const oe={"exercise-set":"Exercise Set","lab-manual":"Lab Manual","notation-guide":"Notation Guide","convention-guide":"Convention Guide",reference:"Reference"};async function ie(e,{era:a,id:o}){const[{supplements:c},{texts:l}]=await Promise.all([A(),L()]),t=c.find(_=>_.id===o);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Supplement not found: ${o}</p>
          <a href="#/supplements" class="btn">Back to Supplements</a>
        </div>
      </div>
    `;return}const u=j(t.path),p=t.format||"md",h=t.texts.map(_=>l.find(v=>v.id===_)).filter(Boolean),n=t.type==="reference"?"Topic":"Era",r=t.era_display;e.innerHTML=`
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${t.title}</span>
        <button class="btn reader__download" title="Download">&#8595; Download</button>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Type</span>
            <span class="supplements__type-badge">${oe[t.type]||t.type}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">${n}</span>
            <span class="reader__meta-value">${r}</span>
          </div>
          ${p!=="md"?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Format</span>
              <span class="badge badge--${p}">${p}</span>
            </div>
          `:""}
          ${t.description?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${t.description}</span>
            </div>
          `:""}
          ${h.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Texts</span>
              ${h.map(_=>`<a href="#/read/${_.era_dir}/${_.id}" class="reader__meta-prereq">${_.title}</a>`).join("")}
            </div>
          `:""}
          ${t.prerequisites.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${t.prerequisites.map(_=>{const v=c.find($=>$.id===_);return v?`<a href="#/supplement/${encodeURIComponent(v.era_dir)}/${v.id}" class="reader__meta-prereq">${v.title}</a>`:`<span class="reader__meta-value">${_}</span>`}).join("")}
            </div>
          `:""}
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading ${t.type==="reference"?"reference":"supplement"}...</div>
          </div>
        </div>
      </div>
    </div>
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const _=document.createElement("a");_.href=u,_.download=t.path.split("/").pop(),_.click()});const d=e.querySelector(".reader__sidebar"),s=e.querySelector(".reader__sidebar-toggle");d.classList.add("reader__sidebar--collapsed"),s.addEventListener("click",()=>{const _=d.classList.toggle("reader__sidebar--collapsed");s.textContent=_?"Show Details":"Hide Details"});const i=e.querySelector(".reader__viewport-inner");let m=null;try{m=await(await le(p)).render(i,u,e)}catch(_){console.error("Supplement reader error:",_),i.innerHTML=`
      <div class="reader__error">
        <p>Failed to load ${t.type==="reference"?"reference":"supplement"}.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${_.message}</p>
        <a href="${u}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{m&&m()}}async function le(e){switch(e){case"epub":return(await w(async()=>{const{default:a}=await import("./epub-reader-i1hTWVgL.js");return{default:a}},[])).default;case"pdf":return(await w(async()=>{const{default:a}=await import("./pdf-reader-f5QtpnoL.js");return{default:a}},[])).default;case"html":return(await w(async()=>{const{default:a}=await import("./html-reader-BvnsfJ7c.js");return{default:a}},[])).default;case"txt":return(await w(async()=>{const{default:a}=await import("./txt-reader-DQg-AX_E.js");return{default:a}},[])).default;case"md":default:return(await w(async()=>{const{default:a}=await import("./md-reader-C6phV3Oz.js");return{default:a}},__vite__mapDeps([0,1]))).default}}function ce(e){e.innerHTML=`
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
  `}const U=document.getElementById("app");U.appendChild(N());const P=document.createElement("main");P.id="content";U.appendChild(P);E("/",e=>V(e));E("/syllabus",e=>W(e));E("/explore",e=>K(e));E("/read/:era/:id",(e,a)=>te(e,a));E("/supplements",e=>re(e));E("/supplement/:era/:id",(e,a)=>ie(e,a));E("/disclaimer",e=>ce(e));G(P);"serviceWorker"in navigator&&window.addEventListener("load",()=>{navigator.serviceWorker.register("/Enchiridion/sw.js").catch(()=>{})});
