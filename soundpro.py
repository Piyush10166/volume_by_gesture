import cv2
import mediapipe as mp
import math
import numpy as np 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)


volume = cast(interface, POINTER(IAudioEndpointVolume))
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands=mp_hands.Hands()
click=cv2.VideoCapture(0)
while True:
    success,img = click.read()
    img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            newlist=[]
            for id,lm  in enumerate (handlms.landmark):
                
                h , w , c =img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)        
                
                newlist.append([id,cx,cy])
                
            if newlist:
                 x1,y1= newlist[4][1],newlist[4][2]
                 x2,y2= newlist[8][1],newlist[8][2]
                 cv2.circle(img,(x1,y1),15,(25,190,150),16)
                 cv2.circle(img,(x2,y2),15,(25,190,150),16)
                 cv2.line(img,(x1,y1),(x2,y2),(25,19,15),5)
                 length = math.hypot(x2-x1,y2-y1)
            if length:
                    z1=(x1+x2)//2
                    z2=(y1+y2)//2
                    cv2.circle(img,(z1,z2),15,(100,30,159),5)
            VolRange= volume.GetVolumeRange()
            minVol = VolRange[0]
            maxVol= VolRange[1]
            vol=np.interp(length,[50,300],[minVol,maxVol])
            volume.SetMasterVolumeLevel(vol, None)
            print(vol)
    
    cv2.imshow("fingers",img)
    cv2.waitKey(1)

    
    




