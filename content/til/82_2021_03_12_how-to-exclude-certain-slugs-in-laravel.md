title: How to exclude certain slugs in Laravel
date: March 12th, 2021
slug: how-to-exclude-certain-slugs-in-laravel
category: Laravel
status: active

Using plain Regular Expressions, you can exclude certain slug from your routes, try adding the following to your `routes/web.php` file:

<pre>
<code class="php">
&lt;php
    Route::match(array('GET', 'POST'), '/{slug}', 'YourController@index')->name('page')->where('slug', '^(?!pattern).*$');
?&gt;
</code>
</pre>

Hope you found this useful!