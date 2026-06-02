from __future__ import annotations

import math
import subprocess
import wave
from pathlib import Path

import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
AUDIO = ROOT / "audio_buttons"
RENDERS = ROOT / "renders"
OUT_SILENT = RENDERS / "边界回声_ComfyUI界面按钮详解_新手跟做_silent.mp4"
OUT_AUDIO = RENDERS / "buttons_narration_combined.wav"
OUT_FINAL = RENDERS / "边界回声_ComfyUI界面按钮详解_新手跟做.mp4"
W, H = 1920, 1080
FPS = 20

COLORS = {
    "bg": (9, 16, 20),
    "panel": (17, 28, 32),
    "panel2": (24, 37, 42),
    "text": (232, 241, 238),
    "muted": (157, 176, 170),
    "cyan": (114, 215, 208),
    "amber": (217, 168, 90),
    "red": (208, 93, 87),
    "green": (118, 202, 151),
    "purple": (185, 142, 255),
}


def font(size: int, bold: bool = False, mono: bool = False):
    if mono:
        paths = [r"C:\Windows\Fonts\consola.ttf"]
    elif bold:
        paths = [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc"]
    else:
        paths = [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc"]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_TITLE = font(74, True)
F_BIG = font(55, True)
F_H2 = font(39, True)
F_BODY = font(30)
F_SMALL = font(23)
F_TINY = font(19)
F_MONO = font(25, mono=True)
F_PATH = font(22, mono=True)


def ease(x):
    x = max(0, min(1, x))
    return 0.5 - 0.5 * math.cos(math.pi * x)


def out(x):
    x = max(0, min(1, x))
    return 1 - (1 - x) ** 3


def rounded(draw, box, r, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def text_wh(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0], b[3] - b[1]


def wrap(draw, text, xy, f, fill, maxw, gap=8):
    x, y = xy
    line = ""
    for ch in text:
        trial = line + ch
        if text_wh(draw, trial, f)[0] <= maxw or not line:
            line = trial
        else:
            draw.text((x, y), line, font=f, fill=fill)
            y += text_wh(draw, line, f)[1] + gap
            line = ch
    if line:
        draw.text((x, y), line, font=f, fill=fill)
        y += text_wh(draw, line, f)[1] + gap
    return y


def pill(draw, xy, text, fill, fg=(7, 13, 16), f=F_SMALL):
    x, y = xy
    tw, th = text_wh(draw, text, f)
    rounded(draw, (x, y, x + tw + 30, y + th + 17), 17, fill)
    draw.text((x + 15, y + 7), text, font=f, fill=fg)


def cursor(draw, x, y, label=None, color=None):
    fill = color or COLORS["text"]
    draw.polygon([(x, y), (x + 32, y + 88), (x + 52, y + 54), (x + 92, y + 54)], fill=fill)
    draw.line((x, y, x + 32, y + 88, x + 52, y + 54, x + 92, y + 54, x, y), fill=COLORS["bg"], width=3)
    if label:
        rounded(draw, (x + 70, y + 36, x + 70 + 300, y + 92), 16, COLORS["cyan"])
        draw.text((x + 90, y + 49), label, font=F_SMALL, fill=COLORS["bg"])


def click_ring(draw, x, y, t, color=None):
    color = color or COLORS["amber"]
    r = int(18 + 40 * ease((t * 2) % 1))
    a = int(230 * (1 - ease((t * 2) % 1)))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((x - r, y - r, x + r, y + r), outline=color + (a,), width=5)
    return overlay


def asset(name):
    return Image.open(ASSETS / name).convert("RGB")


def paste_cover(frame, name, box, t=0, zoom=0.03, darken=0.0, blur=0.0):
    img = asset(name)
    if darken:
        img = ImageEnhance.Brightness(img).enhance(1 - darken)
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    iw, ih = img.size
    scale = max(bw / iw, bh / ih) * (1 + zoom * ease(t))
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    crop = img.crop(((nw - bw) // 2, (nh - bh) // 2, (nw - bw) // 2 + bw, (nh - bh) // 2 + bh))
    frame.paste(crop, (x1, y1))


def base(idx, title, chapter, progress):
    frame = Image.new("RGB", (W, H), COLORS["bg"])
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse((-270, -250, 830, 620), fill=(43, 105, 106, 42))
    od.ellipse((1320, 620, 2230, 1330), fill=(145, 86, 38, 30))
    for x in range(-180, W, 108):
        od.line((x, 0, x + 260, H), fill=(255, 255, 255, 8), width=1)
    frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")
    draw = ImageDraw.Draw(frame)
    draw.text((70, 42), chapter, font=F_SMALL, fill=COLORS["cyan"])
    draw.text((70, 78), title, font=F_H2, fill=COLORS["text"])
    draw.text((1665, 48), f"{idx:02d}/18", font=F_MONO, fill=COLORS["muted"])
    draw.line((70, 140, 1850, 140), fill=(61, 82, 85), width=3)
    draw.line((70, 140, 70 + int(1780 * progress), 140), fill=COLORS["amber"], width=5)
    return frame


def subtitle(draw, text):
    rounded(draw, (210, 910, 1710, 1032), 24, (7, 13, 16), outline=(57, 82, 84), width=2)
    wrap(draw, text, (255, 934), F_BODY, COLORS["text"], 1410, gap=8)


def panel(draw, box, title=None, outline=None):
    rounded(draw, box, 26, COLORS["panel"], outline or (55, 78, 82), 2)
    if title:
        draw.text((box[0] + 34, box[1] + 26), title, font=F_H2, fill=COLORS["text"])


def mock_node(draw, xy, title, body, color):
    x, y = xy
    rounded(draw, (x, y, x + 300, y + 142), 18, COLORS["panel2"], outline=color, width=3)
    draw.text((x + 22, y + 18), title, font=F_BODY, fill=COLORS["text"])
    wrap(draw, body, (x + 22, y + 66), F_SMALL, COLORS["muted"], 245, gap=5)
    draw.ellipse((x - 10, y + 62, x + 12, y + 84), fill=color)
    draw.ellipse((x + 288, y + 62, x + 312, y + 84), fill=color)


def read_segments():
    rows = []
    for line in (ROOT / "narration_buttons_segments.txt").read_text(encoding="utf-8").splitlines():
        if "|" in line:
            sid, text = line.split("|", 1)
            rows.append((sid, text))
    return rows


SEGMENTS = read_segments()
TEXT = dict(SEGMENTS)


SCENES = [
    ("界面按钮总览", "新手跟做版", "intro"),
    ("启动与地址", "先打开页面", "startup"),
    ("四块区域", "先认识界面", "zones"),
    ("左侧功能栏", "常用入口", "sidebar"),
    ("画布操作", "移动、缩放、删除", "canvas"),
    ("节点端口", "线怎么接", "ports"),
    ("选择模型", "Checkpoint Loader", "checkpoint"),
    ("正向提示词", "Positive Prompt", "positive"),
    ("负向提示词", "Negative Prompt", "negative"),
    ("采样参数", "KSampler", "ksampler"),
    ("画面尺寸", "Empty Latent Image", "latent"),
    ("开始生成", "Queue Prompt", "queue"),
    ("输出与历史", "Output / History", "output"),
    ("安装视频节点", "Manager", "manager"),
    ("视频工作流", "图生视频怎么连", "video_flow"),
    ("OP13 跟做", "导入关键帧", "op13"),
    ("视频参数", "先小后大", "video_params"),
    ("保存与复盘", "最后的顺序", "finish"),
]


def audio_durations():
    d = {}
    for sid, _ in SEGMENTS:
        with wave.open(str(AUDIO / f"segment_{sid}.wav"), "rb") as w:
            d[sid] = w.getnframes() / w.getframerate()
    return d


def combine_audio():
    first = AUDIO / "segment_01.wav"
    with wave.open(str(first), "rb") as w:
        params = w.getparams()
        silence = b"\x00" * params.sampwidth * params.nchannels
    with wave.open(str(OUT_AUDIO), "wb") as outw:
        outw.setparams(params)
        for sid, _ in SEGMENTS:
            with wave.open(str(AUDIO / f"segment_{sid}.wav"), "rb") as w:
                outw.writeframes(w.readframes(w.getnframes()))
            outw.writeframes(silence * int(params.framerate * 0.65))


def draw_scene(kind, idx, local_t, dur, text):
    t = local_t / dur
    frame = base(idx + 1, SCENES[idx][0], SCENES[idx][1], (idx + t) / len(SCENES))
    draw = ImageDraw.Draw(frame)

    if kind == "intro":
        paste_cover(frame, "live/01-comfyui-live-home.png", (0, 0, W, H), t, darken=0.48, blur=1.0, zoom=0.04)
        veil = Image.new("RGBA", (W, H), (9, 16, 20, 150))
        frame = Image.alpha_composite(frame.convert("RGBA"), veil).convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text((120, 270), "ComfyUI 界面按钮详解", font=font(96, True), fill=COLORS["cyan"])
        draw.text((120, 390), "新手跟做版", font=font(80, True), fill=COLORS["text"])
        draw.text((125, 510), "每一步点哪里、改哪里、怎么设置", font=F_BIG, fill=COLORS["amber"])
        pill(draw, (130, 635), "用于《边界回声》AI 真人剧视频", COLORS["cyan"])

    elif kind == "startup":
        panel(draw, (120, 230, 930, 785), "双击启动")
        draw.text((175, 350), r"F:\ComfyUI\启动ComfyUI.bat", font=F_MONO, fill=COLORS["cyan"])
        draw.text((175, 430), "如果已经在运行，脚本会直接打开浏览器。", font=F_BODY, fill=COLORS["text"])
        draw.text((175, 520), "打不开时：先点停止脚本，再重新启动。", font=F_BODY, fill=COLORS["amber"])
        paste_cover(frame, "live/01-comfyui-live-home.png", (990, 240, 1785, 760), t, zoom=0.015)
        cursor(draw, 1390, 260, "地址栏")
        draw.text((1020, 790), "http://127.0.0.1:8188", font=F_MONO, fill=COLORS["cyan"])

    elif kind == "zones":
        paste_cover(frame, "live/01-comfyui-live-home.png", (110, 205, 1810, 850), t, zoom=0.01)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        areas = [
            ((112, 205, 175, 850), COLORS["cyan"], "左侧功能栏"),
            ((176, 205, 1600, 850), COLORS["amber"], "中间画布"),
            ((430, 210, 1160, 560), COLORS["purple"], "节点区"),
            ((1590, 625, 1810, 850), COLORS["green"], "队列 / 历史"),
        ]
        for box, color, lab in areas:
            od.rectangle(box, outline=color + (230,), width=6)
            od.rectangle((box[0], box[1] - 42, box[0] + 210, box[1] - 4), fill=color + (230,))
            od.text((box[0] + 10, box[1] - 38), lab, font=F_SMALL, fill=(0, 0, 0, 255))
        frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

    elif kind == "sidebar":
        paste_cover(frame, "live/01-comfyui-live-home.png", (120, 200, 1020, 860), t, zoom=0.01)
        panel(draw, (1090, 230, 1790, 820), "左侧栏最常用")
        items = [("节点", "找 Load Image、KSampler 等节点"), ("模型", "检查模型和 LoRA"), ("工作流", "保存/加载流程"), ("模板", "快速打开示例")]
        y = 335
        for k, v in items:
            pill(draw, (1140, y), k, COLORS["cyan"])
            draw.text((1255, y + 5), v, font=F_BODY, fill=COLORS["text"])
            y += 100
        cursor(draw, 135, 230, "这里")

    elif kind == "canvas":
        paste_cover(frame, "live/01-comfyui-live-home.png", (100, 205, 1820, 840), t, zoom=0.015)
        panel(draw, (180, 665, 1740, 865), "画布操作")
        ops = ["滚轮：缩放", "中键 / 空格拖动：移动画布", "拖节点标题：移动节点", "框选 + Delete：删除节点"]
        x = 235
        for op in ops:
            pill(draw, (x, 735), op, COLORS["amber"])
            x += 360
        cursor(draw, int(700 + 260 * math.sin(t * math.pi * 2)), int(360 + 80 * math.cos(t * math.pi * 2)), "拖动画布")

    elif kind == "ports":
        panel(draw, (130, 235, 1790, 820), "端口和连线")
        mock_node(draw, (260, 450), "Checkpoint", "模型 / CLIP / VAE 输出", COLORS["cyan"])
        mock_node(draw, (720, 450), "CLIP Text Encode", "提示词输入，Conditioning 输出", COLORS["amber"])
        mock_node(draw, (1180, 450), "KSampler", "接模型、正向、负向、latent", COLORS["purple"])
        draw.line((560, 520, 720, 520), fill=COLORS["cyan"], width=6)
        draw.line((1020, 520, 1180, 520), fill=COLORS["amber"], width=6)
        cursor(draw, 520, 486, "从输出拖到输入")

    elif kind == "checkpoint":
        paste_cover(frame, "live/01-comfyui-live-home.png", (115, 220, 1810, 810), t, zoom=0.012)
        rounded(draw, (118, 450, 405, 555), 12, fill=None, outline=COLORS["cyan"], width=6)
        cursor(draw, 360, 512, "点模型下拉框")
        panel(draw, (850, 600, 1760, 855), "选择模型")
        draw.text((900, 700), "v1-5-pruned-emaonly-fp16.safetensors", font=F_MONO, fill=COLORS["cyan"])
        draw.text((900, 755), "以后换写实模型，也是在这个下拉框换。", font=F_BODY, fill=COLORS["text"])

    elif kind == "positive":
        paste_cover(frame, "live/01-comfyui-live-home.png", (110, 210, 1810, 830), t, zoom=0.012)
        rounded(draw, (475, 228, 850, 360), 12, fill=None, outline=COLORS["cyan"], width=6)
        panel(draw, (920, 235, 1780, 805), "正向提示词示例")
        lines = ["cinematic live-action keyframe", "abandoned old north station", "same low camera angle", "wet old children's shoe", "restrained mystery drama"]
        y = 345
        for line in lines:
            draw.text((980, y), line, font=F_MONO, fill=COLORS["text"])
            y += 58
        cursor(draw, 780, 250, "点文本框")

    elif kind == "negative":
        paste_cover(frame, "live/01-comfyui-live-home.png", (110, 210, 1810, 830), t, zoom=0.012)
        rounded(draw, (475, 405, 850, 555), 12, fill=None, outline=COLORS["red"], width=6)
        panel(draw, (920, 235, 1780, 805), "负向提示词示例", outline=COLORS["red"])
        lines = ["anime, cartoon", "changed camera angle", "station lights, neon ads", "large white hair", "watermark, bad face"]
        y = 345
        for line in lines:
            draw.text((980, y), line, font=F_MONO, fill=(255, 218, 213))
            y += 58
        cursor(draw, 780, 430, "这里写禁止项")

    elif kind == "ksampler":
        paste_cover(frame, "live/01-comfyui-live-home.png", (100, 205, 1815, 835), t, zoom=0.012)
        rounded(draw, (875, 215, 1155, 452), 12, fill=None, outline=COLORS["amber"], width=6)
        panel(draw, (1220, 230, 1790, 815), "KSampler 新手参数")
        rows = [("Steps", "20 左右"), ("CFG", "7 - 8"), ("Sampler", "euler"), ("Scheduler", "normal"), ("Denoise", "出图 1.00")]
        y = 340
        for k, v in rows:
            pill(draw, (1270, y), k, COLORS["cyan"])
            draw.text((1430, y + 5), v, font=F_BODY, fill=COLORS["text"])
            y += 80
        cursor(draw, 1110, 315, "别乱改太多")

    elif kind == "latent":
        paste_cover(frame, "live/01-comfyui-live-home.png", (110, 210, 1810, 830), t, zoom=0.012)
        rounded(draw, (528, 565, 807, 685), 12, fill=None, outline=COLORS["cyan"], width=6)
        panel(draw, (930, 260, 1760, 795), "画面尺寸建议")
        rows = [("方图测试", "512 x 512"), ("横版视频", "768 x 432 或 1024 x 576"), ("Batch size", "先设 1"), ("原则", "先跑通，再变大")]
        y = 365
        for k, v in rows:
            pill(draw, (990, y), k, COLORS["amber"])
            draw.text((1170, y + 5), v, font=F_BODY, fill=COLORS["text"])
            y += 86

    elif kind == "queue":
        paste_cover(frame, "live/01-comfyui-live-home.png", (105, 205, 1815, 835), t, zoom=0.012)
        panel(draw, (1220, 270, 1770, 760), "Queue Prompt")
        rounded(draw, (1345, 455, 1645, 535), 22, COLORS["cyan"])
        draw.text((1400, 474), "Queue Prompt", font=F_BODY, fill=COLORS["bg"])
        cursor(draw, 1450, 390, "点一次就好")
        ring = click_ring(draw, 1495, 495, t, COLORS["amber"])
        frame = Image.alpha_composite(frame.convert("RGBA"), ring).convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text((1280, 575), "点完先等进度，不要连续猛点。", font=F_BODY, fill=COLORS["amber"])

    elif kind == "output":
        panel(draw, (120, 230, 1775, 820), "生成完成后看哪里")
        paste_cover(frame, "comfyui-test-output.png", (155, 335, 545, 725), t, zoom=0.025)
        steps = [(650, 350, "1. 看输出节点预览"), (650, 445, "2. 看右侧 History / 队列历史"), (650, 540, r"3. 文件在 F:\ComfyUI\output"), (650, 635, "4. 文件名前缀写 OP13_test 这类名字")]
        for x, y, s in steps:
            pill(draw, (x, y), s, COLORS["cyan"] if "1." in s else COLORS["amber"])

    elif kind == "manager":
        panel(draw, (120, 230, 1780, 820), "安装视频节点")
        cols = [("点 Manager", "进入 ComfyUI-Manager"), ("Custom Nodes Manager", "管理自定义节点"), ("搜索并安装", "Video Helper Suite / AnimateDiff"), ("Restart", "重启 ComfyUI")]
        x = 175
        for i, (a, b) in enumerate(cols):
            mock_node(draw, (x, 430), a, b, COLORS["cyan"] if i < 2 else COLORS["amber"])
            if i < 3:
                draw.line((x + 300, 500, x + 360, 500), fill=COLORS["amber"], width=5)
            x += 405
        draw.text((180, 705), "当前机器已装 Manager；视频节点需要从 Manager 里再装。", font=F_BODY, fill=COLORS["text"])

    elif kind == "video_flow":
        panel(draw, (90, 230, 1830, 820), "图生视频最小结构")
        nodes = [("Load Image", "导入 OP 关键帧"), ("Prompt", "正向/负向"), ("Video Model", "运动控制"), ("Animate", "生成帧序列"), ("Save Video", "保存 MP4")]
        x = 145
        for i, (a, b) in enumerate(nodes):
            mock_node(draw, (x, 450), a, b, COLORS["cyan"] if i < 2 else COLORS["amber"])
            if i < 4:
                draw.line((x + 300, 520, x + 350, 520), fill=COLORS["amber"], width=5)
            x += 355
        cursor(draw, 150, 390, "从这里开始")

    elif kind == "op13":
        paste_cover(frame, "op13-shoe-ruin.png", (115, 230, 920, 820), t, zoom=0.06)
        panel(draw, (995, 245, 1780, 805), "Load Image 设置")
        draw.text((1050, 350), "选择：OP13-1 同机位废站鞋", font=F_BODY, fill=COLORS["text"])
        draw.text((1050, 430), "提示词：鞋不动，环境微动", font=F_BODY, fill=COLORS["cyan"])
        draw.text((1050, 510), "禁止：换背景、换机位、大动作", font=F_BODY, fill=COLORS["amber"])
        draw.text((1050, 590), "目标：先验证连续性", font=F_BODY, fill=COLORS["text"])
        cursor(draw, 760, 650, "导入这张")

    elif kind == "video_params":
        panel(draw, (160, 240, 1760, 820), "视频参数第一轮别贪大")
        rows = [("时长", "3 - 5 秒"), ("FPS", "12 - 24"), ("分辨率", "先低分辨率"), ("运动幅度", "低"), ("检查重点", "同机位 / 背景 / 道具")]
        y = 350
        for k, v in rows:
            pill(draw, (250, y), k, COLORS["cyan"])
            draw.text((430, y + 5), v, font=F_BIG if k in ("时长", "FPS") else F_BODY, fill=COLORS["text"])
            y += 86
        draw.text((1060, 510), "稳定之后，再拉高分辨率和时长。", font=F_BIG, fill=COLORS["amber"])

    elif kind == "finish":
        paste_cover(frame, "op17-op30-contact.jpg", (0, 0, W, H), t, darken=0.55, zoom=0.04)
        veil = Image.new("RGBA", (W, H), (9, 16, 20, 160))
        frame = Image.alpha_composite(frame.convert("RGBA"), veil).convert("RGB")
        draw = ImageDraw.Draw(frame)
        draw.text((135, 260), "新手固定顺序", font=F_TITLE, fill=COLORS["cyan"])
        items = ["保存工作流", "Queue Prompt", "看历史输出", "抽帧复盘", "再做下一镜"]
        x = 145
        for i, item in enumerate(items):
            pill(draw, (x, 455), f"{i+1}. {item}", COLORS["amber"] if i == 0 else COLORS["cyan"], f=F_BODY)
            x += 315
        draw.text((145, 620), "先做 OP13-1 到 OP13-3 的三镜头短段，稳定后再扩展整段。", font=F_BIG, fill=COLORS["text"])

    subtitle(draw, text)
    alpha = 255
    if local_t < 0.45:
        alpha = int(255 * out(local_t / 0.45))
    elif dur - local_t < 0.45:
        alpha = int(255 * out((dur - local_t) / 0.45))
    if alpha < 255:
        frame = Image.blend(Image.new("RGB", (W, H), COLORS["bg"]), frame, alpha / 255)
    return frame


def main():
    RENDERS.mkdir(parents=True, exist_ok=True)
    durs = audio_durations()
    combine_audio()
    scene_durs = [durs[sid] + 0.65 for sid, _ in SEGMENTS]
    total_frames = sum(math.ceil(d * FPS) for d in scene_durs)
    done = 0
    with imageio.get_writer(
        OUT_SILENT,
        fps=FPS,
        codec="libx264",
        quality=8,
        macro_block_size=None,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    ) as writer:
        for idx, ((sid, text), dur) in enumerate(zip(SEGMENTS, scene_durs)):
            n = math.ceil(dur * FPS)
            for fi in range(n):
                writer.append_data(np.asarray(draw_scene(SCENES[idx][2], idx, fi / FPS, dur, text)))
            done += n
            print(f"rendered {idx+1}/18 frames={done}/{total_frames}")
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
