import asyncio
import functools
import os
import platform
import sys
from dataclasses import dataclass, field
from threading import Lock
from typing import *

import httpx
from typing_extensions import ParamSpec

from .json import *
from .lib.objects import Expr
from .typedefs import LazyProxy
from .utils import get_loop

T = TypeVar("T")
P = ParamSpec("P")
FaunaMethod = Literal["query", "stream"]


def singleton(cls: T) -> T:
	instance = None
	lock = Lock()

	@functools.wraps(cls)
	def wrapper(*args, **kwargs):
		nonlocal instance
		if instance is None:
			with lock:
				if instance is None:
					instance = cls(*args, **kwargs)
		return instance

	return wrapper


class RuntimeEnvHeader:
	def __init__(self):
		self.pythonVersion = "{0}.{1}.{2}-{3}".format(*sys.version_info)
		self.driverVersion = "4.5.1"
		self.env = self.getRuntimeEnv()
		self.os = "{0}-{1}".format(platform.system(), platform.release())

	def getRuntimeEnv(self):
		env = [
			{
				"name": "Netlify",
				"check": lambda: "NETLIFY_IMAGES_CDN_DOMAIN" in os.environ,
			},
			{"name": "Vercel", "check": lambda: "VERCEL" in os.environ},
			{
				"name": "Heroku",
				"check": lambda: "PATH" in os.environ
				and ".heroku" in os.environ["PATH"],
			},
			{
				"name": "AWS Lambda",
				"check": lambda: "AWS_LAMBDA_FUNCTION_VERSION" in os.environ,
			},
			{
				"name": "GCP Cloud Functions",
				"check": lambda: "_" in os.environ and "google" in os.environ["_"],
			},
			{
				"name": "GCP Compute Instances",
				"check": lambda: "GOOGLE_CLOUD_PROJECT" in os.environ,
			},
			{
				"name": "Azure Cloud Functions",
				"check": lambda: "WEBSITE_FUNCTIONS_AZUREMONITOR_CATEGORIES"
				in os.environ,
			},
			{
				"name": "Azure Compute",
				"check": lambda: "ORYX_ENV_TYPE" in os.environ
				and "WEBSITE_INSTANCE_ID" in os.environ
				and os.environ["ORYX_ENV_TYPE"] == "AppService",
			},
		]

		try:
			recognized = next(e for e in env if e.get("check")())
			if recognized is not None:
				return recognized.get("name")
		except:
			return "Unknown"

	def __str__(self):
		return "driver=python-{0}; runtime=python-{1} env={2}; os={3}".format(
			self.driverVersion, self.pythonVersion, self.env, self.os
		).lower()


@singleton
@dataclass
class FaunaClient(LazyProxy[httpx.AsyncClient]):
	secret: str = field(default_factory=lambda: os.environ["FAUNA_SECRET"])
	_session: Optional[httpx.AsyncClient] = None
	_session_creation_lock: asyncio.Lock = asyncio.Lock()

	async def __load__(self, method: str) -> httpx.AsyncClient:
		return await self._create_session(method)

	async def _create_session(self, method: FaunaMethod) -> httpx.AsyncClient:
		headers = {
			"X-FaunaDB-Client": str(RuntimeEnvHeader()),
			"Authorization": f"Bearer {self.secret}",
		}
		timeout = httpx.Timeout(10)

		if method == "query":
			return httpx.AsyncClient(base_url="https://db.fauna.com",headers=headers, timeout=timeout)

		if method == "stream":
			stream_headers = {
				"Keep-Alive": "timeout=5",
				"Accept-Encoding": "gzip",
				"Content-Type": "application/json;charset=utf-8",
				"X-Fauna-Driver": "python",
				"X-FaunaDB-API-Version": "4",
			}
			http2 = True
			return httpx.AsyncClient(
				base_url="https://db.fauna.com",
				headers={**headers, **stream_headers}, timeout=timeout, http2=http2
			)

	async def query(self, expr: Expr) -> Any:
		async with self._session_creation_lock:
			if self._session is None:
				self._session = await self.__load__("query")
			response = await self._session.post("/", data=to_json(expr))
			response.raise_for_status()
			data = response.json()
			if data.get("resource") is not None:
				return data["resource"]
			if data.get("errors") is not None:
				return data["errors"]
			return data

	async def stream(self, expr: Expr) -> AsyncGenerator[str, None]:
		async with self._session_creation_lock:
			if self._session is None:
				self._session = await self.__load__("stream")
			async with self._session.stream("POST","/", data=to_json(expr)) as response:
				response.raise_for_status()
				async for line in response.aiter_lines():
					yield line
					if line == "":
						break

	def __del__(self):
		if self._session is not None:
			get_loop().run_until_complete(self.cleanup())

	async def cleanup(self):
		if self._session is not None:
			await self._session.aclose()
			self._session = None