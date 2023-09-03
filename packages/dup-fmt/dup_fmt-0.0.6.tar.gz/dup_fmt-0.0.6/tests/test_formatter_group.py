# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the formatter object.
"""
import unittest
from datetime import datetime

from packaging.version import Version

import dup_fmt.formatter as fmt


class FormatterGroupTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.gp = fmt.FormatterGroup(
            {
                "name": {"fmt": fmt.Naming, "value": "data engineer"},
                "datetime": {
                    "fmt": fmt.Datetime,
                    "value": datetime(2022, 1, 1),
                },
            }
        )
        self.gp2 = fmt.FormatterGroup(
            {
                "version": {
                    "fmt": fmt.Version,
                    "value": Version(version="1.2.3"),
                },
                "datetime": {
                    "fmt": fmt.Datetime,
                    "value": datetime(2022, 1, 1),
                },
            }
        )
        self.gp3 = fmt.FormatterGroup(
            {
                "name": {"fmt": fmt.Naming, "value": "foo bar"},
                "role": {"fmt": fmt.Naming, "value": "data engineer"},
            }
        )
        self.gp_default = fmt.FormatterGroup(
            {
                "version": {"fmt": fmt.Version},
                "datetime": {"fmt": fmt.Datetime},
            }
        )
        self.gp_default2 = fmt.FormatterGroup(
            {
                "version": fmt.Version,
                "datetime": fmt.Datetime,
            }
        )

    def test_fmt_group_properties(self):
        self.assertEqual("FormatterGroup(name, datetime)", self.gp.__repr__())

    def test_fmt_group_parser(self):
        self.assertEqual(
            {
                "datetime": fmt.Datetime.parse("2022-01-01", "%Y-%m-%d"),
                "name": fmt.Naming.parse("data engineer", "%n"),
            },
            self.gp.parser(
                "data_engineer_in_20220101_de",
                fmt="{name:%s}_in_{datetime:%Y%m%d}_{name:%a}",
                _max=False,
            ),
        )
        self.assertEqual(
            {
                "datetime": fmt.Datetime.parse("2022-01-01", "%Y-%m-%d"),
                "name": fmt.Naming.parse("data engineer", "%n"),
            },
            self.gp.parser(
                "data_engineer_in_20220101_de",
                fmt="{name:%s}_in_{datetime:%Y%m%d}_{name:%a}",
                _max=True,
            ),
        )
        self.assertEqual(
            {
                "datetime": fmt.Datetime.parse("2022-01-01", "%Y-%m-%d"),
                "version": fmt.Version.parse("v1.2.3", "v%m.%n.%c"),
            },
            self.gp2.parser(
                "20220101_1_2_3_00",
                fmt="{datetime:%Y%m%d}_{version}_{datetime:%H}",
                _max=True,
            ),
        )
        self.assertEqual(
            {
                "name": fmt.Naming.parse("foo bar", "%n"),
                "role": fmt.Naming.parse("data engineer", "%n"),
            },
            self.gp3.parser(
                "foo_bar|data_engineer",
                fmt="{name:%s}\\|{role:%s}",
                _max=True,
            ),
        )
        # FIXME: parser foo_bar_data to `name` and engineer to `role`
        # self.assertEqual(
        #     {
        #         "name": fmt.Naming.parse("foo bar", "%n"),
        #         "role": fmt.Naming.parse("data engineer", "%n"),
        #     },
        #     self.gp3.parser(
        #         "foo_bar_data_engineer",
        #         fmt="{name:%s}_{role:%s}",
        #         _max=True,
        #     ),
        # )
        self.assertEqual(
            {
                "datetime": fmt.Datetime.parse("2022-11-21", "%Y-%m-%d"),
                "version": fmt.Version.parse("v1.0.0", "v%m.%n.%c"),
            },
            self.gp_default2.parser(
                "20221121_1_0_0",
                fmt="{datetime:%Y%m%d}_{version}",
                _max=True,
            ),
        )

    def test_fmt_group_parser_diff(self):
        self.assertEqual(
            {
                "datetime": fmt.Datetime.parse("2023-01-02", "%Y-%m-%d"),
                "name": fmt.Naming.parse("data engineer", "%n"),
            },
            self.gp.parser(
                "data_engineer_in_20230102_de",
                fmt="{name:%s}_in_{datetime:%Y%m%d}_{name:%a}",
                _max=False,
            ),
        )
        self.assertEqual(
            {
                "datetime": fmt.Datetime.parse("2023-04-25", "%Y-%m-%d"),
                "version": fmt.Version.parse("v1.2.3", "v%m.%n.%c"),
            },
            self.gp_default.parser(
                "20230425_1_2_3",
                fmt="{datetime:%Y%m%d}_{version}",
                _max=True,
            ),
        )

    def test_fmt_group_parser_raise(self):
        with self.assertRaises(fmt.FormatterArgumentError) as context:
            # raise from `cls.__parser_all`
            self.gp.parser(
                "data_engineer_in_20220101_de",
                fmt="{name:%s}_in_{datetime:%Y%m%d}_{name:%a}_extension",
                _max=False,
            )
        self.assertTrue(
            (
                r"with 'format', 'data_engineer_in_20220101_de' does not match "
                r"with the format: '^(?P<name>(?P<strings_snake__name>[a-z0-9]+"
                r"(?:_[a-z0-9]+)*))_in_(?P<datetime>(?P<year__datetime>\d{4})"
                r"(?P<month_pad__datetime>01|02|03|04|05|06|07|08|09|10|11|12)"
                r"(?P<day_pad__datetime>[0-3][0-9]))_"
                r"(?P<name__1>(?P<shorts__1__name>[a-z0-9]+))_extension$'"
            )
            in str(context.exception)
        )

    def test_fmt_group_format(self):
        self.assertEqual(
            "data engineer_2022_01_01_000000_000000.csv",
            self.gp.format("{name}_{datetime:%Y_%m_%d_%H%M%S_%f}.csv"),
        )
        self.assertEqual(
            "dataEngineer_2022_01_01_000000_000000.csv",
            self.gp.format("{name:%c}_{datetime:%Y_%m_%d_%H%M%S_%f}.csv"),
        )
        self.assertEqual(
            "2022_01_01_000000_000000_v1_2_3.csv",
            self.gp2.format("{datetime:%Y_%m_%d_%H%M%S_%f}_v{version:%f}.csv"),
        )
        self.assertEqual(
            "20220101_000000_1_2_3_20220101_000000.csv",
            self.gp2.format("{datetime}_{version}_{datetime}.csv"),
        )

    def test_fmt_group_format_raise(self):
        with self.assertRaises(fmt.FormatterArgumentError) as context:
            self.gp2.format("{datetime:%Y_%m_%d_%H%M%S_%K}_v{version:%f}.csv")
        self.assertTrue(
            (
                "with 'format', string formatter of "
                "'{datetime:%Y_%m_%d_%H%M%S_%K}' does not support "
                "for key '%K' in configuration"
            )
            in str(context.exception)
        )
