import asyncio
from typing import AsyncGenerator, Callable, Coroutine, Dict, Union

from typing_extensions import ParamSpec

from .client import FaunaClient
from .lib.objects import Query, Ref, SetRef
from .typedefs import EventTypes

P = ParamSpec("P")


class Subscription(object):
	def __init__(self, client: FaunaClient):
		self.client = client
		self._handlers: Dict[EventTypes, Callable[[Query], AsyncGenerator[str, None]]] = {}
		self._handlers["set"] = self.stream

	def on(self, event: EventTypes) -> Callable[[Callable[[Query], AsyncGenerator[str, None]]], Callable[[Query], AsyncGenerator[str, None]]]:
		def decorator(func: Callable[[Query], AsyncGenerator[str, None]]) -> Callable[[Query], AsyncGenerator[str, None]]:
			self._handlers[event] = func
			return func
		return decorator

	
	async def stream(self, query: Query) -> AsyncGenerator[Dict[str, str], None]:
		while True:
			async for event in self.client.stream(query):
				yield event
			await asyncio.sleep(1)