#!/usr/bin/env python3
"""Build the City of Decatur Aquatics preview: the Aquatics page, a page per pool, and Aquatics Programs, with
every hour, closure and class time read live from Pool Relay by finder.js (#finder, #today, #week, data-live).
Nothing about WHEN a pool is open is typed here; only fees, passes, policies and facts about the water.
Run: python3 build.py"""
import html, json

E = html.escape
V = {"oakhurst": "vs5xjGaSs6tySEOx9atgBa", "ebster": "ZBmRARSf4O2gg8KPW9caEV",
     "glenlake": "jnrkVpJQieo0lGIGlhs7v7", "mckoy": "eP0CzodY7C1ejZGzDy5qqX"}  # Pool Relay share tokens
FEED = ",".join(V.values())
CITY = "https://www.decaturga.com/parksrec/page/aquatics"
IMG = "https://www.decaturga.com/sites/g/files/vyhlif13251/files/styles/full_node_primary/public/media/parksrec/image/"
POOLS = [
    dict(slug="oakhurst", name="Oakhurst Indoor Pool", facility="Oakhurst Indoor Pool", area="Decatur", kind="yearRound",
         address="450 East Lake Dr, Decatur, GA 30030", phone="404-378-2423", href="oakhurst-pool.html", indoor=True,
         blurb="Indoor, heated and open year-round, inside the Oakhurst Recreation Center (separate entrance on the right side of the building). "
               "5 lanes, 149,000 gallons, and up to 50 swimmers at a time, following American Red Cross lifeguard-to-swimmer ratios."),
    dict(slug="ebster", name="Ebster Pool", facility="Ebster Pool", area="Decatur", kind="yearRound", photo=IMG + "26186/ebster_pool.jpg",
         address="404 W Trinity Pl, Decatur, GA 30030", phone="404-378-4906", href="ebster-pool.html",
         blurb="A summer pool behind the Police Department, at Atlanta Ave. and West Trinity Place: 8 lanes, 25 yards, a big deck, a snack area and a shade shelter. "
               "Home pool of the Decatur Gators swim team, with morning swim lessons and lanes for lap swimmers."),
    dict(slug="glenlake", name="Glenlake Pool", facility="Glenlake Pool", area="Decatur", kind="yearRound",
         address="1121 Church St, Decatur, GA 30030", phone="404-378-7671", href="glenlake-pool.html",
         blurb="Decatur's largest and liveliest pool, on Church Street, with snack areas, sunny patios, shade shelters and shallow water for little ones."),
    dict(slug="mckoy", name="McKoy Pool", facility="McKoy Pool", area="Decatur", kind="yearRound", photo=IMG + "26191/mckoy_pool.jpg",
         address="534 McKoy St, Decatur, GA 30030", phone="", href="mckoy-pool.html",
         blurb="A zero-entry (beach entry) pool that makes getting in easier for older and disabled swimmers, bubblers for young swimmers, and lap lanes "
               "that can be set aside for adult-only lap swimming."),
]
OUTDOOR = [p for p in POOLS if not p.get("indoor")]

def live(mode, pool, **kw):
    attrs = "".join(f' data-{k.replace("_", "-")}="{E(str(v))}"' for k, v in kw.items())
    return f'data-live="{mode}" data-view="{V[pool]}" data-pool="{pool}"{attrs}'

MENU = [("About Us", None), ("Parks", None), ("Recreation Centers", None), ("Aquatics", "index.html"),
        ("Aquatics Programs", "aquatics-programs.html"), ("Ebster Pool", "ebster-pool.html"), ("Glenlake Pool", "glenlake-pool.html"),
        ("McKoy Pool", "mckoy-pool.html"), ("Oakhurst Pool", "oakhurst-pool.html")]

LOGO = """<svg viewBox="0 0 120 70" role="img" aria-label="City of Decatur"><rect x="6" y="34" width="24" height="26" fill="#1f8fd6"/><path d="M4 36 18 22 32 36z" fill="#1f8fd6"/>
<rect x="34" y="26" width="28" height="34" fill="#f2b51b"/><path d="M31 28 48 8 65 28z" fill="#f2b51b"/><rect x="44" y="40" width="8" height="20" fill="#fff"/>
<rect x="66" y="36" width="24" height="24" fill="#e0384b"/><path d="M63 38 78 24 93 38z" fill="#e0384b"/><rect x="94" y="44" width="16" height="16" fill="#3fae49"/>
<path d="M92 46 102 36 112 46z" fill="#3fae49"/></svg>"""

def page(file, title, body, contact):
    menu = "".join(
        f'<a class="{"sub" if i > 3 else ""}{" open" if label == "Aquatics" else ""}{" here" if href == file else ""}" href="{href or "#"}">{E(label)}</a>'
        for i, (label, href) in enumerate(MENU))
    doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a City of Decatur website. A mock-up of {CITY}
     with all four city pools on one live Pool Relay schedule. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)} | Decatur GA preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Zilla+Slab:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="preview-note"><b>Unofficial preview.</b> Not a City of Decatur page &mdash; a mock-up of <a href="{CITY}" target="_blank" rel="noopener noreferrer">the Aquatics pages</a> with all four pools on one live schedule.</div>
<header class="site"><div class="hdr">
  <a class="brand" href="index.html">{LOGO}<span>City of Decatur</span></a>
  <div class="right"><div class="util"><span>Visit</span><span>Contact</span><span>How do I?</span></div>
    <nav aria-label="Main"><span>Community</span><span>Business</span><span>Government</span><span>City Services</span></nav></div>
</div></header>
<div class="page">
  <aside class="side"><h2>Parks &amp; Recreation</h2><nav aria-label="Parks and Recreation">{menu}</nav></aside>
  <main class="main"><h1>{E(title)}</h1>{body}</main>
  <aside class="contact"><h2>Contact Information</h2>{contact}</aside>
</div>
<footer class="site"><div class="in">
  <div><h4>City of Decatur Parks &amp; Recreation</h4><p>Decatur Legacy Park Administrative Building<br>500 S. Columbia Dr., Decatur, GA 30030<br>404-377-0494</p></div>
  <div><h4>About this preview</h4><p>Built to demonstrate embedded <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a> schedules. Not operated by or affiliated with the City of Decatur or Dynamo Swim School. Schedules entered from the city's pool pages and Dynamo's Fall 2026 Oakhurst schedule on October 23, 2026.</p></div>
</div></footer>
<script>window.POOLS = {json.dumps([{k: v for k, v in p.items() if k not in ("blurb",)} for p in POOLS])};</script>
<script src="finder.js"></script>
</body>
</html>
"""
    open(file, "w").write(doc)

CONTACT = """<p><b>Location and Office Hours:</b>Decatur Legacy Park Administrative Building<br>500 S. Columbia Dr.<br>Decatur, GA 30030</p>
<p><b>Phone:</b>404-377-0494</p><p><b>Email:</b>dprd@decaturga.com</p>"""

ADMISSION = """<table class="fees"><tr><th>Age</th><th>Resident</th><th>Non-resident</th></tr>
<tr><td>1 and younger</td><td>Free</td><td>$4</td></tr><tr><td>2–13</td><td>$4</td><td>$6</td></tr>
<tr><td>14–64</td><td>$6</td><td>$8</td></tr><tr><td>65+</td><td>Free</td><td>$6</td></tr></table>
<p class="small muted">Cashless payment; exact change is accepted if you have no other way to pay. Resident rates need a CommunityPass resident
verification: bring a government ID and proof of residency to the Decatur, Ebster or Oakhurst Recreation Center or the Glenlake Tennis Center.</p>"""

# ── Aquatics ─────────────────────────────────────────────────────────────────
cards = "".join(f"""<div class="card"><h3><a href="{p['href']}">{E(p['name'])}</a></h3><p class="small muted">{E(p['address'])}</p>
  <p class="st" {live("closures", p["slug"], label="Closed")} hidden></p>
  <p class="small" {live("swims", p['slug'])}>…</p></div>""" for p in POOLS)
page("index.html", "Aquatics", f"""
    <p class="lede">The City of Decatur has three outdoor pools, Ebster, Glenlake and McKoy, and one indoor pool, Oakhurst, which is open
      year-round. Every pool's schedule on these pages is live: when the city changes it, these pages change with it.</p>
    <h2 id="find">Where can I swim right now?</h2>
    <div id="finder" class="finder" data-view="{FEED}" data-all-label="All pools"></div>
    <h2>The pools</h2>
    <div class="cards">{cards}</div>

    <h2>Pool admission</h2>
    {ADMISSION}
    <h2>Season swim passes (outdoor pools)</h2>
    <table class="fees"><tr><th>Pass</th><th>Resident</th><th>Non-resident</th></tr>
      <tr><td>Individual, 2–13</td><td>$50</td><td>$100</td></tr><tr><td>Individual, 14–64</td><td>$75</td><td>$150</td></tr>
      <tr><td>Individual, 65+</td><td>Free</td><td>$100</td></tr><tr><td>Household of 5 or fewer</td><td>$225 (+$20 each extra)</td><td>$450 (+$40 each extra)</td></tr></table>
    <p class="small muted">Buy online through CommunityPass or at any of the four centers, not at the pool counters. Oakhurst has its own passes; see <a href="oakhurst-pool.html">Oakhurst Pool</a>.</p>

    <h2>Safety and weather</h2>
    <div class="policy"><p>No large floats or tubes that block the lifeguards' view, and no water guns. Children in approved life jackets need close
      supervision; swimmers in diapers need swim diapers. Pools close during thunder and lightning: the two-hour limit is suspended while you wait, you
      can leave and come back later that day, and anyone who paid but couldn't get in the water gets a rain check.</p></div>

    <h2>Rentals</h2>
    <p>Pool parties, lane rentals and group visits (10 or more get $3 resident / $5 non-resident entry) are booked by form, at least two weeks ahead
      with payment in full. Call 404-377-0494.</p>

    <div class="replaces">
      <h2>What this replaces</h2>
      <ul>
        <li><b>"Pool Hours: 6 a.m.–3 p.m."</b> Oakhurst's page says the pool closes at 3pm on weekdays, but Dynamo Swim School teaches there until 7pm
          Monday through Thursday, and the Programs page gives Dynamo's and Integrated Therapy's times only as "throughout the week". Here every class
          is on the calendar, after 3pm too.</li>
        <li><b>Lessons inside open swim, unannounced.</b> On Tuesday and Thursday mornings Dynamo classes run during the city's 9am–3pm open swim. The
          city's schedule doesn't say so; here those lanes are taken out of open swim (which lanes is our estimate).</li>
        <li><b>A schedule in a contractor's PDF.</b> Dynamo's class times are a spreadsheet PDF on Dynamo's own site, which lists its winter break as
          "December 18 through Sunday, January 3, 2026" (the year should be 2027) and closes for Thanksgiving all week, while the city closes on Thanksgiving Day only.
          On one calendar, open swim gets every lane the days Dynamo is off.</li>
        <li><b>Holidays by name, not date.</b> Oakhurst's holiday list ("Easter, Memorial Day, Juneteenth…") gives no dates. Here each closure is on its day.</li>
        <li><b>Last season's hours, still up.</b> In October the outdoor pool pages still show the 2026 season dates. Here each pool says it is closed for the season.</li>
        <li><b>Two numbers for the same question.</b> The Aquatics page says to call 404-377-0494 about pools, lessons and rentals; the Pool Rentals page says 404-377-7231.</li>
      </ul>
    </div>
""", CONTACT)

# ── Oakhurst ─────────────────────────────────────────────────────────────────
oak = POOLS[0]
page("oakhurst-pool.html", "Oakhurst Pool", f"""
    <p class="lede">{E(oak['blurb'])}</p>
    <p class="small">{E(oak['address'])} · {E(oak['phone'])}. Park at the Oakhurst Recreation Center or Oakhurst Park and walk in through the fence between them.</p>
    <div class="top2">
      <section class="now" aria-live="polite"><h2>Right now</h2>
        <div id="today" data-view="{V['oakhurst']}" data-pool="oakhurst"><p class="muted">Loading today’s schedule…</p></div></section>
      <aside class="hours"><h2>Pool hours</h2>
        <div {live("hours", "oakhurst", format="dl", title="Lap Swim|Open Swim")}><p class="muted">…</p></div>
        <p class="small" style="margin:0"><b>Lap swim:</b> <span {live("when", "oakhurst", title="Lap Swim")}>…</span></p>
        <p class="small" style="margin:0 0 6px"><b>Open swim:</b> <span {live("when", "oakhurst", title="Open Swim")}>…</span></p>
        <div class="adjusted" {live("exceptions", "oakhurst", title="Lap Swim|Open Swim")} hidden></div>
      </aside>
    </div>
    <h2>This week</h2>
    <div id="week" data-view="{V['oakhurst']}" data-pool="oakhurst"><p class="muted">Loading the week…</p></div>
    <h2>Lane by lane</h2>
    <p class="small muted">Pick a day to see which of the 5 lanes are open swim, lap swim or a class.</p>
    <div class="frame"><iframe src="https://www.poolrelay.com/embed/{V['oakhurst']}" height="720" title="Oakhurst Indoor Pool, lane by lane" loading="lazy"></iframe></div>
    <h2>Admission and passes</h2>
    {ADMISSION}
    <table class="fees"><tr><th>Indoor pass</th><th>Resident</th><th>Non-resident</th></tr>
      <tr><td>Youth 10-punch</td><td>$35</td><td>$55</td></tr><tr><td>Youth monthly</td><td>$45</td><td>$65</td></tr>
      <tr><td>Senior 10-punch</td><td>Free</td><td>$35</td></tr><tr><td>Senior monthly</td><td>Free</td><td>$45</td></tr>
      <tr><td>Adult 10-punch</td><td>$45</td><td>$65</td></tr><tr><td>Adult monthly</td><td>$55</td><td>$75</td></tr>
      <tr><td>Family (4 people)</td><td>$110</td><td>$160</td></tr></table>
    <p class="small muted">Summer outdoor pool passes aren't valid here. Oakhurst closes for lightning and weather emergencies like the outdoor pools.</p>
    <h2>Programs here</h2>
    <p>Swim lessons, Swim Team Tune Up and adult lessons by Dynamo Swim School, aquatic therapy by Integrated Therapy, Decatur High School swim team, and rentals.
      Class times are on <a href="aquatics-programs.html">Aquatics Programs</a>.</p>
""", f"""<p><b>Oakhurst Pool</b>{E(oak['address'])}</p><p><b>Phone:</b>{E(oak['phone'])}</p>""")

# ── Outdoor pools ────────────────────────────────────────────────────────────
for p in OUTDOOR:
    page(p["href"], p["name"], f"""
    <p class="lede">{E(p['blurb'])}</p>
    <div class="top2">
      <section class="now" aria-live="polite"><h2>Right now</h2>
        <div id="today" data-view="{V[p['slug']]}" data-pool="{p['slug']}"><p class="muted">Loading today’s schedule…</p></div></section>
      <aside class="hours"><h2>Hours</h2>
        <p class="small" style="margin:0" {live("swims", p['slug'])}>…</p>
        <p class="closed" {live("closures", p['slug'], label="Closed")} hidden></p>
        <p class="small muted" style="margin:6px 0 0">When the city enters next season's hours, they appear here and on the calendar below.</p></aside>
    </div>
    <h2>Calendar</h2>
    <div class="frame"><iframe src="https://www.poolrelay.com/embed/{V[p['slug']]}" height="560" title="{E(p['name'])}" loading="lazy"></iframe></div>
    <h2>Admission</h2>
    {ADMISSION}
    <p class="small muted">Season passes for the outdoor pools are on the <a href="index.html">Aquatics</a> page. Pool parties can be booked for after-hours evenings in season.</p>
""", f"""<p><b>{E(p['name'])}</b>{E(p['address'])}</p>{f"<p><b>Phone:</b>{E(p['phone'])}</p>" if p['phone'] else ""}""")

# ── Aquatics programs ────────────────────────────────────────────────────────
LEVELS = [
    ("DynaBabies 1", "6–17 months, one child with one parent", "Swim Lessons – DynaBabies 1"),
    ("DynaBabies 2", "18–36 months, one child with one parent", "Swim Lessons – DynaBabies 2"),
    ("DynaBabies (mixed)", "10–36 months, one child with one parent", "Swim Lessons – DynaBabies (mixed)"),
    ("Preschool", "3–5 years, up to 4 swimmers per teacher", "Swim Lessons – Preschool"),
    ("Preschool/Gradeschool (mixed)", "3–14 years, up to 5 per teacher", "Swim Lessons – PS/GS (mixed)"),
    ("Gradeschool", "6–14 years, up to 5 per teacher", "Swim Lessons – Gradeschool"),
    ("Swim Team Tune Up", "Stroke and conditioning for swim team swimmers", "Swim Team Tune Up"),
    ("Adults", "Adult lessons", "Adult Swim Lessons"),
]
rows = "".join(f'<tr><th>{E(n)}<div class="small muted" style="font-weight:400">{E(a)}</div></th><td class="when" {live("when", "oakhurst", title=t, gap=0)}>…</td></tr>'
               for n, a, t in LEVELS)
page("aquatics-programs.html", "Aquatics Programs", f"""
    <p class="lede">Lessons and therapy at Oakhurst Indoor Pool are run by the city's contractors. Register with them directly.</p>
    <h2>Dynamo Swim School</h2>
    <p>Swim lessons for babies through adults, and Swim Team Tune Up. Class days and times below come from the live schedule.</p>
    <div class="tblwrap"><table class="prog">{rows}</table></div>
    <p class="small"><b>Tuition:</b> one day a week $116/month (4 classes), two days $232/month (8 classes); Swim Team Tune Up and adults $172/month.
      $60 annual registration fee per swimmer. Enrollment continues month to month until you withdraw (by the 15th for the end of that month).</p>
    <p class="small"><b>Register:</b> dynamoswimschool.com · Site director: 470-367-9023</p>
    <p class="closed" {live("closures", "oakhurst", label="Pool closed")} hidden></p>
    <h2>Integrated Therapy</h2>
    <p>Aquatic physical therapy classes. Integrated Therapy doesn't publish its Oakhurst class times; see <a href="https://www.aqua-pt.com/" target="_blank" rel="noopener">aqua-pt.com</a>.
      When its sessions are entered in the pool's schedule they appear on the <a href="oakhurst-pool.html">Oakhurst</a> calendar.</p>
    <h2>Decatur Gators</h2>
    <p>The city's summer swim team, ages 5–18, with home meets at Ebster Pool. Registration and practice times come out each spring.</p>
""", CONTACT)
print("built", 3 + len(OUTDOOR), "pages")
