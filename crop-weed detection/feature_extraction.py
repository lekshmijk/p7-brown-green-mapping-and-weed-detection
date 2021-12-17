import cv2
import glob
from skimage import img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import skimage
from skimage.io import imread, imshow
from skimage.color import rgb2gray, rgb2hsv
from skimage.measure import label, regionprops, regionprops_table
from skimage.filters import threshold_otsu
from scipy.ndimage import median_filter
from matplotlib.patches import Rectangle
from skimage.io import imread, imshow
from skimage.color import rgb2gray, rgb2hsv
from skimage.measure import label, regionprops, regionprops_table
from skimage.filters import threshold_otsu
from scipy.ndimage import median_filter
from matplotlib.patches import Rectangle
import os
import math


current_path = os.getcwd()
path = "C:\\Users\\robin\\OneDrive\\Bureaublad\\dataset\\synthetic_sugarbeat_capsella\\process\\"
os.chdir(path)
img_number = 0

featuresList = []
anotherFeatureList = []

def getContours(img, img_number, file_name, hsv):
        contours = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        BLOB_number = 0

        for cnt in contours: 
            area = cv2.contourArea(cnt)
            #print(area)
            if area > 1500:
                x,y,w,h = cv2.boundingRect(cnt)
                (b1, b2),(major_axis, minor_axis), angle = cv2.fitEllipse(cnt)
                perimeter = cv2.arcLength(cnt, True)
                form_factor = (4 * math.pi * area) / math.pow(perimeter, 2)
                hull = cv2.convexHull(cnt)
                hullArea = cv2.contourArea(hull)
                solidity = area / float(hullArea)
                hullPerimeter = cv2.arcLength(hull,True)
                convexity = hullPerimeter / perimeter
                eccentricity = minor_axis / major_axis
                # Calculate Moments
                moments = cv2.moments(img)
                # Calculate Hu Moments
                huMoments = cv2.HuMoments(moments)
                # Log scale hu moments
                for i in range(0,7):
                    huMoments[i] = -1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))
                BLOB = img[y:y+h, x:x+w]
                BLOB_rgb = imgrgb[y:y+h, x:x+w]
                BLOB_grey = grey[y:y+h, x:x+w]
                BLOB_hsv = hsv[y:y+h,x:x+w]
                cv2.imwrite('C:\\Users\\robin\\OneDrive\\Bureaublad\\dataset\\synthetic_sugarbeat_capsella\\Blobs_rgb\\BLOB'+str(img_number)+'_{}.png'.format(BLOB_number), BLOB_rgb)
                print('BLOB'+str(img_number)+'_{}.png'.format(BLOB_number))
                blob_file = 'BLOB'+str(img_number)+'_{}.png'.format(BLOB_number)
                #cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,12),2)
            
                BLOB_number += 1
            
                hsv_features = hsvFeatures(BLOB_hsv)
                feature = [blob_file, form_factor, eccentricity, convexity, solidity, huMoments[0],huMoments[1],huMoments[2],huMoments[3],huMoments[4],huMoments[5],huMoments[6]]
                feature.extend(hsv_features)
                featuresList.append(feature)

files = os.listdir()

def hsvFeatures(img):

    #hsv = cv2.imread(imagefile, cv2.COLOR_RGB2HSV)  # Read a color picture
    h, s, v = cv2.split(img)
#color_feature = []  #  Initialize color characteristics
#  One-stage moment (mean mean)
    h_mean = np.mean(h)  # np.sum(h)/float(N)
    s_mean = np.mean(s)  # np.sum(s)/float(N)
    v_mean = np.mean(v)  # np.sum(v)/float(N)
#featuresList.append()  #  One-stage moment placement feature array
#  Secondary moments (standard difference STD)
    h_std = np.std(h)  # np.sqrt(np.mean(abs(h - h.mean())**2))
    s_std = np.std(s)  # np.sqrt(np.mean(abs(s - s.mean())**2))
    v_std = np.std(v)  # np.sqrt(np.mean(abs(v - v.mean())**2))
#featuresList.append([])  #  Second order moment placed in a feature array
#  Three-order moment (slope Skewness)
    h_skewness = np.mean(abs(h - h.mean()) ** 3)
    s_skewness = np.mean(abs(s - s.mean()) ** 3)
    v_skewness = np.mean(abs(v - v.mean()) ** 3)
    h_thirdMoment = h_skewness ** (1. / 3)
    s_thirdMoment = s_skewness ** (1. / 3)
    v_thirdMoment = v_skewness ** (1. / 3)
#featuresList.append([])  #  Three-order moments in the feature array
    return [h_mean, s_mean, v_mean, h_std, s_std, v_std,h_thirdMoment, s_thirdMoment, v_thirdMoment]

for file in files:
    #print(file)
    imgrgb = cv2.imread(file)

    grey = cv2.cvtColor(imgrgb,cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(imgrgb, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (25, 25, 25), (70, 255,255))

    imask = mask>0
    green = np.zeros_like(imgrgb, np.uint8)
    green[imask] = imgrgb[imask]

    kernel = np.ones((6,6),np.uint8)
    kernel2 = np.ones((3,3),np.uint8)

    closing2 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)            
    
    getContours(closing2, img_number, file, hsv)
    cv2.imwrite("C:\\Users\\robin\\OneDrive\\Bureaublad\\dataset\\synthetic_sugarbeat_capsella\\processed\\img_"+str(img_number)+".png", closing2)
    img_number +=1



blobs = label(closing2 > 0)

properties =['Blob_path','form_factor', 'eccentricity', 'convexity', 'solidity', 'HuMoments_1', 'HuMoments_2', 'HuMoments_3', 'HuMoments_4','HuMoments_5', 'HuMoments_6', 'HuMoments_7', 'h_mean','s_mean','v_mean','h_std','s_std','v_std','h_3','s_3','v_3']

df = pd.DataFrame(featuresList)

os.chdir(current_path)
df.to_csv('feature_three_classes.csv', index=False, sep=",", header=properties)