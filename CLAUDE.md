# Image Evolution Project

## Project Goal
A web app where users enter a short prompt and three AI models generate 
images sequentially, each better than the last — showcasing the evolution 
of image generation models.

## Tech Stack
- Python 3.11
- FastAPI + Uvicorn (backend server)
- HuggingFace Diffusers + PyTorch with MPS backend (Apple M1)
- Vanilla HTML, CSS, and JavaScript — no frameworks

## Models (loaded once at server startup, in quality order)
Chosen to keep local disk usage and MPS inference time low — full-size
SD 1.4/2.1/SDXL was too slow and too heavy to load on this machine.
1. segmind/tiny-sd — distilled, smallest and fastest, lowest quality
2. OFA-Sys/small-stable-diffusion-v0 — compressed SD, mid quality
3. stabilityai/sd-turbo — step-distilled from SD 2.1; highest quality
   despite running in 1 inference step (guidance_scale must be 0.0)

Loaded with `variant="fp16"` where available so only the fp16 weights are
downloaded, roughly halving disk usage vs. the fp32 checkpoints.

## Project Structure
image-evolution/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── backend/
│   ├── main.py        # FastAPI app and routes
│   ├── models.py      # Model loading and management
│   └── generator.py   # Image generation logic
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── outputs/           # Generated images — gitignored

## Conventions
- All code and comments in English
- Models are loaded into memory once at startup, not per request
- Images are returned as base64 strings in the JSON response
- Use MPS device for all torch operations on Apple M1
- Keep functions small and single-responsibility
