#!/usr/bin/env python3
from api.qa_plus import router as qa_plus_router
from api.hello import router as hello_router
from api.curd_demo import router as curd_router

from public.usage import USAGE as html
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from settings.config import settings

app = FastAPI()

app.include_router(hello_router, prefix="/ai")
app.include_router(qa_plus_router, prefix="/qa_plus")
app.include_router(curd_router, prefix="/curd")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allows all origins
    # allow_credentials=True,
    # allow_methods=["*"],  # Allows all methods
    # allow_headers=["*"],  # Allows all headers
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

@app.get("/")
def _root():
    return Response(content=html, media_type="text/html")
