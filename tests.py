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
