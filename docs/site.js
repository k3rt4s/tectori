// Tectori's public site script handles the client login locally without transmitting or storing form entries.
(() => {
  "use strict";

  const form = document.querySelector("#login-form");
  if (!form) return;

  const username = form.querySelector("#username");
  const password = form.querySelector("#password");
  const message = form.querySelector("#login-message");

  username.addEventListener("input", () => {
    const { selectionStart, selectionEnd } = username;
    username.value = username.value.toLowerCase();
    username.setSelectionRange(selectionStart, selectionEnd);
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    username.value = "";
    password.value = "";
    message.textContent = "Logon failed. Invalid username or password.";
    message.hidden = false;
    username.focus();
  });
})();
