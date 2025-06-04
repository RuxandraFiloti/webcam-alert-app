import cv2 #uses BGR not RGB 

array = cv2.imread("image.png")

print (array.shape) #displays the dimension of array -> e.g. (3,4,3) - 3 columns, 4 rows and 3 channels (BGR)

print(array)