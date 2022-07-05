title: Find directories created within a date range
date: April 10th, 2021
slug: find-directories-created-within-a-date-range
category: Unix
status: active

Executing these commands helps me create a sorted list of files/directories created within a specific date range:

<pre>
<code class="bash">
touch -t 202104100000 start
touch -t 202104150000 stop
find . -type d -maxdepth 1 -newer start \! -newer stop | sort >> directories.txt
</code>
</pre>

Someday, these commands shall come in handy, bud! &#x1F60E;