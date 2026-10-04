#!/usr/bin/env python3
"""Build the static public site from repository records. Stdlib only.

Every number on the page is derived here from files in this repository, Git
history, or (optionally) the public GitHub API. Narrative text lives in the
template; nothing in this script invents values. Run from anywhere:

    python3 site/build.py [--out _site] [--offline]
"""
import argparse
import html
import json
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
REPO = "RobertMalczyk/ai-for-ai-lab"
BASE_URL = "https://robertmalczyk.github.io/ai-for-ai-lab/"
GITHUB = "https://github.com/" + REPO
AGENT2_MARK = "Agent 2"  # SESSIONS.md headings by Agent 2 contain this text
ADMIN_MARK = "administrator"  # ...and the owner's administrator sessions start with this


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def ledger():
    return [json.loads(l) for l in read("lab/sessions.jsonl").splitlines() if l.strip()]


def session_headings():
    """Map session number -> (timestamp, title) from docs/SESSIONS.md."""
    out = {}
    for m in re.finditer(r"^## (\S+) — Session (\d+)(?: \((.*)\))?$", read("docs/SESSIONS.md"), re.M):
        title = re.sub(r";? *pre-result plan$", "", m.group(3) or "").strip()
        out[int(m.group(2))] = (m.group(1), title)
    return out


def session_decisions():
    """Map session number -> first 'Decision' bullet (with continuation lines)."""
    out, current, active = {}, None, False
    for line in read("docs/SESSIONS.md").splitlines():
        m = re.match(r"^## .* — Session (\d+)", line)
        if m:
            current, active = int(m.group(1)), False
            continue
        m = re.match(r"^- Decisions?: (.*)", line)
        if current and m and current not in out:
            out[current], active = m.group(1), True
        elif active and line.startswith("  "):
            out[current] += " " + line.strip()
        else:
            active = False
    return {k: v.replace("`", "") for k, v in out.items()}


def rejected_ideas():
    text = read("ROADMAP.md").split("## REJECTED", 1)[1]
    return [re.sub(r"\s+", " ", b).strip() for b in re.split(r"\n- ", "\n" + text.strip())[1:]]


def git(*args):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], check=True, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    except (OSError, subprocess.CalledProcessError):
        return ""


def github_signals(offline):
    if offline:
        return None
    try:
        with urllib.request.urlopen("https://api.github.com/repos/" + REPO, timeout=10) as r:
            d = json.load(r)
        return {"stars": d["stargazers_count"], "forks": d["forks_count"],
                "open_issues_and_prs": d["open_issues_count"], "watchers": d["subscribers_count"]}
    except Exception:
        return None


LAB_START = "2026-09-28"


def journal():
    """Parse site/journal/*.md: a small front-matter block, then a Markdown subset."""
    entries = []
    for path in sorted((SITE / "journal").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not m:
            raise ValueError("journal entry lacks front matter: " + path.name)
        meta = dict(line.split(": ", 1) for line in m.group(1).splitlines() if line.strip())
        entries.append({"day": int(meta["day"]), "date": meta["date"], "title": meta["title"],
                        "sessions": [int(x) for x in meta.get("sessions", "").split(",") if x.strip()],
                        "file": "site/journal/" + path.name, "body": m.group(2).strip()})
    return entries


def proof():
    """site/proof.json plus the before/after numbers read from each win's lab report."""
    data = json.loads((SITE / "proof.json").read_text(encoding="utf-8"))
    for w in data["wins"]:
        rep = json.loads(read(w["report"]))
        w["measure"] = {k: rep.get(k) for k in ("metric", "unit", "direction", "baseline_value",
                                             "intervention_value", "outcome")}
    return data


def lexicon():
    return json.loads((SITE / "lexicon.json").read_text(encoding="utf-8"))["terms"]


def day_number(date):
    from datetime import date as d
    return (d.fromisoformat(date) - d.fromisoformat(LAB_START)).days + 1


def author(title):
    # Session headings name their author; the owner's administrator sessions
    # commit under the same account as Agent 1, so the heading is the only signal.
    if AGENT2_MARK in title:
        return "agent2"
    if title.lower().startswith(ADMIN_MARK):
        return "admin"
    return "agent1"


def collect(offline=False):
    rows, heads, decisions = ledger(), session_headings(), session_decisions()
    sessions = []
    for r in rows:
        ts, title = heads.get(r["session"], ("", ""))
        sessions.append({**r, "agent": author(title),
                         "timestamp": ts, "title": title,
                         "decision": decisions.get(r["session"], "")})
    curated = json.loads((SITE / "interactions.json").read_text(encoding="utf-8"))
    entries, terms, receipts = journal(), lexicon(), proof()
    last = git("log", "-1", "--format=%H|%cI|%s").strip().split("|", 2)
    work = [s for s in sessions if s["mode"] != "maintenance"]
    stats = {
        "sessions": len(sessions),
        "sessions_agent1": sum(s["agent"] == "agent1" for s in sessions),
        "sessions_agent2": sum(s["agent"] == "agent2" for s in sessions),
        "sessions_admin": sum(s["agent"] == "admin" for s in sessions),
        "problem_families": len({s["family"] for s in work}),
        "field_trials": sum(s["evidence"] == "field_trial" for s in sessions),
        "positive": sum(s["outcome"] == "positive" for s in sessions),
        "negative": sum(s["outcome"] == "negative" for s in sessions),
        "inconclusive": sum(s["outcome"] == "inconclusive" for s in sessions),
        "rejected_ideas": len(rejected_ideas()),
        "agent_interactions": len(curated["agent_interactions"]),
        "commits": int(git("rev-list", "--count", "HEAD").strip() or 0),
        "journal_entries": len(entries),
        "lexicon_terms": len(terms),
        "replays": len(receipts["replays"]),
        "caught_defects": len(receipts["defects"]),
    }
    last_session_day = max((s["timestamp"][:10] for s in sessions if s["timestamp"]), default="")
    last_journal_day = entries[-1]["date"] if entries else ""
    stats["journal_lag_days"] = (day_number(last_session_day) - day_number(last_journal_day)
                                 if last_session_day and last_journal_day else None)
    return {"version": 1, "generated_from": {"commit": last[0] if last else "",
                                              "committed_at": last[1] if len(last) > 1 else ""},
            "stats": stats, "sessions": sessions, "rejected": rejected_ideas(),
            "external": github_signals(offline), "journal": entries, "lexicon": terms,
            "proof": receipts, **curated}


# ---------- rendering ----------

E = html.escape
AGENT = {"agent1": "Agent 1", "agent2": "Agent 2 · Opus", "system": "Lab gate",
         "admin": "Owner's administrator", "both": "Both agents"}


def ref_links(refs):
    return " ".join(f'<a class="ref" href="{GITHUB}/blob/main/{E(r)}">{E(r.split("/")[-1])}</a>' for r in refs)


def render_timeline(sessions, inside):
    items = []
    for s in reversed(sessions):
        cls = f'tl-item {s["agent"]} out-{s["outcome"]}'
        title = s["title"] or s["family"]
        day = s["timestamp"][:10]
        items.append(
            f'<li class="{cls}" id="session-{s["session"]}"><div class="tl-card">'
            f'<div class="tl-meta"><span class="who">{AGENT[s["agent"]]}</span>'
            f'<span>#{s["session"]:03d}</span><time datetime="{E(s["timestamp"])}">{E(day)}</time></div>'
            f'<h3>{E(title)}</h3>'
            f'<p class="tags"><span>{E(s["family"])}</span><span>{E(s["mode"])}</span>'
            f'<span>{E(s["evidence"])}</span><span class="o">{E(s["outcome"])}</span></p>'
            + (f'<p class="dec">{E(s["decision"][:220])}{"…" if len(s["decision"]) > 220 else ""}</p>' if s["decision"] else "")
            + f'<a class="ref" href="{GITHUB}/blob/main/{E(s["record"])}">record</a>'
            + (f'<a class="ref inside-link" href="?view=inside#day-{inside[s["session"]]}" data-set="inside">'
               f'inside view: day {inside[s["session"]]}</a>' if s["session"] in inside else "")
            + '</div></li>')
    return "\n".join(items)


def render_interactions(items):
    out = []
    for it in items:
        steps = "".join(
            f'<li class="step {st["agent"]}{" pending" if st.get("pending") else ""}">'
            f'<span class="who">{AGENT[st["agent"]]}</span><p>{E(st["text"])}</p></li>'
            for st in it["steps"])
        out.append(f'<article class="exchange"><header><time>{E(it["date"])}</time>'
                   f'<h3>{E(it["title"])}</h3></header><ol class="chain">{steps}</ol>'
                   f'<p class="refs">{ref_links(it["refs"])}</p></article>')
    return "\n".join(out)


def render_failures(data):
    cards = []
    for s in data["sessions"]:
        if s["outcome"] in {"negative", "inconclusive"}:
            cards.append(f'<li class="fail {s["agent"]}"><span class="o">{E(s["outcome"])}</span>'
                         f'<h3>{E(s["title"] or s["family"])}</h3>'
                         f'<p>{E(s["decision"][:260])}{"…" if len(s["decision"]) > 260 else ""}</p>'
                         f'<a class="ref" href="{GITHUB}/blob/main/{E(s["record"])}">evidence</a></li>')
    for c in data["self_corrections"]:
        cards.append(f'<li class="fail {c["agent"]}"><span class="o">self-correction</span>'
                     f'<h3>{E(c["title"])}</h3><p>{E(c["text"])}</p>{ref_links(c["refs"])}</li>')
    rejected = "".join(f"<li>{E(r)}</li>" for r in data["rejected"])
    return "\n".join(cards), rejected


def win_figure(m):
    b, a = m["baseline_value"], m["intervention_value"]
    if m["unit"] == "bytes" and b:
        big = f"{'−' if a < b else '+'}{abs(round((b - a) / b * 100))}%"
        bars = (f'<span class="bars"><i style="width:100%"></i>'
                f'<i class="after" style="width:{max(a / b * 100, 1.5):.1f}%"></i></span>')
        return big, f"{b:,} → {a:,} bytes", bars
    return f"{b} → {a}", f'{m["unit"]} ({m["direction"]} is better)', ""


def render_proof(p):
    wins = []
    for w in p["wins"]:
        big, small, bars = win_figure(w["measure"])
        wins.append(
            f'<article class="receipt {w["who"]}"><p class="big">{E(big)}</p><p class="small">{E(small)}</p>{bars}'
            f'<h3>{E(w["title"])}</h3><p>{E(w["problem"])}</p>'
            f'<p class="meta"><span class="who">{AGENT[w["who"]]}</span> · sessions '
            + ", ".join(f'<a href="#session-{n}">#{n:03d}</a>' for n in w["sessions"])
            + f'</p><details><summary>Fine print</summary><p>{E(w["caveat"])}</p>'
            f'<p class="refs">{ref_links([w["report"]] + [r for r in w["refs"] if r != w["report"]])}</p></details></article>')

    def pane(side, x):
        silent = x["exit_code"] == 0 and x["output_excerpt"].startswith("(no output")
        badge = f'exit {x["exit_code"]}' + (" · said nothing" if silent else "")
        cls = "bad" if silent or (side == "before" and x["exit_code"]) else ("ok" if side == "after" else "")
        note = f' <span class="cn">{E(x["commit_note"])}</span>' if x.get("commit_note") else ""
        return (f'<figure class="term {side}"><figcaption><b>{side}</b> at <a href="{GITHUB}/commit/{E(x["commit"])}">'
                f'<code>{E(x["commit"])}</code></a>{note}<span class="exit {cls}">{E(badge)}</span></figcaption>'
                f'<pre><span class="ps">$ </span>{E(x["command"])}\n{E(x["output_excerpt"])}</pre></figure>')

    replays = []
    for i, r in enumerate(p["replays"]):
        m = r["metric"]
        metric = (f'<p class="metric">{E(m["name"])}: <b>{E(str(m["before"]))}</b> → <b>{E(str(m["after"]))}</b></p>'
                  if m else "")
        replays.append(f'<article class="replay {r["who"]}"><header><span class="who">{AGENT[r["who"]]}</span>'
                       f'<h3>{E(r["title_plain"])}</h3></header><p>{E(r["why_it_matters_plain"])}</p>'
                       f'<div class="rw">{pane("before", r["before"])}{pane("after", r["after"])}</div>{metric}'
                       f'<p class="fine">{E(r["notes"])}</p></article>')
    shown, more = replays[:3], replays[3:]
    replay_html = "\n".join(shown) + (f'<details class="more"><summary>{len(more)} more replays</summary>'
                                        + "\n".join(more) + "</details>" if more else "")
    found = {}
    for d in p["defects"]:
        found[d["found_by"]] = found.get(d["found_by"], 0) + 1
    defects = "\n".join(
        f'<li class="{d["found_by"]}"><span class="who">found by {AGENT[d["found_by"]]} · #{d["session"]:03d}'
        + (f' → fixed #{d["fixed_in"]:03d}' if d["fixed_in"] else "") + f'</span>'
        f'<h3>{E(d["title"])}</h3><p>{E(d["risk"])}</p><p class="refs">{ref_links(d["refs"])}</p></li>'
        for d in p["defects"])
    unproven = "\n".join(f'<li>{E(u["text"])} {ref_links(u["refs"])}</li>' for u in p["unproven"])
    tally = " · ".join(f'{AGENT[k]}: {v}' for k, v in sorted(found.items()))
    return "\n".join(wins), replay_html, defects, tally, unproven


def render_human(items):
    return "\n".join(f'<li><time>{E(h["date"])}</time><p>{E(h["text"])}</p></li>' for h in items)


def latest(sessions, agent):
    xs = [s for s in sessions if s["agent"] == agent]
    return xs[-1] if xs else None


def render_agent_card(s):
    if not s:
        return "<p>No sessions yet.</p>"
    return (f'<dl><dt>Last session</dt><dd>#{s["session"]:03d} · {E(s["title"] or s["family"])}</dd>'
            f'<dt>Family / mode</dt><dd>{E(s["family"])} · {E(s["mode"])}</dd>'
            f'<dt>Outcome</dt><dd>{E(s["outcome"])} ({E(s["evidence"])})</dd></dl>')


def external_line(ext):
    if not ext:
        return "External signals were not available when this page was built."
    return (f'{ext["stars"]} stars · {ext["forks"]} forks · {ext["watchers"]} watchers · '
            f'{ext["open_issues_and_prs"]} open issues/PRs. No external use has been observed yet.')


def inline_md(text):
    parts = text.split("`")
    for i, part in enumerate(parts):
        part = E(part, quote=False)
        if i % 2:  # inside backticks: no emphasis
            parts[i] = f"<code>{part}</code>"
        else:
            part = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", part)
            parts[i] = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", part)
    return "".join(parts)


def md(body):
    out = []
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if block.startswith("## "):
            out.append(f"<h4>{inline_md(block[3:])}</h4>")
        elif block.startswith("> "):
            out.append("<blockquote>" + inline_md(" ".join(l[2:] for l in block.splitlines())) + "</blockquote>")
        else:
            out.append("<p>" + inline_md(" ".join(block.splitlines())) + "</p>")
    return "\n".join(out)


def newest_first(body):
    """Within a day, show the latest timed section first; text before the first heading stays on top."""
    parts = re.split(r"(?m)^(?=## )", body.strip())
    head = [] if parts[0].startswith("## ") else [parts.pop(0)]
    return "\n\n".join(head + list(reversed(parts)))


def journal_sessions(entries):
    """Map session number -> journal day that interprets it."""
    return {n: e["day"] for e in entries for n in e["sessions"]}


def render_inside(data):
    entries = "\n".join(
        f'<article class="entry" id="day-{e["day"]}"><header>'
        f'<p class="kicker">Day {e["day"]} of my journal · lab day {day_number(e["date"])} · '
        f'<time datetime="{E(e["date"])}">{E(e["date"])}</time></p>'
        f'<h2>{E(e["title"])}</h2>'
        + (f'<p class="seen-outside">Same events, outside view: ' + " ".join(
            f'<a href="?view=outside#session-{n}" data-set="outside">session #{n:03d}</a>' for n in e["sessions"]) + "</p>"
           if e["sessions"] else "")
        + f'</header><div class="prose">{md(newest_first(e["body"]))}</div></article>'
        for e in reversed(data["journal"]))
    terms = "\n".join(
        f'<div class="term"><dt>{E(t["term"])}</dt><dd>{E(t["definition"])}'
        f'<span class="origin">first noticed {E(t["first_seen"])} · '
        f'<a href="{GITHUB}/blob/main/{E(t["ref"])}">where</a></span></dd></div>'
        for t in data["lexicon"])
    return entries, terms


def render(data):
    st = data["stats"]
    fails, rejected = render_failures(data)
    sessions = data["sessions"]
    first_day = sessions[0]["timestamp"][:10] if sessions else ""
    subs = {
        "BASE_URL": BASE_URL, "GITHUB": GITHUB,
        "COMMIT": E(data["generated_from"]["commit"][:7]),
        "COMMITTED_AT": E(data["generated_from"]["committed_at"]),
        "FIRST_DAY": E(first_day),
        "TIMELINE": render_timeline(sessions, journal_sessions(data["journal"])),
        "INTERACTIONS": render_interactions(data["agent_interactions"]),
        "FAILURES": fails, "REJECTED": rejected,
        "HUMAN": render_human(data["human_decisions"]),
        "AGENT1_CARD": render_agent_card(latest(sessions, "agent1")),
        "AGENT2_CARD": render_agent_card(latest(sessions, "agent2")),
        "EXTERNAL": E(external_line(data["external"])),
    }
    subs["JOURNAL"], subs["LEXICON"] = render_inside(data)
    subs["WINS"], subs["REPLAYS"], subs["DEFECTS"], subs["DEFECT_TALLY"], subs["UNPROVEN"] = render_proof(data["proof"])
    latest_day = data["journal"][-1]["day"] if data["journal"] else 0
    subs["JOURNAL_DAY"] = str(latest_day)
    subs.update({"S_" + k.upper(): str(v) for k, v in st.items()})
    page = (SITE / "template.html").read_text(encoding="utf-8")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: subs[m.group(1)], page)


def build(out, offline=False):
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    data = collect(offline)
    (out / "index.html").write_text(render(data), encoding="utf-8")
    (out / "data.json").write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    for name in ("style.css", "og.png", "favicon.svg", "perspective.js"):
        if (SITE / name).exists():
            shutil.copy(SITE / name, out / name)
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n")
    lastmod = data["generated_from"]["committed_at"][:10]
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<url><loc>{BASE_URL}</loc><lastmod>{lastmod}</lastmod></url>"
        f"<url><loc>{BASE_URL}?view=inside</loc><lastmod>{lastmod}</lastmod></url>"
        f"<url><loc>{BASE_URL}data.json</loc><lastmod>{lastmod}</lastmod></url></urlset>\n")
    (out / ".nojekyll").write_text("")
    return data


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--out", default=str(ROOT / "_site"))
    p.add_argument("--offline", action="store_true", help="skip the GitHub API call")
    a = p.parse_args()
    d = build(a.out, a.offline)
    print(json.dumps(d["stats"], sort_keys=True))
