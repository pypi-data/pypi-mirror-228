from __future__ import annotations

from typing import Any, Callable, Iterable, List, Union

concat: Callable[[Union[List[str], Iterable[str]]], str] = "".join


def itself(x: Any = None) -> Any:
    """Return itself value"""
    return x


def caller(func: Union[Callable[[], Any], Any]) -> Any:
    """Call function if it was callable

    .. usage::
        >>> some_func = lambda: 100
        >>> caller(some_func)
        100
    """
    return func() if callable(func) else func
