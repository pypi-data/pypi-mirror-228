from fastapi import FastAPI
from mangum import Mangum

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

	
	@property
	def handler(self):
		return Mangum(self)
	
	def __call__(self, *args, **kwargs):
		return self.handler(*args, **kwargs)
	
	def __repr__(self):
		return f"<FaunaAPI: {self.title}>"