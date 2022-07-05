title: Checkout branch
date: May 25th, 2020
slug: checkout-branch
category: Git

Want to create a new branch in your project? Simple, just do this:
<pre>
<code class="bash">
git checkout -b new_branch
</code>
</pre>

By doing this, you'll automatically be shifted to a new branch of your project. To check which branch you're working on, type this:
<pre>
<code class="bash">
git branch
</code>
</pre>

And you should be able to see your current branch marked with a `*`:
<pre>
<code class="bash">
master
* new_branch
</code>
</pre>