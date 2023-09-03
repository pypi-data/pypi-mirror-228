# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the formatter group object combine with formatter order object.
"""
import unittest

import dup_fmt.formatter as fmt


class FormatterGroupWithOrder(unittest.TestCase):
    def setUp(self) -> None:
        self.gp = fmt.FormatterGroup(
            {
                "version": fmt.Version,
                "datetime": fmt.Datetime,
            }
        )

        self.my_order_cls = fmt.make_order_fmt(self.gp.formats)

    def test_group_order(self):
        parser = self.gp.parser(
            "20221121_1_0_0",
            fmt="{datetime:%Y%m%d}_{version}",
        )
        self.assertEqual(
            "(version=['v1.0.0'], datetime=['2022-11-21 00:00:00.000'])",
            self.my_order_cls(parser).__str__(),
        )
