Configuration
=============

The webcomics archiver uses JSON files to read and store configuration info.

Archiver Config
---------------

By default, all the configuration information for the tool itself is stored in
the `config.json` file in the root of the project. This contains information
about which database and folders to use to store the data. This file can be
modified, or another file can be substituted by calling the program with with
`--config-file` flag.

Database configuration must be done in both Django's `web/settings.py` under the
`DATABASE` variable and in `config.json`. Django supports a number of different
backends, but the other comics archiver tools only support MySQL and Sqlite3.
Eventually, the CLI tools will be updated to use the Django configuration and
methods, but for now they are still separate.

In `config.json`, there are three sections: `database`, `directories`, and
`static`. Each of these contains the settings which should be used by the
command line tools when downloading or creating static sites.

### Database Configuration ###

The `database` section contains information about which database engine to use,
and how to connect. Eventually, this section will be deprecated and removed once
the Django API is implemented.

### Directory Configuration ###

The `directories` section specifies where on your computer to store the various
files needed and downloaded. The `config` property is the directory which should
be searched for comic configuration files (discussed below). The `comics`
property is the name of the directory which will be used to store the actual
comic image files. Subdirectories will be created for each comic using its
`folder` property as the name. The `html` property is the path to where static
HTML files should be put.

All these directories must be readable by whatever user invokes to tools, and
both the directories specified by `comics` and `html` must also be writable by
that user.

### Static Configuration ###

The `static` section tells the command line tools how to create static sites, if
they are being generated. The `number` property is the number of comics to put
onto each page. The `template` property is the HTML template the tools should
use as the base for creating the final static site.

#### Static HTML Template ####

The HTML template keys off of placeholders formatted like: `@@@name@@@` which
are replaced with various pieces of information as the template is filled in.
Here are all the current options for templates:

* `@@@title@@@` The title of the comic
* `@@@page@@@` The page number for the current page
* `@@@comics@@@` The place to put in the list of comics
* `@@@first@@@` The CSS class which indicates this is the first page
* `@@@last@@@` The CSS class which indicates this is the last page
* `@@@prev_page@@@` The relative URL to the previous page (not used on the first
    page)
* `@@@next_page@@@` The relative URL to the next page (not use on the last page)

See the default template for an example of how these are used.

### Default Config ###

    {
      "database": {
        "type": "sqlite",
        "server": "comics.db",
        "database": "comics",
        "user": null,
        "pass": null
      },
      "directories": {
        "config": "config",
        "comics": "comics",
        "html": "web"
      },
      "static": {
        "number": 25,
        "template": "web/templates/static.html"
      }
    }



Comic Configs
-------------

Each comic you want to trawl for comics requires its own configuration file.
The config file contains information about the comic, where to start, and the
regular expressions to search for to move through the archives and save comics.

### Example Config ###

    {
      "name": "Example Comic",
      "description": "This is an example config file",
      "folder": "example",
      "nextRegex": "Next.gif",
      "comicRegex": "http://example.com/comics/[^/\"']*",
      "notesRegex": null,
      "altText": true,
      "baseUrl": "http://example.com/",
      "startUrl": "http://example.com/archive/1"
    }

Most of these properties should be self explanatory. The `name` and
`description` fields are used when listing the comics, and on pages associated
with this particular comic. The `folder` property is the name of the folder to
be used to store the actual comic image files. The three properties `nextRegex`,
`comicRegex`, and `notesRegex` are all regular expression strings which the CLI
tools will use to look up links to the next page, comic image tags, and any
notes or annotations on the page. The `altText` property is a boolean flag to
indicate to the CLI tools to save the alt-text, if any, for each comic. The
`baseUrl` field tells the CLI tools what to use as the base URL for relative
paths, and the `startUrl` field tells them from where to begin trawling the
archives.
