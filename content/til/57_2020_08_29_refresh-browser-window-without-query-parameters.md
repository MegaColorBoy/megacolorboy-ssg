title: Refresh browser window without query parameters
date: August 29th, 2020
slug: refresh-browser-window-without-query-parameters
category: JavaScript
status: active

If you want to reload the current page in your browser without any query string or parameters, here's how you can do it:

<pre>
<code class="js">
window.location = window.location.pathname;
</code>
</pre>

By doing so, it'll preserve the HTTP/HTTPS protocols of the URL and also remove the fragments that start with a `#`.

If you want to preserve the fragments, you can try this:
<pre>
<code class="js">
var reloadURL = window.location.pathname;
var fragments = (window.location.part === undefined) ? "" : "#" + window.location.part;
window.location = reloadURL + fragments;
</code>
</pre>

Hope you found this useful!