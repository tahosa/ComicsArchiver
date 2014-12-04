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
