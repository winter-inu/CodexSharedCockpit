from pathlib import Path
import json
import time
import urllib.error
import urllib.request
import uuid


SERVER = "http://127.0.0.1:8188"
ROOT = Path(r"F:\CodexSharedCockpit")
KEYFRAME_DIR = ROOT / "episodes" / "season_01" / "episode_01" / "keyframes" / "op06_op14_main_v1"


PROMPTS = {
    "OP06": (
        "cinematic live action film still, old north railway station hall, warm afternoon sunlight through tall windows, "
        "East Asian mother and little girl holding hands, subtle crowd movement, warning screen beginning to glow cold white, "
        "realistic people, handheld camera, shallow depth of field, high detail, natural motion, movie scene"
    ),
    "OP07": (
        "cinematic live action, old railway station alarm, crowd looks up and starts moving, cold white warning light, "
        "mother holding little girl, tense atmosphere, realistic motion, film scene"
    ),
    "OP08": (
        "cinematic live action, chaotic crowd moving backward in old station, mother protecting little girl in pink hoodie, "
        "people rushing past, realistic motion blur, tense movie scene"
    ),
    "OP09": (
        "cinematic close-up live action, little girl's right shoe falling off in crowd chaos, old station floor, "
        "realistic movement, dramatic warm and cold mixed light, film scene"
    ),
    "OP10": (
        "cinematic live action, tall isolation gate rising in old railway station, mother and child separated by crowd, "
        "cold warning light, realistic mechanical movement, tense movie scene"
    ),
    "OP11": (
        "cinematic close-up live action, mother and daughter hands forced to slide apart, crowd chaos behind them, "
        "emotional realistic motion, shallow depth of field, film scene"
    ),
    "OP12": (
        "cinematic live action stillness, one child's shoe left alone on old station floor, people have moved away, "
        "cold warning light mixed with warm sunset, subtle dust and light movement, realistic film scene"
    ),
}


NEGATIVE = (
    "cartoon, anime, illustration, painting, low quality, blurry, distorted face, extra fingers, extra limbs, duplicate people, "
    "watermark, logo, text, subtitles, deformed body, bad hands, bad feet, flicker, overexposed, plastic skin, CGI"
)


def post_json(path: str, payload: dict):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        SERVER + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8", errors="replace"))
        raise


def get_json(path: str):
    with urllib.request.urlopen(SERVER + path, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_keyframe(code: str) -> Path:
    matches = sorted(KEYFRAME_DIR.glob(f"{code}_*.png"))
    if not matches:
        raise FileNotFoundError(code)
    return matches[0]


def submit_segment(code: str, width=512, height=288, frames=16, fps=8, steps=10, denoise=0.52, seed=26060206):
    image = find_keyframe(code)
    prefix = f"BoundaryEcho_{code}_AnimateDiff_i2v_{width}x{height}_{frames}f"
    workflow = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "v1-5-pruned-emaonly-fp16.safetensors"},
        },
        "2": {
            "class_type": "VHS_LoadImagePath",
            "inputs": {
                "image": str(image),
                "custom_width": width,
                "custom_height": height,
            },
        },
        "3": {
            "class_type": "VAEEncode",
            "inputs": {"pixels": ["2", 0], "vae": ["1", 2]},
        },
        "4": {
            "class_type": "RepeatLatentBatch",
            "inputs": {"samples": ["3", 0], "amount": frames},
        },
        "5": {
            "class_type": "ADE_AnimateDiffUniformContextOptions",
            "inputs": {
                "context_length": 16,
                "context_stride": 1,
                "context_overlap": 4,
                "context_schedule": "uniform",
                "closed_loop": False,
                "fuse_method": "flat",
            },
        },
        "6": {
            "class_type": "ADE_AnimateDiffLoaderGen1",
            "inputs": {
                "model": ["1", 0],
                "model_name": "mm_sd_v15_v2.ckpt",
                "beta_schedule": "autoselect",
                "context_options": ["5", 0],
            },
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": PROMPTS[code], "clip": ["1", 1]},
        },
        "8": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": NEGATIVE, "clip": ["1", 1]},
        },
        "9": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["6", 0],
                "seed": seed,
                "steps": steps,
                "cfg": 7.0,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "positive": ["7", 0],
                "negative": ["8", 0],
                "latent_image": ["4", 0],
                "denoise": denoise,
            },
        },
        "10": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["9", 0], "vae": ["1", 2]},
        },
        "11": {
            "class_type": "VHS_VideoCombine",
            "inputs": {
                "images": ["10", 0],
                "frame_rate": fps,
                "loop_count": 0,
                "filename_prefix": prefix,
                "format": "video/h264-mp4",
                "pingpong": False,
                "save_output": True,
                "pix_fmt": "yuv420p",
                "crf": 20,
                "save_metadata": True,
                "trim_to_audio": False,
            },
        },
    }

    client_id = str(uuid.uuid4())
    queued = post_json("/prompt", {"prompt": workflow, "client_id": client_id})
    prompt_id = queued["prompt_id"]
    print(f"queued {code}: {prompt_id}")
    for _ in range(900):
        hist = get_json(f"/history/{prompt_id}")
        if prompt_id in hist:
            print(json.dumps(hist[prompt_id].get("outputs", {}), ensure_ascii=False, indent=2))
            return hist[prompt_id]
        time.sleep(2)
    raise TimeoutError(prompt_id)


if __name__ == "__main__":
    submit_segment("OP06")
