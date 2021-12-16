import csv
import random
import pandas as pd
import numpy as np
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

#model = svm.SVC(kernel ='poly', degree = 2, gamma= 'auto')
#model= svm.SVC(kernel = 'rbf', gamma =1)
#model = svm.SVC(kernel = 'linear')
#model = KNeighborsClassifier(n_neighbors=3)
#model = svm.SVC(C=1,kernel='rbf',gamma='scale')
model = RandomForestClassifier(n_estimators=500)

#0 is crop 1 is weed
# Read data in from file
features = pd.read_csv('C:\\Users\\lekshmi\\Desktop\\code\\asphalt-crack-classifier\\feature_three_classes_final.csv')


# Separate data into training and testing groups
x = features.iloc[:, -19:].values
y = features['Class'].values

#scaler = MinMaxScaler(feature_range=(0, 1))
#rescaled_feature = scaler.fit_transform(data) 
#standardize feature data
x_s = StandardScaler().fit_transform(x)

######################################################################################################
#PCA reduce the amount of feature dimensions
pca = PCA(n_components=3)
principalComponents = pca.fit_transform(x_s)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2', 'principal component 3'])

#concatenates the PCA's to the Class Column
finalDf = pd.concat([principalDf, features[['Class']]], axis = 1)


#the variances explained by each of the principal components
explained_variance = pca.explained_variance_ratio_

###################################################################################################

#Divides data into training and testing samples, and associated training and testing lables. then divides it
x_training, x_testing, y_training, y_testing = train_test_split(x_s, y, test_size=0.2, random_state=42)


# Fit model
model.fit(x_training, y_training)

# Make predictions on the testing set
predictions = model.predict(x_testing)


# Compute how well we performed
correct = (y_testing == predictions).sum()
incorrect = (y_testing != predictions).sum()
total = len(predictions)
#make confusion matrix
conf_matrix = confusion_matrix(y_testing,predictions)

#report = pd.DataFrame(classification_report(y_testing,predictions,output_dict=True))
print(f"Test Result for model: {type(model).__name__}")  
print("_______________________________________________")
print(f"Correctly labelled: {correct}")
print(f"Incorrectly labelled: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")
print("_______________________________________________")
#print(f"CLASSIFICATION REPORT:\n{report}")
#print("_______________________________________________")
print(f"Confusion Matrix: \n")
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=['sugar beet',"  shepherd's purse",'cleaver'])
disp.plot()


#roc curve (doesn't work bc classifier needs to be binary smh):
#metrics.plot_roc_curve(model, x_testing,y_testing)
#plt.show()


#2d plot:
fig = plt.figure()
#plt.grid(b=None,which='major',axis='both')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('2 component PCA')
Classes = ['0','1',]
cmap = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
plt.scatter(principalComponents[:, 0], principalComponents[:, 1], c=y, cmap=cmap, edgecolor='k', s=20)
plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
plt.show()


#3d plot:
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.set_xlabel('PC 1')
ax.set_ylabel('PC 2')
ax.set_zlabel('PC 3')
plt.title('3 component PCA')
ax.scatter3D(principalComponents[:, 0], principalComponents[:, 1], principalComponents[:, 2], c=y, cmap=cmap, edgecolor='k', s=40)
plt.show()


#feature_imp = pd.Series(model.feature_importances_,index=x).sort_values(ascending=False)
#feature_imp