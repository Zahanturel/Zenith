(function() {
  // Load Mermaid from CDN and render <pre class="mermaid"> blocks produced by mdbook-mermaid
  var script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
  script.async = false;
  script.onload = function() {
    mermaid.initialize({ startOnLoad: false, theme: 'default' });
    mermaid.run({ querySelector: 'pre.mermaid', suppressErrors: true });
  };
  document.head.appendChild(script);
})();
