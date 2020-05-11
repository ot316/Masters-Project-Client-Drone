import cv2, time
import numpy as np

for i in range(1,4):
    image = cv2.imread(f'.//test_images/{i}.png', 1)
    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
