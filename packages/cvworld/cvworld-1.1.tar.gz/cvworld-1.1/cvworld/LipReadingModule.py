import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

class LipDetector:
    def __init__(self, max_faces=1, min_detection_conf=0.75):
        self.detector = FaceMeshDetector(maxFaces=max_faces, minDetectionCon=min_detection_conf)

    def find_lip_points(self, img):
        img, faces = self.detector.findFaceMesh(img, draw=False)
        lip_points = []

        if faces:
            face = faces[0]
            lip_points = [
                face[185], face[39], face[37], face[0], face[267],
                face[269], face[409], face[146], face[91], face[180],
                face[85], face[16], face[315], face[405], face[321]
            ]

        return img, lip_points

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    lip_detector = LipDetector()

    while True:
        success, img = cap.read()
        img, lip_points = lip_detector.find_lip_points(img)

        if lip_points:
            for point in lip_points:
                x, y = point
                cv2.circle(img, (x, y), 2, (255, 0, 255), cv2.FILLED)

        cv2.imshow("Images", img)
        cv2.waitKey(1)
