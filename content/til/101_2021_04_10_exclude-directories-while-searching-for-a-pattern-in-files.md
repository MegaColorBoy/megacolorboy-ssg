title: Exclude directories while searching for a pattern in files
date: April 10th, 2021
slug: exclude-directories-while-searching-for-a-pattern-in-files
category: Unix
status: active

Looking for a specific text pattern in a directory but wanted to avoid some paths? Here's a quick command that you can try:

<pre>
<code class="bash">
grep -R --exclude-dir=path/to/directory 'some pattern' /path/to/search
</code>
</pre>

Hope this helps you out!