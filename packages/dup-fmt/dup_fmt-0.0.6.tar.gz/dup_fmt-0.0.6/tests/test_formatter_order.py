# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the formatter object.
"""
import unittest
from typing import Any, Dict, List

import dup_fmt.formatter as fmt
from dup_fmt.exceptions import FormatterTypeError, FormatterValueError


class OrderFormatTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # Set up Datetime formatter
        self.dt = fmt.Datetime.parse("20220101", "%Y%m%d")
        self.dt2 = fmt.Datetime.parse("20220102", "%Y%m%d")
        self.dt_dict = {"value": "20220101", "fmt": "%Y%m%d"}
        self.dt_dict2 = {"value": "01", "fmt": "%d"}
        self.vs = fmt.Version.parse("201", "%m%n%c")
        self.vs2 = fmt.Version.parse("202", "%m%n%c")
        self.sr_dict = {"fmt": "%n", "value": "2"}
        self.sr_dict2 = {"fmt": "%n", "value": "1"}

        self.fmt_order = fmt.OrderFormatter({"timestamp": self.dt})
        self.fmt_order2 = fmt.OrderFormatter({"timestamp": self.dt2})
        self.fmt_order3 = fmt.OrderFormatter({"version": self.vs})
        self.fmt_order4 = fmt.OrderFormatter({"version": self.vs2})
        self.fmt_order5 = fmt.OrderFormatter({"serial": self.sr_dict})
        self.fmt_order6 = fmt.OrderFormatter({"serial": self.sr_dict2})
        self.fmt_order7 = fmt.OrderFormatter(
            {"timestamp": self.dt},
            auto_serial=True,
        )
        self.fmt_order9 = fmt.OrderFormatter(
            {"timestamp": self.dt, "serial": self.sr_dict},
            auto_serial=True,
        )

    def test_order_raise_name_init(self):
        raise_respec: Dict[str, Dict[Any, Any]] = {"number": self.sr_dict2}
        with self.assertRaises(FormatterValueError) as context:
            fmt.OrderFormatter(raise_respec)  # type: ignore
        self.assertTrue(
            "value of key number does not support" in str(context.exception)
        )

    def test_order_raise_type_init(self):
        raise_respec: Dict[str, List[str]] = {"timestamp": ["20210101"]}
        with self.assertRaises(FormatterTypeError) as context:
            fmt.OrderFormatter(raise_respec)  # type: ignore
        self.assertTrue(
            (
                "value of key timestamp does not support "
                "for type <class 'list'>"
            )
            in str(context.exception)
        )

    def test_order_properties(self):
        self.assertEqual(
            (
                "<OrderFormatter(formatters="
                "{'timestamp': [<Datetime.parse('2022-01-01 00:00:00.000000', "
                "'%Y-%m-%d %H:%M:%S.%f')>]})>"
            ),
            self.fmt_order.__repr__(),
        )

        self.assertEqual(
            "(timestamp=['2022-01-01 00:00:00.000'])", self.fmt_order.__str__()
        )

        self.assertEqual(
            "(timestamp=['2022-01-01 00:00:00.000'], serial=['0'])",
            self.fmt_order7.__str__(),
        )

        self.assertEqual(
            "(timestamp=['2022-01-01 00:00:00.000'], serial=['2'])",
            self.fmt_order9.__str__(),
        )

    def test_order_timestamp(self):
        self.assertFalse(self.fmt_order == self.fmt_order2)
        self.assertFalse(self.fmt_order > self.fmt_order2)
        self.assertTrue(self.fmt_order < self.fmt_order2)

    def test_order_version(self):
        self.assertFalse(self.fmt_order3 == self.fmt_order4)
        self.assertTrue(self.fmt_order3 <= self.fmt_order4)

    def test_order_serial(self):
        self.assertTrue(self.fmt_order5 >= self.fmt_order6)
        self.assertFalse(self.fmt_order5 <= self.fmt_order6)

    def test_order_different(self):
        self.assertFalse(self.fmt_order < self.fmt_order6)
        self.assertFalse(self.fmt_order6 < self.fmt_order)
        self.assertFalse(self.fmt_order6 <= self.fmt_order)
        self.assertTrue(self.fmt_order6 != self.fmt_order)

    def test_order_datetime_adjust(self):
        self.assertEqual(
            "(timestamp=['2021-12-01 00:00:00.000'])",
            self.fmt_order.adjust_timestamp(metrics={"months": 1}).__str__(),
        )

    def test_order_datetime_adjust_raise(self):
        with self.assertRaises(fmt.FormatterArgumentError) as context:
            self.fmt_order3.adjust_timestamp(metrics={"months": 1})
        self.assertTrue(
            (
                "with 'timestamp', order formatter object does not have "
                "`timestamp` in name formatter"
            )
            in str(context.exception)
        )

    def test_order_version_adjust(self):
        # FIXME: fix respec value of version adjustment
        self.assertEqual(
            "(version=['v0.0.0'])",
            self.fmt_order3.adjust_version(value="0.0.1").__str__(),
        )
        self.assertEqual(
            "(version=['v0.0.0'])",
            self.fmt_order4.adjust_version(value="0.0.3").__str__(),
        )

    def test_order_version_adjust_raise(self):
        with self.assertRaises(fmt.FormatterArgumentError) as context:
            self.fmt_order.adjust_version("*.1.3")
        self.assertTrue(
            (
                "with 'version', order formatter object does not have "
                "`version` in name formatter"
            )
            in str(context.exception)
        )

    def test_order_serial_adjust(self):
        self.assertEqual(
            "(serial=['1'])", self.fmt_order5.adjust_serial(value=1).__str__()
        )

    def test_order_serial_adjust_raise(self):
        with self.assertRaises(fmt.FormatterArgumentError) as context:
            self.fmt_order.adjust_serial(1)
        self.assertTrue(
            (
                "with 'serial', order formatter object does not have "
                "`serial` in name formatter"
            )
            in str(context.exception)
        )

    def test_order_all_adjust(self):
        self.assertTrue(
            fmt.OrderFormatter(
                {
                    "timestamp": fmt.Datetime.parse("20220102", "%Y%m%d"),
                    "version": fmt.Version.parse("127", "%m%n%c"),
                }
            ).adjust_version("*.1.3")
            <= fmt.OrderFormatter(
                {"version": fmt.Version.parse("114", "%m%n%c")}
            )
        )
