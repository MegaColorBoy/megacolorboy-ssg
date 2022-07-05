title: How to perform mysqldump without a password prompt?
date: April 10th, 2021
slug: how-to-perform-mysqldump-without-a-password-prompt
category: Unix
status: active

If you're performing a mass database backup using `mysqldump`, you'll pretty much find it annoying to type in the password every single time.

To get rid of it, open `/etc/mysql/my.cnf` configuration file and add your database credentials:
<pre>
<code class="mysql">
[mysqldump]
user="your_username"
password="your_password"
</code>
</pre>

Once done, save the `my.cnf` configuration file and now, you can try exporting your database without a hassle like this:
<pre>
<code class="bash">
mysqldump -u your_username database_name > database.sql
</code>
</pre>

Hope this trick helps you out!