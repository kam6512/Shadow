import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

lineColor = (0,0,255)
thickness = 1

img_rgb = cv.imread(""".\samples\\menu.png""")
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread(""".\samples\\test1.png""",0)
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.95
loc = np.where( res >= threshold)
print(loc)
for pt in zip(*loc[::-1]):
   start = pt
   end = (pt[0] + w, pt[1] + h)
   cv.rectangle(img_rgb, start, end, lineColor, thickness)
   break

cv.imwrite(""".\samples\\res.png""",img_rgb)
pointX = ((start[0]+end[0])/2)
pointY = ((start[1]+end[1])/2)

print(start)
print(end)
print(pointX)
print(pointY)



#npm --add-python-to-path='true' --debug install --global windows-build-tools