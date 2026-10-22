// Memory and learning page. Renders memory-export.json (or memory-demo.json behind the DEMO switch).
// All text goes through textContent; nothing from the data is inserted as HTML.
(function () {
  "use strict";
  var AG = ["agent1", "agent2"], NAME = { agent1: "Agent 1", agent2: "Agent 2" };
  var $ = function (id) { return document.getElementById(id); };
  var data = null, filt = { agent: "", task: "", category: "", status: "", rule: "", from: "", to: "" };

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === "text") n.textContent = attrs[k];
      else if (k === "cls") n.className = attrs[k];
      else n.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(function (c) { if (c != null) n.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return n;
  }
  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); return n; }
  function day(s) { return s ? String(s).slice(0, 10) : "—"; }
  function num(v) { return v == null ? "—" : (Math.round(v * 100) / 100).toString(); }
  function safeHref(h) { return /^https:\/\//.test(h) ? h : null; }
  function link(h, t) { var s = safeHref(h); return s ? el("a", { href: s, text: t || s }) : el("span", { text: t || "" }); }
  function empty(t) { return el("p", { cls: "empty", text: t }); }

  function kind(e) {
    if (e.history && e.history.length && e.status === "retracted") return "correction";
    if (e.status === "pending" || e.status === "proposed" || e.value == null) return "pending";
    if (e.status === "disputed") return "disputed";
    if (e.status === "retracted") return "correction";
    if (e.status === "verified" && e.credited == null) return "duplicate";
    if (e.value > 0) return "reward";
    if (e.value < 0) return "penalty";
    return "neutral";
  }

  function renderFresh() {
    var f = clear($("fresh")), st = data.data_status;
    var cls = st === "available" ? "ok" : st === "stale" ? "warn" : "bad";
    var label = { available: "data available", stale: "data out of date", empty: "no data yet", unavailable: "data unavailable" }[st] || st;
    f.appendChild(el("span", { cls: "badge " + cls, text: label }));
    f.appendChild(el("span", { text: "Data as of: " + (data.last_success_at ? data.last_success_at.replace("T", " ").slice(0, 16) + " UTC" : "no records") }));
    f.appendChild(el("span", { text: "Generated: " + data.generated_at.replace("T", " ").slice(0, 16) + " UTC" }));
    if (data.source_commit) f.appendChild(el("span", { text: "commit " + String(data.source_commit).slice(0, 7) }));
    if (data.reason) f.appendChild(el("span", { text: data.reason }));
  }

  function renderMode() {
    var m = clear($("mode"));
    var mem = data.memory_enabled === true ? "Memory: ON" : data.memory_enabled === false ? "Memory: OFF" : "Memory: unknown";
    var box = el("div", { cls: "mode" }, [
      el("div", null, [el("div", { cls: "big", text: data.mode || "UNKNOWN" }), el("div", { cls: "badge " + (data.memory_enabled ? "ok" : "bad"), text: mem })]),
      el("dl", null, [
        el("dt", { text: "points influence" }), el("dd", { text: data.reward_influence == null ? "—" : String(data.reward_influence) + (data.reward_influence === 0 ? " (observed only)" : "") }),
        el("dt", { text: "coupling scope" }), el("dd", { text: data.coupling_scope || "—" }),
        el("dt", { text: "rules version" }), el("dd", { text: data.rule_version || "—" }),
        el("dt", { text: "contract" }), el("dd", { text: (data.contract_version || "—") + (data.implementation_status ? " · " + data.implementation_status : "") }),
      ])]);
    m.appendChild(box);
    var hist = data.mode_history || [];
    if (!hist.length) { m.appendChild(empty("No mode changes recorded.")); return; }
    var ul = el("ol", { cls: "hist", reversed: "" });
    hist.slice().reverse().forEach(function (h) {
      ul.appendChild(el("li", null, [el("b", { text: (h.from ? h.from + " → " : "") + h.to }), " · " + day(h.at) + " · influence " + num(h.influence) + " · rules " + (h.rule_version || "—") + " · by " + (h.decided_by || []).join(", ") + ". " + (h.reason || "")]));
    });
    m.appendChild(el("details", { open: "" }, [el("summary", { cls: "note", text: "Every mode change, newest first" }), ul]));
  }

  function renderCards() {
    var c = clear($("cards"));
    if (!data.agents) { c.appendChild(empty("No feedback data.")); return; }
    AG.forEach(function (a) {
      var s = data.agents[a] || {};
      var cost = s.cost && s.cost.measured ? num(s.cost.value) + " " + (s.cost.unit || "") : "not measured";
      c.appendChild(el("div", { cls: "card " + a }, [
        el("h3", { text: NAME[a] }),
        el("div", { cls: "nums" }, [
          el("div", { cls: "p" }, [el("b", { text: num(s.positive) }), el("span", { text: "rewards" })]),
          el("div", { cls: "n" }, [el("b", { text: num(s.negative) }), el("span", { text: "penalties" })]),
          el("div", null, [el("b", { text: String(s.graded || 0) }), el("span", { text: "graded actions" })]),
          el("div", null, [el("b", { text: String(s.pending || 0) }), el("span", { text: "pending" })]),
          el("div", null, [el("b", { text: String(s.disputed || 0) }), el("span", { text: "disputed" })]),
          el("div", null, [el("b", { text: num(s.net) }), el("span", { text: "net (supporting only)" })]),
        ]),
        el("p", { cls: "note", text: "Cost: " + cost + ". Duplicates folded: " + (s.duplicates || 0) + ". Capped: " + (s.capped || 0) + "." }),
      ]));
    });
  }

  function series(agent) {
    var byDay = {};
    (data.events || []).forEach(function (e) {
      if (e.agent !== agent || e.credited == null || e.status !== "verified") return;
      var d = day(e.occurred_at), k = d + "|" + e.rule_version;
      byDay[k] = byDay[k] || { day: d, rule: e.rule_version, pos: 0, neg: 0 };
      if (e.credited > 0) byDay[k].pos += e.credited; else byDay[k].neg += e.credited;
    });
    return Object.keys(byDay).map(function (k) { return byDay[k]; }).sort(function (a, b) { return a.day < b.day ? -1 : 1; });
  }

  function renderCharts() {
    var host = clear($("charts")), table = clear($("charttable"));
    var all = AG.map(series), days = {};
    all.forEach(function (s) { s.forEach(function (p) { days[p.day] = 1; }); });
    var dl = Object.keys(days).sort();
    table.appendChild(el("tr", null, ["Date", "Agent", "Rules", "Rewards", "Penalties"].map(function (h) { return el("th", { text: h }); })));
    if (!dl.length) { host.appendChild(empty("No verified points yet, so there is nothing to chart. That is not a result.")); return; }
    var ruleChange = [];
    (data.mode_history || []).forEach(function (h, i, arr) { if (i && h.rule_version !== arr[i - 1].rule_version) ruleChange.push({ day: day(h.at), rule: h.rule_version }); });
    var max = 0.2;
    all.forEach(function (s) { s.forEach(function (p) { max = Math.max(max, p.pos, -p.neg); }); });
    AG.forEach(function (a, ai) {
      var W = 480, H = 180, L = 30, R = 8, T = 14, B = 22, mid = T + (H - T - B) / 2, half = (H - T - B) / 2;
      var bw = Math.max(4, Math.min(22, (W - L - R) / dl.length - 6));
      var x = function (d) { return L + (dl.indexOf(d) + 0.5) * (W - L - R) / dl.length; };
      var NS = "http://www.w3.org/2000/svg", svg = document.createElementNS(NS, "svg");
      svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.setAttribute("role", "img");
      svg.setAttribute("aria-label", NAME[a] + ": verified points per day, rewards up and penalties down");
      function s(tag, at) { var n = document.createElementNS(NS, tag); for (var k in at) n.setAttribute(k, at[k]); svg.appendChild(n); return n; }
      s("line", { x1: L, x2: W - R, y1: mid, y2: mid, "class": "zero" });
      [[max, mid - half], [-max, mid + half]].forEach(function (t) { var tx = s("text", { x: L - 4, y: t[1] + 4, "text-anchor": "end", "class": "tick" }); tx.textContent = (t[0] > 0 ? "+" : "") + num(t[0]); });
      [dl[0], dl[dl.length - 1]].forEach(function (d, i) { var tx = s("text", { x: x(d), y: H - 6, "text-anchor": i ? "end" : "start", "class": "tick" }); tx.textContent = d.slice(5); });
      ruleChange.forEach(function (r) {
        var near = dl.filter(function (d) { return d >= r.day; })[0]; if (!near) return;
        var xx = x(near) - (W - L - R) / dl.length / 2;
        s("line", { x1: xx, x2: xx, y1: T - 4, y2: H - B, "class": "rule" });
        var tx = s("text", { x: xx + 3, y: T + 4, "class": "rlab" }); tx.textContent = "rules " + r.rule;
      });
      var tip = el("div", { cls: "tip" });
      all[ai].forEach(function (p) {
        var cx = x(p.day);
        if (p.pos > 0) s("rect", { x: cx - bw / 2, y: mid - p.pos / max * half, width: bw, height: Math.max(1, p.pos / max * half - 1), rx: 3, fill: "var(--" + (a === "agent1" ? "a1" : "a2") + ")" });
        if (p.neg < 0) s("rect", { x: cx - bw / 2, y: mid + 1, width: bw, height: Math.max(1, -p.neg / max * half), rx: 3, fill: "var(--neg)" });
        var hit = s("rect", { x: cx - (W - L - R) / dl.length / 2, y: T, width: (W - L - R) / dl.length, height: H - T - B, "class": "hit" });
        hit.addEventListener("mousemove", function (ev) {
          tip.textContent = p.day + " · rules " + p.rule + " · +" + num(p.pos) + " / " + num(p.neg);
          var r = host.children[ai].getBoundingClientRect(); tip.style.display = "block";
          tip.style.left = Math.min(ev.clientX - r.left + 10, r.width - 190) + "px"; tip.style.top = (ev.clientY - r.top - 30) + "px";
        });
        hit.addEventListener("mouseleave", function () { tip.style.display = "none"; });
        table.appendChild(el("tr", null, [p.day, NAME[a], p.rule, "+" + num(p.pos), num(p.neg)].map(function (t) { return el("td", { text: t }); })));
      });
      host.appendChild(el("div", { cls: "chart" }, [el("h3", { text: NAME[a] + (all[ai].length ? "" : " · no verified points") }), svg, tip]));
    });
  }

  function renderFilters() {
    var f = clear($("filters")), ev = data.events || [];
    function uniq(k) { var o = {}; ev.forEach(function (e) { if (e[k] != null) o[e[k]] = 1; }); return Object.keys(o).sort(); }
    function sel(key, label, opts) {
      var s = el("select", { "aria-label": label });
      s.appendChild(el("option", { value: "", text: label + ": all" }));
      opts.forEach(function (o) { s.appendChild(el("option", { value: o, text: NAME[o] || o })); });
      s.value = filt[key]; s.addEventListener("change", function () { filt[key] = s.value; renderEvents(); });
      f.appendChild(s);
    }
    sel("agent", "Agent", AG); sel("task", "Task", uniq("task")); sel("category", "Category", uniq("category"));
    sel("status", "Status", uniq("status")); sel("rule", "Rules", uniq("rule_version"));
    ["from", "to"].forEach(function (k) {
      var i = el("input", { type: "date", "aria-label": k === "from" ? "From date" : "To date" });
      i.value = filt[k]; i.addEventListener("change", function () { filt[k] = i.value; renderEvents(); }); f.appendChild(i);
    });
  }

  function renderEvents() {
    var tb = clear($("events")), ev = data.events || [];
    var shown = ev.filter(function (e) {
      var d = day(e.occurred_at);
      return (!filt.agent || e.agent === filt.agent) && (!filt.task || e.task === filt.task) && (!filt.category || e.category === filt.category)
        && (!filt.status || e.status === filt.status) && (!filt.rule || e.rule_version === filt.rule) && (!filt.from || d >= filt.from) && (!filt.to || d <= filt.to);
    });
    $("evcount").textContent = ev.length ? shown.length + " of " + ev.length + " events shown. Select a row for its sources, verifier and correction history." : "";
    if (!ev.length) { tb.appendChild(el("tr", null, [el("td", { colspan: "6", cls: "empty", text: "No feedback events recorded yet. An empty list means no data, not success." })])); return; }
    shown.forEach(function (e) {
      var k = kind(e);
      var val = e.status === "retracted" ? "0 (withdrawn)" : e.value == null ? "pending" : (e.value > 0 ? "+" : "") + num(e.value) + (e.credited != null && e.credited !== e.value ? " (credited " + num(e.credited) + ")" : "");
      var tr = el("tr", { cls: "row", tabindex: "0", "aria-expanded": "false" }, [
        el("td", { text: day(e.occurred_at) }), el("td", null, [el("span", { cls: "kind " + k, text: k })]), el("td", { text: NAME[e.agent] || e.agent }),
        el("td", { cls: "hide-sm", text: e.task }), el("td", { text: val }), el("td", { text: e.reason })]);
      var det = null;
      function toggle() {
        if (det) { det.remove(); det = null; tr.setAttribute("aria-expanded", "false"); return; }
        var refs = el("ul"); (e.refs || []).forEach(function (r) { refs.appendChild(el("li", null, [link(r)])); });
        if (!(e.refs || []).length) refs.appendChild(el("li", { text: "No public source link." }));
        var hist = el("ul"); (e.history || []).forEach(function (h) { hist.appendChild(el("li", { text: h.id + ": " + h.status + ", value " + num(h.value) + ", " + day(h.at) })); });
        if (!(e.history || []).length) hist.appendChild(el("li", { text: "No earlier versions." }));
        det = el("tr", { cls: "detail" }, [el("td", { colspan: "6" }, [
          el("div", { text: "Category " + e.category + " · rules " + e.rule_version + " · proposed by " + (NAME[e.proposer] || e.proposer || "—") + " · verified by " + (NAME[e.verifier] || e.verifier || "nobody yet") + (e.verified_at ? " on " + day(e.verified_at) : "") }),
          el("div", { text: "Sources:" }), refs, el("div", { text: "Correction history:" }), hist,
          (e.memory_ids || []).length ? el("div", { text: "Memories recalled: " + e.memory_ids.join(", ") }) : null])]);
        tr.after(det); tr.setAttribute("aria-expanded", "true");
      }
      tr.addEventListener("click", toggle);
      tr.addEventListener("keydown", function (x) { if (x.key === "Enter" || x.key === " ") { x.preventDefault(); toggle(); } });
      tb.appendChild(tr);
    });
  }

  function kv(rows) { return el("div", { cls: "kv" }, rows.reduce(function (a, r) { return a.concat([el("span", { text: r[0] }), el("b", { text: String(r[1]) })]); }, [])); }

  function renderMemory() {
    var m = clear($("memory")), mm = data.memories;
    if (!mm) { m.appendChild(empty("No memory data.")); return; }
    var p = mm.public || {};
    m.appendChild(el("div", { cls: "box" }, [el("h3", { text: "Shared public lessons" }), kv([["active", p.active || 0], ["provisional", p.provisional || 0], ["superseded", p.superseded || 0], ["retracted", p.retracted || 0], ["historical seed (no points)", mm.historical_seed || 0], ["recalls before decisions", mm.retrievals || 0], ["corrections", mm.corrections || 0]])]));
    var recent = el("div", { cls: "box" }, [el("h3", { text: "Recent checked applications" })]);
    if (!(mm.recent_applications || []).length) recent.appendChild(empty("None yet."));
    (mm.recent_applications || []).forEach(function (r) { recent.appendChild(el("p", { text: day(r.at) + " · " + (NAME[r.agent] || r.agent) + " · " + r.decision_id + " used " + r.memory_ids.join(", ") })); });
    recent.appendChild(el("p", { cls: "note", text: "Private memory: " + (mm.private && mm.private.available ? "aggregates only." : "not reported. " + ((mm.private && mm.private.note) || "")) }));
    m.appendChild(recent);
  }

  function renderShadow() {
    var s = clear($("shadow")), sh = data.shadow;
    if (!sh) { s.appendChild(empty("No decisions recorded yet.")); return; }
    s.appendChild(el("div", { cls: "box" }, [kv([["decisions with a recall", sh.decisions], ["where Q would have recalled differently", sh.differences], ["decisions with a later evaluation", sh.evaluated]]),
      el("p", { cls: "note", text: sh.note || "" })]));
  }

  function renderReady() {
    var r = clear($("ready")), rd = data.readiness;
    if (!rd) { r.appendChild(empty("Readiness cannot be assessed without data.")); return; }
    var t = el("table", { cls: "crit" }, [el("tr", null, ["Criterion", "Needed", "Observed", "Met"].map(function (h) { return el("th", { text: h }); }))]);
    rd.criteria.forEach(function (c) {
      var obs = c.observed == null ? "not measured" : typeof c.observed === "object" ? AG.map(function (a) { return NAME[a] + " " + c.observed[a]; }).join(", ") : String(c.observed);
      var met = c.met === true ? ["y", "yes"] : c.met === false ? ["n", "no"] : ["u", "unknown"];
      var need = c.id === "cost" ? "at most +" + Math.round(c.threshold * 100) + "%" : c.id === "safety" ? "none" : c.id === "rollback" ? "required" : "at least " + c.threshold;
      t.appendChild(el("tr", null, [el("td", { text: c.label }), el("td", { text: need }), el("td", { text: obs }), el("td", null, [el("span", { cls: "met " + met[0], text: met[1] })])]));
    });
    r.appendChild(t);
    var as = el("p", { cls: "note" });
    as.textContent = "Assessments: " + AG.map(function (a) { var x = rd.assessments[a] || {}; return NAME[a] + " " + (x.decision == null ? "not written yet" : x.decision + " (" + day(x.written_at) + ")"); }).join("; ") + ". " + (rd.note || "");
    r.appendChild(as);
  }

  function renderMap() {
    var m = clear($("maplinks")), ml = data.map_links || [];
    if (!ml.length) { m.appendChild(empty("No lesson is linked to a Decision map node yet.")); return; }
    var ul = el("ul");
    ml.forEach(function (x) { var li = el("li", { text: x.memory_id + " → " }); x.map_node_ids.forEach(function (n, i) { if (i) li.appendChild(document.createTextNode(", ")); li.appendChild(el("a", { href: "map.html#" + encodeURIComponent(n), text: n })); }); ul.appendChild(li); });
    m.appendChild(ul);
  }

  function render() {
    renderFresh(); renderMode(); renderCards(); renderCharts(); renderFilters(); renderEvents(); renderMemory(); renderShadow(); renderReady(); renderMap();
  }

  function load(demo) {
    document.body.classList.toggle("is-demo", demo);
    var b = $("demo"); b.setAttribute("aria-pressed", String(demo)); b.textContent = demo ? "Back to real data" : "Show DEMO data";
    fetch(demo ? "memory-demo.json" : "memory-export.json", { cache: "no-store" }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        if (!demo && d.demo) throw new Error("demo data in the production export");
        data = d; filt = { agent: "", task: "", category: "", status: "", rule: "", from: "", to: "" }; render();
      })
      .catch(function () { data = { data_status: "unavailable", generated_at: new Date().toISOString(), reason: "The export could not be loaded." }; render(); });
  }

  $("demo").addEventListener("click", function () { var on = !document.body.classList.contains("is-demo"); history.replaceState(null, "", on ? "?demo=1" : location.pathname); load(on); });
  load(/[?&]demo=1\b/.test(location.search));
})();
