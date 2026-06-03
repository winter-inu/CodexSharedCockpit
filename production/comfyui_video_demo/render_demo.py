from __future__ import annotations

import math
import textwrap
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT = ROOT / "renders" / "边界回声_ComfyUI做视频_新手演示.mp4"
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
    "black": (0, 0, 0),
}


def font(size: int, bold: bool = False, mono: bool = False):
    candidates = []
    if mono:
        candidates += [
            r"C:\Windows\Fonts\consola.ttf",
            r"C:\Windows\Fonts\Consola.ttf",
        ]
    elif bold:
        candidates += [
            r"C:\Windows\Fonts\msyhbd.ttc",
            r"C:\Windows\Fonts\msyh.ttc",
        ]
    else:
        candidates += [
            r"C:\Windows\Fonts\msyh.ttc",
            r"C:\Windows\Fonts\msyhbd.ttc",
        ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


F_TITLE = font(74, bold=True)
F_H1 = font(58, bold=True)
F_H2 = font(42, bold=True)
F_BODY = font(32)
F_SMALL = font(24)
F_PATH = font(24, mono=True)
F_MONO = font(28, mono=True)


def ease_out_cubic(x: float) -> float:
    return 1 - (1 - x) ** 3


def ease_in_out(x: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * x)


def mix(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def rounded(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def wrap_text(text: str, max_chars: int) -> list[str]:
    lines = []
    for part in text.split("\n"):
        if not part:
            lines.append("")
        else:
            lines.extend(textwrap.wrap(part, max_chars, break_long_words=False, replace_whitespace=False))
    return lines


def draw_wrapped(draw, text, xy, fnt, fill, max_chars=32, line_gap=12):
    x, y = xy
    for line in wrap_text(text, max_chars):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += text_size(draw, line or " ", fnt)[1] + line_gap
    return y


def fit_image(path: str, box: tuple[int, int, int, int], darken=0.0, blur=0.0) -> Image.Image:
    img = Image.open(ASSETS / path).convert("RGB")
    if darken:
        img = ImageEnhance.Brightness(img).enhance(1 - darken)
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    iw, ih = img.size
    scale = max(bw / iw, bh / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - bw) // 2
    top = (nh - bh) // 2
    return img.crop((left, top, left + bw, top + bh))


def paste_kenburns(base, path, box, t, zoom=0.06, pan=(0.0, 0.0), darken=0.0):
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    img = Image.open(ASSETS / path).convert("RGB")
    if darken:
        img = ImageEnhance.Brightness(img).enhance(1 - darken)
    iw, ih = img.size
    scale = max(bw / iw, bh / ih) * (1 + zoom * ease_in_out(t))
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    max_x = max(0, nw - bw)
    max_y = max(0, nh - bh)
    cx = int(max_x * (0.5 + pan[0] * (t - 0.5)))
    cy = int(max_y * (0.5 + pan[1] * (t - 0.5)))
    crop = img.crop((cx, cy, cx + bw, cy + bh))
    base.paste(crop, (x1, y1))


def base_frame(scene_index: int, title: str, chapter: str, progress: float) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    pix = img.load()
    for y in range(HEIGHT):
        glow = int(18 * (1 - y / HEIGHT))
        for x in range(0, WIDTH, 6):
            if x < WIDTH and y < HEIGHT:
                pass
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((-260, -220, 820, 620), fill=(37, 96, 96, 48))
    od.ellipse((1330, 560, 2200, 1340), fill=(110, 62, 34, 34))
    for x in range(0, WIDTH, 96):
        od.line((x, 0, x + 220, HEIGHT), fill=(255, 255, 255, 10), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.text((70, 42), chapter, font=F_SMALL, fill=COLORS["cyan"])
    draw.text((70, 78), title, font=F_H2, fill=COLORS["text"])
    draw.line((70, 140, 1850, 140), fill=(114, 215, 208), width=2)
    draw.line((70, 140, 70 + int(1780 * progress), 140), fill=COLORS["amber"], width=5)
    draw.text((1655, 48), f"{scene_index:02d}/11", font=F_MONO, fill=COLORS["muted"])
    return img


def draw_panel(draw, xy, title=None):
    rounded(draw, xy, 22, fill=COLORS["panel"], outline=(55, 78, 82), width=2)
    if title:
        draw.text((xy[0] + 28, xy[1] + 22), title, font=F_H2, fill=COLORS["text"])


def draw_pill(draw, xy, text, fill, fg=COLORS["bg"]):
    x, y = xy
    w, h = text_size(draw, text, F_SMALL)
    rounded(draw, (x, y, x + w + 28, y + h + 16), 18, fill=fill)
    draw.text((x + 14, y + 7), text, font=F_SMALL, fill=fg)


def draw_steps(draw, x, y, steps, active=None):
    for i, step in enumerate(steps):
        cy = y + i * 88
        color = COLORS["cyan"] if active is None or i <= active else COLORS["muted"]
        rounded(draw, (x, cy, x + 54, cy + 54), 14, fill=color)
        draw.text((x + 17, cy + 9), str(i + 1), font=F_SMALL, fill=COLORS["bg"])
        draw.text((x + 78, cy + 2), step[0], font=F_BODY, fill=COLORS["text"])
        draw.text((x + 78, cy + 40), step[1], font=F_SMALL, fill=COLORS["muted"])
        if i < len(steps) - 1:
            draw.line((x + 27, cy + 58, x + 27, cy + 82), fill=(114, 215, 208), width=3)


def transition_alpha(local_t: float, dur: float, fade: float = 0.7) -> int:
    if local_t < fade:
        return int(255 * ease_out_cubic(local_t / fade))
    if local_t > dur - fade:
        return int(255 * ease_out_cubic((dur - local_t) / fade))
    return 255


def apply_scene_alpha(frame: Image.Image, alpha: int) -> Image.Image:
    if alpha >= 255:
        return frame
    black = Image.new("RGB", frame.size, COLORS["bg"])
    return Image.blend(black, frame, alpha / 255)


SCENES = [
    {"dur": 9, "chapter": "开场", "title": "ComfyUI 做《边界回声》视频", "kind": "title"},
    {"dur": 16, "chapter": "01 当前进度", "title": "先确认：你不是从零开始", "kind": "progress"},
    {"dur": 16, "chapter": "02 环境检查", "title": "ComfyUI 已经能跑图", "kind": "env"},
    {"dur": 17, "chapter": "03 素材归位", "title": "新手先管好三个文件夹", "kind": "folders"},
    {"dur": 18, "chapter": "04 核心思路", "title": "真人剧视频 = 关键帧 + 运动控制", "kind": "concept"},
    {"dur": 22, "chapter": "05 工作流", "title": "最小视频工作流怎么连", "kind": "workflow"},
    {"dur": 21, "chapter": "06 提示词", "title": "提示词要锁定“边界回声”的规则", "kind": "prompt"},
    {"dur": 20, "chapter": "07 OP13 示例", "title": "同机位废站鞋：最适合先测试", "kind": "op13"},
    {"dur": 18, "chapter": "08 一致性检查", "title": "生成后先看五个问题", "kind": "qa"},
    {"dur": 17, "chapter": "09 输出复盘", "title": "把 MP4 抽帧，写回项目", "kind": "review"},
    {"dur": 13, "chapter": "收束", "title": "建议先做一个 3 镜头短段", "kind": "outro"},
]


def draw_scene(kind: str, local_t: float, dur: float, idx: int) -> Image.Image:
    meta = SCENES[idx]
    t = max(0.0, min(1.0, local_t / dur))
    frame = base_frame(idx + 1, meta["title"], meta["chapter"], (idx + t) / len(SCENES))
    draw = ImageDraw.Draw(frame)
    enter = ease_out_cubic(min(1, local_t / 1.0))

    if kind == "title":
        paste_kenburns(frame, "op13-shoe-ruin.png", (0, 0, WIDTH, HEIGHT), t, zoom=0.08, darken=0.45)
        veil = Image.new("RGBA", (WIDTH, HEIGHT), (9, 16, 20, 118))
        frame = Image.alpha_composite(frame.convert("RGBA"), veil).convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text((120, 285), "ComfyUI", font=font(112, bold=True), fill=COLORS["cyan"])
        draw.text((120, 405), "做《边界回声》AI 真人剧视频", font=font(80, bold=True), fill=COLORS["text"])
        draw.text((126, 525), "从关键帧到视频：新手实操演示", font=F_H2, fill=COLORS["amber"])
        draw_pill(draw, (126, 625), "使用本地项目素材", COLORS["amber"])
        draw_pill(draw, (390, 625), "适合 OP13-OP16 废站段先试", COLORS["cyan"])

    elif kind == "progress":
        draw_panel(draw, (86, 190, 740, 920), "项目当前有这些东西")
        steps = [
            ("剧本与 OP 分镜", "第一集 OP01-OP30 已经拆分"),
            ("角色参考", "澪星 / 澜冰屿角色海报"),
            ("关键帧", "OP06-OP14、OP17-OP30 主控帧"),
            ("复盘图", "OP01-05 已有抽帧复盘"),
        ]
        draw_steps(draw, 125, 295, steps, 3)
        paste_kenburns(frame, "op06-op14-contact.jpg", (790, 210, 1830, 560), t, zoom=0.04)
        paste_kenburns(frame, "op17-op30-contact.jpg", (790, 590, 1830, 940), t, zoom=0.04)
        draw.text((805, 170), "本地关键帧接触表", font=F_BODY, fill=COLORS["muted"])

    elif kind == "env":
        draw_panel(draw, (88, 186, 890, 925), "本机 ComfyUI 状态")
        rows = [
            ("地址", "http://127.0.0.1:8188"),
            ("模型", "v1-5-pruned-emaonly-fp16.safetensors"),
            ("位置", r"F:\ComfyUI\models\checkpoints"),
            ("测试", "已成功生成一张图"),
        ]
        y = 300
        for k, v in rows:
            draw.text((135, y), k, font=F_BODY, fill=COLORS["cyan"])
            draw.text((255, y), v, font=F_PATH if "\\" in v or ":" in v else F_BODY, fill=COLORS["text"])
            y += 86
        paste_kenburns(frame, "comfyui-home.png", (950, 220, 1810, 570), t, zoom=0.03)
        paste_kenburns(frame, "comfyui-test-output.png", (1135, 610, 1565, 1040), t, zoom=0.04)
        draw_pill(draw, (970, 600), "先跑通，再追求复杂视频节点", COLORS["amber"])

    elif kind == "folders":
        draw_panel(draw, (95, 210, 1825, 900), "三个文件夹先记住")
        folders = [
            (r"F:\边界回声\assets\characters", "角色参考，做真人剧一致性"),
            (r"F:\边界回声\episodes\...\keyframes", "关键帧，图生视频的起点"),
            (r"F:\ComfyUI\output", "生成结果，拿来抽帧复盘"),
        ]
        y = 330
        for p, desc in folders:
            rounded(draw, (155, y, 1740, y + 105), 20, fill=COLORS["panel2"], outline=(60, 88, 88), width=2)
            draw.text((190, y + 22), p, font=F_MONO, fill=COLORS["cyan"])
            draw.text((190, y + 63), desc, font=F_SMALL, fill=COLORS["muted"])
            y += 145
        draw.text((155, 795), "新手误区：生成完就到处乱放。正确做法是：每次生成都能追溯到 OP、镜头号、参考图。", font=F_BODY, fill=COLORS["amber"])

    elif kind == "concept":
        paste_kenburns(frame, "lanbingyu-poster.png", (90, 220, 520, 910), t, zoom=0.06, pan=(0.15, 0))
        paste_kenburns(frame, "lingxing-poster.png", (540, 220, 970, 910), t, zoom=0.06, pan=(-0.15, 0))
        draw_panel(draw, (1030, 230, 1810, 890), "做视频前先锁定")
        bullets = [
            "角色脸和服装，不要每段都换人",
            "镜头机位，不要无故切成新场景",
            "道具连续性：鞋、长椅、B-07",
            "运动只服务剧情，不要乱摇乱飞",
        ]
        y = 340
        for b in bullets:
            draw_pill(draw, (1080, y), "检查", COLORS["cyan"])
            draw.text((1190, y + 4), b, font=F_BODY, fill=COLORS["text"])
            y += 100

    elif kind == "workflow":
        draw_panel(draw, (90, 210, 1830, 920), "最小图生视频工作流")
        nodes = [
            ("Load Image", "输入 OP 关键帧"),
            ("正向提示词", "真人剧画风 + 本镜头动作"),
            ("负向提示词", "禁止跑脸、换背景、强光"),
            ("Video / Animate 节点", "生成 3-5 秒测试片段"),
            ("Save Video", "输出 MP4 并复盘"),
        ]
        xs = [155, 455, 785, 1120, 1480]
        y = 430
        for i, (name, desc) in enumerate(nodes):
            rounded(draw, (xs[i], y, xs[i] + 245, y + 150), 22, fill=COLORS["panel2"], outline=COLORS["cyan"], width=3)
            draw.text((xs[i] + 24, y + 28), name, font=F_BODY, fill=COLORS["text"])
            draw_wrapped(draw, desc, (xs[i] + 24, y + 78), F_SMALL, COLORS["muted"], max_chars=13, line_gap=8)
            if i < len(nodes) - 1:
                draw.line((xs[i] + 245, y + 75, xs[i + 1] - 15, y + 75), fill=COLORS["amber"], width=5)
                draw.polygon([(xs[i + 1] - 15, y + 75), (xs[i + 1] - 35, y + 63), (xs[i + 1] - 35, y + 87)], fill=COLORS["amber"])
        draw.text((155, 700), "先做短测试：512 或 768 宽、低步数、3 秒。确认方向对了，再提高分辨率和时长。", font=F_BODY, fill=COLORS["amber"])

    elif kind == "prompt":
        draw_panel(draw, (92, 200, 925, 910), "正向提示词结构")
        prompt_lines = [
            "cinematic live-action keyframe",
            "abandoned old north station, power off",
            "same low camera angle, same shoe position",
            "Lan Bingyu, weak black-haired man",
            "subtle motion, restrained emotion",
        ]
        y = 310
        for line in prompt_lines:
            rounded(draw, (145, y, 850, y + 58), 14, fill=COLORS["panel2"])
            draw.text((165, y + 13), line, font=F_MONO, fill=COLORS["text"])
            y += 74
        draw_panel(draw, (985, 200, 1825, 910), "负向提示词要写具体")
        neg = [
            "anime, cartoon, game character",
            "new background, changed camera angle",
            "station lights, red status lights, neon ads",
            "large white hair, silver bangs",
            "extra text, watermark, distorted face",
        ]
        y = 310
        for line in neg:
            rounded(draw, (1038, y, 1755, y + 58), 14, fill=(50, 30, 32))
            draw.text((1058, y + 13), line, font=F_MONO, fill=(255, 207, 203))
            y += 74

    elif kind == "op13":
        paste_kenburns(frame, "op13-shoe-ruin.png", (95, 215, 910, 900), t, zoom=0.08, pan=(0.12, 0.05))
        paste_kenburns(frame, "op13-lanbingyu-close.png", (965, 215, 1810, 900), t, zoom=0.08, pan=(-0.08, 0))
        draw_pill(draw, (128, 832), "OP13-1：同机位废站鞋", COLORS["amber"])
        draw_pill(draw, (1000, 832), "OP13-6：澜冰屿病弱近景", COLORS["cyan"])
        draw.text((130, 930), "建议第一段先做：鞋子不动，环境微动，远处光弱弱闪一下。不要一上来就做大动作。", font=F_BODY, fill=COLORS["text"])

    elif kind == "qa":
        draw_panel(draw, (120, 220, 1800, 900), "每次生成后，先暂停做五项检查")
        checks = [
            ("角色", "澜冰屿是否还是黑发为主、只有零星白丝？"),
            ("背景", "废站是否仍然断电，没有车站灯和广告光？"),
            ("机位", "鞋子位置、地面缝隙、背景大轮廓是否没换？"),
            ("运动", "动作是否太像预告片，而不是剧情片？"),
            ("可剪辑", "首尾帧是否能和上一镜、下一镜接上？"),
        ]
        for i, (k, v) in enumerate(checks):
            x = 190 + (i % 2) * 790
            y = 330 + (i // 2) * 150
            draw_pill(draw, (x, y), k, COLORS["red"] if i == 1 else COLORS["cyan"])
            draw_wrapped(draw, v, (x + 120, y + 2), F_BODY, COLORS["text"], max_chars=22, line_gap=8)

    elif kind == "review":
        draw_panel(draw, (100, 210, 890, 900), "输出后不要只看成片")
        draw_steps(draw, 150, 325, [
            ("保存 MP4", r"F:\ComfyUI\output 或项目 production"),
            ("抽关键帧", "每 1-2 秒抽一张图检查"),
            ("写回记录", "标注镜头号、版本、问题"),
            ("再生成", "只改一个变量，不要全推倒"),
        ], 3)
        paste_kenburns(frame, "op28-b07.png", (970, 250, 1760, 850), t, zoom=0.05)
        draw.text((1000, 885), "复盘时要盯住剧情线索，例如 B-07 警告、坐标布条、等待回声。", font=F_BODY, fill=COLORS["amber"])

    elif kind == "outro":
        paste_kenburns(frame, "op17-op30-contact.jpg", (0, 0, WIDTH, HEIGHT), t, zoom=0.05, darken=0.5)
        veil = Image.new("RGBA", (WIDTH, HEIGHT), (9, 16, 20, 145))
        frame = Image.alpha_composite(frame.convert("RGBA"), veil).convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text((150, 275), "下一步建议", font=F_TITLE, fill=COLORS["cyan"])
        draw.text((150, 390), "先做 OP13-1 → OP13-3", font=font(72, bold=True), fill=COLORS["text"])
        draw.text((150, 500), "3 个镜头、每镜 3 秒、只测试同机位和废站氛围。", font=F_H2, fill=COLORS["amber"])
        draw.text((150, 640), "跑通小段后，再扩展到 OP13-OP16。", font=F_H2, fill=COLORS["text"])

    alpha = transition_alpha(local_t, dur)
    return apply_scene_alpha(frame, alpha)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    total = sum(s["dur"] for s in SCENES)
    with imageio.get_writer(
        OUT,
        fps=FPS,
        codec="libx264",
        quality=8,
        macro_block_size=None,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    ) as writer:
        elapsed = 0.0
        for idx, scene in enumerate(SCENES):
            frames = int(scene["dur"] * FPS)
            for fi in range(frames):
                local_t = fi / FPS
                frame = draw_scene(scene["kind"], local_t, scene["dur"], idx)
                writer.append_data(np.asarray(frame))
            elapsed += scene["dur"]
            print(f"rendered scene {idx + 1}/{len(SCENES)} ({elapsed:.0f}/{total:.0f}s)")
    print(str(OUT))


if __name__ == "__main__":
    main()
