// Tectori's contact page script submits the form over fetch so a visitor stays on the page, and falls back to the plain POST if JavaScript is unavailable.
(() => {
  "use strict";

  const form = document.querySelector("#contact-form");
  if (!form) return;

  const submitButton = form.querySelector('button[type="submit"]');
  let idleLabel = null;
  const successRegion = document.querySelector("#contact-form-success");
  const errorRegion = document.querySelector("#contact-form-error");
  const errorText = document.querySelector("#contact-form-error-text");

  let submitting = false;
  const SENDING_LABEL = "Sending…";
  const GENERIC_ERROR =
    "Something went wrong sending your message. Please try again.";

  function hideErrorRegion() {
    if (!errorRegion) return;
    errorRegion.hidden = true;
  }

  function showErrorRegion(message) {
    if (!errorRegion) return;
    if (errorText) errorText.textContent = message;
    errorRegion.hidden = false;
    errorRegion.focus();
  }

  function showSuccess() {
    form.hidden = true;
    if (!successRegion) return;
    successRegion.hidden = false;
    successRegion.focus();
  }

  // A non-ok status, a non-JSON body, a body that parses but carries no usable
  // message, and a network failure are all the same case from here: Formspree
  // may have reCAPTCHA enabled on this form, which nobody outside its own
  // dashboard can confirm, and a fetch sending Accept: application/json is not
  // guaranteed a well-formed JSON response if a challenge is in the way. None
  // of those cases may look like success.
  async function readErrorMessage(response) {
    try {
      const body = await response.json();
      if (Array.isArray(body.errors) && body.errors.length) {
        const messages = body.errors
          .map((entry) => entry && entry.message)
          .filter(Boolean);
        if (messages.length) return messages.join(" ");
      }
      if (typeof body.error === "string" && body.error) return body.error;
    } catch (_error) {
      // Body was not JSON, or was empty; fall through to the generic message.
    }
    return GENERIC_ERROR;
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    // The submitting flag, not the button's state, is what stops a second
    // send: a return keypress in a field can fire submit again before the
    // browser settles a disabled button, and Formspree would record the
    // message twice.
    if (submitting) return;
    submitting = true;
    hideErrorRegion();
    // aria-disabled rather than disabled. The visitor just activated this
    // button, so it holds focus; disabling it drops focus to the document
    // with nothing announced, and the label never changes, so a screen
    // reader user gets silence for as long as Formspree takes to answer.
    // Changing the label inside the button reports the state instead.
    if (submitButton) {
      submitButton.setAttribute("aria-disabled", "true");
      idleLabel = submitButton.textContent;
      submitButton.textContent = SENDING_LABEL;
    }

    const data = new FormData(form);
    fetch(form.action, {
      method: "POST",
      body: data,
      headers: { Accept: "application/json" },
    })
      .then((response) => {
        if (response.ok) {
          showSuccess();
          return;
        }
        return readErrorMessage(response).then(showErrorRegion);
      })
      .catch(() => {
        showErrorRegion(GENERIC_ERROR);
      })
      .finally(() => {
        submitting = false;
        if (submitButton) {
          submitButton.removeAttribute("aria-disabled");
          if (idleLabel !== null) submitButton.textContent = idleLabel;
        }
      });
  });
})();
