// Closes the mobile navigation menu on Escape, on a click outside it, or when keyboard focus leaves it.
(() => {
  "use strict";

  const menu = document.querySelector("details.nav-menu");
  if (!menu) return;

  const close = () => { menu.open = false; };

  menu.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !menu.open) return;
    close();
    menu.querySelector("summary").focus();
  });

  menu.addEventListener("focusout", (event) => {
    if (event.relatedTarget && !menu.contains(event.relatedTarget)) close();
  });

  document.addEventListener("click", (event) => {
    if (!menu.contains(event.target)) close();
  });
})();
