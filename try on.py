import os
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

# Load the person image
img = cv2.imread("C:/Users/nihil/OneDrive/Desktop/project/Resources/girl image.jpg")

# Initialize the pose detector
detector = PoseDetector()
img = detector.findPose(img)
lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

# Load dresses
dressFolderPath = "C:/Users/nihil/OneDrive/Desktop/project/Resources/dresses"
listdresses = os.listdir(dressFolderPath)
imageNumber = 0  # Change this index to try different dresses

# Constants
fixedRatio = 262 / 190  # widthOfdress / width between points 11 and 12
dressRatioHeightWidth = 581 / 440  # height/width of dress image
imgButtonRight = cv2.imread("C:/Users/nihil/OneDrive/Desktop/project/Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

if lmList:
    lm11 = lmList[11][1:3]
    lm12 = lmList[12][1:3]
    
    # Load and resize the selected dress
    imgDress = cv2.imread(os.path.join(dressFolderPath, listdresses[imageNumber]), cv2.IMREAD_UNCHANGED)
    widthOfDress = int(abs(lm11[0] - lm12[0]) * fixedRatio)
    imgDress = cv2.resize(imgDress, (widthOfDress, int(widthOfDress * dressRatioHeightWidth)))

    # Compute offset for alignment
    currentScale = abs(lm11[0] - lm12[0]) / 190
    offset = int(44 * currentScale), int(48 * currentScale)

    try:
        # Overlay dress on person
        img = cvzone.overlayPNG(img, imgDress, (lm12[0] - offset[0], lm12[1] - offset[1]))
    except Exception as e:
        print("Overlay failed:", e)

# Display result
cv2.imshow("Try-On Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
