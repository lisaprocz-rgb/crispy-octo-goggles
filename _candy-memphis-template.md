# Candy Memphis HTML Template — Lisa's Hub style

**Use this template for any page that gets pushed to `lisaprocz-rgb/crispy-octo-goggles`.** The hub (index.html) uses this exact style; subpages must match.

When building a page, paste the full skeleton below, then:

1. Replace `[PAGE_TITLE]` with the short title (used in `<title>` and breadcrumb).
2. Replace `[PAGE_HEADING]` with the big H1 (often emoji + name, e.g. `🎬 Movies`).
3. Replace `[PAGE_SUBTITLE]` with a one-line subtitle.
4. Replace `[H1_SHADOW]` with the page accent hex color (see palette below) — drives the text-shadow on the h1.
5. Replace `[CONTENT]` with the body of the page, using the section + card patterns shown below the skeleton.
6. Leave `DYNAMIC_TIMESTAMP` as-is — the inline script swaps it at load time. (If you prefer server-side, you can replace it with today's ET timestamp string before pushing.)

Do NOT alter the CSS block, the live-clock script, or the back-to-hub link. They are shared design across the whole hub.

## Color palette

Use these accent hex values (assign one as the page accent, mix others for cards):

- pink `#ff5c8a`
- yellow `#ffd23f`
- cyan `#3ec6e0`
- purple `#a78bfa`
- magenta `#d68bff`
- blue `#5b9dff`
- green `#3dd6b5`
- lime `#7bd957`
- orange `#ffb84d`
- light blue `#4fc3f7`
- soft pink `#ff8fc7`
- lavender `#b79cff`

Page-to-accent mapping already established on the hub (use these unless you have a reason not to):

- movies.html → pink `#ff5c8a`
- concerts.html → purple `#a78bfa`
- theater-update.html → magenta `#d68bff`
- tv-streaming.html → cyan `#3ec6e0`
- primary.html → blue `#5b9dff`
- bucks-government.html → green `#3dd6b5`
- pa_county_elections_map.html → lime `#7bd957`
- dcl-monitor.html → light blue `#4fc3f7`
- disney-news.html → soft pink `#ff8fc7`

## Full skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[PAGE_TITLE] · Lisa's Hub</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Nunito',sans-serif;min-height:100vh;color:#1f2440;
  background:#fff8f0;
  background-image:radial-gradient(#ffd23f 2px,transparent 2px),
                   radial-gradient(#ff5c8a 2px,transparent 2px);
  background-size:60px 60px;background-position:0 0,30px 30px}
header{text-align:center;padding:2.6rem 1.5rem 1.8rem;position:relative}
.hub-label{font-family:'Baloo 2';font-weight:700;font-size:.78rem;letter-spacing:.28em;
  text-transform:uppercase;color:#ff5c8a;margin-bottom:.6rem}
.hub-label a{color:#ff5c8a;text-decoration:none;border-bottom:2px dotted #ff5c8a;padding-bottom:2px}
.hub-label a:hover{color:#1f2440;border-bottom-color:#1f2440}
h1{font-family:'Baloo 2';font-size:clamp(2.2rem,6.5vw,4rem);font-weight:800;color:#1f2440;
  line-height:1;text-shadow:4px 4px 0 [H1_SHADOW]}
.subtitle{font-size:.95rem;margin-top:.75rem;color:#6b6f8c;font-weight:700}
.gold-line{width:120px;height:8px;margin:1.1rem auto 0;border-radius:8px;
  background:repeating-linear-gradient(90deg,#ff5c8a 0 16px,#3ec6e0 16px 32px,#ffd23f 32px 48px)}
.live-clock{margin-top:1.1rem;display:inline-block;background:#1f2440;color:#fff;
  padding:.5rem 1.3rem;border-radius:14px;font-family:'Baloo 2';font-weight:600;
  font-size:.92rem;box-shadow:4px 4px 0 #ff5c8a}
.live-clock .clock-date{color:#ffd23f}.live-clock .clock-time{color:#fff}
main{max-width:1080px;margin:0 auto;padding:1rem 1.4rem 4rem}
.section-divider{display:flex;align-items:center;gap:.9rem;margin:2.4rem 0 1.2rem}
section:first-of-type .section-divider, .section-group:first-child .section-divider{margin-top:.4rem}
.divider-accent{width:22px;height:22px;background:#ffd23f;border:3px solid #1f2440;
  border-radius:6px;transform:rotate(45deg);flex-shrink:0}
.divider-label{font-family:'Baloo 2';font-size:1.4rem;font-weight:800;color:#1f2440;
  background:#fff;padding:.1rem .9rem;border:3px solid #1f2440;border-radius:14px;
  box-shadow:3px 3px 0 #3ec6e0}
.divider-line{flex:1;height:4px;border-radius:4px;background:#1f2440;opacity:.15}
.sub-label{font-family:'Baloo 2';font-weight:700;font-size:.95rem;color:#1f2440;
  margin:1.2rem 0 .6rem;text-transform:uppercase;letter-spacing:.06em}
.card{position:relative;display:block;background:#fff;color:#1f2440;text-decoration:none;
  border:3px solid #1f2440;border-radius:18px;padding:1.2rem 1.4rem;
  box-shadow:6px 6px 0 var(--accent,#ff5c8a);margin-bottom:1rem;
  transition:transform .16s ease,box-shadow .16s ease}
.card:hover{transform:translate(-2px,-2px);box-shadow:8px 8px 0 var(--accent,#ff5c8a)}
.card strong, .card .card-title{font-family:'Baloo 2';font-size:1.12rem;font-weight:800;
  display:block;margin-bottom:.3rem;color:#1f2440}
.card .sub{display:block;color:#6b6f8c;font-size:.86rem;font-weight:600;line-height:1.5;margin-top:.15rem}
.card .note{color:#1f2440;font-size:.74rem;font-weight:800;display:inline-block;
  background:var(--accent,#ffd23f);padding:.2rem .65rem;border-radius:999px;
  border:2px solid #1f2440;margin:.15rem .35rem .15rem 0;letter-spacing:.04em;text-transform:uppercase}
.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.1rem}
.card-pink{--accent:#ff5c8a}.card-yellow{--accent:#ffd23f}.card-cyan{--accent:#3ec6e0}
.card-purple{--accent:#a78bfa}.card-magenta{--accent:#d68bff}.card-blue{--accent:#5b9dff}
.card-green{--accent:#3dd6b5}.card-lime{--accent:#7bd957}.card-orange{--accent:#ffb84d}
.card-lblue{--accent:#4fc3f7}.card-sopink{--accent:#ff8fc7}.card-lavender{--accent:#b79cff}
.back-to-hub{display:inline-block;font-family:'Baloo 2';font-size:.85rem;font-weight:700;
  background:#fff;color:#1f2440;text-decoration:none;padding:.45rem 1.1rem;border-radius:999px;
  border:3px solid #1f2440;box-shadow:3px 3px 0 #ffd23f;margin-bottom:1.2rem;
  transition:transform .16s ease,box-shadow .16s ease}
.back-to-hub:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 #ffd23f}
table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;
  border:3px solid #1f2440;border-radius:14px;overflow:hidden;margin:.8rem 0 1.4rem;
  font-size:.9rem}
th{background:#1f2440;color:#fff;font-family:'Baloo 2';font-weight:700;text-align:left;
  padding:.55rem .85rem;font-size:.85rem;letter-spacing:.03em}
td{padding:.5rem .85rem;border-top:2px dotted #e6e2d8;font-weight:600}
tr:first-child td{border-top:none}
ul, ol{margin:.6rem 0 1rem 1.4rem;font-size:.92rem;font-weight:600;line-height:1.6}
li{margin-bottom:.25rem}
p{margin:.6rem 0;font-size:.95rem;font-weight:500;line-height:1.6}
a:not(.card):not(.back-to-hub):not(.hub-label a){color:#1f2440;font-weight:700;
  text-decoration:none;border-bottom:2px dotted #ff5c8a;padding-bottom:1px}
a:not(.card):not(.back-to-hub):not(.hub-label a):hover{color:#ff5c8a;border-bottom-color:#1f2440}
.callout{background:#fff;border:3px solid #1f2440;border-radius:16px;
  box-shadow:5px 5px 0 #ffd23f;padding:1rem 1.2rem;margin:.8rem 0}
.callout strong{font-family:'Baloo 2'}
footer{text-align:center;padding:2rem 1rem 2.4rem;color:#6b6f8c;font-size:.84rem;font-weight:700}
.footer-clock{margin-top:.4rem;color:#ff5c8a}
.timestamp-badge{display:inline-block;background:#1f2440;color:#ffd23f;font-family:'Baloo 2';
  font-weight:700;font-size:.78rem;padding:.25rem .75rem;border-radius:999px;letter-spacing:.04em}
@media (max-width:600px){
  h1{font-size:2.4rem}
  main{padding:1rem .9rem 3rem}
  .card{padding:1rem 1.1rem}
}
</style>
</head>
<body>
<header>
<div class="hub-label"><a href="index.html">← Lisa's Hub</a></div>
<h1>[PAGE_HEADING]</h1>
<div class="subtitle">[PAGE_SUBTITLE]</div>
<div class="gold-line"></div>
<div class="live-clock"><span class="clock-date" id="header-date"></span><span class="clock-time" id="header-time"></span></div>
</header>
<main>
[CONTENT]
</main>
<footer>Lisa's Hub · Last updated <span class="timestamp-badge">DYNAMIC_TIMESTAMP</span><div class="footer-clock" id="footer-clock"></div></footer>
<script>
function updateClock(){const now=new Date();const dateStr=now.toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'});const timeStr=now.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit',second:'2-digit',hour12:true});const combined=dateStr+' · '+timeStr;const hDate=document.getElementById('header-date');const hTime=document.getElementById('header-time');const footer=document.getElementById('footer-clock');if(hDate)hDate.textContent=dateStr+' · ';if(hTime)hTime.textContent=timeStr;if(footer)footer.textContent=combined;}
updateClock();setInterval(updateClock,1000);
</script>
</body>
</html>
```

## Content patterns

Inside `[CONTENT]`, prefer this structure:

**Section divider** for top-level groups:

```html
<section class="section-group">
  <div class="section-divider"><span class="divider-accent"></span><span class="divider-label">Section Name</span><span class="divider-line"></span></div>
  ...
</section>
```

**Sub-label** for in-section groupings:

```html
<div class="sub-label">Musicals</div>
```

**Card grid** (auto-fit columns):

```html
<div class="cards-grid">
  <div class="card card-pink"><strong>🎵 Show Name</strong><span class="sub">Theater · note</span></div>
  <div class="card card-cyan"><strong>📺 Title</strong><span class="sub">Where to watch · when</span></div>
</div>
```

**Single info card** (full width):

```html
<div class="card card-purple"><strong>Headline</strong><span class="sub">Details and context.</span></div>
```

**Inline pill / note**: wrap small status text in `<span class="note">…</span>` inside a card — it picks up the card's accent color.

**Tables** (showtimes, schedules, etc.): wrap in standard `<table><tr><th>…</tr><tr><td>…</td></tr></table>`. Styling is automatic.

**Callout** (one-off highlights):

```html
<div class="callout"><strong>Note:</strong> something important.</div>
```

## Things NOT to do

- Do not introduce new color schemes or gradients outside this palette.
- Do not use Segoe UI / system fonts — the brand fonts are Baloo 2 (display) and Nunito (body).
- Do not hardcode dark navy headers, red gradients, or the old beige/burgundy palette from previous templates.
- Do not omit the `← Lisa's Hub` back link in the header.
- Do not change the polka-dot background.

## Timestamp injection

The inline script replaces `DYNAMIC_TIMESTAMP` at page load with the visitor's local time. If you want a server-rendered timestamp that always shows ET regardless of viewer location, replace `DYNAMIC_TIMESTAMP` server-side with the actual string (format: `Sun, May 17 at 6:40 AM ET`) before pushing the file.
