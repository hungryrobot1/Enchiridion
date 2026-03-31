const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["assets/md-reader-C6phV3Oz.js","assets/md-reader-WbfJEqtj.css"])))=>i.map(i=>d[i]);
(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))d(o);new MutationObserver(o=>{for(const a of o)if(a.type==="childList")for(const u of a.addedNodes)u.tagName==="LINK"&&u.rel==="modulepreload"&&d(u)}).observe(document,{childList:!0,subtree:!0});function l(o){const a={};return o.integrity&&(a.integrity=o.integrity),o.referrerPolicy&&(a.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?a.credentials="include":o.crossOrigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function d(o){if(o.ep)return;o.ep=!0;const a=l(o);fetch(o.href,a)}})();const D=[];let L=null;function x(e,t){D.push({pattern:e,handler:t})}function z(e){const t=e.replace(/^#\/?/,"/");for(const{pattern:l,handler:d}of D){const o=F(l,t);if(o!==null)return{handler:d,params:o}}return null}function F(e,t){const l=e.split("/").filter(Boolean),d=t.split("/").filter(Boolean);if(l.length!==d.length)return null;const o={};for(let a=0;a<l.length;a++)if(l[a].startsWith(":"))o[l[a].slice(1)]=decodeURIComponent(d[a]);else if(l[a]!==d[a])return null;return o}function G(e){async function t(){const l=window.location.hash||"#/",d=z(l);L&&(L(),L=null),d?(e.innerHTML="",L=await d.handler(e,d.params)||null):window.location.hash="#/",document.querySelectorAll(".site-header__link").forEach(o=>{const a=o.getAttribute("href");o.classList.toggle("site-header__link--active",a===l||l==="#/"&&a==="#/")})}window.addEventListener("hashchange",t),t()}function N(){const e=document.createElement("header");e.className="site-header",e.innerHTML=`
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
  `;const t=e.querySelector(".site-header__toggle"),l=e.querySelector(".site-header__nav");return t.addEventListener("click",()=>{const d=l.classList.toggle("site-header__nav--open");t.classList.toggle("site-header__toggle--active",d),t.setAttribute("aria-expanded",d)}),l.querySelectorAll(".site-header__link").forEach(d=>{d.addEventListener("click",()=>{l.classList.remove("site-header__nav--open"),t.classList.remove("site-header__toggle--active"),t.setAttribute("aria-expanded","false")})}),e}let S=null;async function T(){return S||(S=await(await fetch("/Enchiridion/text-index.json")).json(),S)}async function W(e){const{texts:t,facets:l}=await T();e.innerHTML=`
    <div class="landing">
      <section class="landing__hero">
        <h1 class="landing__title">Enchiridion</h1>
        <p class="landing__subtitle">An Open Great Books Program for STEM Learning</p>
        <p class="landing__description">
          ${t.length} primary texts spanning 2,500 years of mathematical, scientific,
          and philosophical thought — free and open source.
        </p>
        <p class="landing__principle">
          <em>Timeless learning by letting the books speak for themselves.</em>
        </p>
      </section>

      <section class="landing__stats">
        <div class="landing__stat">
          <span class="landing__stat-number">${t.length}</span>
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
          <p>Follow the complete chronological journey through all ${t.length} texts, from ancient Greece to the information age.</p>
        </a>
        <a href="#/explore" class="landing__card">
          <h3>Explore Texts</h3>
          <p>Search, sort, and filter the full library by era, subject, author, or format.</p>
        </a>
        <a href="#/read/${t[0].era_dir}/${t[0].id}" class="landing__card">
          <h3>Start Reading</h3>
          <p>Begin with ${t[0].title} by ${t[0].author} — the traditional starting point.</p>
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
          ${l.eras.map(d=>`
            <div class="landing__era">
              <span class="landing__era-name">${d.display}</span>
              <span class="landing__era-count">${d.count} texts</span>
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
  `}async function V(e){const{texts:t,facets:l}=await T(),d={};for(const o of l.eras)d[o.id]={display:o.display,texts:t.filter(a=>a.era===o.id)};e.innerHTML=`
    <div class="page syllabus">
      <header class="syllabus__header">
        <h1>The Grand Tour</h1>
        <p>A chronological journey through ${t.length} texts spanning 2,500 years of thought.</p>
        <p class="syllabus__approach">
          <strong>Recommended approach:</strong> proceed chronologically, taking a
          "some of all, all of some" approach — read broadly across subjects within
          each era, and dive deep into areas of particular interest.
        </p>
      </header>

      ${l.eras.map(o=>{const a=d[o.id].texts,u={};for(const p of a){const h=p.topics[0]||"other";u[h]||(u[h]=[]),u[h].push(p)}return`
          <section class="syllabus__era">
            <button class="syllabus__era-toggle" data-era="${o.id}">
              <h2>${o.display}</h2>
              <span class="syllabus__era-count">${o.count} texts</span>
              <span class="syllabus__era-chevron">&#9662;</span>
            </button>
            <div class="syllabus__era-content" id="era-${o.id}">
              ${Object.entries(u).map(([p,h])=>`
                <div class="syllabus__topic-group">
                  <h3>${Y(p)}</h3>
                  <ol class="syllabus__text-list">
                    ${h.map(s=>`
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
  `,e.querySelectorAll(".syllabus__era-toggle").forEach(o=>{o.addEventListener("click",()=>{const a=o.dataset.era,p=document.getElementById(`era-${a}`).classList.toggle("syllabus__era-content--open");o.querySelector(".syllabus__era-chevron").textContent=p?"▴":"▾"})})}function Y(e){return e.split("-").map(t=>t.charAt(0).toUpperCase()+t.slice(1)).join(" ")}const Z="https://raw.githubusercontent.com/hungryrobot1/Enchiridion/main";function C(e){const l=e.split("/").map(d=>encodeURIComponent(d)).join("/");return`${Z}/${l}`}let m={query:"",era:"",topic:"",format:"",sort:"chronological"};async function K(e){const{texts:t,facets:l}=await T();e.innerHTML=`
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
            ${l.eras.map(s=>`
              <option value="${s.id}" ${m.era===s.id?"selected":""}>
                ${s.display}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="topic">
            <option value="">All Topics</option>
            ${l.topics.map(s=>`
              <option value="${s}" ${m.topic===s?"selected":""}>
                ${I(s)}
              </option>
            `).join("")}
          </select>
          <select class="explorer__filter-select" data-filter="format">
            <option value="">All Formats</option>
            ${l.formats.map(s=>`
              <option value="${s}" ${m.format===s?"selected":""}>
                ${s.toUpperCase()}
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
  `;const d=e.querySelector(".explorer__search-input"),o=e.querySelector(".explorer__grid"),a=e.querySelector(".explorer__results-count"),u=e.querySelectorAll(".explorer__filter-select");function p(){let s=t;if(m.query){const n=m.query.toLowerCase();s=s.filter(r=>r.title.toLowerCase().includes(n)||r.author.toLowerCase().includes(n)||r.description.toLowerCase().includes(n)||r.topics.some(i=>i.toLowerCase().includes(n)))}switch(m.era&&(s=s.filter(n=>n.era===m.era)),m.topic&&(s=s.filter(n=>n.topics.includes(m.topic))),m.format&&(s=s.filter(n=>n.format===m.format)),s=[...s],m.sort){case"reverse-chrono":s.sort((n,r)=>r.year_sort-n.year_sort);break;case"title":s.sort((n,r)=>n.title.localeCompare(r.title));break;case"author":s.sort((n,r)=>n.author.localeCompare(r.author));break}if(a.textContent=`${s.length} of ${t.length} texts`,s.length===0){o.innerHTML='<div class="explorer__empty">No texts match your filters.</div>';return}o.innerHTML=s.map(n=>`
      <a href="#/read/${n.era_dir}/${n.id}" class="text-card" data-id="${n.id}">
        <div class="text-card__header">
          <span class="text-card__title">${n.title}</span>
          <span class="badge badge--${n.format}">${n.format}</span>
        </div>
        <div class="text-card__author">${n.author}</div>
        <div class="text-card__year">${n.year_written}${n.translator?` · trans. ${n.translator}`:""}</div>
        <div class="text-card__description">${n.description}</div>
        <div class="text-card__footer">
          ${n.topics.slice(0,3).map(r=>`<span class="topic-pill">${I(r)}</span>`).join("")}
          <button class="text-card__download" data-path="${n.path}" data-filename="${n.filename}" title="Download">
            &#8595; Download
          </button>
        </div>
      </a>
    `).join(""),o.querySelectorAll(".text-card__download").forEach(n=>{n.addEventListener("click",r=>{r.preventDefault(),r.stopPropagation();const i=C(n.dataset.path),c=document.createElement("a");c.href=i,c.download=n.dataset.filename,c.click()})})}let h;d.addEventListener("input",()=>{clearTimeout(h),h=setTimeout(()=>{m.query=d.value,p()},200)}),u.forEach(s=>{s.addEventListener("change",()=>{const n=s.dataset.filter;n==="sort"?m.sort=s.value:m[n]=s.value,p()})}),p(),d.focus()}function I(e){return e.split("-").map(t=>t.charAt(0).toUpperCase()+t.slice(1)).join(" ")}const J="modulepreload",Q=function(e){return"/Enchiridion/"+e},R={},$=function(t,l,d){let o=Promise.resolve();if(l&&l.length>0){let u=function(s){return Promise.all(s.map(n=>Promise.resolve(n).then(r=>({status:"fulfilled",value:r}),r=>({status:"rejected",reason:r}))))};document.getElementsByTagName("link");const p=document.querySelector("meta[property=csp-nonce]"),h=(p==null?void 0:p.nonce)||(p==null?void 0:p.getAttribute("nonce"));o=u(l.map(s=>{if(s=Q(s),s in R)return;R[s]=!0;const n=s.endsWith(".css"),r=n?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${s}"]${r}`))return;const i=document.createElement("link");if(i.rel=n?"stylesheet":J,n||(i.as="script"),i.crossOrigin="",i.href=s,h&&i.setAttribute("nonce",h),document.head.appendChild(i),n)return new Promise((c,v)=>{i.addEventListener("load",c),i.addEventListener("error",()=>v(new Error(`Unable to preload CSS for ${s}`)))})}))}function a(u){const p=new Event("vite:preloadError",{cancelable:!0});if(p.payload=u,window.dispatchEvent(p),!p.defaultPrevented)throw u}return o.then(u=>{for(const p of u||[])p.status==="rejected"&&a(p.reason);return t().catch(a)})};let k=null;async function j(){if(k)return k;const t=await fetch("/Enchiridion/supplement-index.json");return t.ok?(k=await t.json(),k):(k={supplements:[],facets:{eras:[],types:[]}},k)}const B="enchiridion-bookmarks";function M(){try{return JSON.parse(localStorage.getItem(B))||{}}catch{return{}}}function X(e,t){const l=M();l[e]=t,localStorage.setItem(B,JSON.stringify(l))}function ee(e){return M()[e]||null}async function te(e,{era:t,id:l}){const[{texts:d},{supplements:o}]=await Promise.all([T(),j()]),a=d.find(i=>i.id===l);if(!a){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Text not found: ${l}</p>
          <a href="#/explore" class="btn">Back to Explorer</a>
        </div>
      </div>
    `;return}const u=C(a.path),p=a.format==="pdf";e.innerHTML=`
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${a.title}</span>
        ${p?`
          <div class="reader__page-nav">
            <input type="text" class="reader__page-input" aria-label="Current page">
            <span class="reader__page-total"></span>
          </div>
        `:""}
        <div class="reader__toolbar-controls">
          ${p?`
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
            <span class="reader__meta-value">${a.author}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Written</span>
            <span class="reader__meta-value">${a.year_written}</span>
          </div>
          ${a.translator?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Translator</span>
              <span class="reader__meta-value">${a.translator} (${a.year_translated})</span>
            </div>
          `:""}
          <div class="reader__meta-field">
            <span class="reader__meta-label">Era</span>
            <span class="reader__meta-value">${a.era_display}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Format</span>
            <span class="badge badge--${a.format}">${a.format}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Topics</span>
            <div class="reader__meta-topics">
              ${a.topics.map(i=>`<span class="topic-pill">${re(i)}</span>`).join("")}
            </div>
          </div>
          ${a.description?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${a.description}</span>
            </div>
          `:""}
          ${a.prerequisites.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${a.prerequisites.map(i=>{const c=d.find(v=>v.id===i);return c?`<a href="#/read/${c.era_dir}/${c.id}" class="reader__meta-prereq">${c.title}</a>`:`<span class="reader__meta-value">${i}</span>`}).join("")}
            </div>
          `:""}
          ${(()=>{const i=o.filter(c=>c.texts.includes(a.id));return i.length===0?"":`
              <div class="reader__meta-field">
                <span class="reader__meta-label">Supplements</span>
                ${i.map(c=>`<a href="#/supplement/${encodeURIComponent(c.era_dir)}/${c.id}" class="reader__meta-prereq">${c.title}</a>`).join("")}
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
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const i=document.createElement("a");i.href=u,i.download=a.filename,i.click()});const h=e.querySelector(".reader__sidebar"),s=e.querySelector(".reader__sidebar-toggle");h.classList.add("reader__sidebar--collapsed"),s.addEventListener("click",()=>{const i=h.classList.toggle("reader__sidebar--collapsed");s.textContent=i?"Show Details":"Hide Details"});const n=e.querySelector(".reader__viewport-inner");let r=null;try{const i=await ae(a.format);if(p){const c=e.querySelector(".reader__page-input"),v=e.querySelector(".reader__page-total"),_=e.querySelector(".reader__zoom-in"),f=e.querySelector(".reader__zoom-out"),y=e.querySelector(".reader__zoom-level");let E=null;r=await i.render(n,u,e,{onReady:b=>{_.addEventListener("click",()=>b.zoomIn()),f.addEventListener("click",()=>b.zoomOut()),c.addEventListener("keydown",g=>{if(g.key==="Enter"){const q=parseInt(c.value,10);isNaN(q)||b.goToPage(q),c.blur()}}),c.addEventListener("blur",()=>{const g=parseInt(c.value,10);isNaN(g)||b.goToPage(g)}),c.addEventListener("focus",()=>c.select());const w=ee(l);if(w&&w>1){const g=document.createElement("div");g.className="reader__resume-banner",g.innerHTML=`
              <span>Continue from page ${w}?</span>
              <button class="reader__resume-btn" data-action="resume">Resume</button>
              <button class="reader__resume-btn reader__resume-btn--dismiss" data-action="dismiss">Start over</button>
            `,e.querySelector(".reader__toolbar").after(g),g.querySelector('[data-action="resume"]').addEventListener("click",()=>{b.goToPage(w),g.remove()}),g.querySelector('[data-action="dismiss"]').addEventListener("click",()=>{g.remove()})}E=setInterval(()=>{const g=b.getCurrentPage();g>1&&X(l,g)},5e3)},onPageChange:(b,w)=>{c.value=b,c.style.width=`${String(w).length+1}ch`,v.textContent=`of ${w}`},onScaleChange:b=>{y.textContent=`${Math.round(b*50)}%`,_.disabled=b>=4,f.disabled=b<=1}});const P=r;r=()=>{E&&clearInterval(E),P&&P()}}else r=await i.render(n,u,e)}catch(i){console.error("Reader error:",i),n.innerHTML=`
      <div class="reader__error">
        <p>Failed to load text. The file may be temporarily unavailable.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${i.message}</p>
        <a href="${u}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{r&&r()}}async function ae(e){switch(e){case"epub":return(await $(async()=>{const{default:t}=await import("./epub-reader-i1hTWVgL.js");return{default:t}},[])).default;case"pdf":return(await $(async()=>{const{default:t}=await import("./pdf-reader-DEUgGmV0.js");return{default:t}},[])).default;case"html":return(await $(async()=>{const{default:t}=await import("./html-reader-BvnsfJ7c.js");return{default:t}},[])).default;case"txt":return(await $(async()=>{const{default:t}=await import("./txt-reader-DQg-AX_E.js");return{default:t}},[])).default;default:throw new Error(`Unsupported format: ${e}`)}}function re(e){return e.split("-").map(t=>t.charAt(0).toUpperCase()+t.slice(1)).join(" ")}const H={"exercise-set":"Exercise Sets","lab-manual":"Lab Manuals","notation-guide":"Notation Guides","convention-guide":"Convention Guides","study-guide":"Study Guides"},O=Object.keys(H);async function se(e){const{supplements:t,facets:l}=await j();if(t.length===0){e.innerHTML=`
      <div class="page supplements">
        <header class="supplements__header">
          <h1>Supplements</h1>
          <p>Supplementary materials are being developed. Check back soon for exercise sets,
          lab manuals, notation guides, and convention guides.</p>
        </header>
      </div>
    `;return}const d=t.filter(r=>r.type!=="reference"),o=t.filter(r=>r.type==="reference"),a={};for(const r of l.eras)a[r.id]={display:r.display,count:r.count,supplements:d.filter(i=>i.era===r.id)};const u={};for(const r of o){const i=r.topic||"other";u[i]||(u[i]=[]),u[i].push(r)}const p=l.topics||[],h=l.eras.length,s=o.length,n=d.length;e.innerHTML=`
    <div class="page supplements">
      <header class="supplements__header">
        <h1>Supplements</h1>
        <p>${n>0?`${n} supplementary material${n!==1?"s":""} across ${h} section${h!==1?"s":""}`:"Supplementary materials are being developed"}${s>0?`${n>0?", plus ":""}${s} reference${s!==1?"s":""}`:""}.</p>
      </header>

      ${l.eras.map(r=>{const i=a[r.id];if(!i||i.supplements.length===0)return"";const c={};for(const _ of i.supplements){const f=_.type||"other";c[f]||(c[f]=[]),c[f].push(_)}const v=Object.entries(c).sort((_,f)=>{const y=O.indexOf(_[0]),E=O.indexOf(f[0]);return(y>=0?y:999)-(E>=0?E:999)});return`
          <section class="supplements__era">
            <button class="supplements__era-toggle" data-era="${r.id}">
              <h2>${r.display}</h2>
              <span class="supplements__era-count">${r.count} supplement${r.count!==1?"s":""}</span>
              <span class="supplements__era-chevron">&#9662;</span>
            </button>
            <div class="supplements__era-content" id="sup-era-${r.id}">
              ${v.map(([_,f])=>`
                <div class="supplements__type-group">
                  <h3>${H[_]||ne(_)}</h3>
                  <ul class="supplements__list">
                    ${f.map(y=>`
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

        ${p.map(r=>{const i=u[r.id]||[];return i.length===0?"":`
            <section class="supplements__era">
              <button class="supplements__era-toggle" data-era="ref-${r.id}">
                <h2>${r.display}</h2>
                <span class="supplements__era-count">${r.count} reference${r.count!==1?"s":""}</span>
                <span class="supplements__era-chevron">&#9662;</span>
              </button>
              <div class="supplements__era-content" id="sup-era-ref-${r.id}">
                <ul class="supplements__list">
                  ${i.map(c=>{const v=c.url&&!c.path;return`
                    <li>
                      <a href="${v?c.url:`#/supplement/${encodeURIComponent(c.era_dir)}/${c.id}`}"${v?' target="_blank" rel="noopener noreferrer"':""} class="supplements__link">
                        <span class="supplements__title">${c.title}</span>
                        ${c.description?`<span class="supplements__meta">${c.description}</span>`:""}
                      </a>
                    </li>
                  `}).join("")}
                </ul>
              </div>
            </section>
          `}).join("")}
      `:""}
    </div>
  `,e.querySelectorAll(".supplements__era-toggle").forEach(r=>{r.addEventListener("click",()=>{const i=r.dataset.era,v=document.getElementById(`sup-era-${i}`).classList.toggle("supplements__era-content--open");r.querySelector(".supplements__era-chevron").textContent=v?"▴":"▾"})})}function ne(e){return e.split("-").map(t=>t.charAt(0).toUpperCase()+t.slice(1)).join(" ")}const oe={"exercise-set":"Exercise Set","lab-manual":"Lab Manual","notation-guide":"Notation Guide","convention-guide":"Convention Guide",reference:"Reference"};async function ie(e,{era:t,id:l}){const[{supplements:d},{texts:o}]=await Promise.all([j(),T()]),a=d.find(_=>_.id===l);if(!a){e.innerHTML=`
      <div class="reader">
        <div class="reader__error">
          <p>Supplement not found: ${l}</p>
          <a href="#/supplements" class="btn">Back to Supplements</a>
        </div>
      </div>
    `;return}const u=C(a.path),p=a.format||"md",h=a.texts.map(_=>o.find(f=>f.id===_)).filter(Boolean),s=a.type==="reference"?"Topic":"Era",n=a.era_display;e.innerHTML=`
    <div class="reader">
      <div class="reader__toolbar">
        <button class="reader__back" onclick="history.back()">&larr; Back</button>
        <span class="reader__toolbar-title">${a.title}</span>
        <button class="btn reader__download" title="Download">&#8595; Download</button>
      </div>
      <div class="reader__body">
        <aside class="reader__sidebar">
          <button class="reader__sidebar-toggle">Show Details</button>
          <div class="reader__meta-field">
            <span class="reader__meta-label">Type</span>
            <span class="supplements__type-badge">${oe[a.type]||a.type}</span>
          </div>
          <div class="reader__meta-field">
            <span class="reader__meta-label">${s}</span>
            <span class="reader__meta-value">${n}</span>
          </div>
          ${p!=="md"?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Format</span>
              <span class="badge badge--${p}">${p}</span>
            </div>
          `:""}
          ${a.description?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Description</span>
              <span class="reader__meta-value">${a.description}</span>
            </div>
          `:""}
          ${h.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Texts</span>
              ${h.map(_=>`<a href="#/read/${_.era_dir}/${_.id}" class="reader__meta-prereq">${_.title}</a>`).join("")}
            </div>
          `:""}
          ${a.prerequisites.length>0?`
            <div class="reader__meta-field">
              <span class="reader__meta-label">Prerequisites</span>
              ${a.prerequisites.map(_=>{const f=d.find(y=>y.id===_);return f?`<a href="#/supplement/${encodeURIComponent(f.era_dir)}/${f.id}" class="reader__meta-prereq">${f.title}</a>`:`<span class="reader__meta-value">${_}</span>`}).join("")}
            </div>
          `:""}
        </aside>
        <div class="reader__viewport">
          <div class="reader__viewport-inner">
            <div class="reader__loading">Loading ${a.type==="reference"?"reference":"supplement"}...</div>
          </div>
        </div>
      </div>
    </div>
  `,e.querySelector(".reader__download").addEventListener("click",()=>{const _=document.createElement("a");_.href=u,_.download=a.path.split("/").pop(),_.click()});const r=e.querySelector(".reader__sidebar"),i=e.querySelector(".reader__sidebar-toggle");r.classList.add("reader__sidebar--collapsed"),i.addEventListener("click",()=>{const _=r.classList.toggle("reader__sidebar--collapsed");i.textContent=_?"Show Details":"Hide Details"});const c=e.querySelector(".reader__viewport-inner");let v=null;try{v=await(await le(p)).render(c,u,e)}catch(_){console.error("Supplement reader error:",_),c.innerHTML=`
      <div class="reader__error">
        <p>Failed to load ${a.type==="reference"?"reference":"supplement"}.</p>
        <p style="font-size: var(--text-xs); color: var(--color-text-muted);">${_.message}</p>
        <a href="${u}" class="btn" target="_blank" rel="noopener">Open Raw File</a>
      </div>
    `}return()=>{v&&v()}}async function le(e){switch(e){case"epub":return(await $(async()=>{const{default:t}=await import("./epub-reader-i1hTWVgL.js");return{default:t}},[])).default;case"pdf":return(await $(async()=>{const{default:t}=await import("./pdf-reader-DEUgGmV0.js");return{default:t}},[])).default;case"html":return(await $(async()=>{const{default:t}=await import("./html-reader-BvnsfJ7c.js");return{default:t}},[])).default;case"txt":return(await $(async()=>{const{default:t}=await import("./txt-reader-DQg-AX_E.js");return{default:t}},[])).default;case"md":default:return(await $(async()=>{const{default:t}=await import("./md-reader-C6phV3Oz.js");return{default:t}},__vite__mapDeps([0,1]))).default}}function ce(e){e.innerHTML=`
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
  `}const U=document.getElementById("app");U.appendChild(N());const A=document.createElement("main");A.id="content";U.appendChild(A);x("/",e=>W(e));x("/syllabus",e=>V(e));x("/explore",e=>K(e));x("/read/:era/:id",(e,t)=>te(e,t));x("/supplements",e=>se(e));x("/supplement/:era/:id",(e,t)=>ie(e,t));x("/disclaimer",e=>ce(e));G(A);"serviceWorker"in navigator&&window.addEventListener("load",()=>{navigator.serviceWorker.register("/Enchiridion/sw.js").catch(()=>{})});
