title: Remove patterns from multiple files
date: May 27th, 2020
slug: remove-patterns-from-multiple-files
category: Terminal

If you wanted to remove a specific pattern in a list of files, like the ones below:
<pre>
<code class="bash">
23_2020_03_01_article-three.md
22_2020_02_01_article-two.md
21_2020_01_01_article-one.md
</code>
</pre>

You can simply do that using Regular Expressions and the `rename` tool:
<pre>
<code class="bash">
rename 's/[0-9]+_[0-9]+_[0-9]+_[0-9]+_//' *.md
</code>
</pre>

Now, the desired output should look like this:
<pre>
<code class="bash">
article-three.md
article-two.md
article-one.md
</code>
</pre>

This should come in handy if you're lazy to rename each file manually! :)
