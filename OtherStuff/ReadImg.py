import cv2 
ima=cv2.imread('sema.png',0) #el parametro 1 o 0 las hace color o BN respectivamente
cv2.imwrite('XD2.png',ima)
cv2.imshow('XD',ima)
cv2.waitKey(0)
cv2.destroyAllWindows()

