title: How to manually configure your WiFi on Arch Linux?
date: June 9th, 2020
slug: how-to-manually-configure-your-wifi-on-arch-linux
category: Linux
status: active

Recently, I thought of playing around with Arch Linux to learn more about Linux under-the-hood and to see if it can become my new daily driver.

As I booted from live USB, I tried connecting to my WiFi using `wifi-menu` but it never worked after selecting my network name and entering the credentials.

So, I did a little bit of research in [ArchWiki](https://wiki.archlinux.org) and forums and I figured a way to set it up manually using `netctl` by myself.

`netctl` is a network profile manager and it's apparently an Arch Linux project.

## 1. Select your interface
Before you begin to set up your WiFi connection from your computer, check if your network interface is being detected:
<pre>
<code class="bash">
iwconfig
</code>
</pre>
Since it's a WiFi connection, your interface most probably must be `wlan0`. If you see it, then set the interface up:
<pre>
<code class="bash">
ip link set wlan0 up
</code>
</pre>

## 2. Scan for networks
Now, that your interface, use it to scan for your WiFi network:
<pre>
<code class="bash">
iwlist wlan0 scan | less
</code>
</pre>
Once, you execute this command, you must be able to see your WiFi's SSID (or network name).

Now, put your interface down for a while:
<pre>
<code class="bash">
ip link set wlan0 down
</code>
</pre>

## 3. Create a network profile
Alright, go to `/etc/netctl/examples/` directory and make a copy of the `wireless-wpa` file to the `/etc/netctl` directory:
<pre>
<code class="bash">
cd /etc/netctl/examples
cp /etc/netctl/examples/wireless-wpa /etc/netctl/your-wifi-name
</code>
</pre>
Now, go back to `/etc/netctl/` directory and open the `your-wifi-name` file with your preferred text editor and edit the following only:
<pre>
<code class="bash">
ESSID: your-wifi-name
key: your-wifi-password
</code>
</pre>
After you're done editing, save the file.

## 4. Test network profile
To test if your profile is working, do the following:
<pre>
<code class="bash">
netctl start your-wifi-name
ping -c 3 www.google.com
</code>
</pre>

In case, you get an error, try doing this:
<pre>
<code class="bash">
ip link set dev wlan0 down
netctl start your-wifi-name
ping -c 3 www.google.com
</code>
</pre>

If you're able to ping, then it works. Else, edit your network profile and try connecting to it again.

## 5. Enable network profile
If you've reached this stage that means your network profile must be working fine. Just do the following to enable the network profile to run the internet throughout the setup:
<pre>
<code class="bash">
netctl enable your-wifi-name
</code>
</pre>
Try reading more about using [netctl](https://wiki.archlinux.org/index.php/Netctl) in Arch Linux's official wikipage.
