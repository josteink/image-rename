#!/usr/bin/python

import os
import datetime


def get_date_from_exif(filename):
    # We're looking for tags like these:
    # 'EXIF DateTimeDigitized': (0x9004) ASCII=2015:06:17 20:34:16 @ 752,
    # 'EXIF DateTimeOriginal': (0x9003) ASCII=2015:06:17 20:34:16 @ 732,
    # 'Image DateTime': (0x0132) ASCII=2015:06:17 20:34:16 @ 208,
    import exifread
    with open(filename, 'r') as f:
        tags = exifread.process_file(f, details=False)
        if tags is None:
            return None

    datestring = None
    if "EXIF DateTimeOriginal" in tags:
        datestring = tags["EXIF DateTimeOriginal"]
    elif "EXIF DateTimeDigitized" in tags:
        datestring = tags["EXIF DateTimeDigitized"]
    elif "Image DateTime" in tags:
        datestring = tags["Image DateTime"]
    else:
        return None

    date = get_date_from_string(datestring.values)
    return date


def get_date_modified(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def get_date_from_string(file):
    import re

    sep = "(_|-|\\.|\\:| )?"
    datematch = re.compile(
        "^.*" +             # whatever
        "(\\d{4})" + sep +  # year 1
        "(\\d{2})" + sep +  # month 3
        "(\\d{2})" + sep +  # day 5
        "(\\d{2})" + sep +  # hour 7
        "(\\d{2})" + sep +  # minute 9
        "(\\d{2})" +        # seconds 11
        ".*$"               # whatever
    )
    m = datematch.match(file)
    if m is None:
        return None

    # iX = ignored
    [year, i1, month, i2, day, i3, hour, i4, minute, i5, second] = m.groups()
    [iyear, imonth, iday, ihour, iminute, isecond] = map(int, [
        year, month, day, hour, minute, second
    ])

    return datetime.datetime(iyear, imonth, iday, ihour, iminute, isecond)


def get_date_for_file(file):
    date = get_date_from_string(file)
    if date is None:
        date = get_date_from_exif(file)

    if date is None:
        date = get_date_modified(file)

    return date


def format_date(date):
    return "{0}{1:02d}{2:02d}_{3:02d}{4:02d}{5:02d}".format(
        date.year, date.month, date.day,
        date.hour, date.minute, date.second
    )


def get_new_name_for_file(prefix, file):

    date = get_date_for_file(file)
    formatted = format_date(date)

    folder, filename = os.path.split(file)
    base, ext = os.path.splitext(filename)

    # preserve original folder!
    new_name = os.path.join(folder, prefix + formatted + ext)
    return new_name


def process(prefix, test, files):
    if not test:
        print "Renaming..."
    else:
        print "Test only. Not renaming..."

    for file in files:
        if not os.path.isfile(file):
            print "WARNING: '{0}' not found or not file. Skipping.".format(
                file
            )
            continue

        new_name = get_new_name_for_file(prefix, file)
        if new_name == file:
            continue

        print "- '{0}' => '{1}'".format(file, new_name)
        if test:
            continue

        if os.path.isfile(new_name):
            print "ERROR: File with this name already exists. Skipped."
        else:
            os.rename(file, new_name)


def main():
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument("prefix", help="Prefix for renamed files.")
    p.add_argument(
        "-t", "--test",
        help="Only print results, don't actually rename.",
        action="store_true"
    )
    p.add_argument("files", nargs="*", help="The files to rename.")

    args = p.parse_args()
    process(args.prefix, args.test, args.files)


if __name__ == "__main__":
    main()