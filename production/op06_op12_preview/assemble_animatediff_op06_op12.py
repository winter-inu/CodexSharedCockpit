from pathlib import Path
import shutil

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


COMFY_OUTPUT = Path(r"F:\ComfyUI\output")
RENDER_DIR = Path(r"F:\CodexSharedCockpit\production\op06_op12_preview\renders")
FINAL_DIR = Path(r"F:\成片\边界回声_OP06_OP12_ComfyUI动效")

OUT_W, OUT_H = 1280, 720
SOURCE_FPS = 8
OUT_FPS = 24
CROSSFADE_FRAMES = 8


def latest_segment(code: str) -> Path:
    preferred = {
        "OP06": "64f",
        "OP07": "64f",
        "OP08": "64f",
        "OP09": "56f",
        "OP10": "64f",
        "OP11": "64f",
        "OP12": "64f",
    }
    matches = sorted(
        COMFY_OUTPUT.glob(f"BoundaryEcho_{code}_AnimateDiff_i2v_640x360_{preferred[code]}_*.mp4"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not matches:
        raise FileNotFoundError(code)
    return matches[0]


def polish(frame: np.ndarray) -> Image.Image:
    im = Image.fromarray(frame).convert("RGB")
    im = im.resize((OUT_W, OUT_H), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(0.96)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=80, threshold=4))
    return im


def read_frames(path: Path):
    reader = imageio.get_reader(str(path))
    frames = [polish(frame) for frame in reader]
    reader.close()
    return frames


def smooth_frames(frames):
    smoothed = []
    for idx in range(len(frames) - 1):
        a, b = frames[idx], frames[idx + 1]
        smoothed.append(a)
        smoothed.append(Image.blend(a, b, 1 / 3))
        smoothed.append(Image.blend(a, b, 2 / 3))
    smoothed.append(frames[-1])
    return smoothed


def crossfade(prev, nxt, fade_frames):
    if not prev:
        return nxt
    keep_prev = prev[:-fade_frames]
    tail = prev[-fade_frames:]
    head = nxt[:fade_frames]
    rest = nxt[fade_frames:]
    blended = []
    for i, (a, b) in enumerate(zip(tail, head)):
        alpha = (i + 1) / (fade_frames + 1)
        blended.append(Image.blend(a, b, alpha))
    return keep_prev + blended + rest


def main():
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    all_frames = []
    segment_paths = []
    for code in ["OP06", "OP07", "OP08", "OP09", "OP10", "OP11", "OP12"]:
        path = latest_segment(code)
        segment_paths.append(path)
        frames = smooth_frames(read_frames(path))
        all_frames = crossfade(all_frames, frames, CROSSFADE_FRAMES)

    output = RENDER_DIR / "边界回声_OP06_OP12_ComfyUI_AnimateDiff真动效长版.mp4"
    cover = RENDER_DIR / "边界回声_OP06_OP12_ComfyUI_AnimateDiff真动效长版_封面.jpg"
    with imageio.get_writer(str(output), fps=OUT_FPS, codec="libx264", quality=8, macro_block_size=1) as writer:
        for idx, frame in enumerate(all_frames):
            if idx == 20:
                frame.save(cover, quality=92)
            writer.append_data(np.asarray(frame))

    shutil.copy2(output, FINAL_DIR / output.name)
    shutil.copy2(cover, FINAL_DIR / cover.name)
    for path in segment_paths:
        shutil.copy2(path, FINAL_DIR / path.name)

    print(output)
    print(FINAL_DIR / output.name)
    print(len(all_frames), OUT_FPS, len(all_frames) / OUT_FPS)


if __name__ == "__main__":
    main()
