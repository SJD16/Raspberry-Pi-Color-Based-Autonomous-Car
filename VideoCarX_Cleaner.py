#!/usr/bin/env python3

import RPi.GPIO as GPIO  # Raspberry Pi GPIO library
import time  # System time library
import numpy as np
import cv2

# Define LED control pins
ledsPins = (17, 27)

# Set up the GPIO pins

def setupCar():
    GPIO.setmode(GPIO.BCM)
    for Led in ledsPins:
        GPIO.setup(Led, GPIO.OUT, initial=GPIO.HIGH)

# Cleanup function

def destroy():
    for Led in ledsPins:
        GPIO.output(Led, GPIO.HIGH)
    GPIO.cleanup()

# Car movement control

def Car(direction):
    if direction == 1:
        print('Move Forward')
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
    elif direction == 2:
        print('Turn Left')
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.LOW)
    elif direction == 3:
        print('Turn Right')
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)
    elif direction == 4:
        print('Stop')
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)

# Function to process detected contours and draw on the frame

def detect_color(mask, color, direction, frame):
    contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 3000:
            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            nC = cv2.convexHull(c)
            cv2.circle(frame, (x, y), 7, color, -1)
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 1, cv2.LINE_AA)
            cv2.drawContours(frame, [nC], 0, color, 3)
            return direction
    return 0

# Define color ranges in HSV format
redB1, redA1 = np.array([0, 100, 20], np.uint8), np.array([5, 255, 255], np.uint8)
redB2, redA2 = np.array([175, 100, 20], np.uint8), np.array([179, 255, 255], np.uint8)
VerdeB1, VerdeA1 = np.array([45, 100, 20], np.uint8), np.array([70, 255, 255], np.uint8)
B1, B2 = np.array([0, 0, 130], np.uint8), np.array([255, 15, 255], np.uint8)

# Initialize camera
cap = cv2.VideoCapture(0)
setupCar()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to HSV and define regions of interest (ROI)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi_top = hsv_frame[0:120, 0:639]  # Region to detect traffic light colors
    roi_left = hsv_frame[200:300, 400:470]  # Left lane detection
    roi_right = hsv_frame[200:300, 530:610]  # Right lane detection
    
    # Create masks for color detection
    mask_green = cv2.inRange(roi_top, VerdeB1, VerdeA1)
    mask_red1 = cv2.inRange(roi_top, redB1, redA1)
    mask_red2 = cv2.inRange(roi_top, redB2, redA2)
    mask_white_left = cv2.inRange(roi_left, B1, B2)
    mask_white_right = cv2.inRange(roi_right, B1, B2)
    
    # Detect colors and control car accordingly
    Car(detect_color(mask_green, (0, 255, 0), 1, frame))  # Move forward on green
    Car(detect_color(mask_red1, (0, 0, 255), 4, frame))  # Stop on red
    Car(detect_color(mask_red2, (100, 255, 0), 4, frame))  # Stop on red
    Car(detect_color(mask_white_left, (255, 255, 0), 2, frame))  # Turn left
    Car(detect_color(mask_white_right, (255, 255, 0), 3, frame))  # Turn right
    
    # Show processed frame
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
