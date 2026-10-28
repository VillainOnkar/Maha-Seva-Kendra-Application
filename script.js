let LINKS = {};

document.addEventListener("DOMContentLoaded", () => {

  fetch("links.json")
    .then(res => res.json())
    .then(data => {
      LINKS = data;
      console.log("Links loaded");
    });

  document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("click", () => {
      const key = card.dataset.key;
      const url = LINKS[key];

      if (!url) {
      const bar = document.getElementById("link-error");

      bar.classList.add("show");
      bar.style.animation = "topShake 0.4s ease";

      setTimeout(() => {
        bar.classList.remove("show");
      }, 3000);

      return;
    }


      if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.open_site(url);
      } else {
        // fallback (sirf testing ke liye)
        window.location.href = url;
      }
    });
  });

});
