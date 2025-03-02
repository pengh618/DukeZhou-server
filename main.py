#!/usr/bin/env python3
from api import qa_plus
from public.usage import USAGE as html
from api.hello import router as hello_router
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(hello_router, prefix="/ai")
app.include_router(qa_plus.router, prefix="/qa_plus")

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
