import torch
from diffusers import DiffusionPipeline


def load_model(model_id: str) -> DiffusionPipeline:
    pipeline = DiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
    )
    pipeline = pipeline.to("mps")
    return pipeline
