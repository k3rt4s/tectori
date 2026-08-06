// Tectori's public site script handles the local portal preview without transmitting or storing form entries.
(() => {
  "use strict";

  const form = document.querySelector("#login-form");
  if (!form) return;

  const username = form.querySelector("#username");
  const password = form.querySelector("#password");
  const message = form.querySelector("#login-message");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    username.value = "";
    password.value = "";
    message.textContent = "Invalid username and password. Client access is not active yet.";
    message.hidden = false;
    username.focus();
  });
})();
