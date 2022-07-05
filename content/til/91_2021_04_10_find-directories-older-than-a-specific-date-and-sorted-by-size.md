title: Find directories older than a specific date and sorted by size
date: April 10th, 2021
slug: find-directories-older-than-a-specific-date-and-sorted-by-size
category: Unix
status: active

Wanted to see which directories were created on an older date along with their sizes? Try this:

<pre>
<code class="bash">
find . -type d -maxdepth 1 ! -newermt "2021-04-10" -exec du -sh {} \; | sort -h >> oldprojectsizes.txt
</code>
</pre>

Hope you found this tip useful!