# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
# mypy: disable-error-code="attr-defined"
"""
The main object of formatter is able to format every thing you want by less
config when inherit base class.
"""
from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import lru_cache, partial, total_ordering
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypedDict,
    Union,
)

# TODO: Review ``semver`` package instead ``packaging``.
#  docs: https://pypi.org/project/semver/
import packaging.version as pck_version
from dateutil.relativedelta import relativedelta
from dup_utils.core import remove_pad

from .exceptions import (
    FormatterArgumentError,
    FormatterKeyError,
    FormatterTypeError,
    FormatterValueError,
)
from .objects import relativeserial
from .utils import (
    caller,
    concat,
    convert_fmt_str,
    itself,
)

FormatterType = Type["Formatter"]
PriorityCallable = Union[Callable[[Any], Any], Callable[[], Any], partial]
FormatterCallable = Union[Callable[[], Any], partial]

ConstantType = Type["__BaseConstant"]


class PriorityValue(TypedDict):
    """Type Dictionary for value of mapping of ``cls.priorities``"""

    value: PriorityCallable
    level: Optional[Union[int, Tuple[int, ...]]]


class CRegexValue(TypedDict):
    """Type Dictionary for value of mapping of ``cls.formatter``"""

    value: Union[FormatterCallable, str]
    cregex: str


class RegexValue(TypedDict):
    """Type Dictionary for value of mapping of ``cls.formatter``"""

    value: Union[FormatterCallable, str]
    regex: str


ReturnPrioritiesType = Dict[str, PriorityValue]
ReturnFormattersType = Dict[str, Union[CRegexValue, RegexValue]]


@total_ordering
class SlotLevel:
    """Slot level object for order priority values. This was mean if
    you implement this slot level object to attribute on your class
    and update level to an instance when it has some action, it will
    be make the level more than another instance.

    :param level: a level number of the slot object.
    :type level: int

    .. attributes:

        - count
        - value

    .. methods:

        - update

    """

    __slots__ = (
        "level",
        "slot",
    )

    def __init__(self, level: int) -> None:
        """Main initialize of the slot object that define a slot list
        with level input value length of False.
        """
        self.level: int = level
        self.slot: List[bool] = [False] * level

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(level={self.level})>"

    def __str__(self) -> str:
        return str(self.level)

    def __hash__(self) -> int:
        return hash(tuple(self.slot))

    def __eq__(self, other: Union[SlotLevel, Any]) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __lt__(self, other: SlotLevel) -> bool:
        return self.value < other.value

    @property
    def count(self) -> int:
        """Return the counting number of True value in the slot.

        :rtype: int
        :return: the counting number of True value in the slot.
        """
        return len(list(filter(lambda x: x is True, self.slot)))

    @property
    def value(self) -> int:
        """Return a sum of weighted value from a True value in any slot
        position.

        :rtype: int
        :return: a sum of weighted value from a True value in any slot
            position.
        """
        return sum(x[0] * int(x[1]) for x in enumerate(self.slot, start=1))

    def update(
        self,
        numbers: Optional[Union[int, Tuple[int, ...]]] = None,
        strict: bool = True,
    ) -> SlotLevel:
        """Update value in slot from False to True

        :param numbers: updated numbers of this SlotLevel object.
        :type numbers: Union[int, tuple]
        :param strict: a strict flag for raise error when pass out of
            range numbers.
        :type strict: bool(=True)

        :raises ValueError: if updated number does not exist in range.

        :rtype: SlotLevel
        :return: Self that was updated level
        """
        _numbers: Union[int, Tuple[int, ...]] = numbers or (0,)
        for num in SlotLevel.make_tuple(_numbers):
            if num == 0:
                continue
            elif 0 <= (_num := (num - 1)) <= (self.level - 1):
                self.slot[_num] = True
                continue
            if strict:
                raise FormatterValueError(
                    f"number for update the slot level object does not "
                    f"in range of 0 and {self.level}."
                )
        return self

    @staticmethod
    def make_tuple(value: Union[int, Tuple[int, ...]]) -> Tuple[int, ...]:
        """Return tuple of integer value that was created from input value
        parameter if it is not tuple.

        :param value: a tuple of integers or any integer
        :type value: Union[int, tuple]

        :rtype: tuple
        """
        return (value,) if isinstance(value, int) else value


@dataclass(frozen=True)
class PriorityData:
    """Priority Data class"""

    value: PriorityCallable = field(default=itself, repr=False)
    level: Optional[Union[int, Tuple[int, ...]]] = field(default=(0,))


class MetaFormatter(metaclass=ABCMeta):
    """Metaclass Formatter object"""

    __slots__: Tuple[str, ...] = ()


@total_ordering
class Formatter(MetaFormatter):
    """Formatter object for inherit to any formatter subclass that define
    format and parse method. The base class will implement necessary
    properties and method for subclass that should implement or enhance such
    as `the cls.formatter()` method or the `cls.priorities` property.

    :param formats: A mapping value of attributes
    :type formats: Optional[dict](=None)

    .. class attributes::

        - base_fmt: str
        - base_attr_prefix: str
        - base_level: int : the maximum level of slot level of this instance
        - Config: object : Configuration object

    .. attributes::

        - value
        - string
        - validate
        - level
        - priorities
        - __priorities

    .. methods::

        - formatter
        - default

    .. seealso::

        This class is abstract class for any formatter object. It will raise
    `NotImplementedError` when the necessary attributes and methods does not
    implement from subclass.
    """

    # This value must reassign from child class
    base_fmt: Union[str, NotImplementedError] = NotImplementedError(
        "Please implement base_fmt class property "
        "for this sub-formatter class"
    )

    # This value must reassign from child class
    base_attr_prefix: str = ""

    # This value must reassign from child class
    base_level: int = 1

    class Config:
        """Base Configuration"""

        base_config_value: Optional[Any] = None

    @classmethod
    def parse(
        cls,
        value: str,
        fmt: Optional[str] = None,
    ) -> Formatter:
        """Parse string value with its format to subclass of base formatter
        object. This method generates the standard value for itself data.

        :param value: a string value that match with fmt.
        :type value: str
        :param fmt: a format value will use `cls.base_fmt` if it does not pass
            from input argument.
        :type fmt: Optional[str](=None)

        :raises NotImplementedError: if fmt value parameter does not pass form
            input, or `cls.base_fmt` does not implement.
        :raises ValueError: if value does not match with regular expression
            format string.

        :rtype: Formatter
        :return: an instance of Formatter that parse from string value by
            format string.
        """
        _fmt: Union[str, NotImplementedError] = fmt or cls.base_fmt

        if not _fmt or isinstance(_fmt, NotImplementedError):
            raise NotImplementedError("This class does not set default format")

        _fmt = cls.__parse(_fmt)

        if _search := re.search(rf"^{_fmt}$", value):
            return cls(_search.groupdict())

        raise FormatterValueError(
            f"value {value!r} does not match with format {_fmt!r}"
        )

    @classmethod
    def __parse(cls, fmt: str) -> str:
        _cache: Dict[str, int] = {}
        for fmt_search in re.findall(r"(%[-+!*]?\w)", fmt):
            regex: str = cls.regex()[fmt_search]
            if fmt_search in _cache:
                _rgn = re.search(
                    r"\(\?P<(?P<alias_name>\w+)>",
                    regex,
                )
                _sr_re: str = _rgn.group("alias_name")
                regex = re.sub(
                    rf"\(\?P<{_sr_re}>",
                    rf"(?P<{_sr_re}__{_cache[fmt_search]}>",
                    regex,
                )
                _cache[fmt_search] += 1
            else:
                _cache[fmt_search] = 1
            fmt = fmt.replace(fmt_search, regex, 1)
        return fmt

    @classmethod
    @lru_cache(maxsize=None)
    def regex(cls) -> Dict[str, str]:
        """Return mapping of formats and regular expression values of
        `cls.formatter`.

        :rtype: Dict[str, str]
        :return: a mapping of format, and it's regular expression string
            like:
                {
                    "%n": "(?P<normal>...)",
                    ...
                }
        """
        results: Dict[str, str] = {}
        pre_results: Dict[str, str] = {}
        for f, props in cls.formatter().items():
            # issue: https://github.com/python/mypy/issues/8887
            # docs: https://mypy.readthedocs.io/en/stable/ -
            #   literal_types.html#tagged-unions
            if "regex" in props:
                results[f] = props["regex"]  # type: ignore[typeddict-item]
            elif "cregex" in props:
                pre_results[f] = props["cregex"]
            else:
                raise FormatterValueError(
                    "formatter does not contain `regex` or `cregex` "
                    "in dict value"
                )
        for f, cr in pre_results.items():
            # TODO: improve pref of this line when `results` was large
            #  of mapping regex values
            cr = cr.replace("%%", "[ESCAPE]")
            for rf in iter(results):
                if rf in cr:
                    cr = cr.replace(rf, results[rf])
            results[f] = cr.replace("[ESCAPE]", "%%")
        return results

    def values(self) -> Dict[str, str]:
        """Return mapping of formats and formatter values of `cls.formatter`

        :rtype: Dict[str, str]
        :return: a mapping of formats and formatter values like:
                {
                    "%n": "normal-value",
                    ...
                }
        """
        return {
            f: caller(props["value"])
            for f, props in self.formatter(self.value).items()
        }

    def format(self, fmt: str) -> str:
        """Return string value that was filled by the input format pattern
        argument.

        :param fmt: a format string value for mapping with formatter.
        :type fmt: str

        :raises KeyError: if it has any format pattern does not found in
            `cls.formatter`.

        :rtype: str
        :return: a formatted string value
        """
        _formatter: ReturnFormattersType = self.formatter(self.value)
        fmt = fmt.replace("%%", "[ESCAPE]")
        for _sup_fmt in set(re.findall(r"(%[-+!*]?\w)", fmt)):
            try:
                _value: Union[FormatterCallable, str] = _formatter[_sup_fmt][
                    "value"
                ]
                fmt = fmt.replace(
                    _sup_fmt,
                    (_value() if callable(_value) else _value),
                )
            except KeyError as err:
                raise FormatterKeyError(
                    f"the format: {_sup_fmt!r} does not support for "
                    f"{self.__class__.__name__!r}"
                ) from err
        return fmt.replace("[ESCAPE]", "%")

    def __init__(
        self,
        formats: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Main initialization get the format mapping from input argument
        and generate the necessary attributes for define the value of this
        base formatter object.

            The setter of attribute does not do anything to __slot__ variable.
        """
        _formats: Dict[str, Any] = formats or {}
        self.__validate_format(_formats)

        # Set level of SlotLevel object that set from `base_level` and pass this
        # value to _level variable for update process in priorities loop.
        setattr(
            self,
            f"_{self.base_attr_prefix}_level",
            SlotLevel(level=self.base_level),
        )
        _level: SlotLevel = getattr(self, f"_{self.base_attr_prefix}_level")

        # Set None default of any set up value in `cls.__slots__`
        for attr in getattr(self, "__slots__", ()):
            if attr != (
                f"_{self.base_attr_prefix}_{self.__class__.__name__.lower()}"
            ):
                setattr(self, attr, None)

        for name, props in self.__priorities.items():
            # Split name of key of priorities property value.
            # From: <prefix>_<body> -> TO: [<prefix>, <body>]
            attr = name.split("_", maxsplit=1)[0]

            # Set attr condition
            if getattr(self, f"_{self.base_attr_prefix}_{attr}"):
                continue
            elif any(name.endswith(i) for i in {"_default", "_fix"}):
                setattr(
                    self,
                    f"_{self.base_attr_prefix}_{attr}",
                    (props.value() if callable(props.value) else props.value),
                )  # type: ignore[call-arg]

                # Update level by default it will update at first level
                _level.update(props.level)
            elif name in _formats:
                setattr(
                    self,
                    f"_{self.base_attr_prefix}_{attr}",
                    props.value(_formats[name]),  # type: ignore[call-arg]
                )

                # Update level by default it will update at first level
                _level.update(props.level)

        # Set standard property by default is string value or `self.string`
        setattr(
            self,
            f"_{self.base_attr_prefix}_{self.__class__.__name__.lower()}",
            str(self.string),
        )

        # Run validate method.
        if not self.validate:
            raise FormatterValueError(
                "Parsing value does not valid from validator"
            )

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __hash__(self) -> int:
        """Return hashed string value of str property"""
        return hash(self.string)

    def __str__(self) -> str:
        """Return string value of str property"""
        return self.string

    def __repr__(self) -> str:
        """Return represent string"""
        return (
            f"<{self.__class__.__name__}"
            f".parse('{self.string}', "
            f"'{self.base_fmt}')>"
        )

    def __eq__(self, other: Union[Formatter, Any]) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __lt__(self, other: Formatter) -> bool:
        return self.value.__lt__(other.value)  # type: ignore[no-any-return]

    @property
    @abstractmethod
    def value(self) -> Any:  # pragma: no cover
        """Return the value object that define by any subclass."""
        raise NotImplementedError(
            "Please implement value property for this sub-formatter class"
        )

    @property
    @abstractmethod
    def string(self) -> str:  # pragma: no cover
        """Return standard string value that define by any subclass."""
        raise NotImplementedError(
            "Please implement string property for this sub-formatter class"
        )

    @property
    def validate(self) -> bool:
        """Validate method that will run after setup all attributes"""
        return True

    def valid(
        self,
        string: str,
        fmt: str,
    ) -> bool:
        """Return true if the value attribute from parser of string and
        fmt is valid with self.value.
        """
        return self.value.__eq__(
            self.__class__.parse(string, fmt).value,
        )  # type: ignore[no-any-return]

    @property
    def level(self) -> SlotLevel:
        """Return the slot level object of any subclass."""
        return getattr(
            self,
            f"_{self.base_attr_prefix}_level",
        )  # type: ignore[no-any-return]

    @property
    def __priorities(self) -> Dict[str, PriorityData]:
        """Return private property of extracted mapping from
        `self.priorities` value.
        """
        return {k: PriorityData(**v) for k, v in self.priorities.items()}

    @staticmethod
    def __validate_format(formats: Dict[str, Any]):
        """Raise error if any duplication format name do not all equal."""
        for fmt in filter(lambda x: "__" in x, formats):
            if formats[fmt.split("__")[0]] != formats[fmt]:
                raise FormatterValueError(
                    "Parsing with some duplicate format name that have value "
                    "do not all equal."
                )

    @property
    @abstractmethod
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        """"""
        raise NotImplementedError(
            "Please implement priorities property for this sub-formatter class"
        )

    @staticmethod
    @abstractmethod
    def formatter(
        value: Optional[Any] = None,
    ) -> ReturnFormattersType:
        """"""
        raise NotImplementedError(
            "Please implement formatter static method for this "
            "sub-formatter class"
        )

    @staticmethod
    def default(value: str) -> Callable[[], str]:
        """Return wrapper function of value"""
        return lambda: value


class Serial(Formatter):
    """Serial object for register process that implement formatter and
    parser.
    """

    base_fmt: str = "%n"

    base_attr_prefix: str = "sr"

    class Config(Formatter.Config):
        """Configuration of Serial object"""

        serial_max_padding: int = 3
        serial_max_binary: int = 8

    __slots__ = (
        "_sr_number",
        "_sr_serial",
    )

    @property
    def value(self) -> int:
        return int(self.string)

    @property
    def string(self) -> str:
        return self._sr_number  # type: ignore[no-any-return]

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        return {
            "number": {
                "value": lambda x: x,
                "level": 1,
            },
            "number_pad": {
                "value": lambda x: remove_pad(x),
                "level": 1,
            },
            "number_binary": {
                "value": lambda x: str(int(x, 2)),
                "level": 1,
            },
            "number_default": {"value": self.default("0"), "level": 0},
        }

    @staticmethod
    def formatter(
        serial: Optional[int] = None,
    ) -> ReturnFormattersType:
        """Generate formatter that support mapping formatter,
            %n  : Normal format
            %p  : Padding number
            %b  : Binary number

        :param serial: the serial value that pars to generate all format
        :type serial: Optional[int](=None)

        :rtype: Dict[str, Dict[str, Union[Callable, str]]]
        :return: the generated mapping values of all format strings
        """
        _value: str = str(serial or 0)
        return {
            "%n": {"value": lambda: _value, "regex": r"(?P<number>[0-9]*)"},
            "%p": {
                "value": partial(Serial.to_padding, _value),
                "regex": (
                    r"(?P<number_pad>"
                    rf"[0-9]{{{str(Serial.Config.serial_max_padding)}}})"
                ),
            },
            "%b": {
                "value": partial(Serial.to_binary, _value),
                "regex": r"(?P<number_binary>[0-1]*)",
            },
        }

    @staticmethod
    def to_padding(value: str) -> str:
        """Return padding string result with zero value"""
        return (
            value.rjust(Serial.Config.serial_max_padding, "0") if value else ""
        )

    @staticmethod
    def to_binary(value: str) -> str:
        """Return binary number with limit of max zero padding"""
        return (
            f"{int(value):0{str(Serial.Config.serial_max_binary)}b}"
            if value
            else ""
        )


MONTHS: Dict[str, str] = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}

WEEKS: Dict[str, str] = {
    "Mon": "0",
    "Thu": "1",
    "Wed": "2",
    "Tue": "3",
    "Fri": "4",
    "Sat": "5",
    "Sun": "6",
}


class Datetime(Formatter):
    """Datetime object for register process that implement formatter and
    parser.
    """

    base_fmt: str = "%Y-%m-%d %H:%M:%S.%f"

    base_attr_prefix: str = "dt"

    base_level: int = 8

    __slots__ = (
        "_dt_year",
        "_dt_month",
        "_dt_week",
        "_dt_weeks",
        "_dt_day",
        "_dt_hour",
        "_dt_minute",
        "_dt_second",
        "_dt_microsecond",
        "_dt_local",
        "_dt_datetime",
    )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}"
            f".parse('{self.string}000', "
            f"'{self.base_fmt}')>"
        )

    @property
    def value(self) -> datetime:
        return datetime.fromisoformat(self.string)

    @property
    def string(self) -> str:
        return (
            f"{self._dt_year}-{self._dt_month}-{self._dt_day} "
            f"{self._dt_hour}:{self._dt_minute}:{self._dt_second}."
            f"{self._dt_microsecond[:3]}"
        )

    @property
    def iso_date(self) -> str:
        return f"{self._dt_year}-{self._dt_month}-{self._dt_day}"

    @property
    def validate(self) -> bool:  # no cov
        return True

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        """Priority Properties of the datetime object

        :rtype: Dict[str, Dict[str, Union[Callable, Tuple[int, ...], int]]]
        :returns: a priority properties of the datetime object
        """
        # TODO: Check about week value should keep first and validate if
        #  date value does not match with common sense.
        return {
            "local": {
                "value": lambda x: x,
                "level": 4,
            },
            "year": {
                "value": lambda x: x,
                "level": 8,
            },
            "year_cut_pad": {
                "value": lambda x: f"19{x}",
                "level": 8,
            },
            "year_cut": {
                "value": lambda x: f"19{x}",
                "level": 8,
            },
            "year_default": {
                "value": self.default("1990"),
                "level": 0,
            },
            "day_year": {
                "value": self._from_day_year,
                "level": (
                    7,
                    6,
                ),
            },
            "day_year_pad": {
                "value": self._from_day_year,
                "level": (
                    7,
                    6,
                ),
            },
            "month": {
                "value": lambda x: x.rjust(2, "0"),
                "level": 7,
            },
            "month_pad": {
                "value": lambda x: x,
                "level": 7,
            },
            "month_short": {
                "value": lambda x: MONTHS[x],
                "level": 7,
            },
            "month_full": {
                "value": lambda x: MONTHS[x[:3]],
                "level": 7,
            },
            "month_default": {
                "value": self.default("01"),
                "level": 0,
            },
            "day": {
                "value": lambda x: x.rjust(2, "0"),
                "level": 6,
            },
            "day_pad": {
                "value": lambda x: x,
                "level": 6,
            },
            "day_default": {
                "value": self.default("01"),
                "level": 0,
            },
            "week": {
                "value": lambda x: x,
                "level": 0,
            },
            "week_mon": {
                "value": lambda x: str(int(x) % 7),
                "level": 0,
            },
            "week_short": {
                "value": lambda x: WEEKS[x],
                "level": 0,
            },
            "week_full": {
                "value": lambda x: WEEKS[x[:3]],
                "level": 0,
            },
            "weeks_year_mon_pad": {
                "value": self._from_week_year_mon,
                "level": (
                    7,
                    6,
                ),
            },
            "weeks_year_sun_pad": {
                "value": self._from_week_year_sun,
                "level": (
                    7,
                    6,
                ),
            },
            "week_default": {
                "value": lambda: datetime.strptime(
                    self.iso_date, "%Y-%m-%d"
                ).strftime("%w"),
                "level": 0,
            },
            "hour": {
                "value": lambda x: x.rjust(2, "0"),
                "level": (
                    5,
                    4,
                ),
            },
            "hour_pad": {
                "value": lambda x: x,
                "level": (
                    5,
                    4,
                ),
            },
            "hour_12": {
                "value": (
                    lambda x: str(int(x) + 12).rjust(2, "0")
                    if self._dt_local == "PM"
                    else x.rjust(2, "0")
                ),
                "level": 5,
            },
            "hour_12_pad": {
                "value": (
                    lambda x: str(int(x) + 12).rjust(2, "0")
                    if self._dt_local == "PM"
                    else x
                ),
                "level": 5,
            },
            "hour_default": {
                "value": self.default("00"),
                "level": 0,
            },
            "minute": {
                "value": lambda x: x.rjust(2, "0"),
                "level": 3,
            },
            "minute_pad": {
                "value": lambda x: x,
                "level": 3,
            },
            "minute_default": {
                "value": self.default("00"),
                "level": 0,
            },
            "second": {
                "value": lambda x: x.rjust(2, "0"),
                "level": 2,
            },
            "second_pad": {
                "value": lambda x: x,
                "level": 2,
            },
            "second_default": {
                "value": self.default("00"),
                "level": 0,
            },
            "microsecond_pad": {
                "value": lambda x: x,
                "level": 1,
            },
            "microsecond_default": {
                "value": self.default("000000"),
                "level": 0,
            },
        }

    @staticmethod
    def formatter(
        dt: Optional[datetime] = None,
    ) -> ReturnFormattersType:
        """Generate formatter that support mapping formatter,
            %n  : Normal format with `%Y%m%d_%H%M%S`
            %Y  : Year with century as a decimal number.
            %y  : Year without century as a zero-padded decimal number.
            %-y : Year without century as a decimal number.
            %m  : Month as a zero-padded decimal number.
            %-m : Month as a decimal number.
            %b  : Abbreviated month name.
            %B  : Full month name.
            %a  : the abbreviated weekday name
            %A  : the full weekday name
            %w  : weekday as a decimal number, 0 as Sunday and 6 as Saturday.
            %u  : weekday as a decimal number, 1 as Monday and 7 as Sunday.
            %d  : Day of the month as a zero-padded decimal.
            %-d : Day of the month as a decimal number.
            %H  : Hour (24-hour clock) as a zero-padded decimal number.
            %-H : Hour (24-hour clock) as a decimal number.
            %I  : Hour (12-hour clock) as a zero-padded decimal number.
            %-I : Hour (12-hour clock) as a decimal number.
            %M  : minute as a zero-padded decimal number
            %-M : minute as a decimal number
            %S  : second as a zero-padded decimal number
            %-S : second as a decimal number
            %j  : day of the year as a zero-padded decimal number
            %-j : day of the year as a decimal number
            %U  : Week number of the year (Sunday as the first day of the
                week). All days in a new year preceding the first Sunday are
                considered to be in week 0.
            %W  : Week number of the year (Monday as the first day of the week
                ). All days in a new year preceding the first Monday are
                considered
                to be in week 0.
            %p  : Locale’s AM or PM.
            %f  : Microsecond as a decimal number, zero-padded on the left.

        :param dt: a datetime value
        :type dt: Optional[datetime](=None)
        """
        _dt: datetime = dt or datetime.now()
        return {
            "%n": {
                "value": partial(_dt.strftime, "%Y%m%d_%H%M%S"),
                "regex": (
                    r"(?P<year>\d{4})"
                    r"(?P<month_pad>01|02|03|04|05|06|07|08|09|10|11|12)"
                    r"(?P<day_pad>[0-3][0-9])_(?P<hour_pad>[0-2][0-9])"
                    r"(?P<minute_pad>[0-6][0-9])(?P<second_pad>[0-6][0-9])"
                ),
            },
            "%Y": {
                "value": partial(_dt.strftime, "%Y"),
                "regex": r"(?P<year>\d{4})",
            },
            "%y": {
                "value": partial(_dt.strftime, "%y"),
                "regex": r"(?P<year_cut_pad>\d{2})",
            },
            "%-y": {
                "value": partial(Datetime.remove_pad_dt, _dt, "%y"),
                "regex": r"(?P<year_cut>\d{1,2})",
            },
            "%m": {
                "value": partial(_dt.strftime, "%m"),
                "regex": r"(?P<month_pad>01|02|03|04|05|06|07|08|09|10|11|12)",
            },
            "%-m": {
                "value": partial(Datetime.remove_pad_dt, _dt, "%m"),
                "regex": r"(?P<month>1|2|3|4|5|6|7|8|9|10|11|12)",
            },
            "%b": {
                "value": partial(_dt.strftime, "%b"),
                "regex": (
                    r"(?P<month_short>"
                    r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                ),
            },
            "%B": {
                "value": partial(_dt.strftime, "%B"),
                "regex": (
                    r"(?P<month_full>"
                    r"January|February|March|April|May|June|July|"
                    r"August|September|October|November|December)"
                ),
            },
            "%a": {
                "value": partial(_dt.strftime, "%a"),
                "regex": r"(?P<week_shortname>Mon|Thu|Wed|Tue|Fri|Sat|Sun)",
            },
            "%A": {
                "value": partial(_dt.strftime, "%A"),
                "regex": (
                    r"(?P<week_fullname>"
                    r"Monday|Thursday|Wednesday|Tuesday|Friday|"
                    r"Saturday|Sunday)"
                ),
            },
            "%w": {
                "value": partial(_dt.strftime, "%w"),
                "regex": r"(?P<week>[0-6])",
            },
            "%u": {
                "value": partial(_dt.strftime, "%u"),
                "regex": r"(?P<week_mon>[1-7])",
            },
            "%d": {
                "value": partial(_dt.strftime, "%d"),
                "regex": r"(?P<day_pad>[0-3][0-9])",
            },
            "%-d": {
                "value": partial(Datetime.remove_pad_dt, _dt, "%d"),
                "regex": r"(?P<day>\d{1,2})",
            },
            "%H": {
                "value": partial(_dt.strftime, "%H"),
                "regex": r"(?P<hour_pad>[0-2][0-9])",
            },
            "%-H": {
                "value": partial(Datetime.remove_pad_dt, _dt, "%H"),
                "regex": r"(?P<hour>\d{2})",
            },
            "%I": {
                "value": partial(_dt.strftime, "%I"),
                "regex": (
                    r"(?P<hour_12_pad>"
                    r"00|01|02|03|04|05|06|07|08|09|10|11|12)"
                ),
            },
            "%-I": {
                "value": partial(Datetime.remove_pad_dt, _dt, "%I"),
                "regex": r"(?P<hour_12>0|1|2|3|4|5|6|7|8|9|10|11|12)",
            },
            "%M": {
                "value": partial(_dt.strftime, "%M"),
                "regex": r"(?P<minute_pad>[0-6][0-9])",
            },
            "%-M": {
                "value": partial(Datetime.remove_pad_dt, _dt, "%M"),
                "regex": r"(?P<minute>\d{1,2})",
            },
            "%S": {
                "value": partial(_dt.strftime, "%S"),
                "regex": r"(?P<second_pad>[0-6][0-9])",
            },
            "%-S": {
                "value": partial(Datetime.remove_pad_dt, _dt, "%S"),
                "regex": r"(?P<second>\d{1,2})",
            },
            "%j": {
                "value": partial(_dt.strftime, "%j"),
                "regex": r"(?P<day_year_pad>[0-3][0-9][0-9])",
            },
            "%-j": {
                "value": partial(Datetime.remove_pad_dt, _dt, "%j"),
                "regex": r"(?P<day_year>\d{1,3})",
            },
            "%U": {
                "value": partial(_dt.strftime, "%U"),
                "regex": r"(?P<weeks_year_sun_pad>[0-5][0-9])",
            },
            "%W": {
                "value": partial(_dt.strftime, "%W"),
                "regex": r"(?P<weeks_year_mon_pad>[0-5][0-9])",
            },
            "%p": {
                "value": partial(_dt.strftime, "%p"),
                "regex": r"(?P<local>PM|AM)",
            },
            "%f": {
                "value": partial(_dt.strftime, "%f"),
                "regex": r"(?P<microsecond_pad>\d{6})",
            },
        }

    def _from_day_year(self, value: str) -> str:
        """Return date of year"""
        _this_year: datetime = datetime.strptime(
            self._dt_year, "%Y"
        ) + timedelta(days=int(value))
        self._dt_month = _this_year.strftime("%m")
        return _this_year.strftime("%d")

    def _from_week_year_mon(self, value: str) -> str:
        _this_week: str = (
            str(((int(self._dt_week) - 1) % 7) + 1) if self._dt_week else "1"
        )
        _this_year: datetime = datetime.strptime(
            f"{self._dt_year}-W{value}-{_this_week}", "%G-W%V-%u"
        )
        self._dt_month = _this_year.strftime("%m")
        self._dt_day = _this_year.strftime("%d")
        return _this_year.strftime("%w")

    def _from_week_year_sun(self, value: str) -> str:
        _this_year: datetime = datetime.strptime(
            f"{self._dt_year}-W{value}-{self._dt_week or '0'}", "%Y-W%U-%w"
        )
        self._dt_month = _this_year.strftime("%m")
        self._dt_day = _this_year.strftime("%d")
        return _this_year.strftime("%w")

    @staticmethod
    def remove_pad_dt(_dt: datetime, fmt: str) -> str:
        """Return padded datetime string that was formatted"""
        return remove_pad(_dt.strftime(fmt))


class Version(Formatter):
    """Version object for register process that implement formatter and
    parser.

        Version segments reference from Hatch:
        - release	        1.0.0
        - major	            2.0.0
        - minor	            1.1.0
        - micro/patch/fix   1.0.1
        - a/alpha           1.0.0a0
        - b/beta            1.0.0b0
        - c/rc/pre/preview	1.0.0rc0
        - r/rev/post	    1.0.0.post0
        - dev	            1.0.0.dev0

    .. ref::
        - The standard of versioning will align with the PEP0440
        (https://peps.python.org/pep-0440/)

        - Enhance the version object from the packaging library
        (https://packaging.pypa.io/en/latest/version.html)
    """

    base_fmt: str = "%m_%n_%c"

    base_attr_prefix: str = "vs"

    base_level: int = 3

    __slots__ = (
        "_vs_version",
        "_vs_epoch",
        "_vs_major",
        "_vs_minor",
        "_vs_micro",
        "_vs_pre",
        "_vs_post",
        "_vs_dev",
        "_vs_local",
    )

    def __repr__(self) -> str:
        _fmt: str = "v%m.%n.%c"
        if self._vs_epoch != "0":
            _fmt = f"%e{_fmt[1:]}"
        if self._vs_pre:
            _fmt = f"{_fmt}%q"
        if self._vs_post:
            _fmt = f"{_fmt}%p"
        if self._vs_dev:
            _fmt = f"{_fmt}%d"
        if self._vs_local:
            _fmt = f"{_fmt}%l"
        return f"<{self.__class__.__name__}.parse('{self.string}', '{_fmt}')>"

    @property
    def value(self) -> pck_version.Version:
        """"""
        return pck_version.parse(self.string)

    @property
    def string(self) -> str:
        _release: str = f"v{self._vs_major}.{self._vs_minor}.{self._vs_micro}"
        if self._vs_epoch != "0":
            _release = f"{self._vs_epoch}!{_release[1:]}"
        if self._vs_pre:
            _release = f"{_release}{self._vs_pre}"
        if self._vs_post:
            _release = f"{_release}{self._vs_post}"
        if self._vs_dev:
            _release = f"{_release}.{self._vs_dev}"
        if self._vs_local:
            _release = f"{_release}+{self._vs_local}"
        return _release

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        return {
            "epoch": {
                "value": lambda x: x.rstrip("!"),
                "level": 3,
            },
            "epoch_num": {
                "value": lambda x: x,
                "level": 3,
            },
            "epoch_default": {
                "value": self.default("0"),
                "level": 0,
            },
            "major": {
                "value": lambda x: x,
                "level": 3,
            },
            "major_default": {
                "value": self.default("0"),
                "level": 0,
            },
            "minor": {
                "value": lambda x: x,
                "level": 2,
            },
            "minor_default": {
                "value": self.default("0"),
                "level": 0,
            },
            "micro": {
                "value": lambda x: x,
                "level": 1,
            },
            "micro_default": {
                "value": self.default("0"),
                "level": 0,
            },
            "pre": {
                "value": lambda x: self.__from_prefix(x),
                "level": 0,
            },
            "post": {
                "value": lambda x: self.__from_prefix(x),
                "level": 0,
            },
            "post_num": {
                "value": lambda x: x,
                "level": 0,
            },
            "dev": {
                "value": lambda x: x,
                "level": 0,
            },
            "local": {
                "value": lambda x: x.lstrip("+"),
                "level": 0,
            },
            "local_str": {
                "value": lambda x: x,
                "level": 0,
            },
        }

    @staticmethod
    def formatter(
        version: Optional[pck_version.Version] = None,
    ) -> ReturnFormattersType:
        """Generate formatter that support mapping formatter,
            %f  : full version format with `%m_%n_%c`
            %-f : full version format with `%m-%n-%c`
            %m  : major number
            %n  : minor number
            %c  : micro number
            %e  : epoch release
            %q  : pre-release
            %p  : post release
            %-p : post release number
            %d  : dev release
            %l  : local release
            %-l : local release number

        :param version: a version value
        :type version: Optional[packaging.version.Version](=None)

        :rtype: Dict[str, Dict[str, Union[Callable, str]]]
        :return: the generated mapping values of all format strings
        """
        _version: pck_version.Version = version or pck_version.parse("0.0.1")
        return {
            "%f": {
                "value": lambda: (
                    f"{_version.major}_{_version.minor}_{_version.micro}"
                ),
                "cregex": "%m_%n_%c",
            },
            "%-f": {
                "value": lambda: (
                    f"{_version.major}_{_version.minor}_{_version.micro}"
                ),
                "cregex": "%m-%n-%c",
            },
            "%m": {
                "value": partial(str, _version.major),
                "regex": r"(?P<major>\d{1,3})",
            },
            "%n": {
                "value": partial(str, _version.minor),
                "regex": r"(?P<minor>\d{1,3})",
            },
            "%c": {
                "value": partial(str, _version.micro),
                "regex": r"(?P<micro>\d{1,3})",
            },
            "%e": {
                "value": lambda: f"{_version.epoch}!",
                "regex": r"(?P<epoch>[0-9]+!)",
            },
            "%-e": {
                "value": lambda: str(_version.epoch),
                "regex": r"(?P<epoch_num>[0-9]+)",
            },
            "%q": {
                "value": lambda: (
                    concat(map(str, _pre)) if (_pre := _version.pre) else ""
                ),
                "regex": (
                    r"(?P<pre>(a|b|c|rc|alpha|beta|pre|preview)[-_\.]?[0-9]+)"
                ),
            },
            "%p": {
                "value": lambda: str(_version.post or ""),
                "regex": (
                    r"(?P<post>(?:(post|rev|r)[-_\.]?[0-9]+)|(?:-[0-9]+))"
                ),
            },
            "%-p": {
                "value": lambda: str(_version.post or ""),
                "regex": r"(?P<post_num>[0-9]+)",
            },
            "%d": {
                "value": lambda: str(_version.dev or ""),
                "regex": r"(?P<dev>dev[-_\.]?[0-9]+)",
            },
            "%l": {
                "value": lambda: _version.local,
                "regex": r"(?P<local>\+[a-z0-9]+(?:[-_\.][a-z0-9]+)*)",
            },
            "%-l": {
                "value": lambda: f"+{_version.local}",
                "regex": r"(?P<local_str>[a-z0-9]+(?:[-_\.][a-z0-9]+)*)",
            },
        }

    @staticmethod
    def __from_prefix(value: str) -> str:
        """Return replaced value to standard prefix of pre- and post-format

        :param value: a pre- or post-format value
        :type value: str
        """
        for rep, matches in (
            ("a", ["alpha"]),
            ("b", ["beta"]),
            ("rc", ["c", "pre", "preview"]),
            ("post", ["rev", "r", "-"]),
        ):
            for letter in matches:
                if re.match(rf"{letter}[-_.]?[0-9]+", value):
                    return value.replace(letter, rep)
                elif re.match(rf"{rep}[-_.]?[0-9]+", value):
                    return value
        raise FormatterValueError(
            f"Convert prefix dose not valid for value `{value}`"
        )


class Naming(Formatter):
    """Naming object for register process that implement formatter and parser.

    note: A name value that parsing to this class should not contain any
    special characters, this will keep only.
    """

    base_fmt: str = "%n"

    base_attr_prefix: str = "nm"

    base_level: int = 5

    __slots__ = (
        "_nm_naming",
        "_nm_strings",
        "_nm_flats",
        "_nm_shorts",
        "_nm_vowels",
    )

    @property
    def value(self) -> str:
        return self.string

    @property
    def string(self) -> str:
        if self._nm_strings:
            return " ".join(self._nm_strings)
        elif self._nm_flats:
            return self._nm_flats[0]  # type: ignore[no-any-return]
        elif self._nm_shorts:
            return " ".join(self._nm_shorts)
        elif self._nm_vowels:
            return self._nm_vowels[0]  # type: ignore[no-any-return]
        return ""

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        return {
            "strings": {"value": lambda x: x.split(), "level": 5},
            "strings_upper": {
                "value": lambda x: x.lower().split(),
                "level": 5,
            },
            "strings_title": {
                "value": lambda x: x.lower().split(),
                "level": 5,
            },
            "strings_lower": {"value": lambda x: x.split(), "level": 5},
            "strings_camel": {
                "value": lambda x: self.__split_pascal_case(x),
                "level": 5,
            },
            "strings_pascal": {
                "value": lambda x: self.__split_pascal_case(x),
                "level": 5,
            },
            "strings_kebab": {
                "value": lambda x: x.split("-"),
                "level": 5,
            },
            "strings_kebab_upper": {
                "value": lambda x: x.lower().split("-"),
                "level": 5,
            },
            "strings_kebab_title": {
                "value": lambda x: x.lower().split("-"),
                "level": 5,
            },
            "strings_snake": {
                "value": lambda x: x.split("_"),
                "level": 5,
            },
            "strings_snake_upper": {
                "value": lambda x: x.lower().split("_"),
                "level": 5,
            },
            "strings_snake_title": {
                "value": lambda x: x.lower().split("_"),
                "level": 5,
            },
            "flats": {
                "value": lambda x: [x],
                "level": 1,
            },
            "flats_upper": {
                "value": lambda x: [x.lower()],
                "level": 1,
            },
            "shorts": {
                "value": lambda x: list(x),
                "level": 1,
            },
            "shorts_upper": {
                "value": lambda x: list(x.lower()),
                "level": 1,
            },
            "vowels": {
                "value": lambda x: [x],
                "level": 1,
            },
            "vowels_upper": {
                "value": lambda x: [x.lower()],
                "level": 1,
            },
        }

    @staticmethod
    def formatter(
        value: Optional[Union[str, List[str]]] = None,
    ) -> ReturnFormattersType:
        """Generate formatter that support mapping formatter,

            %n  : Normal name format
            %N  : Normal name upper case format
            %-N : Normal name title case format
            %u  : Upper case format
            %l  : Lower case format
            %t  : Title case format

            %a  : Shortname format
            %A  : Shortname upper case format

            %f  : Flat case format
            %F  : Flat upper case format

            %c  : Camel case format
            %-c : Upper first Camel case format

            %p  : Pascal case format

            %s  : Snake case format
            %S  : Snake upper case format
            %-S  : Snake title case format

            %k  : Kebab case format
            %K  : Kebab upper case format
            %-K  : Kebab title case format

            %v  : normal name removed vowel
            %V  : normal name removed vowel with upper case

        :param value:

        docs: https://gist.github.com/SuppieRK/a6fb471cf600271230c8c7e532bdae4b
        """
        _value: List[str] = (
            Naming.__prepare_value(value)
            if isinstance(value, str)
            else (value or [])
        )
        return {
            "%n": {
                "value": partial(Naming.__join_with, " ", _value),
                "cregex": "%l",
            },
            "%N": {
                "value": partial(
                    Naming.__join_with, " ", _value, lambda x: x.upper()
                ),
                "cregex": "%u",
            },
            "%-N": {
                "value": partial(
                    Naming.__join_with, " ", _value, lambda x: x.capitalize()
                ),
                "cregex": "%t",
            },
            "%u": {
                "value": partial(
                    Naming.__join_with, " ", _value, lambda x: x.upper()
                ),
                "regex": r"(?P<strings_upper>[A-Z0-9]+(?:\s[A-Z0-9]+)*)",
            },
            "%l": {
                "value": partial(Naming.__join_with, " ", _value),
                "regex": r"(?P<strings>[a-z0-9]+(?:\s[a-z0-9]+)*)",
            },
            "%t": {
                "value": partial(
                    Naming.__join_with, " ", _value, lambda x: x.capitalize()
                ),
                "regex": (
                    r"(?P<strings_title>[A-Z][a-z0-9]+(?:\s[A-Z]+[a-z0-9]*)*)"
                ),
            },
            "%a": {
                "value": partial(
                    Naming.__join_with, "", _value, lambda x: x[0]
                ),
                "regex": r"(?P<shorts>[a-z0-9]+)",
            },
            "%A": {
                "value": partial(
                    Naming.__join_with, "", _value, lambda x: x[0].upper()
                ),
                "regex": r"(?P<shorts_upper>[A-Z0-9]+)",
            },
            "%c": {
                "value": partial(Naming.camel_case, "_".join(_value)),
                "regex": (
                    r"(?P<strings_camel>[a-z]+"
                    r"((\d)|([A-Z0-9][a-z0-9]+))*([A-Z])?)"
                    # r"(?P<strings_camel>[a-z]+(?:[A-Z0-9]+[a-z0-9]+[A-Za-z0-9]*)*)"
                ),
            },
            "%-c": {
                "value": partial(Naming.pascal_case, "_".join(_value)),
                "cregex": "%p",
            },
            "%p": {
                "value": partial(Naming.pascal_case, "_".join(_value)),
                "regex": (
                    r"(?P<strings_pascal>[A-Z]"
                    r"([A-Z0-9]*[a-z][a-z0-9]*[A-Z]|"
                    r"[a-z0-9]*[A-Z][A-Z0-9]*[a-z])["
                    r"A-Za-z0-9]*)"
                    # r"(?P<strings_pascal>(?:[A-Z][a-z0-9]+)(?:[A-Z]+[a-z0-9]*)*)"
                ),
            },
            "%k": {
                "value": partial(Naming.__join_with, "-", _value),
                "regex": r"(?P<strings_kebab>[a-z0-9]+(?:-[a-z0-9]+)*)",
            },
            "%K": {
                "value": partial(
                    Naming.__join_with, "-", _value, lambda x: x.upper()
                ),
                "regex": r"(?P<strings_kebab_upper>[A-Z0-9]+(?:-[A-Z0-9]+)*)",
            },
            "%-K": {
                "value": partial(
                    Naming.__join_with, "-", _value, lambda x: x.capitalize()
                ),
                "regex": (
                    r"(?P<strings_kebab_title>"
                    r"[A-Z][a-z0-9]+(?:-[A-Z]+[a-z0-9]*)*)"
                ),
            },
            "%f": {
                "value": partial(Naming.__join_with, "", _value),
                "regex": r"(?P<flats>[a-z0-9]+)",
            },
            "%F": {
                "value": partial(
                    Naming.__join_with, "", _value, lambda x: x.upper()
                ),
                "regex": r"(?P<flats_upper>[A-Z0-9]+)",
            },
            "%s": {
                "value": partial(Naming.__join_with, "_", _value),
                "regex": r"(?P<strings_snake>[a-z0-9]+(?:_[a-z0-9]+)*)",
            },
            "%S": {
                "value": partial(
                    Naming.__join_with, "_", _value, lambda x: x.upper()
                ),
                "regex": r"(?P<strings_snake_upper>[A-Z0-9]+(?:_[A-Z0-9]+)*)",
            },
            "%-S": {
                "value": partial(
                    Naming.__join_with, "_", _value, lambda x: x.capitalize()
                ),
                "regex": (
                    r"(?P<strings_snake_title>"
                    r"[A-Z][a-z0-9]+(?:_[A-Z]+[a-z0-9]*)*)"
                ),
            },
            "%v": {
                "value": partial(re.sub, r"[aeiou]", "", "".join(_value)),
                "regex": r"(?P<vowel>[b-df-hj-np-tv-z]+)",
            },
            "%V": {
                "value": partial(
                    re.sub, r"[AEIOU]", "", "".join(_value).upper()
                ),
                "regex": r"(?P<vowel_upper>[B-DF-HJ-NP-TV-Z]+)",
            },
        }

    @staticmethod
    def pascal_case(snake_case: str) -> str:
        """Return a string value with pascal case that reference by
        `inflection`.
        """
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), snake_case)

    @staticmethod
    def camel_case(snake_case: str) -> str:
        """Return a string value with camel case with lower case first
        letter.
        """
        return snake_case[0].lower() + Naming.pascal_case(snake_case)[1:]

    @staticmethod
    def __join_with(
        by: str, values: List[str], func: Optional[Callable[[str], str]] = None
    ) -> str:
        return by.join(map(func, values)) if func else by.join(values)

    @staticmethod
    def __prepare_value(value: str) -> List[str]:
        """Return list of word that split from input value string"""
        result = re.sub(r"[^\-.\w\s]+", "", value)
        return re.sub(r"[\-._\s]]", " ", result).strip().split()

    @staticmethod
    def __split_pascal_case(value: str) -> List[str]:
        return (
            "".join([f" {c.lower()}" if c.isupper() else c for c in value])
            .strip()
            .split()
        )


class __BaseConstant(Formatter):
    """Constant object for register process that implement formatter and
    parser.
    """

    base_attr_prefix: str = "ct"

    base_formatter: Optional[ReturnFormattersType] = None

    __slots__ = ("_ct_constant",)

    def __init__(
        self,
        formats: Optional[Dict[str, Any]] = None,
    ) -> None:
        if not self.base_formatter:
            raise NotImplementedError(
                "The Constant object should define the `cls.base_formatter` "
                "before make a instance."
            )
        super().__init__(formats=formats)

    @property
    def value(self) -> str:
        return self.string

    @property
    def string(self) -> str:
        return str(
            "|".join(
                [
                    getter
                    for v in self.__slots__
                    if (getter := getattr(self, v)) and v != "_ct_constant"
                ]
            )
        )

    @property
    def priorities(
        self,
    ) -> ReturnPrioritiesType:
        """"""
        raise NotImplementedError(
            "Please implement priorities property for this sub-formatter class"
        )

    @classmethod
    def formatter(  # type: ignore[override]
        cls,
        value: Optional[str] = None,
    ) -> Optional[ReturnFormattersType]:
        return cls.base_formatter


def create_const(formatter: Union[Dict[str, str], Formatter]) -> ConstantType:
    if isinstance(formatter, Formatter):
        formatter = formatter.values()

    class CustomConstant(__BaseConstant):
        base_fmt: str = "".join(formatter.keys())

        __slots__ = (
            "_ct_constant",
            *[f"_ct_{convert_fmt_str(fmt)}" for fmt in formatter],
        )

        base_formatter = {
            fmt: {
                "regex": f"(?P<{convert_fmt_str(fmt)}>{formatter[fmt]})",
                "value": formatter[fmt],
            }
            for fmt in formatter.copy()
        }

        @property
        def priorities(self) -> ReturnPrioritiesType:
            return {
                **{
                    convert_fmt_str(fmt): {
                        "value": lambda x: x,
                        "level": 1,
                    }
                    for fmt in ["constant", *formatter]
                },
            }

    return CustomConstant


Constant: Callable[[Dict[str, str]], ConstantType] = create_const

EnvConstant: ConstantType = Constant(
    {
        "%d": "development",
        "%-d": "dev",
        "%s": "sit",
        "%-s": "sit",
        "%u": "uat",
        "%-u": "uat",
        "%p": "production",
        "%-p": "prd",
        "%t": "test",
        "%-t": "test",
        "%b": "sandbox",
        "%-b": "box",
        "%c": "poc",
    }
)


FORMATTERS: Dict[str, Type[Formatter]] = {
    "timestamp": Datetime,
    "version": Version,
    "serial": Serial,
    "naming": Naming,
    "envconst": EnvConstant,
}

FORMATTERS_ADJUST: Dict[str, Any] = {
    "timestamp": relativedelta,
    "serial": relativedelta,
}


class ExpectRegexValue(TypedDict):
    regex: str
    value: Callable[[], Any]


def extract_regex_with_value(
    fmt: FormatterType,
    value: Optional[Any] = None,
) -> Dict[str, RegexValue]:
    """Return extract data from `cls.regex` method and `cls.formatter`

    :param fmt: a formatter object
    :type fmt: FormatterType
    :param value:
    :type value: Optional[Any]

    :rtype: Dict[str, dict]
    :return: an extract data from `cls.regex` method and `cls.formatter`
    """
    regex: Dict[str, str] = fmt.regex()
    formatter: ReturnFormattersType = fmt.formatter(value)
    return {
        i: {
            "regex": regex[i],
            "value": caller(formatter[i]["value"]),
        }
        for i in formatter
    }


def adjust_datetime(
    self: OrderFormatter,
    metrics: Optional[Dict[str, int]] = None,
) -> OrderFormatter:
    """
    :param self: a OrderFormatter instance that want to adjust
    :type self: OrderFormatter
    :param metrics: a mapping of metric value
    :type metrics: Optional[dict](=None)

    :return: a adjusted OrderFormatter instance.
    """
    _metrics: Dict[str, int] = metrics or {}
    if "timestamp" not in self.data:
        raise FormatterArgumentError(
            "timestamp",
            (
                "order formatter object does not have `timestamp` in name "
                "formatter"
            ),
        )
    _replace: List[Formatter] = [
        self.FMTS["timestamp"].parse(
            **{
                "value": (
                    time_data.value
                    - relativedelta(**_metrics)  # type: ignore[arg-type]
                ).strftime("%Y%m%d %H%M%S"),
                "fmt": "%Y%m%d %H%M%S",
            }
        )
        for time_data in self.data["timestamp"]
    ]
    self.data["timestamp"] = _replace
    return self


def adjust_serial(
    self: OrderFormatter,
    metrics: Optional[Dict[str, int]] = None,
) -> OrderFormatter:
    """
    :param self: a OrderFormatter instance that want to adjust
    :type self: OrderFormatter
    :param metrics: a mapping of metric value
    :type metrics: Optional[dict](=None)

    :return: a adjusted OrderFormatter instance.
    """
    _metrics: Dict[str, int] = metrics or {}
    if "serial" not in self.data:
        raise FormatterArgumentError(
            "serial",
            "order formatter object does not have `serial` in name formatter",
        )
    _replace: List[Formatter] = [
        self.FMTS["serial"].parse(
            **{
                "value": (str(serial.value - relativeserial(**_metrics))),
                "fmt": "%n",
            }
        )
        for serial in self.data["serial"]
    ]
    self.data["serial"] = _replace
    return self


# TODO: implement adjust version logic when create relativeversion
def adjust_version(
    self: OrderFormatter,
    metrics: Optional[Dict[str, int]] = None,
):  # type: ignore  # no cov
    _metrics: Dict[str, int] = metrics or {}
    if "version" not in self.data:
        raise FormatterArgumentError(
            "version",
            "order formatter object does not have `version` in name formatter",
        )
    _replace: List[Formatter] = [
        self.FMTS["version"].parse(
            **{
                "value": "",
                "fmt": "",
            }
        )
    ]
    self.data["version"] = _replace
    return self


def adjust_name(
    self: OrderFormatter,
    metrics: Optional[Dict[str, str]] = None,
):  # type: ignore  # no cov
    _metrics: Dict[str, str] = metrics or {}
    if "name" not in self.data:
        raise FormatterArgumentError(
            "name",
            "order formatter object does not have `name` in name formatter",
        )
    _replace: List[Formatter] = [
        self.FMTS["name"].parse(
            **{
                "value": metrics,
                "fmt": "",
            }
        )
        for _ in self.data["name"]
    ]
    self.data["name"] = _replace
    return self


@total_ordering
class OrderFormatter:
    """Order formatter object from mapping dictionary.

    :param formatters: a mapping value
    :type formatters: dict

    :raises TypeError: if value of mapping does not match with dict or
        Formatter type.
    """

    __slots__ = ("data",)

    FMTS: Dict[str, FormatterType] = FORMATTERS

    def __init__(
        self,
        formatters: Dict[str, Union[Formatter, Dict[str, Any]]],
        *,
        auto_serial: bool = False,
    ):
        """Main initialize process of the ordering formatter object."""
        self.data: Dict[str, List[Formatter]] = {}
        for name, value in formatters.items():
            _name: str = re.sub(r"(_\d+)$", "", name)

            if _name not in self.FMTS:
                raise FormatterValueError(
                    f"value of key {_name} does not support"
                )

            name_value: List[Formatter] = self.data.setdefault(_name, [])
            if isinstance(value, Formatter):
                name_value.append(value)
            elif isinstance(value, dict):
                name_value.append(self.FMTS[_name].parse(**value))
            else:
                raise FormatterTypeError(
                    f"value of key {_name} does not support for type "
                    f"{type(value)}"
                )

        if auto_serial and "serial" not in self.data:
            self.data["serial"] = [Serial.parse("0", "%n")]

    def adjust(self, fmt: str, value: int):  # type: ignore  # no cov
        # TODO: merge adjust methods to dynamic method
        _ = value
        if fmt not in self.data:
            raise FormatterArgumentError(
                fmt,
                f"order object does not have `{fmt}` in name formatter",
            )
        return self

    def adjust_timestamp(self, metrics: Dict[str, int]) -> OrderFormatter:
        """Adjust timestamp value in the order formatter object

        :param metrics: a datetime value for this adjustment.
        :type metrics: Dict[str, int]
        """
        return adjust_datetime(self, metrics=metrics)

    def adjust_version(self, value: str) -> OrderFormatter:
        """Adjust version value in the order formatter object

        :param value: str : A version value for this adjustment with format
                '%m.%n.%c'.
        """
        if "version" not in self.data:
            raise FormatterArgumentError(
                "version",
                "order formatter object does not have `version` "
                "in name formatter",
            )
        _replace: List[Formatter] = []
        for version_data in self.data["version"]:
            # `versioning` must have 3 length of tuple
            versioning: Tuple[int, ...] = version_data.value.release
            _values: List[int] = [
                -99 if v == "*" else int(v) for v in value.split(".")
            ]
            _results: List[str] = []

            # TODO: create function: `relativedelta` for version object
            for _ in range(3):
                if _values[_] == 0:
                    _results.append("0")
                elif _values[_] == -99:
                    _results.append(str(versioning[_]))
                elif (major := (versioning[_] - _values[_])) < 0:
                    _results.append("0")
                else:
                    _results.append(str(major))
            _replace.append(
                self.FMTS["version"].parse(
                    **{"value": ".".join(_results), "fmt": "%m.%n.%c"}
                )
            )
        self.data["version"] = _replace
        return self

    def adjust_serial(self, value: int) -> OrderFormatter:
        """Adjust serial value in the order formatter object

        .. note:: This adjust method will replace old value to new.
        """
        return adjust_serial(self, metrics={"number": value})

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(formatters={self.data})>"

    def __str__(self) -> str:
        make_str: List[str] = [
            f"{k}={list(map(str, v))}" for k, v in self.data.items()
        ]
        return f"({', '.join(make_str)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.data == other.data

    def __lt__(self, other: OrderFormatter) -> bool:
        return next(
            (
                self.data[name] < other.data[name]
                for name in self.FMTS
                if (name in self.data and name in other.data)
            ),
            False,
        )

    def __le__(self, other: OrderFormatter) -> bool:
        return next(
            (
                self.data[name] <= other.data[name]
                for name in self.FMTS
                if (name in self.data and name in other.data)
            ),
            self.__eq__(other),
        )


def make_order_fmt(formats: Dict[str, FormatterType]) -> Type[OrderFormatter]:
    """Create new OrderFormatter class with a custom formatter mapping."""

    class CustomOrderFormatter(OrderFormatter):
        FMTS = formats

    return CustomOrderFormatter


class FormatterGroupParseArgs(TypedDict):
    fmt: FormatterType
    value: Optional[Union[str, Any]]


class FormatterGroupParseArgsDefault(TypedDict):
    fmt: FormatterType


@dataclass
class FormatterGroupData:
    """Formatter Data"""

    fmt: FormatterType
    value: Any

    @classmethod
    def parse(
        cls,
        value: Union[
            FormatterGroupParseArgs,
            FormatterGroupParseArgsDefault,
            FormatterType,
        ],
    ) -> FormatterGroupData:
        """Parse any value to this FormatterGroupData class

        :param value: a value that want to parse
        :type value: Union[dict, Type[Formatter]]
        """
        if isinstance(value, dict):
            return cls.parse_dict(value)
        return cls(
            fmt=value,
            value=None,
        )

    @classmethod
    def parse_dict(
        cls,
        values: Union[
            FormatterGroupParseArgs,
            FormatterGroupParseArgsDefault,
        ],
    ) -> FormatterGroupData:
        """Parse dict value to this FormatterGroupData class

        :param values: a dict value
        :type values: dict
        """
        return cls(
            fmt=values["fmt"],
            value=values.get("value"),
        )


# TODO: Can FormatterGroup handle order formatter property?
class FormatterGroup:
    """Group of any Formatters together with dynamic naming like timestamp
    for Datetime formatter object.

    :param formatters: a mapping of formatters.
    :type formatters: Dict[str, dict]
    """

    __slots__ = "formatters"

    def __init__(
        self,
        formatters: Dict[
            str,
            Union[
                FormatterGroupData,
                FormatterGroupParseArgs,
                FormatterGroupParseArgsDefault,
                FormatterType,
            ],
        ],
    ) -> None:
        """Main initialization get the formatter value, a mapping of name
        and formatter from input argument and generate the necessary
        attributes for define the value of this formatter group object.
        """
        self.formatters: Dict[str, FormatterGroupData] = {
            k: v
            if isinstance(v, FormatterGroupData)
            else FormatterGroupData.parse(v)
            for k, v in formatters.items()
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(self.formatters)})"

    @property
    def formats(self) -> Dict[str, FormatterType]:
        """Return the mapping of formatter and alias name of that format"""
        return {k: v.fmt for k, v in self.formatters.items()}

    @property
    def groups(self) -> Dict[str, Dict[str, RegexValue]]:
        """Return the groups of format value and extract Formatter
        values.
        """
        return {
            k: extract_regex_with_value(v.fmt, v.value)
            for k, v in self.formatters.items()
        }

    def parser(
        self,
        value: str,
        fmt: str,
        _max: bool = False,
    ) -> Dict[str, Formatter]:
        """Parse formatter by generator values like timestamp, version,
        or serial.

        :param value:
        :type value: str
        :param fmt:
        :type fmt: str
        :param _max: the max strategy for pick the maximum level from
            duplication formats in parser method.
        :type _max: bool(=False)

        :rtype: Dict[str, Formatter]
        """
        # TODO: Change special character value in format string like: |,
        #  () before passing to parser method.
        results, _ = self.__parser(value, fmt)
        if _max:
            return self.__parser_max(results=results)
        return self.__parser_normal(results=results)

    def __parser_normal(
        self,
        results: Dict[str, Dict[str, str]],
    ) -> Dict[str, Formatter]:
        """Parser with the normal strategy that combine all string value and
        format value together before parsing.

        :param results: result mapping of name and a pair of format values
        :type results: Dict[str, Dict[str, str]]
        """
        rs: Dict[str, Dict[str, str]] = {}
        for result in results:
            if (k := result.split("__", maxsplit=1)[0]) in rs:
                rs[k]["fmt"] += f"__{results[result]['fmt']}"
                rs[k]["value"] += f"__{results[result]['value']}"
            else:
                rs[k] = results[result]
        return {k: self.formatters[k].fmt.parse(**v) for k, v in rs.items()}

    def __parser_max(
        self,
        results: Dict[str, Dict[str, str]],
    ) -> Dict[str, Formatter]:
        """Parser with the max strategy that pick the maximum level from
        duplication formats in parser method.

        :param results: result mapping of name and a pair of format values
        :type results: Dict[str, Dict[str, str]]
        """
        rs: Dict[str, List[Formatter]] = {}
        for result in results:
            if (k := result.split("__", maxsplit=1)[0]) in rs:
                rs[k].append(self.formatters[k].fmt.parse(**results[result]))
            else:
                rs[k] = [self.formatters[k].fmt.parse(**results[result])]

        def get_level_value(fmt: Formatter) -> int:
            return fmt.level.value

        return {k: max(v, key=get_level_value) for k, v in rs.items()}

    def format(self, fmt: str) -> str:
        """Fill the formatter to value input argument.

        :param fmt: a string format value
        :type fmt: str
        """
        for fmt_name, fmt_mapping in self.groups.items():
            # Case I: contain formatter values.
            for _search in re.finditer(
                rf"(?P<name>{{{fmt_name}:(?P<format>[^{{}}]+)?}})", fmt
            ):
                fmt = fmt.replace(
                    f'{{{fmt_name}:{_search.groupdict()["format"]}}}',
                    self.__gen_sub_fmtter(
                        search=_search.groupdict(),
                        mapping=fmt_mapping,
                        key="value",
                    ),
                )
            # Case II: does not set any formatter value or duplicate format
            # name but does not set formatter.
            if re.search(rf"(?P<name>{{{fmt_name}}})", fmt):
                # Get the first format value from the formatter property.
                fmt = fmt.replace(
                    f"{{{fmt_name}}}",
                    caller(fmt_mapping[list(fmt_mapping.keys())[0]]["value"]),
                )
        return fmt

    def __parser(
        self,
        value: str,
        fmt: str,
    ) -> Tuple[Dict[str, Dict[str, str]], Dict[str, str]]:
        """Parse all formatter by generator that return getter and outer
        mapping.

        :param value:
        :type value: str
        :param fmt:
        :type fmt:  str

        :rtype: Tuple[Dict[str, Dict[str, str]], Dict[str, str]]
        :returns: a pair of mappings, like;

            {
                'name': {'fmt': '%s', 'value': 'data_engineer'},
                'name__1': {'fmt': '%a', 'value': 'de'},
                'datetime': {'fmt': '%Y%m%d', 'value': '20220101'}
            }

        """
        _fmt_filled, _fmt_getter = self.__gen_full_regex(fmt=fmt)

        # Parse regular expression to input value
        print("Before raise error:", rf"^{_fmt_filled}$")
        if not (_search := re.search(rf"^{_fmt_filled}$", value)):
            raise FormatterArgumentError(
                "format",
                f"{value!r} does not match with the format: "
                f"'^{_fmt_filled}$'",
            )

        _searches: Dict[str, str] = _search.groupdict()
        print("Group Dict:", _searches)
        print("Format Getter:", _fmt_getter)
        print("-----------")
        _fmt_outer: Dict[str, str] = {}
        for name in _searches.copy():
            if name in _fmt_getter:
                _fmt_getter[name]["value"] = _searches.pop(name)
            else:
                _fmt_outer[name] = _searches.pop(name)

        return _fmt_getter, _fmt_outer

    def __gen_full_regex(
        self,
        fmt: str,
    ) -> Tuple[str, Dict[str, Dict[str, str]]]:
        """Return the both of filled and getter format from the stage format
        value.

        :param fmt: a string format
        :type fmt: str

        :rtype: Tuple[str, Dict[str, Dict[str, str]]]
        :returns: a pair of format value and result of regular expression.
        """
        _get_format: Dict[str, Dict[str, str]] = {}
        for fmt_name, fmt_mapping in self.groups.items():
            print(
                "Regex Search",
                rf"(?P<name>{{{fmt_name}:?(?P<format>[^{{}}]+)?}})",
            )
            for _index, _search in enumerate(
                re.finditer(
                    rf"(?P<name>{{{fmt_name}:?(?P<format>[^{{}}]+)?}})",
                    fmt,
                ),
                start=1,
            ):
                # Search with mapping group with example:
                #   _search.groupdict() -->
                #   {'name': '{datetime:%Y%m%d}', 'format': '%Y%m%d'}
                _search_dict: Dict[str, str]
                _search_fmt_old: str = ""
                if _search_fmt := _search.group("format"):
                    # Case I: contain formatter values.
                    _search_fmt_old = f":{_search_fmt}"
                    _search_dict = _search.groupdict()
                else:
                    # Case II: does not set any formatter value.
                    _search_fmt = list(fmt_mapping.keys())[0]
                    _search_dict = {
                        **_search.groupdict(),
                        **{"format": _search_fmt},
                    }

                print("GroupDict:", _search_dict)
                _search_fmt_re: str = self.__gen_sub_fmtter(
                    search=_search_dict,
                    mapping=fmt_mapping,
                    key="regex",
                    index=_index,
                    suffix=fmt_name,
                )

                # Replace old format value with new mapping formatter
                # value.
                _fmt_name_index: str = f"{fmt_name}{self.__gen_index(_index)}"
                fmt = fmt.replace(
                    f"{{{fmt_name}{_search_fmt_old}}}",
                    f"(?P<{_fmt_name_index}>{_search_fmt_re})",
                    1,
                )

                # Keep the searched format value to getter format dict.
                _get_format[_fmt_name_index] = {"fmt": _search_fmt}
        return fmt, _get_format

    @staticmethod
    def __gen_index(index: int) -> str:
        """Return generated suffix string for duplication values.

        :param index: an index value.
        :type index: int

        :rtype: str
        :return: a suffix string value for adding to index name when name
            was duplicated from string formatter.
        """
        return f"__{str(index - 1)}" if index > 1 else ""

    @staticmethod
    def __gen_sub_fmtter(
        search: Dict[str, str],
        mapping: Dict[str, RegexValue],
        key: Literal["regex", "value"],
        index: int = 1,
        suffix: Optional[str] = None,
    ) -> str:
        """Loop method for find any sub-format from search input argument.

        :param search: a Match object from searching process.
        :type search: re.Match
        :param mapping: a formatter mapping value for getting matching key.
        :type mapping: Dict[
                str, Dict[str, Dict[str, Union[str, Callable[[], Any]]]]
            ]
        :param key: A key value for get value from the `mapping` parameter.
        :type key: str
        :param index:
        :type index: int(=1)

        :rtype: str
        :returns: a searched value
        """
        assert key in {
            "value",
            "regex",
        }, "the `key` argument should be 'value' or 'regex' only."
        _suffix: str = f"__{suffix.lower()}" if suffix else ""
        _search_re: str = search["format"]
        for _fmt in re.findall(r"(%[-+!*]?\w)", _search_re):
            try:
                _fmt_replace: str = caller(mapping[_fmt][key])
                if suffix or (index > 1):
                    _sr = re.search(
                        r"\(\?P<(?P<alias_name>\w+)>",
                        _fmt_replace,
                    )
                    _sr_re: str = _sr.group("alias_name")
                    _sr_idx: str = f"__{str(index - 1)}" if index > 1 else ""
                    _fmt_replace = re.sub(
                        rf"\(\?P<{_sr_re}>",
                        rf"(?P<{_sr_re}{_sr_idx}{_suffix}>",
                        _fmt_replace,
                    )
                _search_re = _search_re.replace(_fmt, _fmt_replace)
            except KeyError as err:
                raise FormatterArgumentError(
                    "format",
                    f"string formatter of {search['name']!r} does not "
                    f"support for key {str(err)} in configuration",
                ) from err
        return _search_re


class Formatters:  # type: ignore  # no cov
    ...


__all__ = (
    "FORMATTERS",
    "FORMATTERS_ADJUST",
    "Formatter",
    "FormatterType",
    "Serial",
    "Datetime",
    "Version",
    "Naming",
    "ConstantType",
    "Constant",
    "EnvConstant",
    "FormatterGroup",
    "OrderFormatter",
    "ReturnPrioritiesType",
    "ReturnFormattersType",
    "make_order_fmt",
)
