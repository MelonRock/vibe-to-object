"""上传把关：照片太糊或者人脸太小，就请顾客换一张。

用法：python src/quality_gate.py photo.jpg
"""
import sys

import cv2

BLUR_MIN = 100.0  # 拉普拉斯方差下限，低于它算糊
FACE_MIN_RATIO = 0.12  # 最小人脸边长 / 照片短边


def blur_score(gray):
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def face_boxes(gray):
    path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(path)
    return detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)


def check(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return False, "读不到这张图片"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if blur_score(gray) < BLUR_MIN:
        return False, "照片太糊"
    faces = face_boxes(gray)
    if len(faces) == 0:
        return True, "没找到人脸，按宠物或物品处理"
    short_side = min(gray.shape[:2])
    smallest = min(min(w, h) for (x, y, w, h) in faces)
    if smallest < FACE_MIN_RATIO * short_side:
        return False, "人脸太小"
    return True, "通过"


if __name__ == "__main__":
    ok, reason = check(sys.argv[1])
    print("OK" if ok else "REJECT", reason)
