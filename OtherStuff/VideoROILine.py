from asyncio.windows_events import NULL
from cv2 import Rodrigues
import numpy as np
import cv2
import threading

#using ROI in the top range, and generate a indicator of possible color to respond
#https://blog.electroica.com/select-roi-or-multiple-rois-bounding-box-in-opencv-python/

#la misma q 2 pero con una funcion q facilita el llamado de esto

def dibujo(mask,color,col):
   contornos,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #error 3 variables spend 2 #_,contornos,_= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #dibuja sobre los contornos
      #cv2.drawContours(frame,contornos, -1, (255,0,0),3)
   #print(col)#distinguir cual color se esta viendo en la ventana
   
   for c in contornos:
      area=cv2.contourArea(c)
      if area > 3000:
         M=cv2.moments(c)
         if(M["m00"]==0):M["m00"]=1
         x=int(M["m10"]/M["m00"])
         y=int(M["m01"]/M["m00"])
         nC=cv2.convexHull(c)
         cv2.circle(frame,(x,y),7,(0,255,0),-1)
         cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
            #se crea una instancia para nuevos contornos (suavizados)
         
            #con el parametro c o nC funciona, sin suavizar y con suavizado
         cv2.drawContours(frame,[nC],0,(255,0,0), 3)
         return col

#declaracion de rangos a rastrear
AzulB1=np.array([100,100,20],np.uint8)# esta seccion ,np.uint8 no se si es necesaria
AzulA1=np.array([125,255,255],np.uint8)
x=0
font = cv2.FONT_HERSHEY_SIMPLEX

#cap = cv2.VideoCapture('prueba00001.avi') #para guardar el video en formato avi
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)#ancho 640 (X)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)#Alto 480 (Y)
print(width/4, height/4)
w,h=[width-1, height/4]
# 640.0 480.0 (X,Y)

while(cap.isOpened()):
   ret, frame = cap.read()

   if ret==True:
      

      #rio1= frame2[447:235, 51:67]# the parameter to resolve the matrix is [Y,X]
      frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convierte la img en escala de grises  
      #rio= frame2[0:120, 0:639]# the parameter to resolve the matrix is [Y,X]
      #420,200
      #470,300
      #530,200
      #590,300
      #400 - 470 x => 200 - 300 y
      #530 - 610 x => 200 - 300 y
      x1=420
      x2=610
      y1=200
      y2=300
      rio= frame2[y1:y2, x1:x2]# the parameter to resolve the matrix is [Y,X]
      #(446, 222, 61, 78)
      #(572, 235, 55, 66)
      #COLOR_BGR2GRAY, COLOR_BGR2RGB
      
      #maskA=cv2.inRange(rio,AzulB1,AzulA1)
      #contornos, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #busqueda de contornos de interes con la mask aplicada
      #print(maskA)
      #maskR2=cv2.inRange(frame2,redB2,redA2)
      #maskF=cv2.add(maskR1,maskR2)
      #maskRed = cv2.bitwise_and(frame,frame, mask=maskF)
      #cv2.imshow('redColor',maskRed)
      #cv2.imshow('frame',frame2)#,frame or frame2) muestra la imagen sin procesar (solo el modelo de color)
      #rio= frame2[240:479, 320:640]# the parameter to resolve the matrix is [Y,X]
      #if ():
      framex=rio
      #x=dibujo(maskA,(255,0,0),1)
      #GrayX= frame[240:479, 320:640]# the parameter to resolve the matrix is [Y,X]
      #GrayX= frame[240:479, 320:640]
      #frame3 = cv2.cvtColor(GrayX, cv2.COLOR_BGR2GRAY) #convierte la img en escala de grises  
      #frame4 = cv2.cvtColor(frame3, cv2.COLOR_GRAY2BGR) #convierte la img en escala de grises  
      #frame[320:640, 240:479]=frame4
      framex2=cv2.cvtColor(framex, cv2.COLOR_GRAY2BGR)
      frame[y1:y2, x1:x2]=framex2
      cv2.imshow('frame',frame)
      #cv2.imshow('Mask',maskF)
      

      if cv2.waitKey(1) & 0xFF == ord('q'): # para salir del bule se usa la letra q
         print(x)
         break

cap.release()
cv2.destroyAllWindows()