const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["assets/md-reader-C6phV3Oz.js","assets/md-reader-WbfJEqtj.css"])))=>i.map(i=>d[i]);
(function(){const a=document.createElement("link").relList;if(a&&a.supports&&a.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))c(o);new MutationObserver(o=>{for(const t of o)if(t.type==="childList")for(const p of t.addedNodes)p.tagName==="LINK"&&p.rel==="modulepreload"&&c(p)}).observe(document,{childList:!0,subtree:!0});function i(o){const t={};return o.integrity&&(t.integrity=o.integrity),o.referrerPolicy&&(t.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?t.credentials="include":o.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function c(o){if(o.ep)return;o.ep=!0;const t=i(o);fetch(o.href,t)}})();const A=[];let E=null;function x(e,a){A.push({pattern:e,handler:a})}function O(e){const a=e.replace(/^#\/?/,"/");for(const{pattern:i,handler:c}of A){const o=I(i,a);if(o!==null)return{handler:c,params:o}}return null}function I(e,a){const i=e.split("/").filter(Boolean),c=a.split("/").filter(Boolean);if(i.length!==c.length)return null;const o={};for(let t=0;t<i.length;t++)if(i[t].startsWith(":"))o[i[t].slice(1)]=decodeURIComponent(c[t]);else if(i[t]!==c[t])return null;return o}function B(e){async function a(){const i=window.location.hash||"#/",c=O(i);E&&(E(),E=null),c?(e.innerHTML="",E=await c.handler(e,c.params)||null):window.location.hash="#/",document.querySelectorAll(".site-header__link").forEach(o=>{const t=o.getAttribute("href");o.classList.toggle("site-header__link--active",t===i||i==="#/"&&t==="#/")})}window.addEventListener("hashchange",a),a()}function H(){const e=document.createElement("header");return e.className="site-header",e.innerHTML=`
    <div class="site-header__inner">
      <a href="#/" class="site-header__title">Enchiridion</a>
      <nav class="site-header__nav">
        <a href="#/" class="site-header__link">Home</a>
        <a href="#/syllabus" class="site-header__link">Syllabus</a>
        <a href="#/explore" class="site-header__link">Explore</a>
        <a href="#/supplements" class="site-header__link">Supplements</a>
      </nav>
    </div>
  `,e}let L=null;async function w(){return L||(L=await(await fetch("/Enchiridion/text-index.json")).json(),L)}async function U(e){const{texts:a,facets:i}=await w();e.innerHTML=`
    <div class="landing">
      <section class="landing__hero">
        <h1 class="landing__title">Enchiridion</h1>
        <p class="landing__subtitle">An Open Great Books Program for STEM Learning</p>
        <p class="landing__description">
          ${a.length} primary texts spanning 2,500 years of mathematical, scientific,
          and philosophical thought — free and open source.
        </p>
        <p class="landing__principle">
          <em>Let the books speak for themselves.</em>
        </p>
      </section>

      <section class="landing__stats">
        <div class="landing__stat">
          <span class="landing__stat-number">${a.length}</span>
          <span class="landing__stat-label">Texts</span>
        </div>
        <div class="landing__stat">
          <span class="landing__stat-number">${i.eras.length}</span>
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

      <section class="landing__eras">
        <h2>The Journey</h2>
        <div class="landing__era-list">
          ${i.eras.map(c=>`
            <div class="landing__era">
              <span class="landing__era-name">${c.display}</span>
              <span class="landing__era-count">${c.count} texts</span>
            </div>
          `).join("")}
        </div>
      </section>
    </div>
  `}async function M(e){const{texts:a,facets:i}=await w(),c={};for(const t of i.eras)c[t.id]={display:t.display,texts:a.filter(p=>p.era===t.id)};e.innerHTML=`
    <div class="page syllabus">
      <header class="syllabus__header">
        <h1>The Grand Tour</h1>
        <p>A chronological journey through ${a.length} texts spanning 2,500 years of STEM thought.</p>
        <p class="syllabus__approach">
          <strong>Recommended approach:</strong> proceed chronologically, taking a
          "some of all, all of some" approach — read broadly across subjects within
          each era, and dive deep into areas of particular interest.
        </p>
      </header>

      ${i.eras.map(t=>{const p=c[t.id].texts,d={};for(const f of p){const r=f.topics[0]||"other";d[r]||(d[r]=[]),d[r].push(f)}return`
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
  `,e.querySelectorAll(".syllabus__era-toggle").forEach(t=>{t.addEventListener("click",()=>{const p=t.dataset.era,f=document.getElementById(`era-${p}`).classList.toggle("syllabus__era-content--open");t.querySelector(".syllabus__era-chevron").textContent=f?"▴":"▾"})});const o=e.querySelector(".syllabus__era-content");o&&(o.classList.add("syllabus__era-content--open"),e.querySelector(".syllabus__era-chevron").textContent="▴")}function F(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const V="https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main";function S(e){const i=e.split("/").map(c=>encodeURIComponent(c)).join("/");return`${V}/${i}`}let m={query:"",era:"",topic:"",format:"",sort:"chronological"};async function G(e){const{texts:a,facets:i}=await w();e.innerHTML=`
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
            ${i.eras.map(r=>`
              <option value="${r.id}" ${m.era===r.id?"selected":""}>
                ${r.display}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="topic">
            <option value="">All Topics</option>
            ${i.topics.map(r=>`
              <option value="${r}" ${m.topic===r?"selected":""}>
                ${C(r)}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="format">
            <option value="">All Formats</option>
            ${i.formats.map(r=>`
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
  `;const c=e.querySelector(".explorer__search-input"),o=e.querySelector(".explorer__grid"),t=e.querySelector(".explorer__results-count"),p=e.querySelectorAll(".explorer__filter-select");function d(){let r=a;if(m.query){const s=m.query.toLowerCase();r=r.filter(l=>l.title.toLowerCase().includes(s)||l.author.toLowerCase().includes(s)||l.description.toLowerCase().includes(s)||l.topics.some(n=>n.toLowerCase().includes(s)))}switch(m.era&&(r=r.filter(s=>s.era===m.era)),m.topic&&(r=r.filter(s=>s.topics.includes(m.topic))),m.format&&(r=r.filter(s=>s.format===m.format)),r=[...r],m.sort){case"reverse-chrono":r.sort((s,l)=>l.year_sort-s.year_sort);break;case"title":r.sort((s,l)=>s.title.localeCompare(l.title));break;case"author":r.sort((s,l)=>s.author.localeCompare(l.author));break}if(t.textContent=`${r.length} of ${a.length} texts`,r.length===0){o.innerHTML='<div class="explorer__empty">No texts match your filters.</div>';return}o.innerHTML=r.map(s=>`
      <a href="#/read/${s.era_dir}/${s.id}" class="text-card" data-id="${s.id}">
        <div class="text-card__header">
          <span class="text-card__title">${s.title}</span>
          <span class="badge badge--${s.format}">${s.format}</span>
        </div>
        <div class="text-card__author">${s.author}</div>
        <div class="text-card__year">${s.year_written}${s.translator?` · trans. ${s.translator}`:""}</div>
        <div class="text-card__description">${s.description}</div>
        <div class="text-card__footer">
          ${s.topics.slice(0,3).map(l=>`<span class="topic-pill">${C(l)}</span>`).join("")}
          <button class="text-card__download" data-path="${s.path}" data-filename="${s.filename}" title="Download">
            &#8595; Download
          </button>
        </div>
      </a>
    `).join(""),o.querySelectorAll(".text-card__download").forEach(s=>{s.addEventListener("click",l=>{l.preventDefault(),l.stopPropagation();const n=S(s.dataset.path),u=document.createElement("a");u.href=n,u.download=s.dataset.filename,u.click()})})}let f;c.addEventListener("input",()=>{clearTimeout(f),f=setTimeout(()=>{m.query=c.value,d()},200)}),p.forEach(r=>{r.addEventListener("change",()=>{const s=r.dataset.filter;s==="sort"?m.sort=r.value:m[s]=r.value,d()})}),d(),c.focus()}function C(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const N="modulepreload",Y=function(e){return"/Enchiridion/"+e},j={},$=function(a,i,c){let o=Promise.resolve();if(i&&i.length>0){let p=function(r){return Promise.all(r.map(s=>Promise.resolve(s).then(l=>({status:"fulfilled",value:l}),l=>({status:"rejected",reason:l}))))};document.getElementsByTagName("link");const d=document.querySelector("meta[property=csp-nonce]"),f=(d==null?void 0:d.nonce)||(d==null?void 0:d.getAttribute("nonce"));o=p(i.map(r=>{if(r=Y(r),r in j)return;j[r]=!0;const s=r.endsWith(".css"),l=s?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${r}"]${l}`))return;const n=document.createElement("link");if(n.rel=s?"stylesheet":N,s||(n.as="script"),n.crossOrigin="",n.href=r,f&&n.setAttribute("nonce",f),document.head.appendChild(n),s)return new Promise((u,h)=>{n.addEventListener("load",u),n.addEventListener("error",()=>h(new Error(`Unable to preload CSS for ${r}`)))})}))}function t(p){const d=new Event("vite:preloadError",{cancelable:!0});if(d.payload=p,window.dispatchEvent(d),!d.defaultPrevented)throw p}return o.then(p=>{for(const d of p||[])d.status==="rejected"&&t(d.reason);return a().catch(t)})};let b=null;async function T(){if(b)return b;const a=await fetch("/Enchiridion/supplement-index.json");return a.ok?(b=await a.json(),b):(b={supplements:[],facets:{eras:[],types:[]}},b)}async function W(e,{era:a,id:i}){const[{texts:c},{supplements:o}]=await Promise.all([w(),T()]),t=c.find(l=>l.id===i);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Text not found: ${i}</p>
          <a href="#/explore" class="btn">Back to Explorer</a>
        </div>
      </div>
    `;return}const p=S(t.path);e.innerHTML=`
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
              ${t.topics.map(l=>`<span class="topic-pill">${Z(l)}</span>`).join("")}
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
              ${t.prerequisites.map(l=>{const n=c.find(u=>u.id===l);return n?`<a href="#/read/${n.era_dir}/${n.id}" class="reader__meta-prereq">${n.title}</a>`:`<span class="reader__meta-value">${l}</span>`}).join("")}
            </div>
          `:""}
          ${(()=>{const l=o.filter(n=>n.texts.includes(t.id));return l.length===0?"":`
              <div class="reader__meta-field">
                <span class="reader__meta-label">Supplements</span>
                ${l.map(n=>`<a href="#/supplement/${encodeURIComponent(n.era_dir)}/${n.id}" class="reader__meta-prereq">${n.title}</a>`).join("")}
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
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const l=document.createElement("a");l.href=p,l.download=t.filename,l.click()});const d=e.querySelector(".reader__sidebar"),f=e.querySelector(".reader__sidebar-toggle");d.classList.add("reader__sidebar--collapsed"),f.addEventListener("click",()=>{const l=d.classList.toggle("reader__sidebar--collapsed");f.textContent=l?"Show Details":"Hide Details"});const r=e.querySelector(".reader__viewport-inner");let s=null;try{s=await(await z(t.format)).render(r,p,e)}catch(l){console.error("Reader error:",l),r.innerHTML=`
      <div class="reader__error">
        <p>Failed to load text. The file may be temporarily unavailable.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${l.message}</p>
        <a href="${p}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{s&&s()}}async function z(e){switch(e){case"epub":return(await $(async()=>{const{default:a}=await import("./epub-reader-BsSYxZ9o.js");return{default:a}},[])).default;case"pdf":return(await $(async()=>{const{default:a}=await import("./pdf-reader-CrR_Zpek.js");return{default:a}},[])).default;case"html":return(await $(async()=>{const{default:a}=await import("./html-reader-BvnsfJ7c.js");return{default:a}},[])).default;case"txt":return(await $(async()=>{const{default:a}=await import("./txt-reader-DQg-AX_E.js");return{default:a}},[])).default;default:throw new Error(`Unsupported format: ${e}`)}}function Z(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const P={"exercise-set":"Exercise Sets","lab-manual":"Lab Manuals","notation-guide":"Notation Guides","convention-guide":"Convention Guides"},R=Object.keys(P);async function J(e){const{supplements:a,facets:i}=await T();if(a.length===0){e.innerHTML=`
      <div class="page supplements">
        <header class="supplements__header">
          <h1>Supplements</h1>
          <p>Supplementary materials are being developed. Check back soon for exercise sets,
          lab manuals, notation guides, and convention guides.</p>
        </header>
      </div>
    `;return}const c=a.filter(n=>n.type!=="reference"),o=a.filter(n=>n.type==="reference"),t={};for(const n of i.eras)t[n.id]={display:n.display,count:n.count,supplements:c.filter(u=>u.era===n.id)};const p={};for(const n of o){const u=n.topic||"other";p[u]||(p[u]=[]),p[u].push(n)}const d=i.topics||[],f=i.eras.length,r=o.length,s=c.length;e.innerHTML=`
    <div class="page supplements">
      <header class="supplements__header">
        <h1>Supplements</h1>
        <p>${s>0?`${s} supplementary material${s!==1?"s":""} across ${f} section${f!==1?"s":""}`:"Supplementary materials are being developed"}${r>0?`${s>0?", plus ":""}${r} reference${r!==1?"s":""}`:""}.</p>
      </header>

      ${i.eras.map(n=>{const u=t[n.id];if(!u||u.supplements.length===0)return"";const h={};for(const v of u.supplements){const g=v.type||"other";h[g]||(h[g]=[]),h[g].push(v)}const _=Object.entries(h).sort((v,g)=>{const y=R.indexOf(v[0]),q=R.indexOf(g[0]);return(y>=0?y:999)-(q>=0?q:999)});return`
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
                    ${g.map(y=>`
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

      ${o.length>0?`
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
                  ${u.map(h=>`
                    <li>
                      <a href="#/supplement/${encodeURIComponent(h.era_dir)}/${h.id}" class="supplements__link">
                        <span class="supplements__title">${h.title}</span>
                        ${h.description?`<span class="supplements__meta">${h.description}</span>`:""}
                      </a>
                    </li>
                  `).join("")}
                </ul>
              </div>
            </section>
          `}).join("")}
      `:""}
    </div>
  `,e.querySelectorAll(".supplements__era-toggle").forEach(n=>{n.addEventListener("click",()=>{const u=n.dataset.era,_=document.getElementById(`sup-era-${u}`).classList.toggle("supplements__era-content--open");n.querySelector(".supplements__era-chevron").textContent=_?"▴":"▾"})});const l=e.querySelector(".supplements__era-content");l&&(l.classList.add("supplements__era-content--open"),e.querySelector(".supplements__era-chevron").textContent="▴")}function K(e){return e.split("-").map(a=>a.charAt(0).toUpperCase()+a.slice(1)).join(" ")}const Q={"exercise-set":"Exercise Set","lab-manual":"Lab Manual","notation-guide":"Notation Guide","convention-guide":"Convention Guide",reference:"Reference"};async function X(e,{era:a,id:i}){const[{supplements:c},{texts:o}]=await Promise.all([T(),w()]),t=c.find(_=>_.id===i);if(!t){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Supplement not found: ${i}</p>
          <a href="#/supplements" class="btn">Back to Supplements</a>
        </div>
      </div>
    `;return}const p=S(t.path),d=t.format||"md",f=t.texts.map(_=>o.find(v=>v.id===_)).filter(Boolean),r=t.type==="reference"?"Topic":"Era",s=t.era_display;e.innerHTML=`
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
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const _=document.createElement("a");_.href=p,_.download=t.path.split("/").pop(),_.click()});const l=e.querySelector(".reader__sidebar"),n=e.querySelector(".reader__sidebar-toggle");l.classList.add("reader__sidebar--collapsed"),n.addEventListener("click",()=>{const _=l.classList.toggle("reader__sidebar--collapsed");n.textContent=_?"Show Details":"Hide Details"});const u=e.querySelector(".reader__viewport-inner");let h=null;try{h=await(await ee(d)).render(u,p,e)}catch(_){console.error("Supplement reader error:",_),u.innerHTML=`
      <div class="reader__error">
        <p>Failed to load ${t.type==="reference"?"reference":"supplement"}.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${_.message}</p>
        <a href="${p}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{h&&h()}}async function ee(e){switch(e){case"epub":return(await $(async()=>{const{default:a}=await import("./epub-reader-BsSYxZ9o.js");return{default:a}},[])).default;case"pdf":return(await $(async()=>{const{default:a}=await import("./pdf-reader-CrR_Zpek.js");return{default:a}},[])).default;case"html":return(await $(async()=>{const{default:a}=await import("./html-reader-BvnsfJ7c.js");return{default:a}},[])).default;case"txt":return(await $(async()=>{const{default:a}=await import("./txt-reader-DQg-AX_E.js");return{default:a}},[])).default;case"md":default:return(await $(async()=>{const{default:a}=await import("./md-reader-C6phV3Oz.js");return{default:a}},__vite__mapDeps([0,1]))).default}}const D=document.getElementById("app");D.appendChild(H());const k=document.createElement("main");k.id="content";D.appendChild(k);x("/",e=>U(e));x("/syllabus",e=>M(e));x("/explore",e=>G(e));x("/read/:era/:id",(e,a)=>W(e,a));x("/supplements",e=>J(e));x("/supplement/:era/:id",(e,a)=>X(e,a));B(k);"serviceWorker"in navigator&&window.addEventListener("load",()=>{navigator.serviceWorker.register("/Enchiridion/sw.js").catch(()=>{})});
