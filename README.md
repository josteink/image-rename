
# image-rename

A simple command-line utility to help unify the file-naming
conventions of photos taken on several different kinds of devices,
which each may have their own naming convention.

This utility will rename all files based on their assumed date of
creation. To determine this date several means will be tried:

* Existing file-name conventions
* EXIF information
* File-system information.

## Dependencies

This utility is written in `python`, and besides core python, also
depend on the `exifread` python-module.

To install these dependencies on a Debian-based distro use the
following commands:

````sh
$ sudo apt-get install python python-pip
$ sudo pip install exifread
````

On other distros, replace with the appropriate commands.

## License

This software is licensed under the GPL license.
