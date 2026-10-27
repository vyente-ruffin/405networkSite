(() => {
  'use strict';
  const form = document.getElementById('contact-form');
  if (!form) return;
  const button = form.querySelector('button[type="submit"]');
  const status = document.getElementById('contact-status');
  const notice = 'Messages are processed by FormSubmit. Complete the spam check when prompted.';

  // Leave normal browser submission intact, including when JavaScript is off.
  form.addEventListener('submit', () => {
    button.disabled = true;
    status.textContent = 'Opening secure spam verification…';
  });
  window.addEventListener('pageshow', () => {
    button.disabled = false;
    status.textContent = notice;
  });
})();
