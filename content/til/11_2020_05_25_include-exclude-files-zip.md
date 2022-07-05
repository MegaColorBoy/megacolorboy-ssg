title: Including and excluding files in zip
date: May 25th, 2020
slug: include-exclude-files.zip
category: Terminal

When zipping a directory or a bunch of files, there'll be a lot of stuff that you want to include and exclude.

To exclude a file:
<pre>
<code class="bash">
zip -r files.zip . -x file_1 file_2
</code>
</pre>

Alternatively, you can choose to include files:
<pre>
<code class="bash">
zip -r files.zip . -i file_1 file_2
</code>
</pre>