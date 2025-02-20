
###########################################################################
#!/usr/bin/env python3
import RPi.GPIO as GPIO  #the pin libaray of raspberry
import time  #the time libaray of system time
import numpy as np
import cv2
import threading


#LedPin = 17  #the BCM pin connect to LED
ledsPins = (17, 27)

#using ROI in the top range, and generate a indicator of possible color to order to the car respond 
#https://blog.electroica.com/select-roi-or-multiple-rois-bounding-box-in-opencv-python/
#https://www.peko-step.com/es/tool/hsvrgb.html
#https://omes-va.com/wp-content/uploads/2019/09/gyuw4.png
#la misma q 2 pero con una funcion q facilita el llamado de esto

def setupCar():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    
    for Led in ledsPins:
       GPIO.setup(Led, GPIO.OUT, initial=GPIO.HIGH)
    # Set LedPin's mode to output,and initial level to High(3.3v)
      
""""
def mainCar():
    while True:
        print ('...LED ON')
         Turn on LED
        GPIO.output(LedPin, GPIO.LOW)
        time.sleep(1)
        print ('LED OFF...')
         Turn off LED
        GPIO.output(LedPin, GPIO.HIGH)
        time.sleep(1)
"""

# Define a destroy function for clean up everything after the script finished
def destroy():
    # Turn off LED
    for Led in ledsPins:
       GPIO.output(Led, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()

def Car (dir):
   if dir == 1:
      print('Up')
      GPIO.output(17, GPIO.HIGH)
      GPIO.output(27, GPIO.HIGH)
   elif dir == 2:
      GPIO.output(17, GPIO.HIGH)
      GPIO.output(27, GPIO.LOW)
      print('Left')
   elif dir == 3:
      GPIO.output(17, GPIO.LOW)
      GPIO.output(27, GPIO.HIGH)
      print('Right')

   elif dir == 4:
      GPIO.output(17, GPIO.LOW)
      GPIO.output(27, GPIO.LOW)
      print('Stop')
   #else:
      #print('Next')


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
         cv2.circle(frame,(x,y),7,color,-1)
         cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font, 0.75,color,1,cv2.LINE_AA)
            #se crea una instancia para nuevos contornos (suavizados)
         
            #con el parametro c o nC funciona, sin suavizar y con suavizado
         cv2.drawContours(frame,[nC],0,color, 3)
         if col>=1:
            return col
         else:
            col=0
            return col


def dibujo2(mask,color,col,framex):
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
         cv2.circle(framex,(x,y),7,color,-1)
         cv2.putText(framex,'{},{}'.format(x,y),(x+10,y), font, 0.75,color,1,cv2.LINE_AA)
            #se crea una instancia para nuevos contornos (suavizados)
         
            #con el parametro c o nC funciona, sin suavizar y con suavizado
         cv2.drawContours(framex,[nC],0,color, 3)
         if col>=1:
            return col
         else:
            col=0
            return col            

#declaracion de rangos a rastrear
#AzulB1=np.array([100,100,20],np.uint8)# esta seccion ,np.uint8 no se si es necesaria
#AzulA1=np.array([125,255,255],np.uint8)
redB1 = np.array([0,100,20],np.uint8)
redA1 = np.array([5,255,255],np.uint8)
redB2 = np.array([175,100,20],np.uint8)
redA2 = np.array([179,255,255],np.uint8)

#RedB1=np.array([100,100,20],np.uint8)# esta seccion ,np.uint8 no se si es necesaria
#RedA1=np.array([125,255,255],np.uint8)

VerdeB1=np.array([45,100,20],np.uint8)# esta seccion ,np.uint8 no se si es necesaria
VerdeA1=np.array([70,255,255],np.uint8)


B1=np.array([0,0,130],np.uint8)# esta seccion ,np.uint8 no se si es necesaria
B2=np.array([255,15,255],np.uint8)# esta seccion ,np.uint8 no se si es necesaria

x=0 #variable como indicador del tipo de color q se identifico
font = cv2.FONT_HERSHEY_SIMPLEX

#cap = cv2.VideoCapture('prueba00001.avi') #para guardar el video en formato avi
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)#ancho 640 (X)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)#Alto 480 (Y)
print(width/4, height/4)
w,h=[width-1, height/4]
# 640.0 480.0 (X,Y)
setupCar()

while(cap.isOpened()):
   ret, frame = cap.read()

   if ret==True:
      
      #print ('threading.active_count())=',threading.active_count())
      frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convierte la img en escala de grises  
      rio= frame2[0:120, 0:639]# the parameter to resolve the matrix is [Y,X]
      #400 - 470 x => 200 - 300 y
      #530 - 610 x => 200 - 300 y
      rioA1=frame2[200:300, 400:470]# the parameter to resolve the matrix is [Y,X]
      rioA2=frame2[ 200:300,530:610]# the parameter to resolve the matrix is [Y,X]
      #COLOR_BGR2GRAY, COLOR_BGR2RGB
      maskV=cv2.inRange(rio,VerdeB1,VerdeA1)
      maskR1=cv2.inRange(rio,redB1,redA1)
      maskR2=cv2.inRange(rio,redB1,redA1)
      framex1=rioA1
      framex2=rioA2
      maskA1=cv2.inRange(rioA1,B1,B2)
      maskA2=cv2.inRange(rioA2,B1,B2)
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
      #deteccion verde   
      x=dibujo(maskV,(255,0,0),1)
      Car(x)
      #deteccion De 2 rojos
      x=dibujo(maskR1,(0,255,0),4)
      Car(x)
      x=dibujo(maskR2,(100,255,0),4)
      Car(x)
      #deteccion de blanco izq
      x=dibujo2(maskA1,(255,255,0),2,framex1)
      Car(x)
      #deteccion de blanco der
      x=dibujo2(maskA2,(255,255,0),3,framex2)
      Car(x)
      framex1=cv2.cvtColor(framex1, cv2.COLOR_HSV2BGR)
      frame[200:300, 400:470]=framex1
      framex2=cv2.cvtColor(framex2, cv2.COLOR_HSV2BGR)
      frame[200:300,530:610]=framex2
      #Car(x)
      #GrayX= frame[240:479, 320:640]# the parameter to resolve the matrix is [Y,X]
      #GrayX= frame[240:479, 320:640]
      #frame3 = cv2.cvtColor(GrayX, cv2.COLOR_BGR2GRAY) #convierte la img en escala de grises  
      #frame4 = cv2.cvtColor(frame3, cv2.COLOR_GRAY2BGR) #convierte la img en escala de grises  
      #frame[320:640, 240:479]=frame4
      #frame[240:479, 320:640]=frame4
      cv2.imshow('frame',frame)
      #cv2.imshow('Mask',maskF)
      

      if cv2.waitKey(1) & 0xFF == ord('q'): # para salir del bule se usa la letra q
         #print(x)
         break

cap.release()
cv2.destroyAllWindows()