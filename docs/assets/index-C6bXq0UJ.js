const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["assets/md-reader-C6phV3Oz.js","assets/md-reader-WbfJEqtj.css"])))=>i.map(i=>d[i]);
(function(){const a=document.createElement("link").relList;if(a&&a.supports&&a.supports("modulepreload"))return;for(const i of document.querySelectorAll('link[rel="modulepreload"]'))c(i);new MutationObserver(i=>{for(const t of i)if(t.type==="childList")for(const p of t.addedNodes)p.tagName==="LINK"&&p.rel==="modulepreload"&&c(p)}).observe(document,{childList:!0,subtree:!0});function l(i){const t={};return i.integrity&&(t.integrity=i.integrity),i.referrerPolicy&&(t.referrerPolicy=i.referrerPolicy),i.crossOrigin==="use-credentials"?t.credentials="include":i.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function c(i){if(i.ep)return;i.ep=!0;const t=l(i);fetch(i.href,t)}})();const R=[];let E=null;function w(e,a){R.push({pattern:e,handler:a})}function I(e){const a=e.replace(/^#\/?/,"/");for(const{pattern:l,handler:c}of R){const i=O(l,a);if(i!==null)return{handler:c,params:i}}return null}function O(e,a){const l=e.split("/").filter(Boolean),c=a.split("/").filter(Boolean);if(l.length!==c.length)return null;const i={};for(let t=0;t<l.length;t++)if(l[t].startsWith(":"))i[l[t].slice(1)]=decodeURIComponent(c[t]);else if(l[t]!==c[t])return null;return i}function B(e){async function a(){const l=window.location.hash||"#/",c=I(l);E&&(E(),E=null),c?(e.innerHTML="",E=await c.handler(e,c.params)||null):window.location.hash="#/",document.querySelectorAll(".site-header__link").forEach(i=>{const t=i.getAttribute("href");i.classList.toggle("site-header__link--active",t===l||l==="#/"&&t==="#/")})}window.addEventListener("hashchange",a),a()}function H(){const e=document.createElement("header");return e.className="site-header",e.innerHTML=`
    <div class="site-header__inner">
      <a href="#/" class="site-header__title">Enchiridion</a>
      <nav class="site-header__nav">
        <a href="#/" class="site-header__link">Home</a>
        <a href="#/syllabus" class="site-header__link">Syllabus</a>
        <a href="#/explore" class="site-header__link">Explore</a>
        <a href="#/supplements" class="site-header__link">Supplements</a>
      </nav>
    </div>
  `,e}let T=null;async function x(){return T||(T=await(await fetch("/Enchiridion/text-index.json")).json(),T)}async function M(e){const{texts:a,facets:l}=await x();e.innerHTML=`
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
          ${l.eras.map(c=>`
            <div class="landing__era">
              <span class="landing__era-name">${c.display}</span>
              <span class="landing__era-count">${c.count} texts</span>
            </div>
          `).join("")}
        </div>
      </section>
    </div>
  `}async function U(e){const{texts:a,facets:l}=await x(),c={};for(const t of l.eras)c[t.id]={display:t.display,texts:a.filter(p=>p.era===t.id)};e.innerHTML=`
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

      ${l.eras.map(t=>{const p=c[t.id].texts,d={};for(const f of p){const r=f.topics[0]||"other";d[r]||(d[r]=[]),d[r].push(f)}return`
          <section class="syllabus__era">
            <button class="syllabus__era-toggle" data-era="${t.id}">
              <h2>${t.display}</h2>
              <span class="syllabus__era-count">${t.count} texts</span>
              <span class="syllabus__era-chevron">&#9662;</span>
            </button>
            <div class="syllabus__era-content" id="era-${t.id}">
              ${Object.entries(d).map(([f,r])=>`
                <div class="syllabus__topic-group">
                  <h3>${F(f)}</h3>
                  <ol class="syllabus__text-list">
                    ${r.map(s=>`
                      <li>
                        <a href="#/read/${s.era_dir}/${s.id}" class="syllabus__text-link">
                          <span class="syllabus__text-title">${s.title}</span>
                          <span class="syllabus__text-meta">
                            ${s.author}, ${s.year_written}
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
  `,e.querySelectorAll(".syllabus__era-toggle").forEach(t=>{t.addEventListener("click",()=>{const p=t.dataset.era,f=document.getElementById(`era-${p}`).classList.toggle("syllabus__era-content--open");t.querySelector(".syllabus__era-chevron").textContent=f?"▴":"▾"})});const i=e.querySelector(".syllabus__era-content");i&&(i.classList.add("syllabus__era-content--open"),e.querySelector(".syllabus__era-chevron").textContent="▴")}function F(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const G="https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main";function L(e){const l=e.split("/").map(c=>encodeURIComponent(c)).join("/");return`${G}/${l}`}let h={query:"",era:"",topic:"",format:"",sort:"chronological"};async function V(e){const{texts:a,facets:l}=await x();e.innerHTML=`
    <div class="page explorer">
      <div class="explorer__controls">
        <div class="explorer__search">
          <input
            type="text"
            class="explorer__search-input"
            placeholder="Search by title, author, or description..."
            value="${h.query}"
          >
        </div>
        <div class="explorer__filters">
          <select class="explorer__filter-select" data-filter="era">
            <option value="">All Eras</option>
            ${l.eras.map(r=>`
              <option value="${r.id}" ${h.era===r.id?"selected":""}>
                ${r.display}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="topic">
            <option value="">All Topics</option>
            ${l.topics.map(r=>`
              <option value="${r}" ${h.topic===r?"selected":""}>
                ${j(r)}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="format">
            <option value="">All Formats</option>
            ${l.formats.map(r=>`
              <option value="${r}" ${h.format===r?"selected":""}>
                ${r.toUpperCase()}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="sort">
            <option value="chronological" ${h.sort==="chronological"?"selected":""}>Chronological</option>
            <option value="reverse-chrono" ${h.sort==="reverse-chrono"?"selected":""}>Reverse Chronological</option>
            <option value="title" ${h.sort==="title"?"selected":""}>Title A-Z</option>
            <option value="author" ${h.sort==="author"?"selected":""}>Author A-Z</option>
          </select>
          <span class="explorer__results-count"></span>
        </div>
      </div>
      <div class="explorer__grid"></div>
    </div>
  `;const c=e.querySelector(".explorer__search-input"),i=e.querySelector(".explorer__grid"),t=e.querySelector(".explorer__results-count"),p=e.querySelectorAll(".explorer__filter-select");function d(){let r=a;if(h.query){const s=h.query.toLowerCase();r=r.filter(o=>o.title.toLowerCase().includes(s)||o.author.toLowerCase().includes(s)||o.description.toLowerCase().includes(s)||o.topics.some(n=>n.toLowerCase().includes(s)))}switch(h.era&&(r=r.filter(s=>s.era===h.era)),h.topic&&(r=r.filter(s=>s.topics.includes(h.topic))),h.format&&(r=r.filter(s=>s.format===h.format)),r=[...r],h.sort){case"reverse-chrono":r.sort((s,o)=>o.year_sort-s.year_sort);break;case"title":r.sort((s,o)=>s.title.localeCompare(o.title));break;case"author":r.sort((s,o)=>s.author.localeCompare(o.author));break}if(t.textContent=`${r.length} of ${a.length} texts`,r.length===0){i.innerHTML='<div class="explorer__empty">No texts match your filters.</div>';return}i.innerHTML=r.map(s=>`
      <a href="#/read/${s.era_dir}/${s.id}" class="text-card" data-id="${s.id}">
        <div class="text-card__header">
          <span class="text-card__title">${s.title}</span>
          <span class="badge badge--${s.format}">${s.format}</span>
        </div>
        <div class="text-card__author">${s.author}</div>
        <div class="text-card__year">${s.year_written}${s.translator?` · trans. ${s.translator}`:""}</div>
        <div class="text-card__description">${s.description}</div>
        <div class="text-card__footer">
          ${s.topics.slice(0,3).map(o=>`<span class="topic-pill">${j(o)}</span>`).join("")}
          <button class="text-card__download" data-path="${s.path}" data-filename="${s.filename}" title="Download">
            &#8595; Download
          </button>
        </div>
      </a>
    `).join(""),i.querySelectorAll(".text-card__download").forEach(s=>{s.addEventListener("click",o=>{o.preventDefault(),o.stopPropagation();const n=L(s.dataset.path),u=document.createElement("a");u.href=n,u.download=s.dataset.filename,u.click()})})}let f;c.addEventListener("input",()=>{clearTimeout(f),f=setTimeout(()=>{h.query=c.value,d()},200)}),p.forEach(r=>{r.addEventListener("change",()=>{const s=r.dataset.filter;s==="sort"?h.sort=r.value:h[s]=r.value,d()})}),d(),c.focus()}function j(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const W="modulepreload",N=function(e){return"/Enchiridion/"+e},C={},y=function(a,l,c){let i=Promise.resolve();if(l&&l.length>0){let p=function(r){return Promise.all(r.map(s=>Promise.resolve(s).then(o=>({status:"fulfilled",value:o}),o=>({status:"rejected",reason:o}))))};document.getElementsByTagName("link");const d=document.querySelector("meta[property=csp-nonce]"),f=(d==null?void 0:d.nonce)||(d==null?void 0:d.getAttribute("nonce"));i=p(l.map(r=>{if(r=N(r),r in C)return;C[r]=!0;const s=r.endsWith(".css"),o=s?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${r}"]${o}`))return;const n=document.createElement("link");if(n.rel=s?"stylesheet":W,s||(n.as="script"),n.crossOrigin="",n.href=r,f&&n.setAttribute("nonce",f),document.head.appendChild(n),s)return new Promise((u,m)=>{n.addEventListener("load",u),n.addEventListener("error",()=>m(new Error(`Unable to preload CSS for ${r}`)))})}))}function t(p){const d=new Event("vite:preloadError",{cancelable:!0});if(d.payload=p,window.dispatchEvent(d),!d.defaultPrevented)throw p}return i.then(p=>{for(const d of p||[])d.status==="rejected"&&t(d.reason);return a().catch(t)})};let $=null;async function S(){if($)return $;const a=await fetch("/Enchiridion/supplement-index.json");return a.ok?($=await a.json(),$):($={supplements:[],facets:{eras:[],types:[]}},$)}async function Y(e,{era:a,id:l}){const[{texts:c},{supplements:i}]=await Promise.all([x(),S()]),t=c.find(o=>o.id===l);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Text not found: ${l}</p>
          <a href="#/explore" class="btn">Back to Explorer</a>
        </div>
      </div>
    `;return}const p=L(t.path);e.innerHTML=`
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
              ${t.topics.map(o=>`<span class="topic-pill">${Z(o)}</span>`).join("")}
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
              ${t.prerequisites.map(o=>{const n=c.find(u=>u.id===o);return n?`<a href="#/read/${n.era_dir}/${n.id}" class="reader__meta-prereq">${n.title}</a>`:`<span class="reader__meta-value">${o}</span>`}).join("")}
            </div>
          `:""}
          ${(()=>{const o=i.filter(n=>n.texts.includes(t.id));return o.length===0?"":`
              <div class="reader__meta-field">
                <span class="reader__meta-label">Supplements</span>
                ${o.map(n=>`<a href="#/supplement/${encodeURIComponent(n.era_dir)}/${n.id}" class="reader__meta-prereq">${n.title}</a>`).join("")}
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
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const o=document.createElement("a");o.href=p,o.download=t.filename,o.click()});const d=e.querySelector(".reader__sidebar"),f=e.querySelector(".reader__sidebar-toggle");d.classList.add("reader__sidebar--collapsed"),f.addEventListener("click",()=>{const o=d.classList.toggle("reader__sidebar--collapsed");f.textContent=o?"Show Details":"Hide Details"});const r=e.querySelector(".reader__viewport-inner");let s=null;try{s=await(await z(t.format)).render(r,p,e)}catch(o){console.error("Reader error:",o),r.innerHTML=`
      <div class="reader__error">
        <p>Failed to load text. The file may be temporarily unavailable.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${o.message}</p>
        <a href="${p}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{s&&s()}}async function z(e){switch(e){case"epub":return(await y(async()=>{const{default:a}=await import("./epub-reader-i1hTWVgL.js");return{default:a}},[])).default;case"pdf":return(await y(async()=>{const{default:a}=await import("./pdf-reader-CrR_Zpek.js");return{default:a}},[])).default;case"html":return(await y(async()=>{const{default:a}=await import("./html-reader-BvnsfJ7c.js");return{default:a}},[])).default;case"txt":return(await y(async()=>{const{default:a}=await import("./txt-reader-DQg-AX_E.js");return{default:a}},[])).default;default:throw new Error(`Unsupported format: ${e}`)}}function Z(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const P={"exercise-set":"Exercise Sets","lab-manual":"Lab Manuals","notation-guide":"Notation Guides","convention-guide":"Convention Guides"},A=Object.keys(P);async function J(e){const{supplements:a,facets:l}=await S();if(a.length===0){e.innerHTML=`
      <div class="page supplements">
        <header class="supplements__header">
          <h1>Supplements</h1>
          <p>Supplementary materials are being developed. Check back soon for exercise sets,
          lab manuals, notation guides, and convention guides.</p>
        </header>
      </div>
    `;return}const c=a.filter(n=>n.type!=="reference"),i=a.filter(n=>n.type==="reference"),t={};for(const n of l.eras)t[n.id]={display:n.display,count:n.count,supplements:c.filter(u=>u.era===n.id)};const p={};for(const n of i){const u=n.topic||"other";p[u]||(p[u]=[]),p[u].push(n)}const d=l.topics||[],f=l.eras.length,r=i.length,s=c.length;e.innerHTML=`
    <div class="page supplements">
      <header class="supplements__header">
        <h1>Supplements</h1>
        <p>${s>0?`${s} supplementary material${s!==1?"s":""} across ${f} section${f!==1?"s":""}`:"Supplementary materials are being developed"}${r>0?`${s>0?", plus ":""}${r} reference${r!==1?"s":""}`:""}.</p>
      </header>

      ${l.eras.map(n=>{const u=t[n.id];if(!u||u.supplements.length===0)return"";const m={};for(const v of u.supplements){const g=v.type||"other";m[g]||(m[g]=[]),m[g].push(v)}const _=Object.entries(m).sort((v,g)=>{const b=A.indexOf(v[0]),q=A.indexOf(g[0]);return(b>=0?b:999)-(q>=0?q:999)});return`
          <section class="supplements__era">
            <button class="supplements__era-toggle" data-era="${n.id}">
              <h2>${n.display}</h2>
              <span class="supplements__era-count">${n.count} supplement${n.count!==1?"s":""}</span>
              <span class="supplements__era-chevron">&#9662;</span>
            </button>
            <div class="supplements__era-content" id="sup-era-${n.id}">
              ${_.map(([v,g])=>`
                <div class="supplements__type-group">
                  <h3>${P[v]||K(v)}</h3>
                  <ul class="supplements__list">
                    ${g.map(b=>`
                      <li>
                        <a href="#/supplement/${encodeURIComponent(b.era_dir)}/${b.id}" class="supplements__link">
                          <span class="supplements__title">${b.title}</span>
                          <span class="supplements__meta">
                            ${b.texts.length>0?b.texts.join(", "):""}
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

      ${i.length>0?`
        <div class="supplements__divider">
          <span>References</span>
        </div>

        ${d.map(n=>{const u=p[n.id]||[];return u.length===0?"":`
            <section class="supplements__era">
              <button class="supplements__era-toggle" data-era="ref-${n.id}">
                <h2>${n.display}</h2>
                <span class="supplements__era-count">${n.count} reference${n.count!==1?"s":""}</span>
                <span class="supplements__era-chevron">&#9662;</span>
              </button>
              <div class="supplements__era-content" id="sup-era-ref-${n.id}">
                <ul class="supplements__list">
                  ${u.map(m=>`
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
  `,e.querySelectorAll(".supplements__era-toggle").forEach(n=>{n.addEventListener("click",()=>{const u=n.dataset.era,_=document.getElementById(`sup-era-${u}`).classList.toggle("supplements__era-content--open");n.querySelector(".supplements__era-chevron").textContent=_?"▴":"▾"})});const o=e.querySelector(".supplements__era-content");o&&(o.classList.add("supplements__era-content--open"),e.querySelector(".supplements__era-chevron").textContent="▴")}function K(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const Q={"exercise-set":"Exercise Set","lab-manual":"Lab Manual","notation-guide":"Notation Guide","convention-guide":"Convention Guide",reference:"Reference"};async function X(e,{era:a,id:l}){const[{supplements:c},{texts:i}]=await Promise.all([S(),x()]),t=c.find(_=>_.id===l);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Supplement not found: ${l}</p>
          <a href="#/supplements" class="btn">Back to Supplements</a>
        </div>
      </div>
    `;return}const p=L(t.path),d=t.format||"md",f=t.texts.map(_=>i.find(v=>v.id===_)).filter(Boolean),r=t.type==="reference"?"Topic":"Era",s=t.era_display;e.innerHTML=`
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
            <span class="supplements__type-badge">${Q[t.type]||t.type}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">${r}</span>
            <span class="reader__meta-value">${s}</span>
          </div>
          ${d!=="md"?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Format</span>
              <span class="badge badge--${d}">${d}</span>
            </div>
          `:""}
          ${t.description?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${t.description}</span>
            </div>
          `:""}
          ${f.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Texts</span>
              ${f.map(_=>`<a href="#/read/${_.era_dir}/${_.id}" class="reader__meta-prereq">${_.title}</a>`).join("")}
            </div>
          `:""}
          ${t.prerequisites.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${t.prerequisites.map(_=>{const v=c.find(g=>g.id===_);return v?`<a href="#/supplement/${encodeURIComponent(v.era_dir)}/${v.id}" class="reader__meta-prereq">${v.title}</a>`:`<span class="reader__meta-value">${_}</span>`}).join("")}
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
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const _=document.createElement("a");_.href=p,_.download=t.path.split("/").pop(),_.click()});const o=e.querySelector(".reader__sidebar"),n=e.querySelector(".reader__sidebar-toggle");o.classList.add("reader__sidebar--collapsed"),n.addEventListener("click",()=>{const _=o.classList.toggle("reader__sidebar--collapsed");n.textContent=_?"Show Details":"Hide Details"});const u=e.querySelector(".reader__viewport-inner");let m=null;try{m=await(await ee(d)).render(u,p,e)}catch(_){console.error("Supplement reader error:",_),u.innerHTML=`
      <div class="reader__error">
        <p>Failed to load ${t.type==="reference"?"reference":"supplement"}.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${_.message}</p>
        <a href="${p}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{m&&m()}}async function ee(e){switch(e){case"epub":return(await y(async()=>{const{default:a}=await import("./epub-reader-i1hTWVgL.js");return{default:a}},[])).default;case"pdf":return(await y(async()=>{const{default:a}=await import("./pdf-reader-CrR_Zpek.js");return{default:a}},[])).default;case"html":return(await y(async()=>{const{default:a}=await import("./html-reader-BvnsfJ7c.js");return{default:a}},[])).default;case"txt":return(await y(async()=>{const{default:a}=await import("./txt-reader-DQg-AX_E.js");return{default:a}},[])).default;case"md":default:return(await y(async()=>{const{default:a}=await import("./md-reader-C6phV3Oz.js");return{default:a}},__vite__mapDeps([0,1]))).default}}const D=document.getElementById("app");D.appendChild(H());const k=document.createElement("main");k.id="content";D.appendChild(k);w("/",e=>M(e));w("/syllabus",e=>U(e));w("/explore",e=>V(e));w("/read/:era/:id",(e,a)=>Y(e,a));w("/supplements",e=>J(e));w("/supplement/:era/:id",(e,a)=>X(e,a));B(k);"serviceWorker"in navigator&&window.addEventListener("load",()=>{navigator.serviceWorker.register("/Enchiridion/sw.js").catch(()=>{})});
