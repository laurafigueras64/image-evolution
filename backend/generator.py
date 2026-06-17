import base64
import io

from diffusers import DiffusionPipeline


def generate_image(pipeline: DiffusionPipeline, prompt: str) -> str:
    result = pipeline(prompt, num_inference_steps=20)
    image = result.images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
