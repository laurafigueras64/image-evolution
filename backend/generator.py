import base64
import io

from diffusers import DiffusionPipeline

GENERATION_PARAMS = {
    # Few steps + low resolution so the distilled model's weaknesses actually show
    "sd-tiny": {"num_inference_steps": 6, "guidance_scale": 6.0, "height": 256, "width": 256},
    "sd-small": {"num_inference_steps": 12, "guidance_scale": 7.0, "height": 384, "width": 384},
    # sd-turbo is step-distilled: 1-4 steps, and guidance must be disabled
    "sd-turbo": {"num_inference_steps": 1, "guidance_scale": 0.0},
}


def generate_image(pipeline: DiffusionPipeline, prompt: str, model_key: str) -> str:
    params = GENERATION_PARAMS.get(model_key, {"num_inference_steps": 20, "guidance_scale": 7.5})
    result = pipeline(prompt, **params)
    image = result.images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
