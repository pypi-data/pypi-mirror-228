# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the Constant formatter object.
"""
import unittest

import dup_fmt.formatter as fmt
from dup_fmt.exceptions import FormatterValueError


class ConstantTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.const: fmt.ConstantType = fmt.Constant(
            {
                "%n": "normal",
                "%s": "special",
            }
        )
        self.const02: fmt.ConstantType = fmt.Constant(
            {
                "%g": "gzip",
                "%-g": "gz",
                "%b": "bz2",
                "%r": "rar",
                "%x": "xz",
                "%z": "zip",
            }
        )
        self.const03: fmt.ConstantType = fmt.Constant(
            fmt.Naming(
                {
                    "shorts": "de",
                    "strings": "data engineer",
                }
            )
        )
        self.ct = self.const.parse("normal_life", "%n_life")
        self.ct02 = self.const02.parse("gzip_life", "%g_life")
        self.ct03 = self.const03.parse("data engineer", "%n")

    def test_const_regex(self):
        self.assertDictEqual(
            {
                "%n": "(?P<november>data engineer)",
                "%N": "(?P<november_upper>DATA ENGINEER)",
                "%-N": "(?P<november_upper_minus>Data Engineer)",
                "%u": "(?P<uniform>DATA ENGINEER)",
                "%l": "(?P<lima>data engineer)",
                "%t": "(?P<tango>Data Engineer)",
                "%a": "(?P<alpha>de)",
                "%A": "(?P<alpha_upper>DE)",
                "%c": "(?P<charlie>dataEngineer)",
                "%-c": "(?P<charlie_minus>DataEngineer)",
                "%p": "(?P<papa>DataEngineer)",
                "%k": "(?P<kilo>data-engineer)",
                "%K": "(?P<kilo_upper>DATA-ENGINEER)",
                "%-K": "(?P<kilo_upper_minus>Data-Engineer)",
                "%f": "(?P<foxtrot>dataengineer)",
                "%F": "(?P<foxtrot_upper>DATAENGINEER)",
                "%s": "(?P<sierra>data_engineer)",
                "%S": "(?P<sierra_upper>DATA_ENGINEER)",
                "%-S": "(?P<sierra_upper_minus>Data_Engineer)",
                "%v": "(?P<victor>dtngnr)",
                "%V": "(?P<victor_upper>DTNGNR)",
            },
            self.const03.regex(),
        )
        self.assertDictEqual(
            {
                "%n": "(?P<november>normal)",
                "%s": "(?P<sierra>special)",
            },
            self.const.regex(),
        )

    def test_const_parser(self):
        ct = self.const.parse("normal_and_special", "%n_and_%s")
        self.assertEqual(ct.value, "normal|special")

    def test_const_parser_raise(self):
        with self.assertRaises(FormatterValueError) as context:
            self.const.parse("special_job", "%s_life")
        self.assertTrue(
            (
                "value 'special_job' does not match "
                "with format '(?P<sierra>special)_life'"
            )
            in str(context.exception)
        )

    def test_const_properties(self):
        self.assertEqual(1, self.ct.level.value)
        self.assertEqual("normal", self.ct.value)
        self.assertEqual("normal", self.ct.string)
        self.assertEqual("gzip", self.ct02.value)
        self.assertEqual("gzip", self.ct02.string)
        self.assertEqual("data engineer", self.ct03.value)
        self.assertEqual("data engineer", self.ct03.string)

    def test_const_format(self):
        self.assertEqual("special", self.ct.format("%s"))
        self.assertEqual("normal normal special", self.ct.format("%n %n %s"))
