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

1. The Django module for python installed
2. A webserver capable of serving Django (a simple one comes with Django if you
     don't want to set up something else)
 * Most webservers will support this

If you want to contribute or extend the tools, you may also want these tools to
setup the development envrionment and automated test systems:

1. NodeJS 1.10 or higher
2. npm for your version of NodeJS
3. Grunt for your version of NodeJS (globally with `npm install -g grunt-cli`)
4. Python Nose (test framework)

Once these tools are installed, you can initialize the systems with `npm
install`. Then, if you want to use the dynamic site, you will also need to edit
the Django config file and do `python manage.py migrate` to create the database
tables. Once you create the tables, you should do `python manage.py createsuperuser`
to create an admin account for the web interface and database.

Configuration
-------------

See the [CONFIG.md](CONFIG.md) for details on how to setup and configure the
various settings for the comics archiver.

Running the tools
-----------------

Comics can either be added through config files (required for creating static
pages), or by adding them through the admin web interface if using the dynamic
functions. Once you have done the necessary setup and creation of config files,
the command line tool can be invoked as follows:

<pre>
comics_cli.py [-c file] [-s]  [-r] [-d level]

  -c  --config-file    Load the configuration from the specified file instead of
                         from the default location (./config.json)
  -s  --static         Create static pages instead of using the database
  -r  --reset          Clears all data in the database before starting
                         USE WITH CAUTION!
  -d  --debug          Set the log level to the specified integer (if -d is
                         given, but no value is specified, it defaults to DEBUG
                         [10]):

                           CRITICAL: 50
                           ERROR: 40
                           WARNING: 30
                           INFO: 20
                           DEBUG: 10
</pre>
