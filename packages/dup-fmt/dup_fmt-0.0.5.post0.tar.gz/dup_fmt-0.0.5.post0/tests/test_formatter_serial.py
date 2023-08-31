# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the Serial formatter object.
"""
import unittest

import dup_fmt.formatter as fmt
from dup_fmt.exceptions import FormatterKeyError


class SerialTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.sr = fmt.Serial({"number": "781"})
        self.sr_default: fmt.Formatter = fmt.Serial()
        self.sr_p: fmt.Formatter = fmt.Serial.parse("009", "%p")
        self.sr_p2: fmt.Formatter = fmt.Serial.parse("00001101", "%b")

    def test_serial_regex(self):
        self.assertDictEqual(
            {
                "%n": "(?P<number>[0-9]*)",
                "%p": "(?P<number_pad>[0-9]{3})",
                "%b": "(?P<number_binary>[0-1]*)",
            },
            fmt.Serial.regex(),
        )

    def test_serial_formatter(self):
        self.assertDictEqual(
            {
                "%b": {
                    "regex": "(?P<number_binary>[0-1]*)",
                    "value": "1000000000",
                },
                "%n": {"regex": "(?P<number>[0-9]*)", "value": "512"},
                "%p": {"regex": "(?P<number_pad>[0-9]{3})", "value": "512"},
            },
            fmt.extract_regex_with_value(
                fmt=fmt.Serial, value=512, called=True
            ),
        )

    def test_serial_properties(self):
        self.assertEqual("<Serial.parse('781', '%n')>", self.sr.__repr__())
        self.assertEqual(hash(self.sr.string), self.sr.__hash__())

        self.assertEqual(9, self.sr_p.value)
        self.assertEqual("9", self.sr_p.string)

        self.assertEqual(13, self.sr_p2.value)
        self.assertEqual("13", self.sr_p2.string)

        self.assertEqual(0, self.sr_default.value)
        self.assertEqual("0", self.sr_default.string)

    def test_serial_format(self):
        self.assertEqual("00001001", self.sr_p.format("%b"))
        self.assertEqual("009", self.sr_p.format("%p"))

        self.assertEqual("00001101", self.sr_p2.format("%b"))
        self.assertEqual("013", self.sr_p2.format("%p"))

        self.assertEqual("00000000", self.sr_default.format("%b"))
        self.assertEqual("000", self.sr_default.format("%p"))

        with self.assertRaises(FormatterKeyError) as context:
            self.sr_default.format("%Z")
        self.assertTrue(
            "the format: '%Z' does not support for 'Serial'"
            in str(context.exception)
        )

    def test_serial_order(self):
        self.assertTrue(self.sr_p <= self.sr_p2)
        self.assertTrue(self.sr_p < self.sr_p2)
        self.assertFalse(self.sr_p == self.sr_p2)
        self.assertFalse(self.sr_p >= self.sr_p2)
        self.assertFalse(self.sr_p > self.sr_p2)

    def test_level_compare(self):
        self.assertEqual(1, self.sr_p.level.value)
        self.assertEqual(0, self.sr_default.level.value)
        self.assertTrue(self.sr_p.level == self.sr_p2.level)
        self.assertFalse(self.sr_default.level == self.sr_p2.level)
        self.assertTrue(self.sr_default.level < self.sr_p2.level)
        self.assertListEqual([True], self.sr_p.level.slot)
        self.assertListEqual([False], self.sr_default.level.slot)
