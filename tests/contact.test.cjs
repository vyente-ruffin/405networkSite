'use strict';
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const vm = require('node:vm');
const test = require('node:test');
const source = readFileSync(join(__dirname, '../website/contact.js'), 'utf8');

function mount(search = '') {
  const formEvents = {}, pageEvents = {};
  const button = { disabled: false };
  const status = { textContent: 'Initial form notice' };
  const form = { querySelector: () => button, addEventListener: (name, callback) => { formEvents[name] = callback; } };
  vm.runInNewContext(source, {
    document: { getElementById: id => id === 'contact-form' ? form : status },
    window: { location: { search }, addEventListener: (name, callback) => { pageEvents[name] = callback; } },
    URLSearchParams,
  });
  return { formEvents, pageEvents, button, status };
}

test('submitting keeps native navigation and prevents an accidental double click', () => {
  const state = mount();
  let prevented = false;
  state.formEvents.submit({ preventDefault: () => { prevented = true; } });
  assert.equal(prevented, false);
  assert.equal(state.button.disabled, true);
  assert.match(state.status.textContent, /verification/i);
});

test('returning with browser Back allows another submission', () => {
  const state = mount();
  state.formEvents.submit({});
  state.pageEvents.pageshow();
  assert.equal(state.button.disabled, false);
  assert.match(state.status.textContent, /FormSubmit/);
});

test('a manually supplied query cannot claim that the form was sent', () => {
  const state = mount('?contact=sent');
  assert.equal(state.status.textContent, 'Initial form notice');
  state.formEvents.submit({});
  state.pageEvents.pageshow();
  assert.match(state.status.textContent, /FormSubmit/);
  assert.doesNotMatch(state.status.textContent, /delivered|inbox/i);
});
