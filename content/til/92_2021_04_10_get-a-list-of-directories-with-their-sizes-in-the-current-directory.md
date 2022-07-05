title: Get a list of directories with their sizes in the current directory
date: April 10th, 2021
slug: get-a-list-of-directories-with-their-sizes-in-the-current-directory
category: Unix
status: active

If you want to sizes of each directory in a list, try the following command:

<pre>
<code class="bash">
du -sh * | sort -h >> directories-sorted.txt
</code>
</pre>

And, if you wanted to find the directory that takes consumes a lot of space in your directory, you can try this:

<pre>
<code class="bash">
du -sh * | sort -h | tail -n 1
</code>
</pre>

Hope these tips do come in handy! &#x1F60A;