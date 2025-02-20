import numpy as np
import cv2
import threading

#declaracion de rangos a rastrear
redB1=np.array([0,20,20],np.uint8)# esta seccion ,np.uint8 no se si es necesaria
redA1=np.array([8,255,255],np.uint8)
print(redB1)
redB2=np.array([175,20,20],np.uint8)
redA2=np.array([255,255,255],np.uint8)
#cap = cv2.VideoCapture('prueba00001.avi') #para guardar el video en formato avi
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
   ret, frame = cap.read()

   if ret==True:
      
      #print ('threading.active_count())=',threading.active_count())
      frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convierte la img en escala de grises  
      #COLOR_BGR2GRAY, COLOR_BGR2RGB
      maskR1=cv2.inRange(frame2,redB1,redA1)
      maskR2=cv2.inRange(frame2,redB2,redA2)
      maskF=cv2.add(maskR1,maskR2)
      maskRed = cv2.bitwise_and(frame,frame, mask=maskF)
      cv2.imshow('redColor',maskRed)
      #cv2.imshow('frame',frame2)#,frame or frame2) muestra la imagen sin procesar (solo el modelo de color)
      cv2.imshow('frame',frame)
      cv2.imshow('Mask',maskF)
      

      if cv2.waitKey(1) & 0xFF == ord('q'): # para salir del bule se usa la letra q
         break

cap.release()
cv2.destroyAllWindows()