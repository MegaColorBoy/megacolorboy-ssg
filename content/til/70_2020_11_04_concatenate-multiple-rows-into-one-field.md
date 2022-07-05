title: Concatenate multiple rows into one field
date: November 4th, 2020
slug: concatenate-multiple-rows-into-one-field
category: MySQL
status: active

Say, you have a table named `hobbies` and wanted to display a list of hobbies based on `user_id`, you'd probably do something like this:
<pre>
<code class="sql">
SELECT title FROM hobbies WHERE user_id = 8;
</code>
</pre>

This would return a list of hobbies like this:
<pre>
<code>
Boxing
Coding
Reading
Fishing
</code>
</pre>

That's simple but what if you wanted to display them in one row? Like this:
<pre>
<code>
Boxing, Coding, Reading, Fishing
</code>
</pre>

You can make use of the `GROUP_CONCAT` method to achieve the same result by executing the following SQL query:
<pre>
<code class="sql">
SELECT GROUP_CONCAT(title, SEPARATOR ', ') FROM hobbies WHERE user_id = 8;
</code>
</pre>

Nice, what if you wanted to view a list of hobbies of all users? In most cases, a table like this might have a many-to-many relationship, so in order to avoid possible duplicates, you can try this:
<pre>
<code class="sql">
SELECT user_id, GROUP_CONCAT(title, SEPARATOR ', ') FROM hobbies
GROUP BY user_id
</code>
</pre>

Hope this tip helps you out!