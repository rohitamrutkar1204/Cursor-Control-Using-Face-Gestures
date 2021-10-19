import cv2
import dlib 
import pyautogui as pag
from imutils import face_utils
import numpy as np
from functions import eye_aspect_ratio
from functions import mouth_aspect_ratio
from functions import direction

left_count=0
right_count=0
wink_count=0
mouth_counter=0
scroll_count=0
read=False
scroll = False
ANCHOR_POINT = (0, 0)
font = cv2.FONT_HERSHEY_SIMPLEX
org = (00, 185)       
fontScale = 1
color = (0, 0, 255)
thickness = 2 


detector = dlib.get_frontal_face_detector()

# Loading the predictor  
predictor = dlib.shape_predictor("E:/CLG/SDP/Gesture Recognition/Code/model/shape_predictor_68_face_landmarks.dat")
#implemented as map inside.
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] #lastart and lend will consist of the start and end coordinates
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"] 
 
cap = cv2.VideoCapture(0)
flag=0
while True:
    ret, frame = cap.read()  
    frame = cv2.flip(frame, 1) 
    # Convert image into grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use detector to find landmarks
    faces = detector(gray,0) #0 is upscaling the img before applying to detetor

    for face in faces:
        x1 = face.left()  # left point
        y1 = face.top()  # top point
        x2 = face.right()  # right point
        y2 = face.bottom()  # bottom point

        #print (face)
        cv2.rectangle(frame,(x1,y1),(x2,y2),color=(0, 255, 0),thickness=3)
        
      
        #print(faces)
        # prdicting points on detected face 
        shape = predictor(gray, box=faces[0]) 
        shape = face_utils.shape_to_np(shape) 
        mouth = shape[mStart:mEnd] 
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd] 
        nose = shape[nStart:nEnd]
        
        #flipping the frame 
        temp = leftEye
        leftEye = rightEye
        rightEye = temp 
    
        
        
        for (x, y) in np.concatenate((mouth, leftEye, rightEye), axis=0):
            cv2.circle(frame, (x, y), 2, (0,255,0), -1)
        
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye) 
        mar = mouth_aspect_ratio(mouth)
        ear = (leftEAR + rightEAR) / 2.0
        nose_point = (nose[3, 0], nose[3, 1]) 
        diff_ear = np.abs(leftEAR - rightEAR)
       # print(ear)
      
        if(diff_ear > 0.04):   # 0.04-> wink threshold  
            #print("left") 
            #print(leftEAR)
            #print("right")
           # print(rightEAR)
            if(leftEAR<rightEAR):
              if(leftEAR<0.20): #0.18->threshold for left eye
                    #print(leftEAR)
                    
                    wink_count=wink_count+1
                    if(wink_count>5): #wait fr 20frames
                        cv2.putText(frame,'LeftClick',org, font, fontScale,color, thickness, cv2.LINE_AA)
                        pag.click(button='left')
                        wink_count=0


            elif(rightEAR<leftEAR): 
                
               if(rightEAR<0.20):
                    wink_count=wink_count+1
                    #print("gs")
                    if(wink_count>10):
                        cv2.putText(frame,'RightClick',org, font, fontScale,color, thickness, cv2.LINE_AA)
                        pag.click(button='right')  
                        wink_count=0
               

            else:
                wink_count=0 
                
        else:
            if(ear<19):
                scroll_count+=1
                if(scroll_count > 25):
                    scroll = not scroll
                    scroll_count=0
            
            else:
                scroll_count=0
        
        if(mar>0.6):
            mouth_counter+=1
            if(mouth_counter>15):
                read=not (read)
                mouth_counter=0
                ANCHOR_POINT =  nose_point  
                
        
        else:
            mouth_counter=0
         
        if read:
            cv2.putText(frame,'Activated',(00, 175) , font, fontScale,color, thickness, cv2.LINE_AA)
            cv2.circle(frame, ANCHOR_POINT, 3, (0,255,0), -1)
            cv2.line(frame, ANCHOR_POINT, nose_point, (255, 0, 0), 2)
            dir = direction(nose_point, ANCHOR_POINT, 60, 35)
            if dir == 'right':
                pag.moveRel(18,0)
            elif dir == 'left':
                pag.moveRel(-18,0)
            elif dir == 'down':
                if (scroll):
                    cv2.putText(frame,'Scroll Down',(00, 145) , font, fontScale,color, thickness, cv2.LINE_AA)
                    pag.scroll(-40)
                else:    
                    pag.moveRel(0,18)
            
            elif dir == 'up':
                if (scroll):
                    cv2.putText(frame,'Scroll Up',(00, 145) , font, fontScale,color, thickness, cv2.LINE_AA)
                    pag.scroll(40)
                else:    
                    pag.moveRel(0,-18)
                
                
                
    cv2.imshow("Face", frame)
 
    # Exit when escape is pressed
    if cv2.waitKey(1) == 27:
        break

# When everything done, release the video capture and video write objects
cap.release()

# Close all windows
cv2.destroyAllWindows()