#!/usr/bin/env python3
from api.qa_plus import router as qa_plus_router
from api.hello import router as hello_router

from public.usage import USAGE as html
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(hello_router, prefix="/ai")
app.include_router(qa_plus_router, prefix="/qa_plus")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def _root():
    return Response(content=html, media_type="text/html")
