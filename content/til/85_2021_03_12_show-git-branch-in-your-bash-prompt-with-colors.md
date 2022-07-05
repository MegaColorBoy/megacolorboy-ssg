title: Show Git branch in your Bash prompt (with colors)
date: March 12th, 2021
slug: show-git-branch-in-your-bash-prompt-with-colors
category: Bash
status: active

Do you work on a project with multiple Git branches but don't know which one you're in? Open your `.bashrc` file and add this:

<pre>
<code class="bash">
force_color_prompt=yes
color_prompt=yes

parse_git_branch() {
 git branch 2&gt; /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

if [ "$color_prompt" = yes ]; then
 PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;31m\]$(parse_git_branch)\[\033[00m\]\$ '
else
 PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w$(parse_git_branch)\$ '
fi

unset color_prompt force_color_prompt
</code>
</pre>

Save the file and execute this command for your changes to take effect:
<pre>
<code class="">
source ~/.bashrc
</code>
</pre>

Now, you should see your colors in your Bash prompt along with the Git branch that you're working on (**Note: this will be shown if you're in a project that uses a Git repository**).

Hope this helps you out!
