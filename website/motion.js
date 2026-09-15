(() => {
  'use strict';
  // Parallax itself is native CSS. This only honors a data-saving preference.
  // No section pinning, custom scrolling, timers, storage, or motion controls.
  const connection = navigator.connection;
  function update() {
    document.documentElement.classList.toggle('save-data', !!connection?.saveData);
  }
  connection?.addEventListener?.('change', update);
  update();
})();
