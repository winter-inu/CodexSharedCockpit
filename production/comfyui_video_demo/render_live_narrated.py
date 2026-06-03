from __future__ import annotations

import math
import wave
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
AUDIO = ROOT / "audio"
RENDERS = ROOT / "renders"
OUT_SILENT = RENDERS / "边界回声_ComfyUI实机演示_中文解说_silent.mp4"
OUT_AUDIO = RENDERS / "narration_combined.wav"
OUT_FINAL = RENDERS / "边界回声_ComfyUI实机演示_中文解说.mp4"
WIDTH, HEIGHT = 1920, 1080
FPS = 24

COLORS = {
    "bg": (9, 16, 20),
    "panel": (17, 28, 32),
    "panel2": (24, 37, 42),
    "text": (232, 241, 238),
    "muted": (157, 176, 170),
    "cyan": (114, 215, 208),
    "amber": (217, 168, 90),
    "red": (208, 93, 87),
}


def font(size: int, bold: bool = False, mono: bool = False):
    candidates = []
    if mono:
        candidates = [r"C:\Windows\Fonts\consola.ttf"]
    elif bold:
        candidates = [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc"]
    else:
        candidates = [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc"]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


F_TITLE = font(72, True)
F_BIG = font(56, True)
F_H2 = font(40, True)
F_BODY = font(31)
F_SMALL = font(24)
F_PATH = font(23, mono=True)
F_MONO = font(26, mono=True)


def ease(x: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, x)))


def out_cubic(x: float) -> float:
    x = max(0, min(1, x))
    return 1 - (1 - x) ** 3


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_size(draw, text, fnt):
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def draw_wrap(draw, text, xy, fnt, fill, max_width, line_gap=10):
    x, y = xy
    line = ""
    for ch in text:
        trial = line + ch
        if text_size(draw, trial, fnt)[0] <= max_width or not line:
            line = trial
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
            y += text_size(draw, line, fnt)[1] + line_gap
            line = ch
    if line:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += text_size(draw, line, fnt)[1] + line_gap
    return y


def fit_asset(name: str, box, cover=True, darken=0.0, blur=0.0):
    img = Image.open(ASSETS / name).convert("RGB")
    if darken:
        img = ImageEnhance.Brightness(img).enhance(1 - darken)
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    iw, ih = img.size
    scale = max(bw / iw, bh / ih) if cover else min(bw / iw, bh / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    if cover:
        return img.crop(((nw - bw) // 2, (nh - bh) // 2, (nw - bw) // 2 + bw, (nh - bh) // 2 + bh))
    canvas = Image.new("RGB", (bw, bh), COLORS["panel"])
    canvas.paste(img, ((bw - nw) // 2, (bh - nh) // 2))
    return canvas


def paste_asset(frame, name, box, t=0.5, zoom=0.035, darken=0.0):
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    img = Image.open(ASSETS / name).convert("RGB")
    if darken:
        img = ImageEnhance.Brightness(img).enhance(1 - darken)
    iw, ih = img.size
    scale = max(bw / iw, bh / ih) * (1 + zoom * ease(t))
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    cx = (nw - bw) // 2
    cy = (nh - bh) // 2
    frame.paste(img.crop((cx, cy, cx + bw, cy + bh)), (x1, y1))


def base(title, chapter, idx, total, progress):
    frame = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((-300, -250, 850, 610), fill=(44, 110, 110, 42))
    od.ellipse((1320, 580, 2220, 1340), fill=(142, 83, 35, 32))
    for x in range(-200, WIDTH, 110):
        od.line((x, 0, x + 260, HEIGHT), fill=(255, 255, 255, 9), width=1)
    frame = Image.alpha_composite(frame.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(frame)
    draw.text((70, 40), chapter, font=F_SMALL, fill=COLORS["cyan"])
    draw.text((70, 78), title, font=F_H2, fill=COLORS["text"])
    draw.text((1680, 48), f"{idx:02d}/{total:02d}", font=F_MONO, fill=COLORS["muted"])
    draw.line((70, 140, 1850, 140), fill=(62, 84, 87), width=3)
    draw.line((70, 140, 70 + int(1780 * progress), 140), fill=COLORS["amber"], width=5)
    return frame


def subtitle(draw, text):
    box = (240, 915, 1680, 1025)
    rounded(draw, box, 24, fill=(8, 13, 16), outline=(58, 80, 80), width=2)
    draw_wrap(draw, text, (285, 938), F_BODY, COLORS["text"], 1350, line_gap=8)


def pill(draw, xy, text, fill):
    x, y = xy
    w, h = text_size(draw, text, F_SMALL)
    rounded(draw, (x, y, x + w + 30, y + h + 18), 18, fill=fill)
    draw.text((x + 15, y + 8), text, font=F_SMALL, fill=(7, 13, 16))


def cursor(draw, x, y, label=None):
    draw.polygon([(x, y), (x + 34, y + 92), (x + 54, y + 55), (x + 98, y + 52)], fill=COLORS["text"])
    draw.line((x, y, x + 34, y + 92, x + 54, y + 55, x + 98, y + 52, x, y), fill=COLORS["bg"], width=3)
    if label:
        rounded(draw, (x + 72, y + 38, x + 72 + 260, y + 95), 16, fill=COLORS["cyan"])
        draw.text((x + 92, y + 51), label, font=F_SMALL, fill=COLORS["bg"])


def node(draw, xy, title, body, color):
    x, y = xy
    rounded(draw, (x, y, x + 285, y + 130), 18, fill=COLORS["panel2"], outline=color, width=3)
    draw.text((x + 22, y + 20), title, font=F_BODY, fill=COLORS["text"])
    draw_wrap(draw, body, (x + 22, y + 66), F_SMALL, COLORS["muted"], 235, line_gap=5)


def read_segments():
    rows = []
    for raw in (ROOT / "narration_segments.txt").read_text(encoding="utf-8").splitlines():
        if "|" in raw:
            sid, text = raw.split("|", 1)
            rows.append((sid, text))
    return rows


SEGMENTS = read_segments()


SCENES = [
    ("实机演示开场", "用本机 ComfyUI 做《边界回声》视频", "title", "01"),
    ("第一步", "确认 ComfyUI 已经启动", "live", "02"),
    ("第二步", "确认模型和输出目录", "model", "03"),
    ("第三步", "找到本地项目素材", "assets", "04"),
    ("OP13 示范", "先用同机位废站鞋做短测", "op13", "05"),
    ("工作流", "图生视频最小连接方式", "workflow", "06"),
    ("正向提示词", "只描述这一镜要发生什么", "positive", "07"),
    ("负向约束", "把不允许发生的错误写清楚", "negative", "08"),
    ("角色连续", "澜冰屿不能跑成别的角色", "character", "09"),
    ("生成策略", "先做三到五秒小测试", "generate", "10"),
    ("复盘检查", "生成后先抽帧看五件事", "qa", "11"),
    ("下一步", "先完成 OP13-1 到 OP13-3", "outro", "12"),
]


def audio_durations():
    durs = {}
    for sid, _ in SEGMENTS:
        path = AUDIO / f"segment_{sid}.wav"
        with wave.open(str(path), "rb") as w:
            durs[sid] = w.getnframes() / w.getframerate()
    return durs


def combine_audio(durations):
    paths = [AUDIO / f"segment_{sid}.wav" for sid, _ in SEGMENTS]
    with wave.open(str(paths[0]), "rb") as first:
        params = first.getparams()
        silence = b"\x00" * params.sampwidth * params.nchannels
    with wave.open(str(OUT_AUDIO), "wb") as out:
        out.setparams(params)
        for p in paths:
            with wave.open(str(p), "rb") as w:
                out.writeframes(w.readframes(w.getnframes()))
            out.writeframes(silence * int(params.framerate * 0.75))


def draw_scene(kind, local_t, dur, idx, text):
    t = local_t / dur
    frame = base(SCENES[idx][1], SCENES[idx][0], idx + 1, len(SCENES), (idx + t) / len(SCENES))
    draw = ImageDraw.Draw(frame)

    if kind == "title":
        paste_asset(frame, "op13-shoe-ruin.png", (0, 0, WIDTH, HEIGHT), t, darken=0.48, zoom=0.08)
        veil = Image.new("RGBA", (WIDTH, HEIGHT), (9, 16, 20, 135))
        frame = Image.alpha_composite(frame.convert("RGBA"), veil).convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text((120, 280), "实机演示", font=font(110, True), fill=COLORS["cyan"])
        draw.text((120, 410), "ComfyUI 做《边界回声》AI 真人剧视频", font=font(64, True), fill=COLORS["text"])
        draw.text((126, 525), "中文解说版：从关键帧到视频短测", font=F_BIG, fill=COLORS["amber"])
        pill(draw, (126, 640), "真实本机页面", COLORS["cyan"])
        pill(draw, (350, 640), "使用本地项目素材", COLORS["amber"])

    elif kind == "live":
        paste_asset(frame, "live/01-comfyui-live-home.png", (110, 210, 1810, 850), t, zoom=0.02)
        rounded(draw, (110, 210, 1810, 850), 16, fill=None, outline=COLORS["cyan"], width=4)
        cursor(draw, 1230, 255, "本机地址")
        draw.text((150, 865), "http://127.0.0.1:8188", font=F_MONO, fill=COLORS["cyan"])

    elif kind == "model":
        rounded(draw, (120, 230, 1800, 820), 26, fill=COLORS["panel"], outline=(55, 78, 82), width=2)
        rows = [
            ("模型文件", r"F:\ComfyUI\models\checkpoints\v1-5-pruned-emaonly-fp16.safetensors"),
            ("测试输出", r"F:\ComfyUI\output\Codex_test_00001_.png"),
            ("启动脚本", r"F:\ComfyUI\启动ComfyUI.bat"),
        ]
        y = 320
        for k, v in rows:
            pill(draw, (170, y), k, COLORS["cyan"])
            draw.text((360, y + 5), v, font=F_PATH, fill=COLORS["text"])
            y += 130
        paste_asset(frame, "comfyui-test-output.png", (1310, 390, 1660, 740), t, zoom=0.04)

    elif kind == "assets":
        paste_asset(frame, "lanbingyu-poster.png", (110, 220, 475, 820), t, zoom=0.04)
        paste_asset(frame, "lingxing-poster.png", (500, 220, 865, 820), t, zoom=0.04)
        paste_asset(frame, "op06-op14-contact.jpg", (940, 230, 1780, 510), t, zoom=0.025)
        paste_asset(frame, "op17-op30-contact.jpg", (940, 550, 1780, 830), t, zoom=0.025)
        pill(draw, (130, 835), "角色参考", COLORS["cyan"])
        pill(draw, (960, 835), "OP 关键帧和复盘", COLORS["amber"])

    elif kind == "op13":
        paste_asset(frame, "op13-shoe-ruin.png", (115, 225, 930, 835), t, zoom=0.08)
        paste_asset(frame, "op13-lanbingyu-close.png", (990, 225, 1805, 835), t, zoom=0.08)
        pill(draw, (145, 785), "同机位废站鞋", COLORS["amber"])
        pill(draw, (1025, 785), "澜冰屿病弱近景", COLORS["cyan"])
        draw.text((150, 855), "先测最稳的一段：鞋不动，环境微动，情绪克制。", font=F_BODY, fill=COLORS["text"])

    elif kind == "workflow":
        xs = [120, 460, 800, 1140, 1480]
        labels = [
            ("Load Image", "导入 OP13 关键帧"),
            ("Prompt + CLIP", "写镜头动作"),
            ("Negative", "写禁止项"),
            ("Video Node", "生成 3-5 秒"),
            ("Save Video", "保存 MP4"),
        ]
        for i, item in enumerate(labels):
            node(draw, (xs[i], 420), item[0], item[1], COLORS["cyan"] if i < 3 else COLORS["amber"])
            if i < 4:
                draw.line((xs[i] + 285, 485, xs[i + 1] - 18, 485), fill=COLORS["amber"], width=5)
                draw.polygon([(xs[i + 1] - 18, 485), (xs[i + 1] - 40, 472), (xs[i + 1] - 40, 498)], fill=COLORS["amber"])
        cursor(draw, 1140, 355, "视频节点")

    elif kind == "positive":
        rounded(draw, (150, 230, 1770, 815), 28, fill=COLORS["panel"], outline=COLORS["cyan"], width=3)
        lines = [
            "cinematic live-action keyframe",
            "abandoned old north station, power off",
            "same low camera angle, same shoe position",
            "wet old children's shoe, subtle environment motion",
            "restrained mystery drama mood",
        ]
        y = 310
        for line in lines:
            rounded(draw, (220, y, 1700, y + 60), 14, fill=COLORS["panel2"])
            draw.text((245, y + 13), line, font=F_MONO, fill=COLORS["text"])
            y += 82
        cursor(draw, 1500, 300, "正向")

    elif kind == "negative":
        rounded(draw, (150, 230, 1770, 815), 28, fill=(31, 20, 22), outline=COLORS["red"], width=3)
        lines = [
            "anime, cartoon, game character",
            "new background, changed camera angle",
            "station lights, red status lights, neon ads",
            "large white hair, silver bangs",
            "extra text, watermark, distorted face",
        ]
        y = 310
        for line in lines:
            rounded(draw, (220, y, 1700, y + 60), 14, fill=(52, 30, 32))
            draw.text((245, y + 13), line, font=F_MONO, fill=(255, 218, 213))
            y += 82
        cursor(draw, 1500, 300, "负向")

    elif kind == "character":
        paste_asset(frame, "lanbingyu-poster.png", (125, 210, 720, 870), t, zoom=0.045)
        rounded(draw, (800, 245, 1780, 810), 28, fill=COLORS["panel"], outline=COLORS["cyan"], width=3)
        checks = ["黑发为主", "零星细碎白丝", "病弱、克制", "不要动画男主", "不要游戏角色立绘"]
        y = 330
        for c in checks:
            pill(draw, (860, y), "锁定", COLORS["amber"])
            draw.text((980, y + 5), c, font=F_BODY, fill=COLORS["text"])
            y += 82

    elif kind == "generate":
        rounded(draw, (160, 245, 1760, 820), 30, fill=COLORS["panel"], outline=COLORS["amber"], width=3)
        draw.text((230, 330), "小测试参数建议", font=F_BIG, fill=COLORS["amber"])
        rows = [("时长", "3 - 5 秒"), ("分辨率", "先低后高"), ("步数", "先少后多"), ("目标", "只判断方向是否正确")]
        y = 445
        for k, v in rows:
            pill(draw, (250, y), k, COLORS["cyan"])
            draw.text((395, y + 4), v, font=F_BODY, fill=COLORS["text"])
            y += 86
        cursor(draw, 1420, 590, "Queue Prompt")

    elif kind == "qa":
        rounded(draw, (130, 220, 1790, 840), 30, fill=COLORS["panel"], outline=COLORS["cyan"], width=3)
        checks = [
            ("角色", "有没有跑脸、换发型？"),
            ("背景", "废站有没有突然亮灯？"),
            ("道具", "鞋和 B-07 有没有丢？"),
            ("运动", "动作有没有过猛？"),
            ("剪辑", "首尾帧能不能接？"),
        ]
        for i, (k, v) in enumerate(checks):
            x = 210 + (i % 2) * 780
            y = 335 + (i // 2) * 145
            pill(draw, (x, y), k, COLORS["red"] if i == 1 else COLORS["cyan"])
            draw.text((x + 125, y + 5), v, font=F_BODY, fill=COLORS["text"])
        paste_asset(frame, "op28-b07.png", (1240, 600, 1660, 805), t, zoom=0.04)

    elif kind == "outro":
        paste_asset(frame, "op17-op30-contact.jpg", (0, 0, WIDTH, HEIGHT), t, zoom=0.05, darken=0.50)
        veil = Image.new("RGBA", (WIDTH, HEIGHT), (9, 16, 20, 155))
        frame = Image.alpha_composite(frame.convert("RGBA"), veil).convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text((140, 285), "下一步实操", font=F_TITLE, fill=COLORS["cyan"])
        draw.text((140, 400), "OP13-1 → OP13-3", font=font(84, True), fill=COLORS["text"])
        draw.text((140, 525), "三镜头短段，每镜三到五秒。", font=F_BIG, fill=COLORS["amber"])
        draw.text((140, 625), "先跑通一致性，再扩展整段。", font=F_BIG, fill=COLORS["text"])

    subtitle(draw, text)
    alpha = 255
    if local_t < 0.55:
        alpha = int(255 * out_cubic(local_t / 0.55))
    elif dur - local_t < 0.55:
        alpha = int(255 * out_cubic((dur - local_t) / 0.55))
    if alpha < 255:
        frame = Image.blend(Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"]), frame, alpha / 255)
    return frame


def main():
    RENDERS.mkdir(parents=True, exist_ok=True)
    durs = audio_durations()
    combine_audio(durs)
    scene_lengths = [durs[sid] + 0.75 for sid, _ in SEGMENTS]
    total_frames = sum(int(math.ceil(d * FPS)) for d in scene_lengths)
    with imageio.get_writer(
        OUT_SILENT,
        fps=FPS,
        codec="libx264",
        quality=8,
        macro_block_size=None,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    ) as writer:
        done = 0
        for idx, (_, _, kind, sid) in enumerate(SCENES):
            text = dict(SEGMENTS)[sid]
            dur = scene_lengths[idx]
            n = int(math.ceil(dur * FPS))
            for fi in range(n):
                writer.append_data(np.asarray(draw_scene(kind, fi / FPS, dur, idx, text)))
            done += n
            print(f"rendered {idx + 1}/{len(SCENES)} frames={done}/{total_frames}")
    import imageio_ffmpeg
    import subprocess
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.check_call([
        ffmpeg, "-y",
        "-i", str(OUT_SILENT),
        "-i", str(OUT_AUDIO),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(OUT_FINAL),
    ])
    print(str(OUT_FINAL))


if __name__ == "__main__":
    main()
