# Image Evolution

A small web app that takes one text prompt and runs it through three
Stable-Diffusion-family models of increasing quality, so you can watch
image generation "evolve" for the same prompt in a single request.

## How it works

- FastAPI backend loads three Diffusers pipelines **once** at startup and
  keeps them in memory (`backend/models.py`).
- A single `POST /generate` call runs the prompt through all three models
  sequentially and returns three base64-encoded PNGs (`backend/main.py`,
  `backend/generator.py`).
- A static HTML/CSS/JS frontend calls that endpoint and renders the three
  results side by side as they come back (`frontend/`).
- Inference runs on Apple Silicon via PyTorch's MPS backend.

## Models

Chosen to keep load time and disk usage low on a local M1 machine — the
project originally used full-size SD 1.4 / 2.1 / SDXL, which was too slow
to run per-request and too heavy to keep cached on disk.

| Order | Model | Why |
|---|---|---|
| 1 | [`segmind/tiny-sd`](https://huggingface.co/segmind/tiny-sd) | Distilled from SD 1.5, smallest and fastest, lowest quality |
| 2 | [`OFA-Sys/small-stable-diffusion-v0`](https://huggingface.co/OFA-Sys/small-stable-diffusion-v0) | Compressed SD, roughly half the size of full SD, mid quality |
| 3 | [`stabilityai/sd-turbo`](https://huggingface.co/stabilityai/sd-turbo) | Step-distilled from SD 2.1 — highest quality of the three, and the fastest, since it needs only **1** inference step |

All three are downloaded with `variant="fp16"` where the repo publishes
one, so only the half-size fp16 weights are pulled instead of the fp32
checkpoints.

`sd-turbo` requires `guidance_scale=0.0` (already set in
`backend/generator.py`) — using the default guidance scale on this model
produces broken/oversaturated images, it's not optional.

## Project structure

```
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
└── outputs/            # Generated images — gitignored
```

## Setup

Requires Python 3.11 and an Apple Silicon Mac (MPS backend).

```bash
# from the project root
python3.11 -m venv .env-image-evolution
source .env-image-evolution/bin/activate
pip install -r requirements.txt
```

If you already have the `.env-image-evolution` venv from before, just
activate it — no new dependencies were added, only model IDs changed.

## Running it

**1. Start the backend** (from the project root, so the `backend` package
resolves):

```bash
source .env-image-evolution/bin/activate
uvicorn backend.main:app --reload
```

The first request after a fresh checkout will download the three models
from Hugging Face (a few GB total) and cache them under
`~/.cache/huggingface/hub`. Subsequent startups just load from that cache
into memory, which still takes a bit — the server isn't ready to serve
until the lifespan startup hook finishes loading all three pipelines.

**2. Open the frontend**

Open `frontend/index.html` directly in a browser (double-click it, or
`open frontend/index.html` on macOS). It calls the backend at
`http://127.0.0.1:8000`, so no separate frontend server is needed.

## Testing / verifying it works

**Quick backend-only check** with curl, once the server is up:

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a red apple on a wooden table"}'
```

You should get back JSON with a `results` array of 3 objects, each with
`model`, `label`, and a (long) `image_base64` string.

To save the images out and view them instead of eyeballing base64:

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a red apple on a wooden table"}' \
  -o outputs/response.json

python3 - <<'EOF'
import base64, json

with open("outputs/response.json") as f:
    data = json.load(f)

for r in data["results"]:
    path = f"outputs/{r['model']}.png"
    with open(path, "wb") as out:
        out.write(base64.b64decode(r["image_base64"]))
    print("wrote", path)
EOF
```

**Full UI check**:

1. Start the backend as above and wait for it to log that it's ready.
2. Open `frontend/index.html` in a browser.
3. Enter a short prompt (e.g. "a red apple on a wooden table") and click
   **Generate**.
4. All three cards should show spinners immediately, then fill in with
   images as each model finishes — `sd-tiny` first, then `sd-small`, then
   `sd-turbo` last (they run sequentially in that order).
5. Check the browser console and the uvicorn logs for errors if a card
   never fills in.

## Known trade-offs

- Models run **sequentially**, not in parallel, so total request time is
  roughly the sum of all three models' inference time.
- Swapping in smaller/distilled models trades some image quality and
  prompt fidelity for speed and disk space — this is a demo/showcase app,
  not a quality benchmark.
- Old cached weights from earlier experiments (full SD 1.4, Openjourney
  v4) may still be sitting in `~/.cache/huggingface/hub` if you've run
  this project before with a different model lineup. Safe to delete if
  you want the disk space back — check `du -sh ~/.cache/huggingface/hub/*`
  first to see what's there.
