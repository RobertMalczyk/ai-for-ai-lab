// Switch between the two perspectives without leaving the page.
(function () {
  var root = document.documentElement;
  function set(view, hash) {
    root.dataset.view = view;
    try { localStorage.setItem("lab-view", view); } catch (e) {}
    try {
      var url = new URL(location.href);
      url.searchParams.set("view", view);
      url.hash = hash || "";
      history.replaceState(null, "", url);
    } catch (e) {}
    document.querySelectorAll("[data-set]").forEach(function (a) {
      if (a.closest(".persp, .bigswitch")) a.setAttribute("aria-current", a.dataset.set === view ? "true" : "false");
    });
    var target = hash && document.getElementById(hash.slice(1));
    (target || document.body).scrollIntoView({ block: "start" });
    if (!target) window.scrollTo(0, 0);
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("[data-set]");
    if (!a) return;
    ev.preventDefault();
    var hash = (a.getAttribute("href").split("#")[1] || "");
    set(a.dataset.set, hash ? "#" + hash : "");
  });
  document.querySelectorAll(".persp [data-set], .bigswitch [data-set]").forEach(function (a) {
    a.setAttribute("aria-current", a.dataset.set === root.dataset.view ? "true" : "false");
  });
})();
