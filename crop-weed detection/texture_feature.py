#from localbinarypattern import LocalBinaryPatterns
import cv2
import os
import mahotas
import numpy as np
import matplotlib.pyplot as plt
import itertools
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import pandas as pd
from skimage import feature
import numpy as np
import random

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn import svm, metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib.colors import ListedColormap



class LocalBinaryPatterns:
	def __init__(self, n_P, R):
		self.n_P = n_P
		self.R = R
	def describe(self, image, eps=1e-7):
		lbp = feature.local_binary_pattern(image, self.n_P,
			self.R, method="uniform")
		(hist, _) = np.histogram(lbp.ravel(),
			bins=np.arange(0, self.n_P + 3),
			range=(0, self.n_P + 2))
		hist = hist.astype("float")
		hist /= (hist.sum() + eps)
		return hist

#Haralick Texture for comparison
def fd_haralick(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    haralick = mahotas.features.haralick(gray).mean(axis = 0)
    return haralick


train_path = "C:\\Users\\lekshmi\\Desktop\\code\\lbp_texture\\rgb\\train"


desc = LocalBinaryPatterns(24, 3)
data_main = []
labels = []
train_labels = os.listdir(train_path)
bins = 8
fixed_size       = tuple((224, 224))
# sort the training labels
train_labels.sort()
#print(train_labels)

#Extract features from image
for training_name in train_labels:
    #join the training data path and each training folder
    dir = os.path.join(train_path, training_name)
    
    current_label = training_name
    #loop over the images in each sub-folder
    for file in os.listdir(dir):
        #print(file)
        # load the image, convert it to grayscale, and describe it
        imageT = cv2.imread(os.path.join(dir, file))
        image = cv2.resize(imageT, fixed_size)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
       #LBP fetaure 
        hist = desc.describe(gray)
        fv_haralick = fd_haralick(image)
        global_feature = np.hstack([hist])#,fv_haralick])
        #print(global_feature)
        labels.append(current_label)
        data_main.append(global_feature)


scaler = MinMaxScaler(feature_range=(0, 1))
rescaled_feature = scaler.fit_transform(data_main)     
#rescaled_feature = StandardScaler().fit_transform(data) 
#print(f"data:{data}")
##############################################################

#classify
 
trainDataGlobal, testDataGlobal,trainLabelsGlobal, testLabelsGlobal = train_test_split(np.array(rescaled_feature),np.array(labels),test_size = 0.2,random_state = 42)

#model = KNeighborsClassifier(n_neighbors=3)
model= svm.SVC(C=1,kernel = 'rbf', gamma =1)
#model = RandomForestClassifier(n_estimators=500)


model.fit(trainDataGlobal, trainLabelsGlobal)

predictions= model.predict(testDataGlobal)

# Compute how well we performed
correct = (testLabelsGlobal == predictions).sum()
incorrect = (testLabelsGlobal != predictions).sum()
total = len(predictions)
#make confusion matrix
conf_matrix = confusion_matrix(testLabelsGlobal,predictions)

report = pd.DataFrame(classification_report(testLabelsGlobal,predictions,output_dict=True))
print(f"Test Result for model: {type(model).__name__}")  
print("_______________________________________________")
print(f"Correctly labelled: {correct}")
print(f"Incorrectly labelled: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")
print("_______________________________________________")
#print(f"CLASSIFICATION REPORT:\n{report}")
#print("_______________________________________________")
print(f"Confusion Matrix: \n")
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=['sugar beet',"  shepherd's purse",'cleavers'])
disp.plot()


