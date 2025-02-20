import numpy as np
import cv2
import threading

#declaracion de rangos a rastrear
AzulB1=np.array([100,100,20],np.uint8)# esta seccion ,np.uint8 no se si es necesaria
AzulA1=np.array([125,255,255],np.uint8)
B1=np.array([0,0,130],np.uint8)# esta seccion ,np.uint8 no se si es necesaria
B2=np.array([255,15,255],np.uint8)# esta seccion ,np.uint8 no se si es necesaria

#cap = cv2.VideoCapture('prueba00001.avi') #para guardar el video en formato avi
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
   ret, frame = cap.read()

   if ret==True:
      
      #print ('threading.active_count())=',threading.active_count())
      frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convierte la img en escala de grises  
      #COLOR_BGR2GRAY, COLOR_BGR2RGB
      mask=cv2.inRange(frame2,B1,B2)
      #contornos, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #busqueda de contornos de interes con la mask aplicada
      contornos,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #error 3 variables spend 2 #_,contornos,_= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #dibuja sobre los contornos
      #cv2.drawContours(frame,contornos, -1, (255,0,0),3)
      
      for c in contornos:
         area=cv2.contourArea(c)
         if area > 3000:
            M=cv2.moments(c)
            if(M["m00"]==0):M["m00"]=1
            x=int(M["m10"]/M["m00"])
            y=int(M["m01"]/M["m00"])
            cv2.circle(frame,(x,y),7,(0,255,0),-1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            #se crea una instancia para nuevos contornos (suavizados)
            nC=cv2.convexHull(c)
            #con el parametro c o nC funciona, sin suavizar y con suavizado
            cv2.drawContours(frame,[nC],0,(255,0,0), 3)
      #maskR2=cv2.inRange(frame2,redB2,redA2)
      #maskF=cv2.add(maskR1,maskR2)
      #maskRed = cv2.bitwise_and(frame,frame, mask=maskF)
      #cv2.imshow('redColor',maskRed)
      #cv2.imshow('frame',frame2)#,frame or frame2) muestra la imagen sin procesar (solo el modelo de color)
      
      cv2.imshow('frame',frame)
      #cv2.imshow('Mask',maskF)
      

      if cv2.waitKey(1) & 0xFF == ord('q'): # para salir del bule se usa la letra q
         break

cap.release()
cv2.destroyAllWindows()