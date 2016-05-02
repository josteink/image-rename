#!/usr/bin/python

import unittest
import image_rename
from datetime import datetime


class Tests(unittest.TestCase):
    def test_new_name_preserves_folder(self):
        import os

        file_with_folder = "folder/boo-2016-01-01 12:23:34.jpg"
        res = image_rename.get_new_name_for_file("test_", file_with_folder)

        folder, file = os.path.split(res)
        self.assertEqual("folder", folder)

    def test_date_is_parsed_correctly(self):
        cases = [
            "img_20160102_132334.jpg",
            "img_2016-01-02 13:23:34.jpg",
            "img_2016.01.02.13.23.34.jpg"
        ]

        expected = datetime(2016, 1, 2, 13, 23, 34)
        for case in cases:
            res = image_rename.get_date_from_string(case)
            self.assertEqual(expected, res)

    def test_exif_date_is_parsed_correctly(self):
        expected = datetime(2016, 1, 30, 23, 58, 56)
        res = image_rename.get_date_from_exif("test-data/IMG_1769.JPG")
        self.assertEqual(expected, res)


if __name__ == "__main__":
    unittest.main()
