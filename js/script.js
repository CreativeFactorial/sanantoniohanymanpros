// San Antonio Handyman lead-gen site — lightweight vanilla JS
// No dependencies, no tracking beyond what you wire up in the head snippets.

document.addEventListener('DOMContentLoaded', function () {

  // Mark the current nav link as active for a small on-page SEO/UX boost.
  var here = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.main-nav a, .footer-links a').forEach(function (link) {
    var href = link.getAttribute('href');
    if (href === here) link.setAttribute('aria-current', 'page');
  });

  // Lead form: basic client-side honeypot spam check + conversion redirect.
  // Works out of the box on Netlify (data-netlify="true" on the <form>).
  // If you're NOT hosting on Netlify, swap the form action to your endpoint
  // of choice (Formspree, Basin, your own webhook, etc). See README.
  var form = document.getElementById('quote-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      var honeypot = form.querySelector('input[name="company"]');
      if (honeypot && honeypot.value) {
        // Bot filled the hidden field — silently block submission.
        e.preventDefault();
        return false;
      }
      // If you wire up a fetch()-based submission instead of a native
      // POST, push a dataLayer/gtag conversion event here before redirect.
    });
  }

  // Click-to-call / click-to-quote conversion tracking hook.
  // Fires a dataLayer event if GTM/GA4 is installed (see index.html <head>).
  document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
    link.addEventListener('click', function () {
      if (window.dataLayer) {
        window.dataLayer.push({ event: 'click_to_call', link_text: link.textContent.trim() });
      }
      if (typeof gtag === 'function') {
        gtag('event', 'click_to_call', { event_category: 'lead', event_label: link.textContent.trim() });
      }
    });
  });
});
