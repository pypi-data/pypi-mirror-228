# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
"""
Test the Serial formatter object.
"""
import unittest

import dup_fmt.objects as obj


class SerialTestCase(unittest.TestCase):
    def setUp(self) -> None:
        ...

    def test_relative_serial(self):
        self.assertEqual(
            hash(5), obj.relativeserial(**{"number": 5}).__hash__()
        )
        self.assertEqual(
            "<relativeserial(number=5)>",
            obj.relativeserial(**{"number": 5}).__repr__(),
        )
        self.assertEqual(10, (5 + obj.relativeserial(**{"number": 5})))
        self.assertEqual(10, (obj.relativeserial(**{"number": 5}) + 5))
        self.assertEqual(0, (obj.relativeserial(**{"number": 5}) - 5))
        self.assertEqual(0, (5 - obj.relativeserial(**{"number": 5})))
        self.assertEqual(49, obj.relativeserial(**{"number": 49}))
        self.assertTrue(
            obj.relativeserial(**{"number": 10})
            == (
                obj.relativeserial(**{"number": 5})
                + obj.relativeserial(**{"number": 5})
            )
        )
        self.assertTrue(
            obj.relativeserial(**{"number": 0})
            == (
                obj.relativeserial(**{"number": 5})
                - obj.relativeserial(**{"number": 5})
            )
        )
        self.assertTrue(
            obj.relativeserial(**{"number": 15})
            >= (
                obj.relativeserial(**{"number": 5})
                + obj.relativeserial(**{"number": 5})
            )
        )
        self.assertFalse(obj.relativeserial(**{"number": 15}) <= 10)
        self.assertTrue(
            obj.relativeserial(**{"number": 15})
            <= obj.relativeserial(**{"number": 20})
        )
        self.assertFalse(obj.relativeserial(**{"number": 15}) < 4)
        self.assertEqual(
            obj.relativeserial(**{"number": 15}),
            -obj.relativeserial(**{"number": -15}),
        )
        self.assertFalse(obj.relativeserial(**{"number": 0}) == 0.012)
        with self.assertRaises(TypeError) as context:
            assert obj.relativeserial(**{"number": 15}) < 0.11
        self.assertTrue(
            "'<' not supported between instances of 'relativeserial' and 'float'"
            in str(context.exception)
        )

        with self.assertRaises(TypeError) as context:
            assert obj.relativeserial(**{"number": 15}) <= 9.9
        self.assertTrue(
            "'<=' not supported between instances of 'relativeserial' and "
            "'float'" in str(context.exception)
        )
