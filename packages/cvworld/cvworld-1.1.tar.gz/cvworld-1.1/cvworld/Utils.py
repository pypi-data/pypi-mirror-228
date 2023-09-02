import cv2
import numpy as np


def cornerRect(img, bbox, l=30, t=5, rt=1, colorR=(255, 0, 255), colorC=(25, 25, 112)):
    x, y, w, h = bbox
    x1, y1 = x + w, y + h
    if rt != 0:
        cv2.rectangle(img, bbox, colorR, rt)
    # Top Left  x,y
    cv2.line(img, (x, y), (x + l, y), colorC, t)
    cv2.line(img, (x, y), (x, y + l), colorC, t)
    # Top Right  x1,y
    cv2.line(img, (x1, y), (x1 - l, y), colorC, t)
    cv2.line(img, (x1, y), (x1, y + l), colorC, t)
    # Bottom Left  x,y1
    cv2.line(img, (x, y1), (x + l, y1), colorC, t)
    cv2.line(img, (x, y1), (x, y1 - l), colorC, t)
    # Bottom Right  x1,y1
    cv2.line(img, (x1, y1), (x1 - l, y1), colorC, t)
    cv2.line(img, (x1, y1), (x1, y1 - l), colorC, t)

    return img

def putTextRect(img, text, pos, scale=3, thickness=3, colorT=(0, 0, 0),
                colorR=(255, 153, 255), font=cv2.FONT_HERSHEY_TRIPLEX,
                offset=10, border=None, colorB=(0, 255, 0)):

    ox, oy = pos
    (w, h), _ = cv2.getTextSize(text, font, scale, thickness)

    x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset

    cv2.rectangle(img, (x1, y1), (x2, y2), colorR, cv2.FILLED)
    if border is not None:
        cv2.rectangle(img, (x1, y1), (x2, y2), colorB, border)
    cv2.putText(img, text, (ox, oy), font, scale, colorT, thickness)

    return img, [x1, y2, x2, y1]

def rotateImage(img, angle, scale=1):
    h, w = img.shape[:2]
    center = (w / 2, h / 2)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=scale)
    img = cv2.warpAffine(src=img, M=rotate_matrix, dsize=(w, h))
    return img

def blur(img, kernal=(5, 5), sigmax=0):
    img = cv2.GaussianBlur(img, kernal, sigmax)
    return img

def canny(img, threshold1=75, threshold2=100):
    img = cv2.Canny(img, threshold1, threshold2)
    return img

def edge(img, kernal=(5,5), sigmax=0, threshold1=75, threshold2=100
         , low_yellow=np.array([18, 94, 140]), up_yellow=np.array([48, 255, 255])):
    img = cv2.GaussianBlur(img, kernal, sigmax)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low_yellow, up_yellow)
    img = cv2.Canny(mask, threshold1, threshold2)
    return img

def threshold_image(img, threshold):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binary

def line(img, pt1, pt2, color=(255, 0, 255), t=2):
    img = cv2.line(img, pt1, pt2, color, t)
    return img

def circle(img, centre, radius, color=(255, 0, 255), t=cv2.FILLED):
    img = cv2.circle(img, centre, radius, color, t)
    return img

def videocapture(img):
    img = cv2.VideoCapture(img)
    return img

def imshow(winName, img):
    img = cv2.imshow(winName, img)
    return img

def waitkey(delay):
    img = cv2.waitKey(delay)
    return img

def main():
    cap = videocapture(0)
    while True:
        success, img = cap.read()
        img = edge(img, (5, 5), 0, 75, 100)
        imshow("EDGES", img)
        waitkey(0)

if __name__ == "__main__":
    main()
