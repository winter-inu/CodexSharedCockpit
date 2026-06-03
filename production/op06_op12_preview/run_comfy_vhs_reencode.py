from pathlib import Path
import json
import time
import urllib.error
import urllib.request
import uuid


SERVER = "http://127.0.0.1:8188"
VIDEO = Path(r"F:\CodexSharedCockpit\production\op06_op12_preview\renders\边界回声_OP06_OP12_关键帧视频预览.mp4")


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
        body = exc.read().decode("utf-8", errors="replace")
        print(body)
        raise


def get_json(path: str):
    with urllib.request.urlopen(SERVER + path, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    client_id = str(uuid.uuid4())
    workflow = {
        "1": {
            "class_type": "VHS_LoadVideoPath",
            "inputs": {
                "video": str(VIDEO),
                "force_rate": 10,
                "custom_width": 960,
                "custom_height": 540,
                "frame_load_cap": 0,
                "skip_first_frames": 0,
                "select_every_nth": 1,
                "format": "None",
            },
        },
        "2": {
            "class_type": "VHS_VideoCombine",
            "inputs": {
                "images": ["1", 0],
                "frame_rate": 10,
                "loop_count": 0,
                "filename_prefix": "BoundaryEcho_OP06_OP12_ComfyUI_VHS_540p",
                "format": "video/h264-mp4",
                "pingpong": False,
                "save_output": True,
                "pix_fmt": "yuv420p",
                "crf": 19,
                "save_metadata": True,
                "trim_to_audio": False,
            },
        },
    }
    queued = post_json("/prompt", {"prompt": workflow, "client_id": client_id})
    prompt_id = queued["prompt_id"]
    print(f"prompt_id={prompt_id}")

    for _ in range(240):
        hist = get_json(f"/history/{prompt_id}")
        if prompt_id in hist:
            print(json.dumps(hist[prompt_id].get("outputs", {}), ensure_ascii=False, indent=2))
            return
        time.sleep(2)
    raise TimeoutError("ComfyUI VHS re-encode did not finish in time")


if __name__ == "__main__":
    main()
