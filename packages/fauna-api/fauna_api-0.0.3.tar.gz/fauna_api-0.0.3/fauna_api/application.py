import functools
import typing

from fastapi import APIRouter as Router
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing_extensions import ParamSpec

from .odm import FaunaModel

P = ParamSpec("P")

class FaunaAPI(FastAPI):
	"""Fully Serverless Backend"""
	def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
		super().__init__(*args, title="Fauna API", **kwargs)

		@self.on_event("startup")
		async def startup():
			await FaunaModel.create_all()

		@self.on_event("shutdown")
		async def shutdown():
			await FaunaModel.cleanup()

	def sse(self,path:str):
		def decorator(func:typing.Callable[P,typing.AsyncIterable[str]]) -> typing.Callable[P,StreamingResponse]:
			@functools.wraps(func)
			async def wrapper(*args:P.args,**kwargs:P.kwargs) -> StreamingResponse:
				return StreamingResponse(
					func(*args,**kwargs),
					media_type="text/event-stream"
				)
			self.get(path)(wrapper)
			return wrapper
		return decorator
	

class APIRouter(Router):
	def sse(self,path:str):
		def decorator(func:typing.Callable[P,typing.AsyncIterable[str]]) -> typing.Callable[P,StreamingResponse]:
			@functools.wraps(func)
			async def wrapper(*args:P.args,**kwargs:P.kwargs) -> StreamingResponse:
				return StreamingResponse(
					func(*args,**kwargs),
					media_type="text/event-stream"
				)
			self.get(path)(wrapper)
			return wrapper
		return decorator