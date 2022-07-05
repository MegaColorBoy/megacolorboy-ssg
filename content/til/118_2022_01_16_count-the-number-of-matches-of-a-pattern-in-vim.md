title: Count the number of matches of a pattern in VIM
date: January 16th, 2022
slug: count-the-number-of-matches-of-a-pattern-in-vim
category: VIM
status: active

You can the count the number of matches of a pattern by using the `n` flag while using the substitute command. Try the following command:

<pre>
<code class="bash">
:%s/something//gn
</code>
</pre>

If you want to know on how many lines it matches, just omit the `g` flag:

<pre>
<code class="bash">
:%s/something//n
</code>
</pre>

Hope this tip helped you out!
