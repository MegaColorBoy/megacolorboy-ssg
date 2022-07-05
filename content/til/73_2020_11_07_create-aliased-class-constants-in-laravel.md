title: Create aliased class constants in Laravel
date: November 7th, 2020
slug: create-aliased-class-constants-in-laravel
category: Laravel
status: active

There are many ways to define constants in Laravel but I learnt a neat technique where you can define constants using an alias.

First off, create the following directory:

<pre>
<code class="bash">
mkdir app/Constants
</code>
</pre>

Next, create a file named `MyConstants.php` in the `app/Constants` directory and copy-paste the following code:

<pre>
<code class="php">
&lt;?php
namespace App\Constants;

class MyConstants {
    const HELLO = 'hello';
}
?&gt;
</code>
</pre>

Then, go to the `config/app.php` file and define your new alias:

<pre>
<code class="php">
'aliases' => [
    // previously defined aliases...
    'MyConstants' => App\Constants\MyConstants::class,
]
</code>
</pre>

Lastly, execute the following commands to update your app's configuration:

<pre>
<code class="bash">
php artisan config:clear
composer dump-autoload
php artisan config:cache
</code>
</pre>

After that, you can use your new constants anywhere (Controllers, Models or Blades) like this:

<pre>
<code class="php">
&lt;?php
echo MyConstants::HELLO;
?&gt;
</code>
</pre>

Learning this new technique helps me keep the code clean and makes it easier to trace the constants.

Hope you find this tip useful!
