#!/usr/bin/python

import unittest
import image_rename


class Tests(unittest.TestCase):
    def test_new_name_preserves_folder(self):
        import os

        file_with_folder = "folder/boo-2016-01-01 12:23:34.jpg"
        res = image_rename.get_new_name_for_file("test_", file_with_folder)

        folder, file = os.path.split(res)
        self.assertEqual("folder", folder)

    def test_date_is_parsed_correctly(self):
        from datetime import datetime
        cases = [
            "img_20160102_132334.jpg",
            "img_2016-01-02 13:23:34.jpg",
            "img_2016.01.02.13.23.34.jpg"
        ]

        reference = datetime(2016, 1, 2, 13, 23, 34)
        for case in cases:
            res = image_rename.get_date_from_string(case)
            self.assertEqual(reference, res)
