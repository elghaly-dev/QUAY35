(function () {
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]");
    if (!b) return;
    var text = b.getAttribute("data-copy");
    if (navigator.clipboard && text) {
      navigator.clipboard.writeText(text);
    }
    var lab = b.getAttribute("data-label");
    if (lab) {
      b.textContent = b.getAttribute("data-copied-label") || "Copied";
      setTimeout(function () {
        b.textContent = lab;
      }, 900);
    }
  });

  function openWallets() {
    if (location.hash !== "#wallets") return;
    var d = document.getElementById("wallets");
    if (d) d.open = true;
  }
  window.addEventListener("hashchange", openWallets);
  openWallets();
})();
