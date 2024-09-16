// No longer need to manage API keys, so remove save and restore functionality entirely.

document.addEventListener('DOMContentLoaded', () => {
  // Display a message indicating no API key is needed in this stubbed mode.
  const status = document.getElementById('status');
  status.textContent = 'No API key needed. Mock mode is active.';
  setTimeout(() => {
    status.textContent = '';
  }, 750);
});
