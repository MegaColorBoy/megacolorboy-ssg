title: Set up reCaptcha in Laravel
date: May 25th, 2020
slug: set-up-recaptcha
category: Laravel

I mean, come on, you need to have a reCaptcha in your forms, no matter what.

Here are the steps:

## 1. Install using Composer
<pre>
<code class="bash">
composer require anhskohbo/no-captcha
</code>
</pre>

## 2. Add provider and alias to configuration
Open your `config/app.php` file and add this to your providers array:
<pre>
<code class="php">
Anhskohbo\NoCaptcha\NoCaptchaServiceProvider::class,
</code>
</pre>

And this to your aliases array:
<pre>
<code class="php">
'NoCaptcha' => Anhskohbo\NoCaptcha\Facades\NoCaptcha::class,
</code>
</pre>

## 3. Publish configuration
<pre>
<code class="bash">
php artisan vendor:publish --provider="Anhskohbo\NoCaptcha\NoCaptchaServiceProvider"
</code>
</pre>

## 4. Add sitekey and secret key to .env file
Open your `.env` file and add this:
<pre>
<code class="php">
NOCAPTCHA_SITEKEY=yoursitekey
NOCAPTCHA_SECRET=yoursecret
</code>
</pre>

## How to use it?
Now, you can use it in your validator using like this:
<pre>
<code class="php">
$validate = Validator::make(Input::all(),[
    'g-recaptcha-response' => 'required|captcha'
]);
</code>
</pre>
