import torch
from diffusers import DiffusionPipeline

MODEL_REGISTRY = {
    "sd-v1-4": "CompVis/stable-diffusion-v1-4",
    "sd-v2-1": "stabilityai/stable-diffusion-2-1",
    "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
}


def load_model(model_key: str) -> DiffusionPipeline:
    model_id = MODEL_REGISTRY[model_key]
    pipeline = DiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
    )
    pipeline = pipeline.to("mps")
    return pipeline


def load_all_models() -> dict:
    return {key: load_model(key) for key in MODEL_REGISTRY}
