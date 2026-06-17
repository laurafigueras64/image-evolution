from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.models import load_all_models
from backend.generator import generate_image

MODEL_LABELS = {
    "sd-v1-4": "2022 · SD v1.4",
    "sd-v2-1": "2022 · SD v2.1",
    "sdxl":    "2023 · SDXL",
}

pipelines = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    pipelines.update(load_all_models())
    yield
    pipelines.clear()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class GenerateRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate(request: GenerateRequest):
    results = []
    for model_key, label in MODEL_LABELS.items():
        image_base64 = generate_image(pipelines[model_key], request.prompt)
        results.append({
            "model": model_key,
            "label": label,
            "image_base64": image_base64,
        })
    return {"results": results}
