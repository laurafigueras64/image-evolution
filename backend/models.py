import torch
from diffusers import DiffusionPipeline

MODEL_REGISTRY = {
    "sd-tiny": "segmind/tiny-sd",
    "sd-small": "OFA-Sys/small-stable-diffusion-v0",
    "sd-turbo": "stabilityai/sd-turbo",
}


def load_model(model_key: str) -> DiffusionPipeline:
    model_id = MODEL_REGISTRY[model_key]
    try:
        # fp16 variant halves the download/disk size vs. the fp32 weights
        pipeline = DiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16",
        )
    except (ValueError, EnvironmentError):
        pipeline = DiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
        )
    pipeline = pipeline.to("mps")
    return pipeline


def load_all_models() -> dict:
    return {key: load_model(key) for key in MODEL_REGISTRY}
