# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the formatter object.
"""
import unittest

import dup_fmt.formatter as fmt


class NamingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.nm: fmt.Naming = fmt.Naming.parse("data engineer", "%n")
        self.nm2: fmt.Naming = fmt.Naming(
            {
                "shorts": "de",
                "strings": "data engineer",
            }
        )
        self.nm3: fmt.Naming = fmt.Naming({"flats": "framework"})
        self.nm4: fmt.Naming = fmt.Naming({"vowels": "dtengnr"})
        self.nm5: fmt.Naming = fmt.Naming({"shorts": "de"})
        self.nm_default: fmt.Naming = fmt.Naming()
        self.nm_p: fmt.Naming = fmt.Naming.parse("dataEngineer", "%c")

    def test_naming_regex(self):
        self.assertDictEqual(
            {
                "%u": "(?P<strings_upper>[A-Z0-9]+(?:\\s[A-Z0-9]+)*)",
                "%l": "(?P<strings>[a-z0-9]+(?:\\s[a-z0-9]+)*)",
                "%t": "(?P<strings_title>[A-Z][a-z0-9]+(?:\\s[A-Z]+[a-z0-9]*)*)",
                "%a": "(?P<shorts>[a-z0-9]+)",
                "%A": "(?P<shorts_upper>[A-Z0-9]+)",
                "%c": "(?P<strings_camel>[a-z]+((\\d)|([A-Z0-9][a-z0-9]+))*([A-Z])?)",
                "%p": "(?P<strings_pascal>[A-Z]([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|[a-z0-9]*[A-Z][A-Z0-9]*[a-z])[A-Za-z0-9]*)",
                "%k": "(?P<strings_kebab>[a-z0-9]+(?:-[a-z0-9]+)*)",
                "%K": "(?P<strings_kebab_upper>[A-Z0-9]+(?:-[A-Z0-9]+)*)",
                "%-K": "(?P<strings_kebab_title>[A-Z][a-z0-9]+(?:-[A-Z]+[a-z0-9]*)*)",
                "%f": "(?P<flats>[a-z0-9]+)",
                "%F": "(?P<flats_upper>[A-Z0-9]+)",
                "%s": "(?P<strings_snake>[a-z0-9]+(?:_[a-z0-9]+)*)",
                "%S": "(?P<strings_snake_upper>[A-Z0-9]+(?:_[A-Z0-9]+)*)",
                "%-S": "(?P<strings_snake_title>[A-Z][a-z0-9]+(?:_[A-Z]+[a-z0-9]*)*)",
                "%v": "(?P<vowel>[b-df-hj-np-tv-z]+)",
                "%V": "(?P<vowel_upper>[B-DF-HJ-NP-TV-Z]+)",
                "%n": "(?P<strings>[a-z0-9]+(?:\\s[a-z0-9]+)*)",
                "%N": "(?P<strings_upper>[A-Z0-9]+(?:\\s[A-Z0-9]+)*)",
                "%-N": "(?P<strings_title>[A-Z][a-z0-9]+(?:\\s[A-Z]+[a-z0-9]*)*)",
                "%-c": "(?P<strings_pascal>[A-Z]([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|[a-z0-9]*[A-Z][A-Z0-9]*[a-z])[A-Za-z0-9]*)",
            },
            fmt.Naming.regex(),
        )

    def test_naming_properties(self):
        self.assertEqual(
            "<Naming.parse('data engineer', '%n')>", self.nm.__repr__()
        )
        self.assertEqual(
            "<Naming.parse('data engineer', '%n')>", self.nm2.__repr__()
        )
        self.assertEqual(
            "<Naming.parse('framework', '%n')>", self.nm3.__repr__()
        )

        self.assertEqual("data engineer", self.nm.__str__())
        self.assertEqual("data engineer", self.nm2.__str__())
        self.assertEqual("framework", self.nm3.__str__())
        self.assertEqual("dtengnr", self.nm4.__str__())
        self.assertEqual("d e", self.nm5.__str__())
        self.assertEqual("", self.nm_default.__str__())
        self.assertEqual("data engineer", self.nm_p.__str__())

        # Test `cls.string` property
        self.assertEqual("data engineer", self.nm.string)

        # Test `cls.value` property
        self.assertEqual("data engineer", self.nm.value)

    def test_naming_format(self):
        self.assertEqual("data_engineer", self.nm.format("%s"))
        self.assertEqual("DATA-ENGINEER", self.nm.format("%K"))
        self.assertEqual("de", self.nm.format("%a"))
        self.assertEqual("dataEngineer", self.nm.format("%c"))
        self.assertEqual("data_engineer", self.nm2.format("%s"))
