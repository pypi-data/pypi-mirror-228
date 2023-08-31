# -------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------
# mypy: disable-error-code="attr-defined"
"""
The standard object that use for keep main value for compare data in formatter.
"""
from __future__ import annotations

import re
from functools import total_ordering
from typing import (
    Any,
    ClassVar,
    Optional,
    Pattern,
    Union,
)


class VersionFormat:  # type: ignore  # no cov
    """Version object that build from below packages:
    - packaging
    - semver
    """

    _REGEX_TEMPLATE: ClassVar[
        str
    ] = r"""
        ^
        (?P<major>0|[1-9]\d*)
        (?:
            \.
            (?P<minor>0|[1-9]\d*)
            (?:
                \.
                (?P<patch>0|[1-9]\d*)
            ){opt_patch}
        ){opt_minor}
        (?:-(?P<prerelease>
            (?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)
            (?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*
        ))?
        (?:\+(?P<build>
            [0-9a-zA-Z-]+
            (?:\.[0-9a-zA-Z-]+)*
        ))?
        $
    """
    #: Regex for a semver version
    _REGEX: ClassVar[Pattern[str]] = re.compile(
        _REGEX_TEMPLATE.format(opt_patch="", opt_minor=""),
        re.VERBOSE,
    )
    #: Regex for a semver version that might be shorter
    _REGEX_OPTIONAL_MINOR_AND_PATCH: ClassVar[Pattern[str]] = re.compile(
        _REGEX_TEMPLATE.format(opt_patch="?", opt_minor="?"),
        re.VERBOSE,
    )
    ...


@total_ordering
class relativeserial:
    """Relative delta for the Serial object.

    .. examples::

        >>> 5 + relativeserial(**{"number": 5})
        10

        >>> relativeserial(**{"number": 5}) + 5
        10

        >>> relativeserial(**{"number": 5}) - 5
        0

        >>> relativeserial(**{"number": 5}) - 12
        -7

        >>> 10 - relativeserial(**{"number": 5})
        5

        >>> 2 - relativeserial(**{"number": 5})
        -3

        >>> -relativeserial(**{"number": 5})
        <relativeserial(number=-5)>

    """

    def __init__(self, number: int = 0) -> None:
        self.number: int = number

    def __hash__(self) -> int:
        return hash(self.number)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(number={self.number})>"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.number == other
        elif isinstance(other, relativeserial):
            return self.number == other.number
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.number < other
        elif isinstance(other, relativeserial):
            return self.number < other.number
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.number <= other
        elif isinstance(other, relativeserial):
            return self.number <= other.number
        return NotImplemented

    def __neg__(self) -> relativeserial:
        return self.__class__(number=-self.number)

    def __add__(
        self,
        other: Union[int, relativeserial],
    ) -> Union[int, relativeserial]:
        if isinstance(other, int):
            return self.__radd__(other)
        return self.__class__(number=(self.number + other.number))

    def __sub__(
        self,
        other: Union[int, relativeserial],
    ) -> Union[int, relativeserial]:
        if isinstance(other, int):
            return self.number - other
        return self.__class__(number=(self.number - other.number))

    def __radd__(self, other: int) -> int:
        return other + self.number

    def __rsub__(self, other: int) -> int:
        return other - self.number


# TODO: create relativeversion
# @total_ordering
class relativeversion:  # no cov
    def __init__(
        self,
        epoch: int = 0,
        major: int = 0,
        minor: int = 0,
        micro: int = 0,
        alpha: Optional[int] = None,
        beta: Optional[int] = None,
        pre: Optional[int] = None,
        post: Optional[int] = None,
    ) -> None:
        self.epoch: int = epoch
        self.major: int = major
        self.minor: int = minor
        self.micro: int = micro
        self.alpha: Optional[int] = alpha
        self.beta: Optional[int] = beta
        self.pre: Optional[int] = pre
        self.post: Optional[int] = post

    def __hash__(self) -> int:
        release = f"{self.major}.{self.minor}.{self.micro}"
        if self.alpha:
            release = f"{release}.a{self.alpha}"
        if self.beta:
            release = f"{release}.b{self.beta}"
        if self.pre:
            release = f"{release}.pre{self.pre}"
        if self.post:
            release = f"{release}.post{self.post}"
        return hash(release)  # type: ignore

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}()>"

    def __eq__(self, other) -> bool:  # type: ignore
        if isinstance(other, relativeversion):
            return (
                self.epoch == other.epoch
                and self.major == other.major
                and self.minor == other.minor
                and self.micro == other.micro
                and self.alpha == other.alpha
            )
        return ...  # type: ignore

    def __lt__(self, other: Any) -> bool:  # type: ignore
        return ...  # type: ignore

    def __le__(self, other: Any) -> bool:  # type: ignore
        return ...  # type: ignore

    def __neg__(self) -> relativeversion:
        return self.__class__(
            epoch=-self.epoch,
            major=-self.major,
            minor=-self.minor,
            micro=-self.micro,
            alpha=(-self.alpha if self.alpha else None),
            beta=(-self.beta if self.beta else None),
            pre=(-self.pre if self.pre else None),
            post=(-self.post if self.post else None),
        )  # type: ignore

    def __add__(
        self,
        other: Union[relativeversion],
    ):  # type: ignore
        return ...

    def __sub__(
        self,
        other: Union[relativeversion],
    ):  # type: ignore
        return ...

    def __radd__(self, other):  # type: ignore
        return ...

    def __rsub__(self, other):  # type: ignore
        return ...


__all__ = ("relativeserial",)
