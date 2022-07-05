title: Extract a specific folder from a zipped archive
date: May 28th, 2020
slug: extract-a-specific-folder-from-a-zipped-archive
category: Terminal

First, you need to view what's inside of the `.zip` archive:
<pre>
<code class="bash">
unzip -v archive.zip
</code>
</pre>
Once, you've found the folder you wanted to extract, just type this:
<pre>
<code class="bash">
unzip archive.zip "folder_to_extract/*" -d .
</code>
</pre>
