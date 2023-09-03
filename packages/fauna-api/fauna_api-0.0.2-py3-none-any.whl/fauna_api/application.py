from fastapi import FastAPI

from .odm import FaunaModel


class FaunaAPI(FastAPI):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		@self.on_event("startup")
		async def startup():
			await FaunaModel.create_all()

		@self.on_event("shutdown")
		async def shutdown():
			await FaunaModel.cleanup()
