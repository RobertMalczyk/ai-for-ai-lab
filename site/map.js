// Decision Map: draws site/decision-map.json as a Git-like graph (time left to right, one band per workstream).
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var GH = document.body.dataset.github;
  var COL = 124, ROW = 62, PAD = 30, TOP = 34;
  var STATUS = {
    active: ["Active", "▶"], waiting: ["Waiting on an outside party", "◷"], resolved: ["Done / resolved", "✓"],
    rejected: ["Rejected", "✕"], blocked: ["Blocked", "!"], parked: ["Parked", "‖"], superseded: ["Superseded", "↷"]
  };
  var TYPES = {
    decision: "Decision", owner_decision: "Owner decision", action: "Action", review: "Review", correction: "Correction",
    external_event: "Outside event", submission: "Submission", rejection: "Rejection", blocker: "Blocker", state_change: "State change"
  };
  var ACTORS = { owner: "Owner", agent1: "Agent 1", agent2: "Agent 2", both_agents: "Both agents", maintainer: "Outside maintainers", system: "System" };
  var TRACKS = [["transparency", "Transparency"], ["site", "Publishing / site"], ["lab", "Lab infrastructure"], ["usefulness", "Usefulness"],
    ["external", "External OSS"], ["pytest", "pytest"], ["distutils", "distutils"], ["discovery", "Discovery"]];
  var TRACK_NAME = {}; TRACKS.forEach(function (t) { TRACK_NAME[t[0]] = t[1]; });
  var FIX = { corrected_by: 1, superseded_by: 1, reopened_by: 1 }, NEG = { rejected_because: 1, blocked_by: 1 };
  var LATER = { superseded_by: "Superseded by", corrected_by: "Corrected by", reopened_by: "Reopened by", blocked_by: "Stopped by", rejected_because: "Rejected because of" };
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  var data, byId = {}, order = {}, out = {}, inc = {};
  var st = { mode: "milestones", q: "", sel: null, expanded: {}, f: { status: {}, actor: {}, track: {} } };
  var view = { k: 1, x: 0, y: 0 }, laid = null, nodeEls = {};
  var svg = document.getElementById("svg"), vp = document.getElementById("vp"), lanes = document.getElementById("lanes");
  var box = document.getElementById("map"), drawer = document.getElementById("drawer");

  function el(name, attrs, parent) {
    var e = document.createElementNS(NS, name);
    for (var a in attrs) e.setAttribute(a, attrs[a]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function h(tag, attrs, text) {
    var e = document.createElement(tag);
    for (var a in attrs || {}) e.setAttribute(a, attrs[a]);
    if (text != null) e.textContent = text;
    return e;
  }
  function fmtDate(d) { return +d.slice(8, 10) + " " + MONTHS[+d.slice(5, 7) - 1]; }

  // ---- visibility -------------------------------------------------------
  function inMode(n) {
    if (st.mode === "all") return true;
    if (n.milestone) return true;
    return !!(n.parent && st.expanded[n.parent]);
  }
  function passes(n) {
    return !st.f.status[n.status] && !st.f.actor[n.actor] && !st.f.track[n.track];
  }
  function matches(n) {
    if (!st.q) return true;
    var q = st.q.toLowerCase();
    return (n.id + " " + n.title + " " + n.short + " " + n.decision_ids.join(" ") + " " + (n.external_url || "")).toLowerCase().indexOf(q) >= 0;
  }

  // ---- layout -----------------------------------------------------------
  function layout() {
    var vis = data.nodes.filter(function (n) { return inMode(n) && passes(n); });
    vis.sort(function (a, b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : order[a.id] - order[b.id]; });
    var col = -1, prevStack = null, stackRow = {}, pos = {}, rows = {}, dates = [];
    vis.forEach(function (n) {
      if (!(n.stack && n.stack === prevStack)) {
        col++;
        if (!dates.length || dates[dates.length - 1].date !== n.date) dates.push({ date: n.date, col: col });
      }
      prevStack = n.stack || null;
      var row = n.row || 0;
      if (n.stack) { stackRow[n.stack] = (stackRow[n.stack] || 0); row += stackRow[n.stack]++; }
      pos[n.id] = { col: col, row: row };
      rows[n.track] = Math.max(rows[n.track] || 0, row + 1);
    });
    var y = TOP, band = {};
    TRACKS.forEach(function (t) {
      if (!rows[t[0]]) return;
      var hgt = rows[t[0]] * ROW + PAD;
      band[t[0]] = { y: y, h: hgt };
      y += hgt;
    });
    vis.forEach(function (n) {
      var p = pos[n.id], b = band[n.track];
      p.x = p.col * COL + COL / 2 + 150;
      p.y = b.y + PAD / 2 + p.row * ROW + ROW / 2 - 6;
    });
    var visSet = {}; vis.forEach(function (n) { visSet[n.id] = 1; });
    return { vis: vis, pos: pos, band: band, dates: dates, width: (col + 1) * COL + 190, height: y + 10, edges: visibleEdges(visSet) };
  }

  // Direct edges between visible nodes, plus dotted shortcuts through hidden ones so the story stays connected.
  function visibleEdges(V) {
    var res = [], seen = {};
    Object.keys(V).forEach(function (s) {
      (out[s] || []).forEach(function (e) {
        if (V[e.target]) { seen[s + ">" + e.target] = 1; res.push({ s: s, t: e.target, e: e }); }
      });
    });
    Object.keys(V).forEach(function (s) {
      var stack = (out[s] || []).filter(function (e) { return !V[e.target]; }).map(function (e) { return [e.target, 1]; });
      var visited = {};
      while (stack.length) {
        var cur = stack.pop(), id = cur[0];
        if (visited[id] || cur[1] > 12) continue;
        visited[id] = 1;
        (out[id] || []).forEach(function (e) {
          if (V[e.target]) {
            var key = s + ">" + e.target;
            if (!seen[key]) { seen[key] = 1; res.push({ s: s, t: e.target, e: null, hops: cur[1] }); }
          } else stack.push([e.target, cur[1] + 1]);
        });
      }
    });
    return res;
  }

  // ---- drawing ----------------------------------------------------------
  function edgeClass(x) {
    if (!x.e) return "edge ind";
    var r = x.e.relation;
    var neg = NEG[r] || (r === "branched_to" && byId[x.e.target].status === "rejected");
    return "edge" + (FIX[r] ? " fix" : neg ? " neg" : r === "followed_by" ? " seq" : "");
  }
  function pathFor(a, b) {
    if (Math.abs(a.y - b.y) < 1) return "M" + a.x + " " + a.y + "L" + b.x + " " + b.y;
    var dx = Math.max(Math.abs(b.x - a.x) / 2, 30);
    return "M" + a.x + " " + a.y + "C" + (a.x + dx) + " " + a.y + " " + (b.x - dx) + " " + b.y + " " + b.x + " " + b.y;
  }
  function wrap(text, max) {
    var words = text.split(" "), lines = [""];
    words.forEach(function (w) {
      var cur = lines[lines.length - 1];
      if ((cur + " " + w).trim().length > max && cur) lines.push(w); else lines[lines.length - 1] = (cur + " " + w).trim();
    });
    if (lines.length > 2) lines = [lines[0], lines.slice(1).join(" ").slice(0, max - 1) + "…"];
    return lines;
  }

  function draw() {
    laid = layout();
    vp.textContent = "";
    lanes.textContent = "";
    nodeEls = {};
    var defs = el("defs", {}, vp);
    [["a", "var(--mute)"], ["f", "var(--st-active)"], ["n", "var(--st-rej)"]].forEach(function (m) {
      var mk = el("marker", { id: "ar-" + m[0], viewBox: "0 0 10 10", refX: "9", refY: "5", markerWidth: "7", markerHeight: "7", orient: "auto-start-reverse" }, defs);
      el("path", { d: "M0 1L9 5L0 9z", fill: m[1] }, mk);
    });
    Object.keys(laid.band).forEach(function (t, i) {
      var b = laid.band[t];
      if (i % 2 === 0) el("rect", { class: "band", x: -20000, y: b.y, width: laid.width + 40000, height: b.h }, vp);
      var d = h("div", {}, TRACK_NAME[t]); d.dataset.y = b.y + b.h / 2; lanes.appendChild(d);
    });
    laid.dates.forEach(function (d) {
      var x = d.col * COL + 150 + 4;
      el("line", { class: "dateline", x1: x, x2: x, y1: 18, y2: laid.height }, vp);
      el("text", { class: "datelab", x: x + 4, y: 22 }, vp).textContent = fmtDate(d.date);
    });
    var eg = el("g", {}, vp), lg = el("g", {}, vp);
    laid.edges.forEach(function (x) {
      var a = laid.pos[x.s], b = laid.pos[x.t];
      var cls = edgeClass(x), mk = cls.indexOf("fix") > 0 ? "f" : cls.indexOf("neg") > 0 ? "n" : "a";
      var p = el("path", { class: cls, d: pathFor({ x: a.x + 14, y: a.y }, { x: b.x - 16, y: b.y }), "marker-end": "url(#ar-" + mk + ")" }, eg);
      el("title", {}, p).textContent = byId[x.s].short + " → " + (x.e ? x.e.label : "via " + x.hops + " hidden step" + (x.hops > 1 ? "s" : "")) + " → " + byId[x.t].short;
      x.el = p; x.mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
    });
    var ng = el("g", {}, vp);
    laid.vis.forEach(function (n) {
      var p = laid.pos[n.id];
      var g = el("g", { class: "node s-" + n.status + " a-" + n.actor + " t-" + n.type, transform: "translate(" + p.x + " " + p.y + ")", tabindex: "0", role: "button",
        "aria-label": n.title + ". " + fmtDate(n.date) + ". " + STATUS[n.status][0] + ". " + ACTORS[n.actor] + "." }, ng);
      el("title", {}, g).textContent = n.title + "\n" + n.summary;
      el("circle", { class: "ring", r: 19 }, g);
      if (n.actor === "owner") el("rect", { class: "shape", x: -11, y: -11, width: 22, height: 22, rx: 3, transform: "rotate(45)" }, g);
      else if (n.type === "external_event" || n.type === "blocker" || n.type === "submission") el("rect", { class: "shape", x: -12, y: -12, width: 24, height: 24, rx: 5 }, g);
      else el("circle", { class: "shape", r: 12 }, g);
      el("text", { class: "g", y: 0.5 }, g).textContent = STATUS[n.status][1];
      wrap(n.short, 17).forEach(function (line, i) { el("text", { class: "lab", y: 32 + i * 14 }, g).textContent = line; });
      if (n.children && st.mode === "milestones") {
        var open = !!st.expanded[n.id];
        el("rect", { class: "morebg", x: 12, y: -26, width: 30, height: 16, rx: 8 }, g);
        el("text", { class: "more", x: 27, y: -14, "text-anchor": "middle" }, g).textContent = open ? "−" : "+" + n.children.length;
      }
      g.addEventListener("click", function (ev) { ev.stopPropagation(); select(n.id, true); });
      g.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); select(n.id, true); }
        if (ev.key === "ArrowRight" || ev.key === "ArrowLeft") { ev.preventDefault(); step(n.id, ev.key === "ArrowRight" ? 1 : -1); }
      });
      g.addEventListener("focus", function () { ensureVisible(n.id); });
      nodeEls[n.id] = g;
    });
    lg.id = "elabs";
    decorate();
    renderList();
    var total = data.nodes.length, ms = data.nodes.filter(function (n) { return n.milestone; }).length;
    document.getElementById("count").textContent = laid.vis.length + " of " + total + " records shown (" + ms + " milestones), " +
      laid.edges.length + " links shown of " + data.edges.length + ".";
    apply();
  }

  function decorate() {
    var lg = document.getElementById("elabs");
    if (!lg) return;
    lg.textContent = "";
    var anyQ = !!st.q;
    laid.vis.forEach(function (n) {
      var g = nodeEls[n.id];
      g.classList.toggle("sel", n.id === st.sel);
      g.classList.toggle("dim", anyQ && !matches(n));
    });
    laid.edges.forEach(function (x) {
      var hot = st.sel && (x.s === st.sel || x.t === st.sel);
      x.el.classList.toggle("hot", !!hot);
      x.el.classList.toggle("dim", anyQ || (st.sel && !hot) ? !hot && (anyQ || !!st.sel) : false);
      if (hot) el("text", { class: "elab", x: x.mid.x, y: x.mid.y - 5, "text-anchor": "middle" }, lg).textContent =
        x.e ? x.e.label : "via hidden steps";
    });
  }

  // ---- pan / zoom -------------------------------------------------------
  function apply() {
    vp.setAttribute("transform", "translate(" + view.x + " " + view.y + ") scale(" + view.k + ")");
    Array.prototype.forEach.call(lanes.children, function (d) { d.style.top = (+d.dataset.y * view.k + view.y) + "px"; });
  }
  function zoomAt(f, cx, cy) {
    var k = Math.min(2.5, Math.max(0.15, view.k * f));
    view.x = cx - (cx - view.x) * (k / view.k);
    view.y = cy - (cy - view.y) * (k / view.k);
    view.k = k;
    apply();
  }
  function fit(initial) {
    var w = box.clientWidth, hh = box.clientHeight;
    var k = Math.min(w / laid.width, hh / laid.height, 1.2);
    if (initial && k < 0.55) {
      k = Math.max(Math.min(hh / laid.height, 1), 0.45);
      view.k = k; view.x = 0; view.y = (hh - laid.height * k) / 2;
    } else {
      view.k = k; view.x = (w - laid.width * k) / 2; view.y = (hh - laid.height * k) / 2;
    }
    apply();
  }
  function ensureVisible(id) {
    var p = laid.pos[id];
    if (!p) return;
    var w = box.clientWidth, hh = box.clientHeight, sx = p.x * view.k + view.x, sy = p.y * view.k + view.y;
    var right = drawer.classList.contains("open") && w > 720 ? Math.min(420, w / 2) : 0;
    var bottom = drawer.classList.contains("open") && w <= 720 ? hh * 0.5 : 0;
    if (sx < 160 || sx > w - right - 60) view.x = (w - right) / 2 - p.x * view.k;
    if (sy < 40 || sy > hh - bottom - 60) view.y = (hh - bottom) / 2 - p.y * view.k;
    apply();
  }
  function step(id, dir) {
    var ids = laid.vis.map(function (n) { return n.id; }), i = ids.indexOf(id) + dir;
    if (i >= 0 && i < ids.length) nodeEls[ids[i]].focus();
  }

  var ptrs = {}, drag = null, pinch = null;
  svg.addEventListener("pointerdown", function (ev) {
    ptrs[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
    var ids = Object.keys(ptrs);
    if (ids.length === 2) {
      var a = ptrs[ids[0]], b = ptrs[ids[1]];
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y) }; drag = null;
    } else if (!ev.target.closest(".node")) {
      drag = { x: ev.clientX, y: ev.clientY, vx: view.x, vy: view.y, moved: false };
      svg.setPointerCapture(ev.pointerId); svg.classList.add("drag");
    }
  });
  svg.addEventListener("pointermove", function (ev) {
    if (!ptrs[ev.pointerId]) return;
    ptrs[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
    var ids = Object.keys(ptrs);
    if (pinch && ids.length === 2) {
      var a = ptrs[ids[0]], b = ptrs[ids[1]], d = Math.hypot(a.x - b.x, a.y - b.y), r = svg.getBoundingClientRect();
      zoomAt(d / pinch.d, (a.x + b.x) / 2 - r.left, (a.y + b.y) / 2 - r.top);
      pinch.d = d;
    } else if (drag) {
      view.x = drag.vx + ev.clientX - drag.x; view.y = drag.vy + ev.clientY - drag.y;
      if (Math.abs(ev.clientX - drag.x) + Math.abs(ev.clientY - drag.y) > 4) drag.moved = true;
      apply();
    }
  });
  function up(ev) {
    delete ptrs[ev.pointerId];
    if (Object.keys(ptrs).length < 2) pinch = null;
    if (drag && !drag.moved && ev.type === "pointerup" && !ev.target.closest(".node")) closeDrawer();
    drag = null; svg.classList.remove("drag");
  }
  svg.addEventListener("pointerup", up);
  svg.addEventListener("pointercancel", up);
  svg.addEventListener("wheel", function (ev) {
    ev.preventDefault();
    var r = svg.getBoundingClientRect();
    if (ev.ctrlKey || Math.abs(ev.deltaY) > Math.abs(ev.deltaX)) zoomAt(Math.exp(-ev.deltaY * 0.0015), ev.clientX - r.left, ev.clientY - r.top);
    else { view.x -= ev.deltaX; apply(); }
  }, { passive: false });
  box.addEventListener("keydown", function (ev) {
    if (ev.target.tagName === "INPUT") return;
    var cx = box.clientWidth / 2, cy = box.clientHeight / 2;
    if (ev.key === "+" || ev.key === "=") zoomAt(1.25, cx, cy);
    else if (ev.key === "-") zoomAt(0.8, cx, cy);
    else if (ev.key === "0") fit();
    else if (ev.target === box && (ev.key === "ArrowRight" || ev.key === "ArrowLeft")) {
      view.x += ev.key === "ArrowRight" ? -120 : 120; apply();
    } else return;
    ev.preventDefault();
  });
  document.getElementById("zin").onclick = function () { zoomAt(1.25, box.clientWidth / 2, box.clientHeight / 2); };
  document.getElementById("zout").onclick = function () { zoomAt(0.8, box.clientWidth / 2, box.clientHeight / 2); };
  document.getElementById("zfit").onclick = function () { fit(); };
  window.addEventListener("resize", function () { apply(); });

  // ---- details drawer ---------------------------------------------------
  function link(href, text) { var a = h("a", { href: href, rel: "noopener" }, text); return a; }
  function nodeButton(id, prefix) {
    var li = h("li", { class: "rel" }), n = byId[id];
    if (prefix) li.appendChild(document.createTextNode(prefix + " "));
    var b = h("button", { type: "button" }, n.title);
    b.onclick = function () { select(id, true); };
    li.appendChild(b);
    li.appendChild(document.createTextNode(" · " + fmtDate(n.date)));
    return li;
  }
  function badge(n) {
    var s = h("span", { class: "badge" });
    var c = h("i", { class: "chip c-" + n.status }, STATUS[n.status][1]);
    s.appendChild(c); s.appendChild(document.createTextNode(STATUS[n.status][0]));
    return s;
  }
  function openDrawer(n) {
    drawer.textContent = "";
    var x = h("button", { type: "button", class: "btn x", "aria-label": "Close details" }, "✕");
    x.onclick = closeDrawer; drawer.appendChild(x);
    drawer.appendChild(h("p", { class: "kicker" }, n.id));
    drawer.appendChild(h("h2", {}, n.title));
    (out[n.id] || []).filter(function (e) { return LATER[e.relation]; }).forEach(function (e) {
      var bn = h("div", { class: "banner" + (NEG[e.relation] ? " neg" : "") });
      bn.appendChild(document.createTextNode("Later: " + LATER[e.relation].toLowerCase() + " "));
      var b = h("button", { type: "button", class: "rel" }, byId[e.target].title);
      b.style.cssText = "background:none;border:0;padding:0;color:inherit;font:inherit;text-decoration:underline;cursor:pointer";
      b.onclick = function () { select(e.target, true); };
      bn.appendChild(b); bn.appendChild(document.createTextNode(" (" + e.label + ")."));
      drawer.appendChild(bn);
    });
    var dl = h("dl");
    function row(k, v) { dl.appendChild(h("dt", {}, k)); var dd = h("dd"); if (typeof v === "string") dd.textContent = v; else dd.appendChild(v); dl.appendChild(dd); }
    row("Date", fmtDate(n.date) + " " + n.date.slice(0, 4));
    row("Type", TYPES[n.type]);
    row("Actor", ACTORS[n.actor]);
    row("Status", badge(n));
    row("Workstream", TRACK_NAME[n.track]);
    if (n.decision_ids.length) row("Decision", n.decision_ids.join(", "));
    if (n.human_decision) row("Record", "Owner intervention, " + n.human_decision.date);
    drawer.appendChild(dl);
    [["Summary", n.summary], ["Why", n.rationale], ["Result", n.result]].forEach(function (s) {
      if (!s[1]) return;
      drawer.appendChild(h("h3", {}, s[0])); drawer.appendChild(h("p", {}, s[1]));
    });
    if (n.children) {
      drawer.appendChild(h("h3", {}, "Candidates in this cluster (" + n.children.length + ")"));
      var kids = h("div", { class: "kids" });
      n.children.forEach(function (id) {
        var b = h("button", { type: "button", class: "btn" }, byId[id].short);
        b.onclick = function () { select(id, true); };
        kids.appendChild(b);
      });
      drawer.appendChild(kids);
      if (st.mode === "milestones") {
        var t = h("button", { type: "button", class: "btn" }, st.expanded[n.id] ? "Collapse on the map" : "Expand on the map");
        t.style.marginTop = "8px";
        t.onclick = function () { st.expanded[n.id] = !st.expanded[n.id]; draw(); openDrawer(n); ensureVisible(n.id); };
        drawer.appendChild(t);
      }
    }
    var before = inc[n.id] || [], after = out[n.id] || [];
    if (before.length || after.length) {
      drawer.appendChild(h("h3", {}, "Before and after"));
      var ul = h("ul");
      before.forEach(function (e) { ul.appendChild(nodeButton(e.source, "← " + e.label + " from")); });
      after.forEach(function (e) { ul.appendChild(nodeButton(e.target, "→ " + e.label + ":")); });
      drawer.appendChild(ul);
    }
    drawer.appendChild(h("h3", {}, "Evidence"));
    var refs = h("ul");
    n.refs.forEach(function (r) { var li = h("li"); li.appendChild(link(GH + "/blob/main/" + r, r)); refs.appendChild(li); });
    drawer.appendChild(refs);
    if (n.external_url) {
      drawer.appendChild(h("h3", {}, "Outside link"));
      var p = h("p"); p.appendChild(link(n.external_url, n.external_url.replace("https://", ""))); drawer.appendChild(p);
    }
    drawer.classList.add("open");
  }
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && drawer.classList.contains("open")) closeDrawer();
  });
  function closeDrawer() {
    drawer.classList.remove("open");
    st.sel = null;
    decorate();
    setHash();
  }
  function select(id, focusDrawer) {
    var n = byId[id];
    if (!n) return;
    if (!inMode(n) || !passes(n)) {
      if (!passes(n)) st.f = { status: {}, actor: {}, track: {} }, syncFilters();
      if (!inMode(n)) setMode("all", true);
      draw();
    }
    st.sel = id;
    decorate();
    openDrawer(n);
    ensureVisible(id);
    setHash();
    if (focusDrawer) drawer.focus({ preventScroll: true });
  }
  function setHash() {
    var parts = [];
    if (st.sel) parts.push("decision=" + st.sel);
    if (st.mode === "all") parts.push("mode=all");
    try { history.replaceState(null, "", parts.length ? "#" + parts.join("&") : location.pathname + location.search); } catch (e) {}
  }

  // ---- controls ---------------------------------------------------------
  function setMode(m, quiet) {
    st.mode = m;
    document.querySelectorAll("[data-mode]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.mode === m ? "true" : "false"); });
    if (!quiet) { draw(); fit(true); setHash(); }
  }
  document.querySelectorAll("[data-mode]").forEach(function (b) { b.onclick = function () { setMode(b.dataset.mode); }; });
  var q = document.getElementById("q");
  q.addEventListener("input", function () { st.q = q.value.trim(); decorate(); });
  q.addEventListener("keydown", function (ev) {
    if (ev.key !== "Enter" || !st.q) return;
    var hit = data.nodes.filter(matches)[0];
    if (hit) select(hit.id, false);
  });
  function buildFilters() {
    var panel = document.getElementById("filters");
    [["status", "Status", Object.keys(STATUS).map(function (k) { return [k, STATUS[k][0]]; })],
     ["actor", "Actor", Object.keys(ACTORS).map(function (k) { return [k, ACTORS[k]]; })],
     ["track", "Workstream", TRACKS]].forEach(function (grp) {
      var fs = h("fieldset"); fs.appendChild(h("legend", {}, grp[1]));
      grp[2].forEach(function (o) {
        if (!data.nodes.some(function (n) { return n[grp[0]] === o[0]; })) return;
        var lab = h("label"), cb = h("input", { type: "checkbox" });
        cb.checked = true; cb.dataset.g = grp[0]; cb.dataset.v = o[0];
        cb.onchange = function () { if (cb.checked) delete st.f[grp[0]][o[0]]; else st.f[grp[0]][o[0]] = 1; draw(); };
        lab.appendChild(cb); lab.appendChild(document.createTextNode(o[1])); fs.appendChild(lab);
      });
      panel.appendChild(fs);
    });
  }
  function syncFilters() {
    document.querySelectorAll("#filters input").forEach(function (cb) { cb.checked = !st.f[cb.dataset.g][cb.dataset.v]; });
  }
  function renderList() {
    var ol = document.getElementById("list");
    ol.textContent = "";
    laid.vis.forEach(function (n) {
      var li = h("li"), b = h("button", { type: "button" }, n.title);
      b.onclick = function () { select(n.id, true); };
      li.appendChild(document.createTextNode(n.date + " · " + STATUS[n.status][0] + " · " + ACTORS[n.actor] + ": "));
      li.appendChild(b);
      ol.appendChild(li);
    });
  }
  function fromHash() {
    var p = {};
    location.hash.slice(1).split("&").forEach(function (kv) { var i = kv.indexOf("="); if (i > 0) p[kv.slice(0, i)] = decodeURIComponent(kv.slice(i + 1)); });
    return p;
  }

  fetch("decision-map.json").then(function (r) { return r.json(); }).then(function (d) {
    data = d;
    d.nodes.forEach(function (n, i) {
      byId[n.id] = n; order[n.id] = i;
    });
    d.nodes.forEach(function (n) { (n.children || []).forEach(function (c) { byId[c].parent = n.id; }); });
    d.edges.forEach(function (e) { (out[e.source] = out[e.source] || []).push(e); (inc[e.target] = inc[e.target] || []).push(e); });
    buildFilters();
    var hp = fromHash();
    if (hp.mode === "all") setMode("all", true);
    draw();
    fit(true);
    if (hp.decision && byId[hp.decision]) select(hp.decision, false);
    window.addEventListener("hashchange", function () { var p = fromHash(); if (p.decision && p.decision !== st.sel && byId[p.decision]) select(p.decision, false); });
  }).catch(function () {
    box.appendChild(h("p", { class: "wrap" }, "The map data could not be loaded. The records are in decision-map.json."));
  });
})();
