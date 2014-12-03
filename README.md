The Webcomics Archiver
======================

Have you ever found yourself wanting to read your favorite webcomics more than
one at a time? Ever wanted to read them while offline, or without all the ads
and other surrounding distractions? The Webcomics archiver is a toolset for
saving and reading your comics in the way you want.

There are a few choices for how to set up the system: a static set of HTML and
image files, or a dynamic site which can be kept up to date. The static files
are great for offline reading, or reading on a computer which is not running a
web server. For the more interactive experience, you can set up your own
computer as a web server and have more flexibility over how you read.

Installation
------------

For all the different uses, you will need at least Python version 2.7. For
creating the static files, this is all you need, but for the dynamic setup you
will need the following in addition:

1. PHP 5.4 or higher
2. A webserver capable of running PHP (Apache is recommended)
3. SQLite3, MySQL, or MariaDB

If you want to contribute or extend the tools, you may also want these tools to
setup the development envrionment and automated test systems:

1. NodeJS 1.10 or higher
2. npm for your version of NodeJS
3. Grunt for your version of NodeJS (globally with `npm install -g grunt-cli`)
4. PHP CLI tools
5. Composer for PHP

Once these tools are installed, you can initialize the systems with `npm
install`.

Configuration
-------------

See the [CONFIG.md](CONFIG.md) for details on how to setup and configure the
various settings for the comics archiver.

Running the tools
-----------------

TODO: Write usage
