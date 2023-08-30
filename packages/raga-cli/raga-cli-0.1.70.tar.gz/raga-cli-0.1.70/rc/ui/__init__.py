from contextlib import contextmanager
from typing import (
    Any,
    Dict,
    Optional,
    TextIO,
)

import colorama



@contextmanager
def disable_colorama():
    import sys

    colorama.deinit()
    try:
        yield
    finally:
        if sys.stdout:
            sys.stdout.flush()
        if sys.stderr:
            sys.stderr.flush()
        colorama.reinit()


class Formatter:
    def __init__(
        self, theme: Optional[Dict] = None, defaults: Optional[Dict] = None
    ) -> None:
        from collections import defaultdict

        theme = theme or {
            "success": {"color": "green", "style": "bold"},
            "warn": {"color": "yellow"},
            "error": {"color": "red", "style": "bold"},
        }
        self.theme = defaultdict(lambda: defaults or {}, theme)

    def format(  # noqa: A003
        self, message: str, style: Optional[str] = None, **kwargs
    ) -> str:
        from dvc.utils import colorize

        return colorize(message, **self.theme[style])


class Console:
    def __init__(
        self, formatter: Optional[Formatter] = None, enable: bool = False
    ) -> None:
        from contextvars import ContextVar

        self.formatter: Formatter = formatter or Formatter()
        self._enabled: bool = enable
        self._paginate: ContextVar[bool] = ContextVar("_paginate", default=False)

    def enable(self) -> None:
        self._enabled = True

    def success(self, message: str) -> None:
        self.write(message, style="success")

    def error(self, message: str) -> None:
        self.error_write(message, style="error")

    def warn(self, message: str) -> None:
        self.error_write(message, style="warn")

    def error_write(
        self,
        *objects: Any,
        style: Optional[str] = None,
        sep: Optional[str] = None,
        end: Optional[str] = None,
        styled: bool = False,
        force: bool = True,
    ) -> None:
        return self.write(
            *objects,
            style=style,
            sep=sep,
            end=end,
            stderr=True,
            force=force,
            styled=styled,
        )


    def write(
        self,
        *objects: Any,
        style: Optional[str] = None,
        sep: Optional[str] = None,
        end: Optional[str] = None,
        stderr: bool = False,
        force: bool = False,
        styled: bool = False,
        file: Optional[TextIO] = None,
    ) -> None:
        import sys

        from dvc.progress import Tqdm

        sep = " " if sep is None else sep
        end = "\n" if end is None else end
        if not self._enabled and not force:
            return
        values = (self.formatter.format(obj, style) for obj in objects)
        return print(*values, sep=sep, end=end, file=file)


ui = Console()
