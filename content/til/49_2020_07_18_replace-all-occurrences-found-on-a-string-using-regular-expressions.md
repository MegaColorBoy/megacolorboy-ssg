title: Replace all occurrences found on a string using Regular Expressions
date: July 18th, 2020
slug: replace-all-occurrences-found-on-a-string-using-regular-expressions
category: Regular Expressions
status: active

Let's say you have the following string and you must replace all occurrences of **"Hello"** with **"Bye"**:
<pre>
<code class="js">
var str = "Hello Hello Hello World";
</code>
</pre>

You may think of using the `.replace()` method to solve this problem:
<pre>
<code class="js">
var newStr = str.replace("Hello", "Bye")
</code>
</pre>

But unfortunately, it only replaces the first occurrence in the string:
<pre>
<code class="js">
console.log(newStr); // returns "Bye Hello Hello World" as the output.
</code>
</pre>

Using the power of Regular Expressions, you can replace all occurrences in one go:
<pre>
<code class="js">
function replaceAll(str, search, replace){
    var re = new RegExp(search, "g");
    return str.replace(re, replace);
}    
</code>
</pre>

Now, when you execute the following, you'll get a string that replaced all occurrences:
<pre>
<code class="js">
var newStr = replaceAll(str, "Hello", "Bye");
console.log(newStr); // returns "Bye Bye Bye World" as the output.
</code>
</pre>

Until next time, then!