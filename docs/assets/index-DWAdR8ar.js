(function(){const s=document.createElement("link").relList;if(s&&s.supports&&s.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))o(r);new MutationObserver(r=>{for(const n of r)if(n.type==="childList")for(const d of n.addedNodes)d.tagName==="LINK"&&d.rel==="modulepreload"&&o(d)}).observe(document,{childList:!0,subtree:!0});function l(r){const n={};return r.integrity&&(n.integrity=r.integrity),r.referrerPolicy&&(n.referrerPolicy=r.referrerPolicy),r.crossOrigin==="use-credentials"?n.credentials="include":r.crossOrigin==="anonymous"?n.credentials="omit":n.credentials="same-origin",n}function o(r){if(r.ep)return;r.ep=!0;const n=l(r);fetch(r.href,n)}})();const w=[];let h=null;function g(t,s){w.push({pattern:t,handler:s})}function S(t){const s=t.replace(/^#\/?/,"/");for(const{pattern:l,handler:o}of w){const r=q(l,s);if(r!==null)return{handler:o,params:r}}return null}function q(t,s){const l=t.split("/").filter(Boolean),o=s.split("/").filter(Boolean);if(l.length!==o.length)return null;const r={};for(let n=0;n<l.length;n++)if(l[n].startsWith(":"))r[l[n].slice(1)]=decodeURIComponent(o[n]);else if(l[n]!==o[n])return null;return r}function A(t){async function s(){const l=window.location.hash||"#/",o=S(l);h&&(h(),h=null),o?(t.innerHTML="",h=await o.handler(t,o.params)||null):window.location.hash="#/",document.querySelectorAll(".site-header__link").forEach(r=>{const n=r.getAttribute("href");r.classList.toggle("site-header__link--active",n===l||l==="#/"&&n==="#/")})}window.addEventListener("hashchange",s),s()}function C(){const t=document.createElement("header");return t.className="site-header",t.innerHTML=`
    <div class="site-header__inner">
      <a href="#/" class="site-header__title">Enchiridion</a>
      <nav class="site-header__nav">
        <a href="#/" class="site-header__link">Home</a>
        <a href="#/syllabus" class="site-header__link">Syllabus</a>
        <a href="#/explore" class="site-header__link">Explore</a>
      </nav>
    </div>
  `,t}let m=null;async function y(){return m||(m=await(await fetch("/Enchiridion/text-index.json")).json(),m)}async function j(t){const{texts:s,facets:l}=await y();t.innerHTML=`
    <div class="landing">
      <section class="landing__hero">
        <h1 class="landing__title">Enchiridion</h1>
        <p class="landing__subtitle">An Open Great Books Program for STEM Learning</p>
        <p class="landing__description">
          ${s.length} primary texts spanning 2,500 years of mathematical, scientific,
          and philosophical thought — free and open source.
        </p>
        <p class="landing__principle">
          <em>Let the books speak for themselves.</em>
        </p>
      </section>

      <section class="landing__stats">
        <div class="landing__stat">
          <span class="landing__stat-number">${s.length}</span>
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
          <p>Follow the complete chronological journey through all ${s.length} texts, from ancient Greece to the information age.</p>
        </a>
        <a href="#/explore" class="landing__card">
          <h3>Explore Texts</h3>
          <p>Search, sort, and filter the full library by era, subject, author, or format.</p>
        </a>
        <a href="#/read/${s[0].era_dir}/${s[0].id}" class="landing__card">
          <h3>Start Reading</h3>
          <p>Begin with ${s[0].title} by ${s[0].author} — the traditional starting point.</p>
        </a>
      </section>

      <section class="landing__eras">
        <h2>The Journey</h2>
        <div class="landing__era-list">
          ${l.eras.map(o=>`
            <div class="landing__era">
              <span class="landing__era-name">${o.display}</span>
              <span class="landing__era-count">${o.count} texts</span>
            </div>
          `).join("")}
        </div>
      </section>
    </div>
  `}async function k(t){const{texts:s,facets:l}=await y(),o={};for(const n of l.eras)o[n.id]={display:n.display,texts:s.filter(d=>d.era===n.id)};t.innerHTML=`
    <div class="page syllabus">
      <header class="syllabus__header">
        <h1>The Grand Tour</h1>
        <p>A chronological journey through ${s.length} texts spanning 2,500 years of STEM thought.</p>
        <p class="syllabus__approach">
          <strong>Recommended approach:</strong> proceed chronologically, taking a
          "some of all, all of some" approach — read broadly across subjects within
          each era, and dive deep into areas of particular interest.
        </p>
      </header>

      ${l.eras.map(n=>{const d=o[n.id].texts,i={};for(const u of d){const a=u.topics[0]||"other";i[a]||(i[a]=[]),i[a].push(u)}return`
          <section class="syllabus__era">
            <button class="syllabus__era-toggle" data-era="${n.id}">
              <h2>${n.display}</h2>
              <span class="syllabus__era-count">${n.count} texts</span>
              <span class="syllabus__era-chevron">&#9662;</span>
            </button>
            <div class="syllabus__era-content" id="era-${n.id}">
              ${Object.entries(i).map(([u,a])=>`
                <div class="syllabus__topic-group">
                  <h3>${P(u)}</h3>
                  <ol class="syllabus__text-list">
                    ${a.map(e=>`
                      <li>
                        <a href="#/read/${e.era_dir}/${e.id}" class="syllabus__text-link">
                          <span class="syllabus__text-title">${e.title}</span>
                          <span class="syllabus__text-meta">
                            ${e.author}, ${e.year_written}
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
  `,t.querySelectorAll(".syllabus__era-toggle").forEach(n=>{n.addEventListener("click",()=>{const d=n.dataset.era,u=document.getElementById(`era-${d}`).classList.toggle("syllabus__era-content--open");n.querySelector(".syllabus__era-chevron").textContent=u?"▴":"▾"})});const r=t.querySelector(".syllabus__era-content");r&&(r.classList.add("syllabus__era-content--open"),t.querySelector(".syllabus__era-chevron").textContent="▴")}function P(t){return t.split("-").map(s=>s.charAt(0).toUpperCase()+s.slice(1)).join(" ")}const R="https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main";function E(t){const l=t.split("/").map(o=>encodeURIComponent(o)).join("/");return`${R}/${l}`}let p={query:"",era:"",topic:"",format:"",sort:"chronological"};async function O(t){const{texts:s,facets:l}=await y();t.innerHTML=`
    <div class="page explorer">
      <div class="explorer__controls">
        <div class="explorer__search">
          <input
            type="text"
            class="explorer__search-input"
            placeholder="Search by title, author, or description..."
            value="${p.query}"
          >
        </div>
        <div class="explorer__filters">
          <select class="explorer__filter-select" data-filter="era">
            <option value="">All Eras</option>
            ${l.eras.map(a=>`
              <option value="${a.id}" ${p.era===a.id?"selected":""}>
                ${a.display}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="topic">
            <option value="">All Topics</option>
            ${l.topics.map(a=>`
              <option value="${a}" ${p.topic===a?"selected":""}>
                ${$(a)}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="format">
            <option value="">All Formats</option>
            ${l.formats.map(a=>`
              <option value="${a}" ${p.format===a?"selected":""}>
                ${a.toUpperCase()}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="sort">
            <option value="chronological" ${p.sort==="chronological"?"selected":""}>Chronological</option>
            <option value="reverse-chrono" ${p.sort==="reverse-chrono"?"selected":""}>Reverse Chronological</option>
            <option value="title" ${p.sort==="title"?"selected":""}>Title A-Z</option>
            <option value="author" ${p.sort==="author"?"selected":""}>Author A-Z</option>
          </select>
          <span class="explorer__results-count"></span>
        </div>
      </div>
      <div class="explorer__grid"></div>
    </div>
  `;const o=t.querySelector(".explorer__search-input"),r=t.querySelector(".explorer__grid"),n=t.querySelector(".explorer__results-count"),d=t.querySelectorAll(".explorer__filter-select");function i(){let a=s;if(p.query){const e=p.query.toLowerCase();a=a.filter(c=>c.title.toLowerCase().includes(e)||c.author.toLowerCase().includes(e)||c.description.toLowerCase().includes(e)||c.topics.some(_=>_.toLowerCase().includes(e)))}switch(p.era&&(a=a.filter(e=>e.era===p.era)),p.topic&&(a=a.filter(e=>e.topics.includes(p.topic))),p.format&&(a=a.filter(e=>e.format===p.format)),a=[...a],p.sort){case"reverse-chrono":a.sort((e,c)=>c.year_sort-e.year_sort);break;case"title":a.sort((e,c)=>e.title.localeCompare(c.title));break;case"author":a.sort((e,c)=>e.author.localeCompare(c.author));break}if(n.textContent=`${a.length} of ${s.length} texts`,a.length===0){r.innerHTML='<div class="explorer__empty">No texts match your filters.</div>';return}r.innerHTML=a.map(e=>`
      <a href="#/read/${e.era_dir}/${e.id}" class="text-card" data-id="${e.id}">
        <div class="text-card__header">
          <span class="text-card__title">${e.title}</span>
          <span class="badge badge--${e.format}">${e.format}</span>
        </div>
        <div class="text-card__author">${e.author}</div>
        <div class="text-card__year">${e.year_written}${e.translator?` · trans. ${e.translator}`:""}</div>
        <div class="text-card__description">${e.description}</div>
        <div class="text-card__footer">
          ${e.topics.slice(0,3).map(c=>`<span class="topic-pill">${$(c)}</span>`).join("")}
          <button class="text-card__download" data-path="${e.path}" data-filename="${e.filename}" title="Download">
            &#8595; Download
          </button>
        </div>
      </a>
    `).join(""),r.querySelectorAll(".text-card__download").forEach(e=>{e.addEventListener("click",c=>{c.preventDefault(),c.stopPropagation();const _=E(e.dataset.path),f=document.createElement("a");f.href=_,f.download=e.dataset.filename,f.click()})})}let u;o.addEventListener("input",()=>{clearTimeout(u),u=setTimeout(()=>{p.query=o.value,i()},200)}),d.forEach(a=>{a.addEventListener("change",()=>{const e=a.dataset.filter;e==="sort"?p.sort=a.value:p[e]=a.value,i()})}),i(),o.focus()}function $(t){return t.split("-").map(s=>s.charAt(0).toUpperCase()+s.slice(1)).join(" ")}const B="modulepreload",D=function(t){return"/Enchiridion/"+t},x={},v=function(s,l,o){let r=Promise.resolve();if(l&&l.length>0){let d=function(a){return Promise.all(a.map(e=>Promise.resolve(e).then(c=>({status:"fulfilled",value:c}),c=>({status:"rejected",reason:c}))))};document.getElementsByTagName("link");const i=document.querySelector("meta[property=csp-nonce]"),u=(i==null?void 0:i.nonce)||(i==null?void 0:i.getAttribute("nonce"));r=d(l.map(a=>{if(a=D(a),a in x)return;x[a]=!0;const e=a.endsWith(".css"),c=e?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${a}"]${c}`))return;const _=document.createElement("link");if(_.rel=e?"stylesheet":B,e||(_.as="script"),_.crossOrigin="",_.href=a,u&&_.setAttribute("nonce",u),document.head.appendChild(_),e)return new Promise((f,T)=>{_.addEventListener("load",f),_.addEventListener("error",()=>T(new Error(`Unable to preload CSS for ${a}`)))})}))}function n(d){const i=new Event("vite:preloadError",{cancelable:!0});if(i.payload=d,window.dispatchEvent(i),!i.defaultPrevented)throw d}return r.then(d=>{for(const i of d||[])i.status==="rejected"&&n(i.reason);return s().catch(n)})};async function H(t,{era:s,id:l}){const{texts:o}=await y(),r=o.find(e=>e.id===l);if(!r){t.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Text not found: ${l}</p>
          <a href="#/explore" class="btn">Back to Explorer</a>
        </div>
      </div>
    `;return}const n=E(r.path);t.innerHTML=`
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${r.title}</span>
        <button class="btn reader__download" title="Download">&#8595; Download</button>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Author</span>
            <span class="reader__meta-value">${r.author}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Written</span>
            <span class="reader__meta-value">${r.year_written}</span>
          </div>
          ${r.translator?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Translator</span>
              <span class="reader__meta-value">${r.translator} (${r.year_translated})</span>
            </div>
          `:""}
          <div class="reader__meta-field">
            <span class="reader__meta-label">Era</span>
            <span class="reader__meta-value">${r.era_display}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Format</span>
            <span class="badge badge--${r.format}">${r.format}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Topics</span>
            <div class="reader__meta-topics">
              ${r.topics.map(e=>`<span class="topic-pill">${I(e)}</span>`).join("")}
            </div>
          </div>
          ${r.description?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${r.description}</span>
            </div>
          `:""}
          ${r.prerequisites.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${r.prerequisites.map(e=>{const c=o.find(_=>_.id===e);return c?`<a href="#/read/${c.era_dir}/${c.id}" class="reader__meta-prereq">${c.title}</a>`:`<span class="reader__meta-value">${e}</span>`}).join("")}
            </div>
          `:""}
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading text...</div>
          </div>
        </div>
      </div>
    </div>
  `,t.querySelector(".reader__download").addEventListener("click",()=>{const e=document.createElement("a");e.href=n,e.download=r.filename,e.click()});const d=t.querySelector(".reader__sidebar"),i=t.querySelector(".reader__sidebar-toggle");d.classList.add("reader__sidebar--collapsed"),i.addEventListener("click",()=>{const e=d.classList.toggle("reader__sidebar--collapsed");i.textContent=e?"Show Details":"Hide Details"});const u=t.querySelector(".reader__viewport-inner");let a=null;try{a=await(await U(r.format)).render(u,n,t)}catch(e){console.error("Reader error:",e),u.innerHTML=`
      <div class="reader__error">
        <p>Failed to load text. The file may be temporarily unavailable.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${e.message}</p>
        <a href="${n}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{a&&a()}}async function U(t){switch(t){case"epub":return(await v(async()=>{const{default:s}=await import("./epub-reader-i1hTWVgL.js");return{default:s}},[])).default;case"pdf":return(await v(async()=>{const{default:s}=await import("./pdf-reader-CrR_Zpek.js");return{default:s}},[])).default;case"html":return(await v(async()=>{const{default:s}=await import("./html-reader-BvnsfJ7c.js");return{default:s}},[])).default;case"txt":return(await v(async()=>{const{default:s}=await import("./txt-reader-DQg-AX_E.js");return{default:s}},[])).default;default:throw new Error(`Unsupported format: ${t}`)}}function I(t){return t.split("-").map(s=>s.charAt(0).toUpperCase()+s.slice(1)).join(" ")}const L=document.getElementById("app");L.appendChild(C());const b=document.createElement("main");b.id="content";L.appendChild(b);g("/",t=>j(t));g("/syllabus",t=>k(t));g("/explore",t=>O(t));g("/read/:era/:id",(t,s)=>H(t,s));A(b);"serviceWorker"in navigator&&window.addEventListener("load",()=>{navigator.serviceWorker.register("/Enchiridion/sw.js").catch(()=>{})});
