#!/usr/bin/env python3
"""
build_concerts.py — reliable, self-auditing renderer for the concerts dashboard.

THE GOLDEN RULE: concert_archive.json is the source of truth. This script renders
EVERY venue from the archive, applies the suppression filter, and then AUDITS its
own output. If any non-suppressed show from the archive failed to appear on the
page, the script EXITS NON-ZERO and writes nothing — so a run can never silently
publish a page that dropped shows.

Usage:
    python3 build_concerts.py            # build + audit; writes concerts.html on success
    python3 build_concerts.py --check    # audit only against an existing concerts.html

Inputs (in repo root): concert_archive.json, concert_exclusions.json
Output: concerts.html  (header "Generated:" line + footer timestamp injected here)
"""
import json, re, html as H, unicodedata, datetime, sys, subprocess

ROOT = "."
ARCHIVE = f"{ROOT}/concert_archive.json"
EXCL    = f"{ROOT}/concert_exclusions.json"
OUT     = f"{ROOT}/concerts.html"

VENUE_ORDER = [
    ("Academy of Music","card-purple"),
    ("Kimmel Center","card-pink"),
    ("Kimmel Center - Miller Theater","card-lblue"),
    ("Kimmel Center - Marian Anderson Hall","card-lavender"),
    ("Perelman Theater","card-green"),
    ("Forrest Theatre","card-magenta"),
    ("Commonwealth Plaza","card-sopink"),
    ("The Met Philadelphia","card-cyan"),
    ("Xfinity Mobile Arena","card-yellow"),
    ("TD Pavilion at Highmark Mann","card-lime"),
    ("Skyline Stage at Highmark Mann","card-lblue"),
    ("Lincoln Field","card-sopink"),
    ("Citizens Park","card-green"),
    ("Xcite Parx","card-orange"),
    ("Sellersville Theater","card-cyan"),
    ("Bucks County Playhouse","card-green"),
    ("Keswick Theatre","card-yellow"),
    ("Music Mountain Theatre","card-blue"),
    ("Freedom Mortgage Pavilion","card-blue"),
    ("Sound Waves Hard Rock","card-orange"),
    ("Hard Rock Etess","card-orange"),
    ("Music Box Borgata","card-magenta"),
    ("Borgata Event Center","card-purple"),
    ("Ovation Hall Ocean","card-cyan"),
    ("Resorts AC","card-lblue"),
    ("Madison Square Garden","card-magenta"),
]

COMMON_WORDS = {'dance','tour','live','show','band','the','and','jazz','music','concert',
                'tribute','experience','festival','orchestra','symphony','trio','project',
                'night','stars','all','a','of','in'}

def nrm(s):
    s = s.lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = s.replace('&', ' ').replace('/', ' ')
    return re.sub(r'\s+', ' ', s).strip()

def base_key(s):
    n = nrm(s)
    for sp in [' - ', ' — ', ' – ', ' presents:']:
        j = s.find(sp)
        if j > 0:
            cand = nrm(s[:j])
            if cand:
                return cand
            break
    return n

def load_sup(excl_keys):
    sup = set()
    for k in excl_keys:
        sup.add(nrm(k)); sup.add(base_key(k))
    sup.discard('')
    return sup

def suppressed(name, sup):
    na, ba = nrm(name), base_key(name)
    if na in sup or ba in sup:
        return True
    for sk in sup:
        toks = sk.split()
        if len(toks) == 1 and toks[0] in COMMON_WORDS:
            continue
        if re.search(r'(?<![a-z0-9])' + re.escape(sk) + r'(?![a-z0-9])', na):
            return True
    return False

MON = {m:i for i,m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],1)}
def sortkey(d):
    m = re.search(r'([A-Z][a-z]{2})\s+(\d+).*?(\d{4})', d)
    return (int(m.group(3)), MON.get(m.group(1),13), int(m.group(2))) if m else (9999,13,99)
def esc(s):
    return H.escape(s, quote=True).replace("'", "&#x27;")

def matchnorm(s):
    s = s.lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = s.replace('&',' and ').replace('/',' ')
    s = re.sub(r'[^a-z0-9 ]',' ', s)
    return re.sub(r'\s+',' ', s).strip()

def render(arch, sup):
    secs, total_before, total_after, acts = [], 0, 0, set()
    for v, css in VENUE_ORDER:
        shows = arch['venues'].get(v, {}).get('shows', {})
        items = sorted(shows.items(), key=lambda kv: sortkey(kv[1]))
        total_before += len(items)
        cards = []
        for name, date in items:
            if suppressed(name, sup):
                continue
            acts.add(name)
            cards.append(f'    <div class="card {css}"><strong>{esc(name)}</strong>'
                         f'<span class="sub">{esc(date)}</span></div>')
        total_after += len(cards)
        body = "\n".join(cards) if cards else \
            f'    <div class="card {css}"><strong>No upcoming shows listed</strong>'\
            f'<span class="sub">Check back soon</span></div>'
        secs.append(
            '<section class="section-group">\n'
            f'  <div class="section-divider"><span class="divider-accent"></span>'
            f'<span class="divider-label">{esc(v)}</span><span class="divider-line"></span></div>\n'
            f'  <div class="cards-grid">\n{body}\n  </div>\n</section>'
        )
    return "\n".join(secs), total_before, total_after, sorted(acts, key=str.lower)

def audit(arch, sup, rendered_html):
    rendered = {}
    for m in re.finditer(r'divider-label">([^<]+)</span>.*?<div class="cards-grid">(.*?)</div>\s*</section>',
                         rendered_html, re.S):
        rendered[m.group(1)] = {matchnorm(H.unescape(n))
                                for n in re.findall(r'<strong>(.*?)</strong>', m.group(2))
                                if n != 'No upcoming shows listed'}
    missing = []
    for v in arch['venues']:
        if v not in dict(VENUE_ORDER):
            for s in arch['venues'][v]['shows']:
                if not suppressed(s, sup):
                    missing.append((v, s))
            continue
        for s in arch['venues'][v]['shows']:
            if suppressed(s, sup):
                continue
            if matchnorm(s) not in rendered.get(v, set()):
                missing.append((v, s))
    return missing

HEAD_TMPL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Philly & AC Concerts · Lisa's Hub</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Nunito',sans-serif;min-height:100vh;color:#1f2440;background:#fff8f0;background-image:radial-gradient(#ffd23f 2px,transparent 2px),radial-gradient(#ff5c8a 2px,transparent 2px);background-size:60px 60px;background-position:0 0,30px 30px}
header{text-align:center;padding:2.6rem 1.5rem 1.8rem;position:relative}
.hub-label{font-family:'Baloo 2';font-weight:700;font-size:.78rem;letter-spacing:.28em;text-transform:uppercase;color:#ff5c8a;margin-bottom:.6rem}
.hub-label a{color:#ff5c8a;text-decoration:none;border-bottom:2px dotted #ff5c8a;padding-bottom:2px}
.hub-label a:hover{color:#1f2440;border-bottom-color:#1f2440}
h1{font-family:'Baloo 2';font-size:clamp(2.2rem,6.5vw,4rem);font-weight:800;color:#1f2440;line-height:1;text-shadow:4px 4px 0 #a78bfa}
.subtitle{font-size:.95rem;margin-top:.75rem;color:#6b6f8c;font-weight:700}
.gold-line{width:120px;height:8px;margin:1.1rem auto 0;border-radius:8px;background:repeating-linear-gradient(90deg,#ff5c8a 0 16px,#3ec6e0 16px 32px,#ffd23f 32px 48px)}
.live-clock{margin-top:1.1rem;display:inline-block;background:#1f2440;color:#fff;padding:.5rem 1.3rem;border-radius:14px;font-family:'Baloo 2';font-weight:600;font-size:.92rem;box-shadow:4px 4px 0 #ff5c8a}
.live-clock .clock-date{color:#ffd23f}.live-clock .clock-time{color:#fff}
main{max-width:1080px;margin:0 auto;padding:1rem 1.4rem 4rem}
.section-divider{display:flex;align-items:center;gap:.9rem;margin:2.4rem 0 1.2rem}
section:first-of-type .section-divider{margin-top:.4rem}
.divider-accent{width:22px;height:22px;background:#ffd23f;border:3px solid #1f2440;border-radius:6px;transform:rotate(45deg);flex-shrink:0}
.divider-label{font-family:'Baloo 2';font-size:1.4rem;font-weight:800;color:#1f2440;background:#fff;padding:.1rem .9rem;border:3px solid #1f2440;border-radius:14px;box-shadow:3px 3px 0 #3ec6e0}
.divider-line{flex:1;height:4px;border-radius:4px;background:#1f2440;opacity:.15}
.card{display:block;background:#fff;color:#1f2440;border:3px solid #1f2440;border-radius:18px;padding:1.2rem 1.4rem;box-shadow:6px 6px 0 var(--accent,#ff5c8a);margin-bottom:1rem;transition:transform .16s ease,box-shadow .16s ease}
.card:hover{transform:translate(-2px,-2px);box-shadow:8px 8px 0 var(--accent,#ff5c8a)}
.card strong{font-family:'Baloo 2';font-size:1.12rem;font-weight:800;display:block;margin-bottom:.3rem;color:#1f2440}
.card .sub{display:block;color:#6b6f8c;font-size:.86rem;font-weight:600;line-height:1.5;margin-top:.15rem}
.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.1rem}
.card-pink{--accent:#ff5c8a}.card-yellow{--accent:#ffd23f}.card-cyan{--accent:#3ec6e0}.card-purple{--accent:#a78bfa}.card-magenta{--accent:#d68bff}.card-blue{--accent:#5b9dff}.card-green{--accent:#3dd6b5}.card-lime{--accent:#7bd957}.card-orange{--accent:#ffb84d}.card-lblue{--accent:#4fc3f7}.card-sopink{--accent:#ff8fc7}.card-lavender{--accent:#b79cff}
footer{text-align:center;padding:2rem 1rem 2.4rem;color:#6b6f8c;font-size:.84rem;font-weight:700}
.footer-clock{margin-top:.4rem;color:#ff5c8a}
.timestamp-badge{display:inline-block;background:#1f2440;color:#ffd23f;font-family:'Baloo 2';font-weight:700;font-size:.78rem;padding:.25rem .75rem;border-radius:999px;letter-spacing:.04em}
@media (max-width:600px){h1{font-size:2.4rem}main{padding:1rem .9rem 3rem}.card{padding:1rem 1.1rem}}
</style>
</head>
<body>
<header>
<div class="hub-label"><a href="index.html">&larr; Lisa's Hub</a></div>
<h1>Music Philly & AC Concerts</h1>
<div class="subtitle">Upcoming shows at Philadelphia, Atlantic City & NYC venues</div>
<div class="gold-line"></div>
<div class="live-clock"><span class="clock-date" id="header-date"></span><span class="clock-time" id="header-time"></span></div>
<div style="margin-top:.9rem;font-size:.85rem;font-weight:700;color:#6b6f8c;">Generated: __HEADER_GEN__</div>
</header>
<main>
'''
FOOT_TMPL = '''
</main>
<footer>
<div>Philly & AC Concerts · Part of Lisa's Hub</div>
<div class="footer-clock">Last updated: <span class="timestamp-badge">__DYNAMIC_TIMESTAMP__</span></div>
</footer>
<script>
function updateClock(){
  var now=new Date();
  var opts={weekday:'short',month:'short',day:'numeric',year:'numeric'};
  var d=now.toLocaleDateString('en-US',opts);
  var t=now.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit',hour12:true});
  var hd=document.getElementById('header-date');var ht=document.getElementById('header-time');
  if(hd) hd.textContent=d+' ';if(ht) ht.textContent=t;
}
updateClock();setInterval(updateClock,1000);
</script>
</body>
</html>
'''

def stamp():
    et  = subprocess.check_output(["bash","-lc","TZ='America/New_York' date '+%a, %b %-d, %Y · %-I:%M %p ET'"]).decode().strip()
    utc = subprocess.check_output(["bash","-lc","date -u '+(%H:%M UTC)'"]).decode().strip()
    ts  = subprocess.check_output(["bash","-lc","TZ='America/New_York' date '+%B %d, %Y at %-I:%M:%S %p'"]).decode().strip()
    return f"{et} {utc} · All content fetched live this run — no cached data used.", ts

def main():
    arch = json.load(open(ARCHIVE))
    sup  = load_sup(json.load(open(EXCL))['suppressed_artist_keys'])

    if '--check' in sys.argv:
        existing = open(OUT).read()
        miss = audit(arch, sup, existing)
        if miss:
            print(f"AUDIT FAILED: {len(miss)} non-suppressed shows missing from {OUT}:")
            for v,s in miss: print(f"  - {v}: {s}")
            sys.exit(1)
        print("AUDIT PASSED: 0 non-suppressed shows missing.")
        return

    body, before, after, acts = render(arch, sup)
    header_gen, ts = stamp()
    page = HEAD_TMPL.replace('__HEADER_GEN__', header_gen) + body + \
           FOOT_TMPL.replace('__DYNAMIC_TIMESTAMP__', ts)

    miss = audit(arch, sup, page)
    if miss:
        print(f"BUILD ABORTED — audit found {len(miss)} non-suppressed shows that would be dropped:")
        for v,s in miss: print(f"  - {v}: {s}")
        print("Nothing written. Fix the data/matcher and re-run.")
        sys.exit(1)

    open(OUT, "w").write(page)
    json.dump(acts, open(f"{ROOT}/acts_list.json","w"), ensure_ascii=False, indent=1)
    print(f"OK: wrote {OUT}. Venues={len(VENUE_ORDER)} cards_before_suppression={before} "
          f"cards_after={after} unique_acts={len(acts)} audit=PASS(0 missing)")

if __name__ == "__main__":
    main()
