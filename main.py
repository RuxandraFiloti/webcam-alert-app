import cv2 #uses BGR
import time 
from emailing import send_email

video = cv2.VideoCapture(0) # 0 - the number for one laptop camera
time.sleep(1) #give the camera some time to reload - creates 1 frame/sec

first_frame = None

status_list = []


while True:
    status = 0 #no object

    check, frame = video.read() #frame is a numpy matrix

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts the frame to gray

    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0) 
    #GaussianBlur method - process the image
    #(21, 21) - the amount of blur to apply on the image
    # 0 - standard abbreviation - 0 is the most common

    #cv2.imshow("My Video", gray_frame_gau) #imshow() shows the frames (every fraction/sec) from the camera 

    if first_frame is None:
        first_frame = gray_frame_gau 
    
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau) #absdiff compares differences
    #cv2.imshow("My Video", delta_frame) #imshow() shows the frames (every fraction/sec) from the camera 

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1] #is a list
    #if a pixel has a value of >= 60, it reassigns 255 to that pixel

    dil_frame = cv2.dilate(thresh_frame, None, iterations=2) #removes the noise
    #None - configuration matrix
    #iterations=2 - applies processing on the image 

    #cv2.imshow("My Video", dil_frame) #imshow() shows the frames (every fraction/sec) from the camera 

    #find the contours - detects the countours from those white areas
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle =  cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        if rectangle.any():
            status = 1 #when there are rectangles   
            

    status_list.append(status) #appends the old and new statuses (status=1 is when an object entered the frame)
    status_list = status_list[-2:] #only the last items of the list

    if status_list[0] == 1 and status_list[1] == 0:
        send_email()
    

    cv2.imshow("Video", frame)


    key = cv2.waitKey(1)
    
    if key == ord("q"): #press q, stops the camera
        break

video.release()


