from pathlib import Path
import shutil

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(r"F:\CodexSharedCockpit")
KEYFRAME_DIR = ROOT / "episodes" / "season_01" / "episode_01" / "keyframes" / "op06_op14_main_v1"
RENDER_DIR = ROOT / "production" / "op06_op12_preview" / "renders"
FINAL_DIR = Path(r"F:\成片\边界回声_OP06_OP12_ComfyUI预览")
COMFY_OUTPUT = Path(r"F:\ComfyUI\output")

WIDTH, HEIGHT = 1920, 1080
FPS = 20
XFADE_SEC = 0.7


SCENES = [
    ("OP06", "第一次异常前兆", 8, "旧北站候车大厅出现第一丝不对劲，温暖日光开始被冷白警示吞没。"),
    ("OP07", "系统正式警报", 9, "警报正式响起，人群和广播屏把危险推到所有人面前。"),
    ("OP08", "人群反向混乱", 8, "妈妈护住小夏，反向奔逃的人潮让空间开始失控。"),
    ("OP09", "右脚鞋掉落", 7, "小夏被推挤时右脚鞋脱落，失去控制的细节第一次被定格。"),
    ("OP10", "隔离门升起", 8, "高长隔离门升起，母女之间的距离被机械地切开。"),
    ("OP11", "双手被迫滑开", 8, "两只手被迫滑开，情绪从混乱转成无法挽回。"),
    ("OP12", "掉落鞋无人定格", 9, "人潮退去，只剩那只鞋留在地面，事故记忆被钉住。"),
]


def pick_font(size: int):
    candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
        Path(r"C:\Windows\Fonts\arial.ttf"),
    ]
    for font_path in candidates:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size)
    return ImageFont.load_default()


TITLE_FONT = pick_font(58)
SUBTITLE_FONT = pick_font(34)
SMALL_FONT = pick_font(26)


def find_keyframe(code: str) -> Path:
    matches = sorted(KEYFRAME_DIR.glob(f"{code}_*.png"))
    if not matches:
        raise FileNotFoundError(f"Missing keyframe for {code} in {KEYFRAME_DIR}")
    return matches[0]


def cover_image(path: Path, zoom: float, pan_x: float, pan_y: float) -> Image.Image:
    src = Image.open(path).convert("RGB")
    src_ratio = src.width / src.height
    dst_ratio = WIDTH / HEIGHT
    if src_ratio > dst_ratio:
        new_h = int(HEIGHT * zoom)
        new_w = int(new_h * src_ratio)
    else:
        new_w = int(WIDTH * zoom)
        new_h = int(new_w / src_ratio)
    resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)
    max_x = max(0, new_w - WIDTH)
    max_y = max(0, new_h - HEIGHT)
    left = int(max_x * pan_x)
    top = int(max_y * pan_y)
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def draw_panel(draw: ImageDraw.ImageDraw, xy, text, font, fill=(255, 255, 255), pad=(22, 13)):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0] + pad[0] * 2
    h = bbox[3] - bbox[1] + pad[1] * 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=(0, 0, 0, 150))
    draw.text((x + pad[0], y + pad[1] - 2), text, font=font, fill=fill)


def wrap_text(text: str, font, max_width: int):
    lines = []
    current = ""
    dummy = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(dummy)
    for ch in text:
        test = current + ch
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def add_overlays(frame: Image.Image, code: str, title: str, note: str, scene_t: float, scene_dur: float, total_t: float, total_dur: float):
    overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.rectangle((0, 0, WIDTH, 180), fill=(0, 0, 0, 85))
    draw.rectangle((0, HEIGHT - 205, WIDTH, HEIGHT), fill=(0, 0, 0, 105))

    draw_panel(draw, (58, 48), "OP06-OP12 ComfyUI 素材预览", SMALL_FONT, fill=(230, 244, 255))
    draw.text((58, 105), f"{code}  {title}", font=TITLE_FONT, fill=(255, 255, 255))

    y = HEIGHT - 155
    for line in wrap_text(note, SUBTITLE_FONT, WIDTH - 150)[:2]:
        draw.text((58, y), line, font=SUBTITLE_FONT, fill=(255, 255, 255))
        y += 46

    bar_x, bar_y, bar_w, bar_h = 58, HEIGHT - 52, WIDTH - 116, 10
    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=5, fill=(255, 255, 255, 80))
    draw.rounded_rectangle((bar_x, bar_y, bar_x + int(bar_w * total_t / total_dur), bar_y + bar_h), radius=5, fill=(255, 210, 116, 230))
    draw.text((WIDTH - 260, HEIGHT - 92), f"{int(total_t):02d}s / {int(total_dur):02d}s", font=SMALL_FONT, fill=(235, 235, 235))

    local = min(1, max(0, scene_t / scene_dur))
    draw.arc((WIDTH - 125, 45, WIDTH - 65, 105), -90, -90 + int(360 * local), fill=(255, 210, 116, 240), width=6)

    return Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")


def make_frame(scene_idx: int, local_frame: int, total_frame: int, paths):
    code, title, dur, note = SCENES[scene_idx]
    scene_frames = int(dur * FPS)
    local = local_frame / max(1, scene_frames - 1)
    total_dur = sum(s[2] for s in SCENES)
    total_t = total_frame / FPS

    zoom = 1.055 + 0.035 * local
    pan_x = 0.42 + 0.12 * np.sin((scene_idx + 1) * 0.77)
    pan_y = 0.48 + 0.08 * np.cos((scene_idx + 1) * 0.91)
    img = cover_image(paths[scene_idx], zoom, pan_x, pan_y)

    fade_frames = int(XFADE_SEC * FPS)
    if scene_idx > 0 and local_frame < fade_frames:
        prev = cover_image(paths[scene_idx - 1], 1.09, pan_x, pan_y)
        alpha = local_frame / fade_frames
        img = Image.blend(prev, img, alpha)

    if scene_idx < len(SCENES) - 1 and local_frame > scene_frames - fade_frames:
        nxt = cover_image(paths[scene_idx + 1], 1.055, pan_x, pan_y)
        alpha = (local_frame - (scene_frames - fade_frames)) / fade_frames
        img = Image.blend(img, nxt, alpha)

    if local_frame < int(0.45 * FPS):
        alpha = local_frame / max(1, int(0.45 * FPS))
        black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        img = Image.blend(black, img, alpha)

    if scene_idx == len(SCENES) - 1 and local_frame > scene_frames - int(0.65 * FPS):
        fade = (local_frame - (scene_frames - int(0.65 * FPS))) / max(1, int(0.65 * FPS))
        black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        img = Image.blend(img, black, fade)

    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=3))
    return add_overlays(img, code, title, note, local_frame / FPS, dur, total_t, total_dur)


def main():
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    COMFY_OUTPUT.mkdir(parents=True, exist_ok=True)

    paths = [find_keyframe(code) for code, _, _, _ in SCENES]
    output = RENDER_DIR / "边界回声_OP06_OP12_关键帧视频预览.mp4"
    preview_png = RENDER_DIR / "边界回声_OP06_OP12_关键帧视频预览_封面.png"

    total_frames = sum(int(dur * FPS) for _, _, dur, _ in SCENES)
    with imageio.get_writer(str(output), fps=FPS, codec="libx264", quality=8, macro_block_size=1) as writer:
        frame_index = 0
        cover_saved = False
        for scene_idx, (_, _, dur, _) in enumerate(SCENES):
            for local_frame in range(int(dur * FPS)):
                frame = make_frame(scene_idx, local_frame, frame_index, paths)
                if not cover_saved and frame_index >= int(2.0 * FPS):
                    frame.save(preview_png)
                    cover_saved = True
                writer.append_data(np.asarray(frame))
                frame_index += 1

    for target_dir in (FINAL_DIR, COMFY_OUTPUT):
        shutil.copy2(output, target_dir / output.name)
        shutil.copy2(preview_png, target_dir / preview_png.name)

    print(output)
    print(preview_png)
    print(total_frames)


if __name__ == "__main__":
    main()
