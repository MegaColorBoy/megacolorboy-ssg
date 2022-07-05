title: How to delete files inside a zip file?
date: July 21st, 2020
slug: how-to-delete-files-inside-a-zip-file
category: Terminal
status: active

Ever compressed your project directory but forgot to delete that useless file or folder and turns out the compresed file is larger than it's supposed to be? 

Here's a quick solution you can try:

If you want to delete a file inside a `.zip` file, try this:
<pre>
<code class="bash">
zip --delete file.zip "file.ext"
</code>
</pre>

And if you want to delete a folder, try this:
<pre>
<code class="bash">
zip --delete file.zip "folder/*"
</code>
</pre>

Hope this helps you out!