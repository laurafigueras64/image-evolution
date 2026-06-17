from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from backend.models import load_model
from backend.generator import generate_image

pipelines = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipelines["sd-v1-4"] = load_model("CompVis/stable-diffusion-v1-4")
    yield
    pipelines.clear()


app = FastAPI(lifespan=lifespan)


class GenerateRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate(request: GenerateRequest):
    pipeline = pipelines["sd-v1-4"]
    image_base64 = generate_image(pipeline, request.prompt)
    return {"model": "sd-v1-4", "image_base64": image_base64}
