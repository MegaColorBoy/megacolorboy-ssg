title: Increase execution time in PHP
date: August 23rd, 2020
slug: increase-execution-time-in-php
category: PHP
status: active

Ever process a file that's larger than 2GB and got an error that said something like this:
> Maximum execution time of 30 seconds exceeded

Though, PHP doesn't have an efficient way of processing files of large sizes, you can prevent your web application from timing out by adding this to your code:

<pre>
<code class="php">
&lt;?php
// 300 seconds == 5 minutes
ini_set('max_execution_time', 300);
?&gt;
</code>
</pre>

Hopefully, some day, this might come in handy for you! &#128540;