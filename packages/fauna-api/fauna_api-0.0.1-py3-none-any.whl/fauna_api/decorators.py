"""
Flaskaesque helper functions for aiohttp.
"""
import asyncio
import functools
import typing
from concurrent.futures import ProcessPoolExecutor
from typing import Any

from typing_extensions import ParamSpec

T = typing.TypeVar("T")
P = ParamSpec("P")


def async_io(
    func: typing.Callable[P, T]
) -> typing.Callable[P, typing.Coroutine[T, Any, Any]]:
    """
    Decorator to convert an IO bound function to a coroutine by running it in a thread pool.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


def async_cpu(
    func: typing.Callable[P, T]
) -> typing.Callable[P, typing.Coroutine[T, Any, Any]]:
    """
    Decorator to convert a CPU bound function to a coroutine by running it in a process pool.
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        with ProcessPoolExecutor() as pool:
            try:
                return await asyncio.get_running_loop().run_in_executor(
                    pool, func, *args, **kwargs
                )
            except RuntimeError:
                return await asyncio.get_event_loop().run_in_executor(
                    pool, func, *args, **kwargs
                )

    return wrapper