"""镜头避让：人脸框不能进入镜头区和裁切区。

坐标都按画布比例（0 到 1）。人脸框可以来自 MediaPipe 或任何检测器，
先换算成 (x, y, w, h) 的比例坐标。

用法：python src/camera_safe_zone.py templates/default.json 0.10,0.05,0.20,0.20
"""
import json
import sys


def overlaps(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def inside_trim(box, margin):
    x, y, w, h = box
    return x >= margin and y >= margin and x + w <= 1 - margin and y + h <= 1 - margin


def check(faces, template):
    cam = template["camera_zone"]
    cam_box = (cam["x"], cam["y"], cam["w"], cam["h"])
    margin = template["trim_margin"]
    problems = []
    for i, face in enumerate(faces, start=1):
        if overlaps(face, cam_box):
            problems.append(f"第 {i} 张脸进入镜头区")
        if not inside_trim(face, margin):
            problems.append(f"第 {i} 张脸碰到裁切线")
    return problems


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        template = json.load(f)
    faces = [tuple(map(float, arg.split(","))) for arg in sys.argv[2:]]
    problems = check(faces, template)
    print("OK" if not problems else "\n".join(problems))
