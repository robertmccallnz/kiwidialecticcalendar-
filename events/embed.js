/* Kiwi Dialectic course events — embeddable widget.
 *
 * Usage on any site:
 *   <div id="kd-events"></div>
 *   <script src="https://robertmccallnz.github.io/kiwidialecticcalendar-/events/embed.js"
 *           data-target="#kd-events"
 *           data-course="te-pa-tuwatawata"     // optional: filter to one course
 *           data-limit="6"
 *           data-style="dark"></script>
 *
 * Pulls from events.json on the same origin. No external deps.
 */
(function(){
  const SCRIPT = document.currentScript;
  const FEED   = "https://robertmccallnz.github.io/kiwidialecticcalendar-/events.json";
  const TARGET = SCRIPT.getAttribute("data-target") || "#kd-events";
  const COURSE = SCRIPT.getAttribute("data-course") || "";
  const LIMIT  = parseInt(SCRIPT.getAttribute("data-limit") || "8", 10);
  const STYLE  = SCRIPT.getAttribute("data-style") || "dark";

  const palettes = {
    dark:  {bg:"#0c0c0c",ink:"#f5f0e6",red:"#c41e1e",grey:"#8a8a8a",rule:"#262626",accent:"#1a0a0a"},
    light: {bg:"#fffaf0",ink:"#1a1a1a",red:"#c41e1e",grey:"#6a6a6a",rule:"#e8e0cf",accent:"#fff4d6"}
  };
  const P = palettes[STYLE] || palettes.dark;

  const STYLE_TAG = `
.kd-events{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:${P.bg};color:${P.ink};padding:18px;border:1px solid ${P.rule};max-width:680px}
.kd-events h3{font-family:"Bebas Neue",sans-serif;letter-spacing:3px;color:${P.red};margin:0 0 12px;font-size:1.1rem}
.kd-events .kd-row{display:grid;grid-template-columns:72px 1fr;gap:12px;padding:10px 0;border-bottom:1px solid ${P.rule}}
.kd-events .kd-row:last-child{border-bottom:none}
.kd-events .kd-date .d{font-family:"Bebas Neue",sans-serif;font-size:1.6rem;line-height:1;color:${P.ink}}
.kd-events .kd-date .m{font-size:.78rem;color:${P.grey};letter-spacing:2px;text-transform:uppercase}
.kd-events .kd-date .t{font-size:.72rem;color:${P.grey};margin-top:2px}
.kd-events .kd-meta a{color:${P.ink};text-decoration:none;font-weight:600;font-size:.95rem}
.kd-events .kd-meta a:hover{color:${P.red}}
.kd-events .kd-teaser{color:${P.grey};font-size:.86rem;margin:3px 0 0}
.kd-events .kd-claim{display:inline-block;margin-top:4px;font-size:.72rem;color:${P.red};letter-spacing:1px;text-transform:uppercase;text-decoration:none;border:1px solid ${P.red};padding:2px 7px}
.kd-events .kd-foot{margin-top:14px;font-size:.78rem;color:${P.grey}}
.kd-events .kd-foot a{color:${P.ink}}
  `;

  function mount(){
    const target = document.querySelector(TARGET);
    if (!target){ console.warn("[kd-events] target not found:", TARGET); return; }
    const style = document.createElement("style");
    style.textContent = STYLE_TAG;
    document.head.appendChild(style);
    target.classList.add("kd-events");
    target.innerHTML = '<div class="kd-row" style="border:none;color:'+P.grey+'">Loading events…</div>';
    fetch(FEED, {cache:"no-store"})
      .then(r => r.json())
      .then(data => render(target, data))
      .catch(e => target.innerHTML = '<div class="kd-row" style="border:none;color:'+P.grey+'">Couldn’t load events.</div>');
  }

  function render(target, data){
    const now = new Date();
    let events = data.events
      .map(e => ({...e, _d: new Date(e.start)}))
      .filter(e => e._d >= new Date(now.getTime() - 6*3600*1000))
      .sort((a,b) => a._d - b._d);
    if (COURSE) events = events.filter(e => e.course_slug === COURSE);
    events = events.slice(0, LIMIT);

    const header = COURSE
      ? `Upcoming — ${data.events.find(e => e.course_slug===COURSE)?.course_title || COURSE}`
      : "Upcoming course events";

    if (events.length === 0){
      target.innerHTML = `<h3>${header}</h3><div class="kd-row" style="border:none;color:${P.grey}">No upcoming events.</div>`;
      return;
    }
    const rows = events.map(e => {
      const day  = e._d.toLocaleDateString("en-NZ",{day:"2-digit",timeZone:"Pacific/Auckland"});
      const mon  = e._d.toLocaleDateString("en-NZ",{month:"short",timeZone:"Pacific/Auckland"});
      const time = e._d.toLocaleTimeString("en-NZ",{hour:"2-digit",minute:"2-digit",timeZone:"Pacific/Auckland"});
      const claim = e.claim_url || (e.badge_slug ? `https://robertmccallnz.github.io/kiwidialecticcalendar-/badges/${e.badge_slug}/` : null);
      return `<div class="kd-row">
        <div class="kd-date"><div class="d">${day}</div><div class="m">${mon}</div><div class="t">${time}</div></div>
        <div class="kd-meta">
          <a href="${e.link||'#'}" target="_blank" rel="noopener">${e.title}</a>
          ${e.teaser ? `<p class="kd-teaser">${e.teaser}</p>` : ''}
          ${claim ? `<a class="kd-claim" href="${claim}" target="_blank" rel="noopener">Claim pou tohu</a>` : ''}
        </div>
      </div>`;
    }).join("");
    target.innerHTML = `<h3>${header}</h3>${rows}
      <div class="kd-foot">
        <a href="https://robertmccallnz.github.io/kiwidialecticcalendar-/events/" target="_blank" rel="noopener">All events</a> ·
        <a href="https://robertmccallnz.github.io/kiwidialecticcalendar-/the-kiwi-dialectic-courses.ics">.ics</a> ·
        <a href="https://robertmccallnz.github.io/kiwidialecticcalendar-/events.rss">RSS</a>
      </div>`;
  }

  if (document.readyState === "loading"){
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
