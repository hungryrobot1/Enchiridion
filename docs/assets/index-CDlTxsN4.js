const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["assets/md-reader-C6phV3Oz.js","assets/md-reader-WbfJEqtj.css"])))=>i.map(i=>d[i]);
(function(){const a=document.createElement("link").relList;if(a&&a.supports&&a.supports("modulepreload"))return;for(const s of document.querySelectorAll('link[rel="modulepreload"]'))n(s);new MutationObserver(s=>{for(const t of s)if(t.type==="childList")for(const u of t.addedNodes)u.tagName==="LINK"&&u.rel==="modulepreload"&&n(u)}).observe(document,{childList:!0,subtree:!0});function l(s){const t={};return s.integrity&&(t.integrity=s.integrity),s.referrerPolicy&&(t.referrerPolicy=s.referrerPolicy),s.crossOrigin==="use-credentials"?t.credentials="include":s.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function n(s){if(s.ep)return;s.ep=!0;const t=l(s);fetch(s.href,t)}})();const O=[];let T=null;function $(e,a){O.push({pattern:e,handler:a})}function N(e){const a=e.replace(/^#\/?/,"/");for(const{pattern:l,handler:n}of O){const s=W(l,a);if(s!==null)return{handler:n,params:s}}return null}function W(e,a){const l=e.split("/").filter(Boolean),n=a.split("/").filter(Boolean);if(l.length!==n.length)return null;const s={};for(let t=0;t<l.length;t++)if(l[t].startsWith(":"))s[l[t].slice(1)]=decodeURIComponent(n[t]);else if(l[t]!==n[t])return null;return s}function V(e){async function a(){const l=window.location.hash||"#/",n=N(l);T&&(T(),T=null),n?(e.innerHTML="",T=await n.handler(e,n.params)||null):window.location.hash="#/",document.querySelectorAll(".site-header__link").forEach(s=>{const t=s.getAttribute("href");s.classList.toggle("site-header__link--active",t===l||l==="#/"&&t==="#/")})}window.addEventListener("hashchange",a),a()}function Y(){const e=document.createElement("header");e.className="site-header",e.innerHTML=`
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
        <a href="#/modules" class="site-header__link">Modules</a>
      </nav>
    </div>
  `;const a=e.querySelector(".site-header__toggle"),l=e.querySelector(".site-header__nav");return a.addEventListener("click",()=>{const n=l.classList.toggle("site-header__nav--open");a.classList.toggle("site-header__toggle--active",n),a.setAttribute("aria-expanded",n)}),l.querySelectorAll(".site-header__link").forEach(n=>{n.addEventListener("click",()=>{l.classList.remove("site-header__nav--open"),a.classList.remove("site-header__toggle--active"),a.setAttribute("aria-expanded","false")})}),e}let q=null;async function k(){return q||(q=await(await fetch("/Enchiridion/text-index.json")).json(),q)}async function Z(e){const{texts:a,facets:l}=await k();e.innerHTML=`
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
          <span class="landing__stat-number">${l.eras.length}</span>
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
        <a href="#/modules" class="landing__card">
          <h3>Modules</h3>
          <p>Progressive skill-building sequences — from Ancient Greek to programming — that run alongside the primary texts.</p>
        </a>
        <a href="#/read/${a[0].era_dir}/${a[0].id}" class="landing__card">
          <h3>Start Reading</h3>
          <p>Begin with ${a[0].title} by ${a[0].author} — the traditional starting point.</p>
        </a>
      </section>

      <section class="landing__about">
        <h2>About the Program</h2>
        <div class="landing__about-content">
          <h3>What Is Enchiridion?</h3>
          <p>The purpose of Enchiridion is to advocate for a future-proof model of education that keeps humanity's traditions at the center: one that is resistant to the disruption and the existential challenges raised by radical technological and political change. It strives for neutrality in its presentation of a breadth and juxtaposition of primary sources. It is a STEM-focused curriculum, organized in the format of a Great Books program.</p>
          <p>The Great Books program offers a canonical and historically-minded view of its texts, rooted in philosophy and critical thinking, while the STEM focus equips the reader with the relevant technical skills and knowledge for the modern day. While science, math, and computer science make up the majority of texts, there are also other topics including philosophy, literature, history, economics, psychology, and more.</p>

          <h3>How It Works</h3>
          <p>The program offers two kinds of materials: primary texts and supplementary resources. Primary texts are original writings from the western canon. Supplementary resources include lab manuals, enchiridia (handbooks), and additional exercises developed in-house to provide tools for engaging with the program more deeply.</p>
          <p>In a Great Books program, texts are meant to be read and rigorously discussed in chronological order. A syllabus called "The Grand Tour" is provided to give readers a general idea of the sequence to read the books in, but readers are also welcome to explore the different sections of the program at any point and choose the texts and topics that interest them most. Additionally, over time, shorter syllabi will be posted in order to provide a more focused examination of specific threads through history.</p>

          <h3>Who It's For</h3>
          <p>The intended audience of Enchiridion is anyone with a desire for knowledge. While not a replacement for formal education, it can supplement the studies of university students and homeschoolers, or provide general guidance for independent reading groups and adult learners. All of this is offered free of charge and open-source, for use by anyone.</p>

          <h3>Why It Matters</h3>
          <p>Modern technology is advancing faster than our ability to understand it, and risks unleashing unprecedented disruption to our existing civilizational frameworks: economic structures, governmental institutions, the production and dissemination of new ideas, and even the very definition of what it means to be human. The development of artificial general intelligence in particular could become the most transformative event in the intellectual history of mankind since the advent of the written language. It is incumbent on humanity to respond to these mounting forces with reflection and choice before the window for a viable response is lost.</p>
        </div>
      </section>

      <section class="landing__eras">
        <h2>The Journey</h2>
        <div class="landing__era-list">
          ${l.eras.map(n=>`
            <div class="landing__era">
              <span class="landing__era-name">${n.display}</span>
              <span class="landing__era-count">${n.count} texts</span>
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
  `}async function K(e){const{texts:a,facets:l}=await k(),n={};for(const s of l.eras)n[s.id]={display:s.display,texts:a.filter(t=>t.era===s.id)};e.innerHTML=`
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

      ${l.eras.map(s=>{const t=n[s.id].texts,u={};for(const i of t){const d=i.topics[0]||"other";u[d]||(u[d]=[]),u[d].push(i)}return`
          <section class="syllabus__era">
            <button class="syllabus__era-toggle" data-era="${s.id}">
              <h2>${s.display}</h2>
              <span class="syllabus__era-count">${s.count} texts</span>
              <span class="syllabus__era-chevron">&#9662;</span>
            </button>
            <div class="syllabus__era-content" id="era-${s.id}">
              ${Object.entries(u).map(([i,d])=>`
                <div class="syllabus__topic-group">
                  <h3>${J(i)}</h3>
                  <ol class="syllabus__text-list">
                    ${d.map(r=>`
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
  `,e.querySelectorAll(".syllabus__era-toggle").forEach(s=>{s.addEventListener("click",()=>{const t=s.dataset.era,i=document.getElementById(`era-${t}`).classList.toggle("syllabus__era-content--open");s.querySelector(".syllabus__era-chevron").textContent=i?"▴":"▾"})})}function J(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const Q="https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main";function S(e){const l=e.split("/").map(n=>encodeURIComponent(n)).join("/");return`${Q}/${l}`}let m={query:"",era:"",topic:"",format:"",sort:"chronological"};async function X(e){const{texts:a,facets:l}=await k();e.innerHTML=`
    <div class="page explorer">
      <div class="explorer__controls">
        <div class="explorer__search">
          <input
            type="text"
            class="explorer__search-input"
            placeholder="Search by title, author, or description..."
            value="${m.query}"
          >
        </div>
        <div class="explorer__filters">
          <select class="explorer__filter-select" data-filter="era">
            <option value="">All Eras</option>
            ${l.eras.map(r=>`
              <option value="${r.id}" ${m.era===r.id?"selected":""}>
                ${r.display}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="topic">
            <option value="">All Topics</option>
            ${l.topics.map(r=>`
              <option value="${r}" ${m.topic===r?"selected":""}>
                ${I(r)}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="format">
            <option value="">All Formats</option>
            ${l.formats.map(r=>`
              <option value="${r}" ${m.format===r?"selected":""}>
                ${r.toUpperCase()}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="sort">
            <option value="chronological" ${m.sort==="chronological"?"selected":""}>Chronological</option>
            <option value="reverse-chrono" ${m.sort==="reverse-chrono"?"selected":""}>Reverse Chronological</option>
            <option value="title" ${m.sort==="title"?"selected":""}>Title A-Z</option>
            <option value="author" ${m.sort==="author"?"selected":""}>Author A-Z</option>
          </select>
          <span class="explorer__results-count"></span>
        </div>
      </div>
      <div class="explorer__grid"></div>
    </div>
  `;const n=e.querySelector(".explorer__search-input"),s=e.querySelector(".explorer__grid"),t=e.querySelector(".explorer__results-count"),u=e.querySelectorAll(".explorer__filter-select");function i(){let r=a;if(m.query){const o=m.query.toLowerCase();r=r.filter(c=>c.title.toLowerCase().includes(o)||c.author.toLowerCase().includes(o)||c.description.toLowerCase().includes(o)||c.topics.some(p=>p.toLowerCase().includes(o)))}switch(m.era&&(r=r.filter(o=>o.era===m.era)),m.topic&&(r=r.filter(o=>o.topics.includes(m.topic))),m.format&&(r=r.filter(o=>o.format===m.format)),r=[...r],m.sort){case"reverse-chrono":r.sort((o,c)=>c.year_sort-o.year_sort);break;case"title":r.sort((o,c)=>o.title.localeCompare(c.title));break;case"author":r.sort((o,c)=>o.author.localeCompare(c.author));break}if(t.textContent=`${r.length} of ${a.length} texts`,r.length===0){s.innerHTML='<div class="explorer__empty">No texts match your filters.</div>';return}s.innerHTML=r.map(o=>`
      <a href="#/read/${o.era_dir}/${o.id}" class="text-card" data-id="${o.id}">
        <div class="text-card__header">
          <span class="text-card__title">${o.title}</span>
          <span class="badge badge--${o.format}">${o.format}</span>
        </div>
        <div class="text-card__author">${o.author}</div>
        <div class="text-card__year">${o.year_written}${o.translator?` · trans. ${o.translator}`:""}</div>
        <div class="text-card__description">${o.description}</div>
        <div class="text-card__footer">
          ${o.topics.slice(0,3).map(c=>`<span class="topic-pill">${I(c)}</span>`).join("")}
          <button class="text-card__download" data-path="${o.path}" data-filename="${o.filename}" title="Download">
            &#8595; Download
          </button>
        </div>
      </a>
    `).join(""),s.querySelectorAll(".text-card__download").forEach(o=>{o.addEventListener("click",c=>{c.preventDefault(),c.stopPropagation();const p=S(o.dataset.path),_=document.createElement("a");_.href=p,_.download=o.dataset.filename,_.click()})})}let d;n.addEventListener("input",()=>{clearTimeout(d),d=setTimeout(()=>{m.query=n.value,i()},200)}),u.forEach(r=>{r.addEventListener("change",()=>{const o=r.dataset.filter;o==="sort"?m.sort=r.value:m[o]=r.value,i()})}),i(),n.focus()}function I(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const ee="modulepreload",ae=function(e){return"/Enchiridion/"+e},M={},y=function(a,l,n){let s=Promise.resolve();if(l&&l.length>0){let u=function(r){return Promise.all(r.map(o=>Promise.resolve(o).then(c=>({status:"fulfilled",value:c}),c=>({status:"rejected",reason:c}))))};document.getElementsByTagName("link");const i=document.querySelector("meta[property=csp-nonce]"),d=(i==null?void 0:i.nonce)||(i==null?void 0:i.getAttribute("nonce"));s=u(l.map(r=>{if(r=ae(r),r in M)return;M[r]=!0;const o=r.endsWith(".css"),c=o?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${r}"]${c}`))return;const p=document.createElement("link");if(p.rel=o?"stylesheet":ee,o||(p.as="script"),p.crossOrigin="",p.href=r,d&&p.setAttribute("nonce",d),document.head.appendChild(p),o)return new Promise((_,f)=>{p.addEventListener("load",_),p.addEventListener("error",()=>f(new Error(`Unable to preload CSS for ${r}`)))})}))}function t(u){const i=new Event("vite:preloadError",{cancelable:!0});if(i.payload=u,window.dispatchEvent(i),!i.defaultPrevented)throw u}return s.then(u=>{for(const i of u||[])i.status==="rejected"&&t(i.reason);return a().catch(t)})};let x=null;async function j(){if(x)return x;const a=await fetch("/Enchiridion/supplement-index.json");return a.ok?(x=await a.json(),x):(x={supplements:[],facets:{eras:[],types:[]}},x)}const B="enchiridion-bookmarks";function H(){try{return JSON.parse(localStorage.getItem(B))||{}}catch{return{}}}function te(e,a){const l=H();l[e]=a,localStorage.setItem(B,JSON.stringify(l))}function re(e){return H()[e]||null}async function se(e,{era:a,id:l}){const[{texts:n},{supplements:s}]=await Promise.all([k(),j()]),t=n.find(p=>p.id===l);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Text not found: ${l}</p>
          <a href="#/explore" class="btn">Back to Explorer</a>
        </div>
      </div>
    `;return}const u=S(t.path),i=t.format==="pdf";e.innerHTML=`
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${t.title}</span>
        ${i?`
          <div class="reader__page-nav">
            <input type="text" class="reader__page-input" aria-label="Current page">
            <span class="reader__page-total"></span>
          </div>
        `:""}
        <div class="reader__toolbar-controls">
          ${i?`
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
              ${t.topics.map(p=>`<span class="topic-pill">${oe(p)}</span>`).join("")}
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
              ${t.prerequisites.map(p=>{const _=n.find(f=>f.id===p);return _?`<a href="#/read/${_.era_dir}/${_.id}" class="reader__meta-prereq">${_.title}</a>`:`<span class="reader__meta-value">${p}</span>`}).join("")}
            </div>
          `:""}
          ${(()=>{const p=s.filter(_=>_.texts.includes(t.id));return p.length===0?"":`
              <div class="reader__meta-field">
                <span class="reader__meta-label">Supplements</span>
                ${p.map(_=>`<a href="#/supplement/${encodeURIComponent(_.era_dir)}/${_.id}" class="reader__meta-prereq">${_.title}</a>`).join("")}
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
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const p=document.createElement("a");p.href=u,p.download=t.filename,p.click()});const d=e.querySelector(".reader__sidebar"),r=e.querySelector(".reader__sidebar-toggle");d.classList.add("reader__sidebar--collapsed"),r.addEventListener("click",()=>{const p=d.classList.toggle("reader__sidebar--collapsed");r.textContent=p?"Show Details":"Hide Details"});const o=e.querySelector(".reader__viewport-inner");let c=null;try{const p=await ne(t.format);if(i){const _=e.querySelector(".reader__page-input"),f=e.querySelector(".reader__page-total"),h=e.querySelector(".reader__zoom-in"),v=e.querySelector(".reader__zoom-out"),L=e.querySelector(".reader__zoom-level");let C=null;c=await p.render(o,u,e,{onReady:b=>{h.addEventListener("click",()=>b.zoomIn()),v.addEventListener("click",()=>b.zoomOut()),_.addEventListener("keydown",g=>{if(g.key==="Enter"){const P=parseInt(_.value,10);isNaN(P)||b.goToPage(P),_.blur()}}),_.addEventListener("blur",()=>{const g=parseInt(_.value,10);isNaN(g)||b.goToPage(g)}),_.addEventListener("focus",()=>_.select());const w=re(l);if(w&&w>1){const g=document.createElement("div");g.className="reader__resume-banner",g.innerHTML=`
              <span>Continue from page ${w}?</span>
              <button class="reader__resume-btn" data-action="resume">Resume</button>
              <button class="reader__resume-btn reader__resume-btn--dismiss" data-action="dismiss">Start over</button>
            `,e.querySelector(".reader__toolbar").after(g),g.querySelector('[data-action="resume"]').addEventListener("click",()=>{b.goToPage(w),g.remove()}),g.querySelector('[data-action="dismiss"]').addEventListener("click",()=>{g.remove()})}C=setInterval(()=>{const g=b.getCurrentPage();g>1&&te(l,g)},5e3)},onPageChange:(b,w)=>{_.value=b,_.style.width=`${String(w).length+1}ch`,f.textContent=`of ${w}`},onScaleChange:b=>{L.textContent=`${Math.round(b*50)}%`,h.disabled=b>=4,v.disabled=b<=1}});const R=c;c=()=>{C&&clearInterval(C),R&&R()}}else c=await p.render(o,u,e)}catch(p){console.error("Reader error:",p),o.innerHTML=`
      <div class="reader__error">
        <p>Failed to load text. The file may be temporarily unavailable.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${p.message}</p>
        <a href="${u}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{c&&c()}}async function ne(e){switch(e){case"epub":return(await y(async()=>{const{default:a}=await import("./epub-reader-i1hTWVgL.js");return{default:a}},[])).default;case"pdf":return(await y(async()=>{const{default:a}=await import("./pdf-reader-DEUgGmV0.js");return{default:a}},[])).default;case"html":return(await y(async()=>{const{default:a}=await import("./html-reader-BvnsfJ7c.js");return{default:a}},[])).default;case"txt":return(await y(async()=>{const{default:a}=await import("./txt-reader-DQg-AX_E.js");return{default:a}},[])).default;default:throw new Error(`Unsupported format: ${e}`)}}function oe(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const U={"exercise-set":"Exercise Sets","lab-manual":"Lab Manuals","notation-guide":"Notation Guides","convention-guide":"Convention Guides","study-guide":"Study Guides"},D=Object.keys(U);async function le(e){const{supplements:a,facets:l}=await j();if(a.length===0){e.innerHTML=`
      <div class="page supplements">
        <header class="supplements__header">
          <h1>Supplements</h1>
          <p>Supplementary materials are being developed. Check back soon for exercise sets,
          lab manuals, notation guides, and convention guides.</p>
        </header>
      </div>
    `;return}const n=a.filter(i=>i.type!=="reference"),s={};for(const i of l.eras)s[i.id]={display:i.display,count:n.filter(d=>d.era===i.id).length,supplements:n.filter(d=>d.era===i.id)};const t=l.eras.filter(i=>n.some(d=>d.era===i.id)).length,u=n.length;e.innerHTML=`
    <div class="page supplements">
      <header class="supplements__header">
        <h1>Supplements</h1>
        <p>${u>0?`${u} supplementary material${u!==1?"s":""} across ${t} section${t!==1?"s":""}`:"Supplementary materials are being developed"}.</p>
      </header>

      ${l.eras.map(i=>{const d=s[i.id];if(!d||d.supplements.length===0)return"";const r={};for(const c of d.supplements){const p=c.type||"other";r[p]||(r[p]=[]),r[p].push(c)}const o=Object.entries(r).sort((c,p)=>{const _=D.indexOf(c[0]),f=D.indexOf(p[0]);return(_>=0?_:999)-(f>=0?f:999)});return`
          <section class="supplements__era">
            <button class="supplements__era-toggle" data-era="${i.id}">
              <h2>${i.display}</h2>
              <span class="supplements__era-count">${i.count} supplement${i.count!==1?"s":""}</span>
              <span class="supplements__era-chevron">&#9662;</span>
            </button>
            <div class="supplements__era-content" id="sup-era-${i.id}">
              ${o.map(([c,p])=>`
                <div class="supplements__type-group">
                  <h3>${U[c]||ie(c)}</h3>
                  <ul class="supplements__list">
                    ${p.map(_=>`
                      <li>
                        <a href="#/supplement/${encodeURIComponent(_.era_dir)}/${_.id}" class="supplements__link">
                          <span class="supplements__title">${_.title}</span>
                          <span class="supplements__meta">
                            ${_.texts.length>0?_.texts.join(", "):""}
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

    </div>
  `,e.querySelectorAll(".supplements__era-toggle").forEach(i=>{i.addEventListener("click",()=>{const d=i.dataset.era,o=document.getElementById(`sup-era-${d}`).classList.toggle("supplements__era-content--open");i.querySelector(".supplements__era-chevron").textContent=o?"▴":"▾"})})}function ie(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const de={"exercise-set":"Exercise Set","lab-manual":"Lab Manual","notation-guide":"Notation Guide","convention-guide":"Convention Guide",reference:"Reference"};async function ce(e,{era:a,id:l}){const[{supplements:n},{texts:s}]=await Promise.all([j(),k()]),t=n.find(h=>h.id===l);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Supplement not found: ${l}</p>
          <a href="#/supplements" class="btn">Back to Supplements</a>
        </div>
      </div>
    `;return}const u=S(t.path),i=t.format||"md",d=t.texts.map(h=>s.find(v=>v.id===h)).filter(Boolean),r=t.type==="reference"?"Topic":"Era",o=t.era_display;e.innerHTML=`
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
            <span class="supplements__type-badge">${de[t.type]||t.type}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">${r}</span>
            <span class="reader__meta-value">${o}</span>
          </div>
          ${i!=="md"?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Format</span>
              <span class="badge badge--${i}">${i}</span>
            </div>
          `:""}
          ${t.description?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${t.description}</span>
            </div>
          `:""}
          ${d.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Texts</span>
              ${d.map(h=>`<a href="#/read/${h.era_dir}/${h.id}" class="reader__meta-prereq">${h.title}</a>`).join("")}
            </div>
          `:""}
          ${t.prerequisites.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${t.prerequisites.map(h=>{const v=n.find(L=>L.id===h);return v?`<a href="#/supplement/${encodeURIComponent(v.era_dir)}/${v.id}" class="reader__meta-prereq">${v.title}</a>`:`<span class="reader__meta-value">${h}</span>`}).join("")}
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
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const h=document.createElement("a");h.href=u,h.download=t.path.split("/").pop(),h.click()});const c=e.querySelector(".reader__sidebar"),p=e.querySelector(".reader__sidebar-toggle");c.classList.add("reader__sidebar--collapsed"),p.addEventListener("click",()=>{const h=c.classList.toggle("reader__sidebar--collapsed");p.textContent=h?"Show Details":"Hide Details"});const _=e.querySelector(".reader__viewport-inner");let f=null;try{f=await(await pe(i)).render(_,u,e)}catch(h){console.error("Supplement reader error:",h),_.innerHTML=`
      <div class="reader__error">
        <p>Failed to load ${t.type==="reference"?"reference":"supplement"}.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${h.message}</p>
        <a href="${u}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{f&&f()}}async function pe(e){switch(e){case"epub":return(await y(async()=>{const{default:a}=await import("./epub-reader-i1hTWVgL.js");return{default:a}},[])).default;case"pdf":return(await y(async()=>{const{default:a}=await import("./pdf-reader-DEUgGmV0.js");return{default:a}},[])).default;case"html":return(await y(async()=>{const{default:a}=await import("./html-reader-BvnsfJ7c.js");return{default:a}},[])).default;case"txt":return(await y(async()=>{const{default:a}=await import("./txt-reader-DQg-AX_E.js");return{default:a}},[])).default;case"md":default:return(await y(async()=>{const{default:a}=await import("./md-reader-C6phV3Oz.js");return{default:a}},__vite__mapDeps([0,1]))).default}}let E=null;async function z(){if(E)return E;const a=await fetch("/Enchiridion/module-index.json");return a.ok?(E=await a.json(),E):(E={modules:[]},E)}function ue(e){return!e||e.length===0?"":e.map(a=>a.split("-").map(l=>l.charAt(0).toUpperCase()+l.slice(1)).join(" ")).join(", ")}async function _e(e){const{modules:a}=await z();if(a.length===0){e.innerHTML=`
      <div class="page modules">
        <header class="modules__header">
          <h1>Modules</h1>
          <p>Progressive learning modules are being developed. Check back soon.</p>
        </header>
      </div>
    `;return}const l=a.reduce((n,s)=>n+s.chapters.length,0);e.innerHTML=`
    <div class="page modules">
      <header class="modules__header">
        <h1>Modules</h1>
        <p>${a.length} progressive learning module${a.length!==1?"s":""}, ${l} chapters total. Skill-building sequences that run alongside the primary texts.</p>
      </header>

      ${a.map(n=>{const s=n.chapters.length,t=n.prerequisites.length>0,u=n.resources.length>0,i=n.references.length>0;return`
          <section class="modules__module">
            <button class="modules__toggle" data-module="${n.id}">
              <h2>${n.title}</h2>
              <span class="modules__count">${s} chapter${s!==1?"s":""}</span>
              <span class="modules__chevron">&#9662;</span>
            </button>
            <div class="modules__content" id="mod-${n.id}">
              <p class="modules__description">${n.description}</p>

              ${t?`
                <p class="modules__prerequisites">
                  Prerequisites: ${n.prerequisites.map(d=>{const r=a.find(o=>o.id===d);return r?`<a href="#/modules" data-prereq="${d}">${r.title}</a>`:d}).join(", ")}
                </p>
              `:""}

              <h3 class="modules__section-heading">Chapters</h3>
              <ul class="modules__chapters">
                ${n.chapters.map((d,r)=>{const o=ue(d.alongside);return`
                    <li>
                      <a href="#/module/${n.id}/${d.filename}" class="modules__chapter-link">
                        <span class="modules__chapter-title">${d.title}</span>
                        ${o?`<span class="modules__chapter-alongside">${o}</span>`:""}
                      </a>
                    </li>
                  `}).join("")}
              </ul>

              ${u?`
                <h3 class="modules__section-heading">Resources</h3>
                <ul class="modules__resources">
                  ${n.resources.map(d=>`
                    <li>
                      <a href="#/module/${n.id}/resource/${d.filename}" class="modules__resource-link">${d.title}</a>
                    </li>
                  `).join("")}
                </ul>
              `:""}

              ${i?`
                <h3 class="modules__section-heading">References</h3>
                <ul class="modules__references">
                  ${n.references.map(d=>{const r=d.url&&!d.path;return`
                      <li>
                        <a href="${r?d.url:d.path?`#/supplement/${encodeURIComponent(d.era_dir)}/${d.id}`:d.url||"#"}"${r?' target="_blank" rel="noopener noreferrer"':""} class="modules__ref-link">
                          <span class="modules__ref-title">${d.title}</span>
                          ${d.description?`<span class="modules__ref-description">${d.description}</span>`:""}
                        </a>
                      </li>
                    `}).join("")}
                </ul>
              `:""}
            </div>
          </section>
        `}).join("")}
    </div>
  `,e.querySelectorAll(".modules__toggle").forEach(n=>{n.addEventListener("click",()=>{const s=n.dataset.module,u=document.getElementById(`mod-${s}`).classList.toggle("modules__content--open");n.querySelector(".modules__chevron").textContent=u?"▴":"▾"})})}async function F(e,{id:a,chapter:l}){const[{modules:n},{texts:s}]=await Promise.all([z(),k()]),t=n.find(d=>d.id===a);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Module not found: ${a}</p>
          <a href="#/modules" class="btn">Back to Modules</a>
        </div>
      </div>
    `;return}const u=l.startsWith("resource/"),i=u?l.replace("resource/",""):l;return u?me(e,t,i):he(e,t,i,s)}async function he(e,a,l,n){const s=a.chapters.findIndex(h=>h.filename===l);if(s===-1){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Chapter not found: ${l}</p>
          <a href="#/modules" class="btn">Back to Modules</a>
        </div>
      </div>
    `;return}const t=a.chapters[s],u=`supplements/modules/${a.id}/${l}`,i=S(u),d=s>0?a.chapters[s-1]:null,r=s<a.chapters.length-1?a.chapters[s+1]:null,o=(t.alongside||[]).map(h=>n.find(v=>v.id===h)).filter(Boolean);e.innerHTML=`
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back">&larr; Back</button>
        <span class="reader__toolbar-title">${a.title}</span>
        <button class="btn reader__download" title="Download">&#8595; Download</button>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Module</span>
            <a href="#/modules" class="reader__meta-value" style="color: var(--color-accent)">${a.title}</a>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Chapter</span>
            <span class="reader__meta-value">${s} of ${a.chapters.length-1}</span>
          </div>
          ${o.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Alongside</span>
              ${o.map(h=>`<a href="#/read/${h.era_dir}/${h.id}" class="reader__meta-prereq">${h.title}</a>`).join("")}
            </div>
          `:""}
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading chapter...</div>
          </div>
        </div>
      </div>
    </div>
  `,e.querySelector(".reader__back").addEventListener("click",()=>history.back()),e.querySelector(".reader__download").addEventListener("click",()=>{const h=document.createElement("a");h.href=i,h.download=l,h.click()});const c=e.querySelector(".reader__sidebar"),p=e.querySelector(".reader__sidebar-toggle");c.classList.add("reader__sidebar--collapsed"),p.addEventListener("click",()=>{const h=c.classList.toggle("reader__sidebar--collapsed");p.textContent=h?"Show Details":"Hide Details"});const _=e.querySelector(".reader__viewport-inner");let f=null;try{f=await(await y(async()=>{const{default:L}=await import("./md-reader-C6phV3Oz.js");return{default:L}},__vite__mapDeps([0,1]))).default.render(_,i,e);const v=document.createElement("div");v.className="module-reader__nav",v.innerHTML=`
      <a href="${d?`#/module/${a.id}/${d.filename}`:"#"}"
         class="module-reader__nav-btn ${d?"":"module-reader__nav-btn--disabled"}">
        <span class="module-reader__nav-label">&larr; Previous</span>
        <span class="module-reader__nav-title">${d?d.title:""}</span>
      </a>
      <a href="${r?`#/module/${a.id}/${r.filename}`:"#"}"
         class="module-reader__nav-btn ${r?"":"module-reader__nav-btn--disabled"}"
         style="text-align: right">
        <span class="module-reader__nav-label">Next &rarr;</span>
        <span class="module-reader__nav-title">${r?r.title:""}</span>
      </a>
    `,_.appendChild(v)}catch(h){console.error("Module reader error:",h),_.innerHTML=`
      <div class="reader__error">
        <p>Failed to load chapter.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${h.message}</p>
        <a href="${i}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{f&&f()}}async function me(e,a,l){const n=a.resources.find(c=>c.filename===l),s=n?n.title:l,t=`supplements/modules/${a.id}/${l}`,u=S(t);e.innerHTML=`
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back">&larr; Back</button>
        <span class="reader__toolbar-title">${s}</span>
        <button class="btn reader__download" title="Download">&#8595; Download</button>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Module</span>
            <a href="#/modules" class="reader__meta-value" style="color: var(--color-accent)">${a.title}</a>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Type</span>
            <span class="supplements__type-badge">Resource</span>
          </div>
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading resource...</div>
          </div>
        </div>
      </div>
    </div>
  `,e.querySelector(".reader__back").addEventListener("click",()=>history.back()),e.querySelector(".reader__download").addEventListener("click",()=>{const c=document.createElement("a");c.href=u,c.download=l,c.click()});const i=e.querySelector(".reader__sidebar"),d=e.querySelector(".reader__sidebar-toggle");i.classList.add("reader__sidebar--collapsed"),d.addEventListener("click",()=>{const c=i.classList.toggle("reader__sidebar--collapsed");d.textContent=c?"Show Details":"Hide Details"});const r=e.querySelector(".reader__viewport-inner");let o=null;try{o=await(await y(async()=>{const{default:p}=await import("./md-reader-C6phV3Oz.js");return{default:p}},__vite__mapDeps([0,1]))).default.render(r,u,e)}catch(c){console.error("Resource reader error:",c),r.innerHTML=`
      <div class="reader__error">
        <p>Failed to load resource.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${c.message}</p>
        <a href="${u}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{o&&o()}}function fe(e){e.innerHTML=`
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
  `}const G=document.getElementById("app");G.appendChild(Y());const A=document.createElement("main");A.id="content";G.appendChild(A);$("/",e=>Z(e));$("/syllabus",e=>K(e));$("/explore",e=>X(e));$("/read/:era/:id",(e,a)=>se(e,a));$("/supplements",e=>le(e));$("/supplement/:era/:id",(e,a)=>ce(e,a));$("/modules",e=>_e(e));$("/module/:id/:chapter",(e,a)=>F(e,a));$("/module/:id/resource/:filename",(e,a)=>F(e,{id:a.id,chapter:`resource/${a.filename}`}));$("/disclaimer",e=>fe(e));V(A);"serviceWorker"in navigator&&window.addEventListener("load",()=>{navigator.serviceWorker.register("/Enchiridion/sw.js").catch(()=>{})});
