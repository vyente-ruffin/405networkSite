(() => {
  'use strict';
  const form = document.getElementById('contact-form');
  if (!form) return;
  // Delivery has not been configured. Do not transmit or store a visitor's
  // message, expose a recipient, or claim that a message was sent.
  // Keep the disabled HTML button as the no-JavaScript safeguard as well.
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    document.getElementById('contact-status').textContent =
      'Sending isn’t connected yet. Nothing has been sent or saved. Please use our existing inquiry form for now.';
  });
})();
