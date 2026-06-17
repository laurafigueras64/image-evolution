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
1. CompVis/stable-diffusion-v1-4
2. stabilityai/stable-diffusion-2-1
3. stabilityai/stable-diffusion-xl-base-1.0

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
